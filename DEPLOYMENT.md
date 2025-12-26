# Quick Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available for containers

## Start Pipeline
```bash
# Option 1: Use the automated start script
./start.sh

# Option 2: Manual startup
docker-compose up -d
sleep 30
./scripts/setup_elasticsearch.sh
```

## Verify Deployment
```bash
# Check all services are running
docker-compose ps

# Test API endpoints
python3 test_pipeline.py

# Manual API tests
curl http://localhost:5000/health
curl http://localhost:5000/anomalies/recent?minutes=5
```

## Monitor Anomalies
- **API**: http://localhost:5000/anomalies/recent
- **Kibana**: http://localhost:5601 (create index pattern: `anomalies`)
- **Logs**: `docker-compose logs -f streaming`

## Stop Pipeline
```bash
docker-compose down -v
```

## Key Features Delivered
✓ Kafka producer simulating sensor data  
✓ Spark Streaming with Isolation Forest anomaly detection  
✓ Real-time anomaly storage in Elasticsearch  
✓ REST API for querying anomalies  
✓ Complete Docker orchestration  
✓ Sub-second anomaly detection and alerting