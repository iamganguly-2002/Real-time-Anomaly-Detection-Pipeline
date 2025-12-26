# Real-time Anomaly Detection Pipeline

## 📌 Overview

The **Real-time Anomaly Detection Pipeline** is a distributed streaming system that ingests live sensor data, detects anomalies in real time, and makes the results available through APIs and dashboards within seconds.

This project demonstrates how modern streaming technologies and online machine learning techniques can be combined to build a production-style real-time analytics pipeline.

---

## 🛠 Technologies

- **Apache Kafka** – Real-time data ingestion  
- **Apache Spark Streaming** – Stream processing and anomaly detection  
- **Python** – Data generation, preprocessing, ML logic, and APIs  
- **Elasticsearch** – Storage and indexing of detected anomalies  
- **Kibana** – Visualization and monitoring  
- **Docker & Docker Compose** – Containerized deployment and orchestration  

---

## 🧠 Problem Description

In real-world systems such as IoT monitoring, industrial systems, and financial platforms, detecting abnormal behavior as soon as it occurs is critical.

This project builds a **real-time streaming pipeline** that:
- Continuously ingests sensor data
- Preprocesses and normalizes streaming messages
- Detects anomalies using an online anomaly detection approach
- Stores only relevant anomaly events
- Exposes APIs and dashboards for monitoring and analysis

---

## 🏗 System Architecture


### Component Responsibilities

- **Producer**: Simulates live sensor data with normal and anomalous behavior  
- **Kafka**: Acts as a fault-tolerant message broker  
- **Spark Streaming**: Consumes Kafka streams, preprocesses data, and performs anomaly detection  
- **Elasticsearch**: Stores detected anomalies for fast querying  
- **REST API**: Provides endpoints to query recent anomalies  
- **Kibana**: Visualizes anomaly data in real time  

---

## ⚙️ Key Features

- Real-time ingestion of sensor data using Kafka topics  
- Stream-level preprocessing and normalization  
- Online anomaly detection suitable for continuous data streams  
- Persistent anomaly storage using Elasticsearch  
- REST endpoints for querying anomaly data  
- Fully Dockerized setup for reproducible deployment  

---

## 📦 Deliverables

- Kafka topic producer simulator  
- Spark Streaming job code  
- Online anomaly detection logic  
- Elasticsearch index setup and storage  
- REST service with example query endpoints  
- Docker Compose–based deployment instructions  

---

## 🚀 Getting Started

### Prerequisites
- Docker  
- Docker Compose  

### Run the Pipeline Locally

```bash
git clone https://github.com/vijay-illuru/Real-time-Anomaly-Detection-Pipeline.git
cd Real-time-Anomaly-Detection-Pipeline
docker compose up --build
