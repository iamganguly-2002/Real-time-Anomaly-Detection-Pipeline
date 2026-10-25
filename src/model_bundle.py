from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler


@dataclass
class ModelBundle:
    model_name: str
    feature_columns: list[str]
    scaler: StandardScaler
    model: BaseEstimator

    def predict(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            X = X[self.feature_columns].copy()

        X_scaled = self.scaler.transform(X)

        if hasattr(self.model, "predict"):
            return np.asarray(self.model.predict(X_scaled))

        if hasattr(self.model, "fit_predict"):
            return np.asarray(self.model.fit_predict(X_scaled))

        raise ValueError(f"Model {self.model_name} does not support prediction.")
