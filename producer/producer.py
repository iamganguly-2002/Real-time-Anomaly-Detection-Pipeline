import json
import time
import random
import os
from kafka import KafkaProducer
from datetime import datetime

class SensorDataProducer:
    def __init__(self):
        # ✅ ALWAYS USE DOCKER SERVICE NAME
        kafka_bootstrap_servers = os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS",
            "kafka:9092"   # safe default inside Docker
        )

        print(f"[Producer] Connecting to Kafka at {kafka_bootstrap_servers}")

        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),

            # ✅ CRITICAL FIXES
            api_version=(0, 10),        # avoids broker version lookup failure
            retries=5,
            linger_ms=10
        )

        self.topic = "sensor-data"

    def generate_normal_data(self):
        return {
            "sensor_id": f"sensor_{random.randint(1, 10)}",
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(random.normalvariate(25, 3), 2),
            "humidity": round(random.normalvariate(60, 10), 2),
            "pressure": round(random.normalvariate(1013, 5), 2),
            "vibration": round(random.normalvariate(0.5, 0.1), 3)
        }

    def generate_anomaly_data(self):
        anomaly_type = random.choice(
            ["temperature", "humidity", "pressure", "vibration"]
        )

        data = self.generate_normal_data()

        if anomaly_type == "temperature":
            data["temperature"] = round(
                random.choice([
                    random.normalvariate(50, 5),
                    random.normalvariate(-10, 3)
                ]), 2
            )

        elif anomaly_type == "humidity":
            data["humidity"] = round(
                random.choice([
                    random.normalvariate(95, 2),
                    random.normalvariate(5, 2)
                ]), 2
            )

        elif anomaly_type == "pressure":
            data["pressure"] = round(
                random.choice([
                    random.normalvariate(1050, 5),
                    random.normalvariate(980, 5)
                ]), 2
            )

        else:
            data["vibration"] = round(
                random.normalvariate(2.0, 0.3), 3
            )

        return data

    def run(self):
        print("[Producer] Starting sensor data stream...")
        while True:
            try:
                if random.random() < 0.05:  # 5% anomaly rate
                    data = self.generate_anomaly_data()
                    print(f"[ANOMALY] {data}")
                else:
                    data = self.generate_normal_data()
                    print(f"[NORMAL] {data}")

                self.producer.send(self.topic, value=data)
                self.producer.flush()   # ✅ ensure delivery
                time.sleep(1)

            except Exception as e:
                print(f"[Producer ERROR] {e}")
                time.sleep(5)

if __name__ == "__main__":
    SensorDataProducer().run()
