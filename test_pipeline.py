#!/usr/bin/env python3
import requests
import time
import json

def test_api_endpoints():
    base_url = "http://localhost:5001"
    
    print("Testing Real-time Anomaly Detection Pipeline API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
    
    # Wait a bit for some data to be processed
    print("\nWaiting 30 seconds for anomaly detection...")
    time.sleep(30)
    
    # Test recent anomalies
    try:
        response = requests.get(f"{base_url}/anomalies/recent?minutes=10")
        data = response.json()
        print(f"✓ Recent anomalies: {response.status_code}")
        print(f"  Found {data.get('count', 0)} anomalies in last 10 minutes")
    except Exception as e:
        print(f"✗ Recent anomalies failed: {e}")
    
    # Test anomaly stats
    try:
        response = requests.get(f"{base_url}/anomalies/stats?hours=1")
        data = response.json()
        print(f"✓ Anomaly stats: {response.status_code}")
        print(f"  Total anomalies: {data.get('total_anomalies', 0)}")
    except Exception as e:
        print(f"✗ Anomaly stats failed: {e}")
    
    # Test filtered anomalies
    try:
        response = requests.get(f"{base_url}/anomalies?hours=1&limit=10")
        data = response.json()
        print(f"✓ Filtered anomalies: {response.status_code}")
        print(f"  Total found: {data.get('total', 0)}")
    except Exception as e:
        print(f"✗ Filtered anomalies failed: {e}")

if __name__ == "__main__":
    test_api_endpoints()