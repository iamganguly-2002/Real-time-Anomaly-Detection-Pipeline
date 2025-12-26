#!/bin/bash

echo "Setting up Elasticsearch indices..."

# Wait for Elasticsearch to be ready
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"yellow\|green"'; do
    echo "Waiting for Elasticsearch..."
    sleep 5
done

# Create anomalies index
curl -X PUT "localhost:9200/anomalies" -H 'Content-Type: application/json' -d'
{
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
  },
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  }
}'

echo "Elasticsearch setup completed!"