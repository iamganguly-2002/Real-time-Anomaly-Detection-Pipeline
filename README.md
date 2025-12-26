# Real-time Anomaly Detection Pipeline

A complete streaming pipeline that ingests sensor data from Kafka, detects anomalies using machine learning, and provides real-time alerts through Elasticsearch and REST APIs.

## Architecture

- **Kafka**: Message streaming platform for sensor data
- **Spark Streaming**: Real-time data processing with anomaly detection
- **Elasticsearch**: Storage for anomalies and search capabilities
- **Flask API**: REST endpoints for querying anomalies
- **Kibana**: Visualization dashboard
- **Docker Compose**: Complete orchestration

## Quick Start

### 1. Start the Pipeline
```bash
docker-compose up -d
```

### 2. Setup Elasticsearch Index
```bash
./scripts/setup_elasticsearch.sh
```

### 3. Verify Services
- Kafka: `localhost:9092`
- Elasticsearch: `http://localhost:9200`
- Kibana: `http://localhost:5601`
- API: `http://localhost:5001`
- Spark UI: `http://localhost:8080`

## API Endpoints

### Get Recent Anomalies
```bash
curl "http://localhost:5001/anomalies/recent?minutes=10"
```

### Get Anomalies by Time Range
```bash
curl "http://localhost:5001/anomalies?hours=24&limit=50"
```

### Get Anomaly Statistics
```bash
curl "http://localhost:5001/anomalies/stats?hours=24"
```

### Filter by Sensor
```bash
curl "http://localhost:5001/anomalies?sensor_id=sensor_1&hours=12"
```

## Example API Responses

### Recent Anomalies
```json
{
  "recent_anomalies": [
    {
      "sensor_id": "sensor_3",
      "timestamp": "2024-01-15T10:30:45",
      "temperature": 52.3,
      "humidity": 65.2,
      "pressure": 1015.1,
      "vibration": 0.45,
      "anomaly_score": -0.15,
      "is_anomaly": true,
      "detection_timestamp": "2024-01-15T10:30:47"
    }
  ],
  "count": 1,
  "time_window": "10 minutes"
}
```

### Anomaly Statistics
```json
{
  "total_anomalies": 23,
  "by_sensor": [
    {"sensor_id": "sensor_1", "count": 8},
    {"sensor_id": "sensor_3", "count": 7}
  ],
  "by_hour": [
    {"timestamp": "2024-01-15T10:00:00", "count": 5}
  ]
}
```

## Monitoring

### View Logs
```bash
docker-compose logs -f streaming
docker-compose logs -f producer
docker-compose logs -f api
```

### Kibana Dashboard
1. Open `http://localhost:5601`
2. Create index pattern: `anomalies`
3. Visualize anomaly trends and patterns

## Configuration

### Anomaly Detection Parameters
- **Contamination Rate**: 10% (adjustable in `streaming_job.py`)
- **Training Window**: 1000 samples
- **Detection Frequency**: Every 5 seconds

### Data Generation
- **Normal Data**: Gaussian distribution around typical sensor values
- **Anomaly Rate**: 5% of generated data
- **Sensors**: 10 simulated sensors

## Scaling

### Horizontal Scaling
```bash
docker-compose up --scale spark-worker=3 --scale producer=2
```

### Production Deployment
- Use external Kafka cluster
- Configure Spark cluster with multiple workers
- Set up Elasticsearch cluster
- Add monitoring and alerting

## Troubleshooting

### Common Issues
1. **Services not starting**: Check Docker resources and ports
2. **No anomalies detected**: Wait for model training (50+ samples)
3. **API errors**: Verify Elasticsearch connection

### Health Checks
```bash
curl http://localhost:5001/health
curl http://localhost:9200/_cluster/health
```

## Development

### Local Testing
```bash
# Test producer
cd producer && python producer.py

# Test API
cd api && python app.py

# Manual Elasticsearch queries
curl -X GET "localhost:9200/anomalies/_search?pretty"
```

## License

MIT License