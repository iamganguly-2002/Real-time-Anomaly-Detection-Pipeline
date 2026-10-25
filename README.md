# Anomaly Detection for Industrial Sensor Monitoring

A modular machine learning project for detecting abnormal sensor readings using multiple unsupervised anomaly detection algorithms, comparing their performance, and exposing the best model through a FastAPI API and Streamlit dashboard.

## Overview

This project simulates an industrial IoT monitoring workflow where sensor readings can become abnormal due to equipment faults, environment changes, or sensor drift. Instead of relying on a single model, the project trains and evaluates multiple anomaly detection algorithms and selects the best-performing one.

The system is designed for:
- model comparison and evaluation
- deployment-ready inference via API
- a simple interactive dashboard for demonstrations
- portfolio and interview presentation

## Key features

- Synthetic sensor dataset generation with normal and anomalous patterns
- Five anomaly detection algorithms:
  - Isolation Forest
  - Local Outlier Factor
  - One-Class SVM
  - DBSCAN
  - Elliptic Envelope
- Automated model selection based on evaluation metrics
- FastAPI backend for real-time prediction
- Streamlit UI for user interaction and demo use
- Modular Python project structure for maintainability
- Notebook for EDA and exploratory analysis

## Project architecture

```text
Real-time-Anomaly-Detection-Pipeline/
├── app/
│   └── main.py                  # FastAPI backend
├── src/
│   ├── data_generation.py      # Synthetic dataset creation
│   ├── modeling.py             # Model registry and training logic
│   ├── evaluation.py           # Metric computation
│   ├── train_and_select.py     # Model comparison + best model selection
│   ├── model_bundle.py         # Saved model wrapper
│   ├── logger_config.py        # Logging configuration
│   └── __init__.py
├── notebooks/
│   ├── anomaly_detection_eda.ipynb
│   └── README.md
├── artifacts/
│   ├── best_model.joblib
│   └── model_comparison.json
├── data/
│   └── sensor_anomalies_dataset.csv
├── logs/
│   └── anomaly_training.log
├── streamlit_app.py            # Streamlit dashboard
├── requirements.txt            # Python dependencies
├── README.md                  # Project overview
├── description.md             # Detailed project description
├── .gitignore
└── .venv/
```

## Dataset

The project creates a synthetic sensor dataset with the following features:
- temperature
- humidity
- pressure
- vibration
- label (0 = normal, 1 = anomaly)

The data includes both normal operating values and abnormal values designed to mimic real-world equipment faults. The anomaly rate is around 8%, which creates a realistic but balanced dataset for benchmarking.

## Workflow

1. Generate synthetic dataset
2. Split into train and test sets
3. Standardize features
4. Train multiple anomaly detection models
5. Convert model predictions into binary labels
6. Compute evaluation metrics
7. Select the best model by F1-score
8. Save the trained model and metadata
9. Serve the model using FastAPI
10. Visualize and test it in Streamlit

## Technologies used

- Python
- scikit-learn
- pandas
- numpy
- FastAPI
- Streamlit
- Jupyter Notebook

## Best model

The project evaluates all models and compares them using:
- accuracy
- precision
- recall
- F1-score

The best-performing model is selected automatically and saved under artifacts for reuse in inference.

## Setup

### 1. Create a virtual environment

```bash
cd /home/indranil/Desktop/Real-time-Anomaly-Detection-Pipeline
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the models and generate artifacts

```bash
python3 -m src.train_and_select
```

## Run the backend

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

## Run the Streamlit frontend

```bash
streamlit run streamlit_app.py
```

## Demo

Open the Streamlit app in the browser and enter sensor values such as:
- temperature
- humidity
- pressure
- vibration

The app calls the FastAPI backend and predicts whether the sensor reading is normal or anomalous.

## Example API request

```bash
curl -X POST "http://127.0.0.1:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"temperature": 25, "humidity": 55, "pressure": 1013, "vibration": 0.5},
      {"temperature": 50, "humidity": 90, "pressure": 1060, "vibration": 2.2}
    ]
  }'
```

## Resume-ready summary

This project demonstrates an end-to-end anomaly detection workflow for IoT sensor monitoring, including synthetic data generation, multi-model comparison, best-model selection, model serving through a FastAPI API, and a Streamlit-based demo dashboard for prediction and visualization.

## Future improvements

- integrate real sensor data from industrial systems
- add model drift monitoring
- use time-series forecasting for predictive maintenance
- deploy the API to cloud infrastructure
- add database logging for predictions

## License

This project is intended for educational and portfolio use.
