import os
import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from sklearn.ensemble import IsolationForest
import numpy as np
from elasticsearch import Elasticsearch

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
        self.training_data = []
        self.min_training_samples = 50
        
    def update_model(self, data):
        self.training_data.extend(data)
        if len(self.training_data) > 1000:
            self.training_data = self.training_data[-1000:]
        
        if len(self.training_data) >= self.min_training_samples:
            self.model.fit(self.training_data)
            self.is_trained = True
    
    def detect_anomalies(self, data):
        if not self.is_trained:
            return [0] * len(data)
        return self.model.predict(data)

class StreamingAnomalyDetection:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("AnomalyDetection") \
            .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        
        self.es_client = Elasticsearch([{
            'host': os.getenv('ELASTICSEARCH_HOST', 'localhost:9200').split(':')[0],
            'port': int(os.getenv('ELASTICSEARCH_HOST', 'localhost:9200').split(':')[1])
        }])
        
        self.detector = AnomalyDetector()
        self.setup_elasticsearch()
    
    def setup_elasticsearch(self):
        index_mapping = {
            "mappings": {
                "properties": {
                    "sensor_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "temperature": {"type": "float"},
                    "humidity": {"type": "float"},
                    "pressure": {"type": "float"},
                    "vibration": {"type": "float"},
                    "anomaly_score": {"type": "float"},
                    "is_anomaly": {"type": "boolean"},
                    "detection_timestamp": {"type": "date"}
                }
            }
        }
        
        if not self.es_client.indices.exists(index="anomalies"):
            self.es_client.indices.create(index="anomalies", body=index_mapping)
    
    def process_batch(self, df, epoch_id):
        if df.count() == 0:
            return
        
        # Convert to pandas for processing
        pandas_df = df.toPandas()
        
        # Extract features for anomaly detection
        features = pandas_df[['temperature', 'humidity', 'pressure', 'vibration']].values
        
        # Update model with new data
        self.detector.update_model(features.tolist())
        
        # Detect anomalies
        predictions = self.detector.detect_anomalies(features)
        
        # Process results
        for idx, row in pandas_df.iterrows():
            is_anomaly = predictions[idx] == -1 if self.detector.is_trained else False
            
            if is_anomaly:
                anomaly_doc = {
                    'sensor_id': row['sensor_id'],
                    'timestamp': row['timestamp'],
                    'temperature': row['temperature'],
                    'humidity': row['humidity'],
                    'pressure': row['pressure'],
                    'vibration': row['vibration'],
                    'anomaly_score': float(self.detector.model.decision_function([features[idx]])[0]) if self.detector.is_trained else 0.0,
                    'is_anomaly': True,
                    'detection_timestamp': datetime.now().isoformat()
                }
                
                try:
                    self.es_client.index(index="anomalies", body=anomaly_doc)
                    print(f"Anomaly detected and stored: {anomaly_doc}")
                except Exception as e:
                    print(f"Error storing anomaly: {e}")
    
    def run(self):
        schema = StructType([
            StructField("sensor_id", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("temperature", FloatType(), True),
            StructField("humidity", FloatType(), True),
            StructField("pressure", FloatType(), True),
            StructField("vibration", FloatType(), True)
        ])
        
        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')) \
            .option("subscribe", "sensor-data") \
            .load()
        
        parsed_df = df.select(
            from_json(col("value").cast("string"), schema).alias("data")
        ).select("data.*")
        
        query = parsed_df.writeStream \
            .foreachBatch(self.process_batch) \
            .outputMode("append") \
            .trigger(processingTime='5 seconds') \
            .start()
        
        print("Streaming job started. Waiting for data...")
        query.awaitTermination()

if __name__ == "__main__":
    detector = StreamingAnomalyDetection()
    detector.run()