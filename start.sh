#!/bin/bash

echo "Starting Real-time Anomaly Detection Pipeline..."

# Start infrastructure services first
echo "Starting infrastructure services..."
docker-compose up -d zookeeper kafka elasticsearch kibana spark-master spark-worker

# Wait for services to be ready
echo "Waiting for services to initialize..."
sleep 30

# Setup Elasticsearch
echo "Setting up Elasticsearch indices..."
./scripts/setup_elasticsearch.sh

# Start application services
echo "Starting application services..."
docker-compose up -d producer streaming api

echo "Pipeline started successfully!"
echo ""
echo "Services available at:"
echo "- API: http://localhost:5001"
echo "- Kibana: http://localhost:5601"
echo "- Spark UI: http://localhost:8080"
echo "- Elasticsearch: http://localhost:9200"
echo ""
echo "Test the API:"
echo "curl http://localhost:5001/health"
echo "curl http://localhost:5001/anomalies/recent"