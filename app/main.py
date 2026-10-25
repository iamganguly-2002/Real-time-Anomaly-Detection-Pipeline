from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.data_generation import FEATURE_COLUMNS
from src.train_and_select import run_training_pipeline

ARTIFACT_DIR = Path(__file__).resolve().parent.parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "best_model.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_comparison.json"

app = FastAPI(title="Anomaly Detection Demo API", version="1.0.0")


class SensorRecord(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    vibration: float


class PredictionRequest(BaseModel):
    records: list[SensorRecord]


def load_model_bundle():
    if not MODEL_PATH.exists():
        run_training_pipeline()

    if not MODEL_PATH.exists():
        raise HTTPException(status_code=500, detail="Model artifact not found after training.")

    return joblib.load(MODEL_PATH)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Anomaly detection API is running."}


@app.get("/model-info")
def model_info():
    bundle = load_model_bundle()
    metadata = {}
    if METADATA_PATH.exists():
        metadata = json.loads(METADATA_PATH.read_text())

    return {
        "model_name": bundle.model_name,
        "feature_columns": bundle.feature_columns,
        "metadata": metadata,
    }


@app.post("/predict")
def predict_anomalies(request: PredictionRequest):
    if not request.records:
        raise HTTPException(status_code=400, detail="At least one record is required.")

    bundle = load_model_bundle()
    df = pd.DataFrame([record.model_dump() for record in request.records])

    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required features: {missing}")

    predictions = bundle.predict(df)
    prediction_labels = np.where(predictions == -1, 1, 0)

    results = []
    for idx, label in enumerate(prediction_labels):
        results.append(
            {
                "index": idx,
                "anomaly": bool(label == 1),
                "status": "anomaly" if label == 1 else "normal",
            }
        )

    return {
        "model_name": bundle.model_name,
        "count": len(results),
        "predictions": results,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
