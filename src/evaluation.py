from __future__ import annotations

from typing import Dict

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def convert_predictions_to_binary(predictions: np.ndarray) -> np.ndarray:
    pred_array = np.asarray(predictions)
    return np.where(pred_array == -1, 1, 0)


def evaluate_predictions(y_true: np.ndarray, predictions: np.ndarray) -> Dict[str, float]:
    y_pred = convert_predictions_to_binary(predictions)
    y_true = np.asarray(y_true).astype(int)

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }
