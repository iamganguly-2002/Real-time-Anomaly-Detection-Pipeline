# Project Description

## 1. Project goal

This project is a machine learning anomaly detection system designed for industrial sensor monitoring. It is built to detect unusual readings in sensor data that might indicate equipment failure, environmental drift, unstable operating conditions, or abnormal machine behavior.

The project is intentionally kept lightweight and practical so it can run easily on a normal laptop, while still demonstrating a realistic workflow used in data science and AI projects.

## 2. Problem being solved

In real industrial environments, machines produce continuous sensor readings such as temperature, humidity, pressure, and vibration. Normal operating conditions can vary a lot, but abnormal states are relatively rare. Traditional rule-based monitoring often fails when conditions are noisy or when new patterns emerge.

This project addresses that issue by using anomaly detection algorithms that learn the structure of normal behavior and flag unexpected values as anomalies.

## 3. What kind of anomaly detection this is

This is an IoT / industrial sensor anomaly detection project.

It is not a network intrusion detection project and not a cybersecurity anomaly project. Instead, it focuses on:
- equipment monitoring
- sensor health
- industrial process stability
- predictive maintenance support

## 4. Dataset description

The project uses a synthetic dataset generated to mimic sensor-based industrial monitoring.

### Features

The dataset contains the following sensor features:
- temperature
- humidity
- pressure
- vibration

### Label

- 0 = normal behavior
- 1 = anomalous behavior

### Why synthetic data?

Synthetic data is useful for a demo project because it:
- avoids dependency on private or restricted data
- is easy to generate in large quantity
- provides clear anomaly patterns
- allows controlled evaluation and reproducible benchmarks
- works well for resume and interview presentation

### Data characteristics

The dataset is generated so that:
- normal readings stay within expected operating ranges
- anomalies represent unusual conditions like high temperature, abnormal vibration, abnormal pressure, or altered humidity patterns
- the anomaly rate is small but significant enough to benchmark model performance

## 5. Why machine learning is used here

This project builds a supervised evaluation setup around unsupervised anomaly detection models.

The anomaly detection algorithms are trained on the structure of normal observations and then used to detect outliers. Because anomalies are rare, the project uses standard classification-style evaluation after converting predictions into binary labels.

This is a common pattern in anomaly detection projects where the objective is to flag unusual data rather than predict a fixed class in a fully labeled dataset.

## 6. Algorithms used

The project compares five anomaly detection algorithms:

### 1. Isolation Forest
A tree-based algorithm that isolates anomalies by random partitioning. Anomalies are easier to isolate and therefore require fewer splits.

### 2. Local Outlier Factor (LOF)
A density-based method that compares the local density of a point with its neighbors. Points with significantly lower density than neighbors are treated as anomalies.

### 3. One-Class SVM
A support vector method trained to learn the boundary of normal data. Points outside the learned boundary are considered anomalies.

### 4. DBSCAN
A clustering algorithm that groups dense regions together. Points in sparse regions or outside clusters can be treated as anomalies.

### 5. Elliptic Envelope
A Gaussian-based model that fits an ellipse around normal data in feature space. Points outside the enveloped region are treated as outliers.

## 7. Model evaluation strategy

The project trains each model on a dataset split into train and test portions. After inference, predictions are converted into binary labels and compared against the true labels.

The following metrics are used:
- Accuracy
- Precision
- Recall
- F1-score

The best model is automatically chosen based on F1-score, since it balances precision and recall in anomaly detection tasks.

## 8. Data and feature pipeline

The project follows a standard ML workflow:

1. Generate synthetic sensor data
2. Save the dataset to the data folder
3. Load data into a pandas DataFrame
4. Separate feature columns from target labels
5. Split data into train/test sets
6. Standardize numerical features
7. Train multiple anomaly detection models
8. Convert predictions into binary labels
9. Evaluate each model
10. Select the best-performing model
11. Save the best model artifact

## 9. File-by-file explanation

### README.md
Main project overview, setup instructions, and quick usage guide for GitHub and local execution.

### description.md
Full conceptual and technical documentation explaining the goal, dataset, workflow, and file responsibilities.

### requirements.txt
Lists all Python dependencies required to run the project, including machine learning, API, dashboard, and analysis packages.

### .gitignore
Prevents generated data, logs, notebooks, environment folders, and editor files from being accidentally committed.

### src/data_generation.py
Responsible for generating the synthetic dataset. It creates sensor values for both normal and anomalous behavior using controlled rules. This is the base of the entire workflow.

### src/modeling.py
Defines the model registry and prediction logic for each anomaly detection algorithm. This file centralizes the training and inference interfaces used by the project.

### src/evaluation.py
Converts raw anomaly predictions into binary labels and computes metrics like accuracy, precision, recall, and F1-score.

### src/train_and_select.py
This is the main training pipeline. It loads the generated dataset, trains all models, evaluates them, selects the best one, and stores results in artifacts.

### src/model_bundle.py
Wraps the final trained model, scaler, and feature list into a single object for inference, making API prediction easier and cleaner.

### src/logger_config.py
Sets up logging so training steps and runtime activity are recorded to the logs directory.

### app/main.py
FastAPI application that loads the best-trained model and exposes HTTP endpoints for model inference and health checks.

### streamlit_app.py
Interactive dashboard for demonstrating model predictions. It accepts sensor inputs and sends them to the API for classification.

### notebooks/anomaly_detection_eda.ipynb
Notebook that walks through data loading, dataset summary, descriptive statistics, exploratory analysis, model training, and result comparison.

### data/sensor_anomalies_dataset.csv
Generated CSV dataset used to train and evaluate the models.

### artifacts/model_comparison.json
Stores metric values for all models so that comparisons are visible and reproducible.

### artifacts/best_model.joblib
Saved best model artifact used for inference in the API and UI.

### logs/anomaly_training.log
Stores runtime logs from model training and evaluation.

## 10. API workflow

The FastAPI backend serves a prediction endpoint that accepts sensor readings and returns whether the input is likely anomalous.

The API is useful because it demonstrates how a trained model can be deployed as a real service, even in a small demo project.

Typical API flow:
- user sends a JSON payload with sensor values
- the app loads the scaler and best model
- the app preprocesses the values
- the model predicts anomaly status
- the API returns the prediction result

## 11. UI workflow

The Streamlit app acts as the front-end interface for the project. It allows the user to manually enter values or view benchmark results and then query the model through the API.

This is especially useful for portfolio demos because it provides a cleaner explanation than a raw script or notebook alone.

## 12. Why this project is good for interviews and resumes

This project demonstrates several important skills:
- data generation and preprocessing
- machine learning model building
- model comparison and selection
- feature engineering awareness
- API deployment
- end-to-end project design
- dashboard-based demo presentation

It shows that the candidate can take a problem from idea to working ML solution, not just train a model in a notebook.

## 13. Project strengths

- simple and clean structure
- easy to run on a local laptop
- no heavy infrastructure needed
- realistic industrial monitoring theme
- multiple anomaly detection algorithms
- modern portfolio-ready output

## 14. Example interview explanation

If asked, “What does your project do?” you can answer:

> This project builds an anomaly detection system for industrial sensor monitoring. It simulates sensor readings such as temperature, humidity, pressure, and vibration, then trains several anomaly detection models to identify abnormal behavior. After comparing their performance, the project selects the best model and exposes it through a FastAPI API and Streamlit dashboard so the system can be demonstrated in a real-world use case.

## 15. Final note

This project is a simplified but realistic demonstration of how anomaly detection is used in IoT and industrial monitoring. It balances technical depth with ease of use, making it ideal for portfolio projects, interviews, and educational learning.
