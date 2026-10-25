from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


def get_model_registry() -> Dict[str, object]:
    return {
        "Isolation Forest": IsolationForest(contamination=0.08, random_state=42),
        "Local Outlier Factor": LocalOutlierFactor(n_neighbors=20, contamination=0.08),
        "One-Class SVM": OneClassSVM(nu=0.08, kernel="rbf", gamma="scale"),
        "DBSCAN": DBSCAN(eps=1.2, min_samples=15),
        "Elliptic Envelope": EllipticEnvelope(contamination=0.08),
    }


def fit_and_predict(model_name: str, X_train: np.ndarray, X_test: np.ndarray) -> Tuple[object, StandardScaler, np.ndarray]:
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    if model_name == "Isolation Forest":
        model = IsolationForest(contamination=0.08, random_state=42)
        model.fit(X_train_scaled)
        predictions = model.predict(X_test_scaled)

    elif model_name == "Local Outlier Factor":
        model = LocalOutlierFactor(n_neighbors=20, contamination=0.08)
        predictions = model.fit_predict(X_test_scaled)

    elif model_name == "One-Class SVM":
        model = OneClassSVM(nu=0.08, kernel="rbf", gamma="scale")
        model.fit(X_train_scaled)
        predictions = model.predict(X_test_scaled)

    elif model_name == "DBSCAN":
        model = DBSCAN(eps=1.2, min_samples=15)
        predictions = model.fit_predict(X_test_scaled)

    elif model_name == "Elliptic Envelope":
        model = EllipticEnvelope(contamination=0.08)
        model.fit(X_train_scaled)
        predictions = model.predict(X_test_scaled)

    else:
        raise ValueError(f"Unsupported model: {model_name}")

    return model, scaler, predictions
