from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

es_client = Elasticsearch([{
    'host': os.getenv('ELASTICSEARCH_HOST', 'localhost:9200').split(':')[0],
    'port': int(os.getenv('ELASTICSEARCH_HOST', 'localhost:9200').split(':')[1])
}])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/anomalies', methods=['GET'])
def get_anomalies():
    try:
        # Query parameters
        hours = int(request.args.get('hours', 24))
        sensor_id = request.args.get('sensor_id')
        limit = int(request.args.get('limit', 100))
        
        # Build query
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"is_anomaly": True}},
                        {"range": {
                            "detection_timestamp": {
                                "gte": (datetime.now() - timedelta(hours=hours)).isoformat()
                            }
                        }}
                    ]
                }
            },
            "sort": [{"detection_timestamp": {"order": "desc"}}],
            "size": limit
        }
        
        if sensor_id:
            query["query"]["bool"]["must"].append({"term": {"sensor_id": sensor_id}})
        
        response = es_client.search(index="anomalies", body=query)
        
        anomalies = []
        for hit in response['hits']['hits']:
            anomaly = hit['_source']
            anomaly['id'] = hit['_id']
            anomalies.append(anomaly)
        
        return jsonify({
            'anomalies': anomalies,
            'total': response['hits']['total']['value'],
            'query_time': f"{hours} hours"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anomalies/stats', methods=['GET'])
def get_anomaly_stats():
    try:
        hours = int(request.args.get('hours', 24))
        
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"is_anomaly": True}},
                        {"range": {
                            "detection_timestamp": {
                                "gte": (datetime.now() - timedelta(hours=hours)).isoformat()
                            }
                        }}
                    ]
                }
            },
            "aggs": {
                "by_sensor": {
                    "terms": {"field": "sensor_id", "size": 20}
                },
                "by_hour": {
                    "date_histogram": {
                        "field": "detection_timestamp",
                        "calendar_interval": "1h"
                    }
                }
            },
            "size": 0
        }
        
        response = es_client.search(index="anomalies", body=query)
        
        stats = {
            'total_anomalies': response['hits']['total']['value'],
            'by_sensor': [
                {'sensor_id': bucket['key'], 'count': bucket['doc_count']}
                for bucket in response['aggregations']['by_sensor']['buckets']
            ],
            'by_hour': [
                {'timestamp': bucket['key_as_string'], 'count': bucket['doc_count']}
                for bucket in response['aggregations']['by_hour']['buckets']
            ],
            'query_time': f"{hours} hours"
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anomalies/recent', methods=['GET'])
def get_recent_anomalies():
    try:
        minutes = int(request.args.get('minutes', 10))
        
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"is_anomaly": True}},
                        {"range": {
                            "detection_timestamp": {
                                "gte": (datetime.now() - timedelta(minutes=minutes)).isoformat()
                            }
                        }}
                    ]
                }
            },
            "sort": [{"detection_timestamp": {"order": "desc"}}],
            "size": 50
        }
        
        response = es_client.search(index="anomalies", body=query)
        
        anomalies = []
        for hit in response['hits']['hits']:
            anomaly = hit['_source']
            anomaly['id'] = hit['_id']
            anomalies.append(anomaly)
        
        return jsonify({
            'recent_anomalies': anomalies,
            'count': len(anomalies),
            'time_window': f"{minutes} minutes"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)