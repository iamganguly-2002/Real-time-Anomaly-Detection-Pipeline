from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from src.data_generation import DATASET_PATH, FEATURE_COLUMNS, ensure_dataset_exists
from src.evaluation import evaluate_predictions
from src.logger_config import logger
from src.model_bundle import ModelBundle
from src.modeling import fit_and_predict, get_model_registry

ARTIFACT_DIR = Path(__file__).resolve().parent.parent / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def run_training_pipeline() -> dict:
    dataset_path = ensure_dataset_exists(n_rows=25000, anomaly_rate=0.08, seed=42)
    logger.info("Loading dataset from %s", dataset_path)

    df = pd.read_csv(dataset_path)
    X = df[FEATURE_COLUMNS].values
    y = df["label"].astype(int).values

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    results = []
    best_result = None
    best_bundle = None

    for model_name in get_model_registry():
        model, scaler, predictions = fit_and_predict(model_name, X_train, X_test)
        metrics = evaluate_predictions(y_test, predictions)

        result = {
            "model_name": model_name,
            "metrics": metrics,
        }
        results.append(result)
        logger.info("Model %s -> %s", model_name, metrics)

        if best_result is None or metrics["f1"] > best_result["metrics"]["f1"]:
            best_result = result
            best_bundle = ModelBundle(
                model_name=model_name,
                feature_columns=list(FEATURE_COLUMNS),
                scaler=scaler,
                model=model,
            )

    if best_bundle is None or best_result is None:
        raise RuntimeError("No model was trained successfully.")

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_path": str(dataset_path),
        "rows": len(df),
        "feature_columns": FEATURE_COLUMNS,
        "best_model": best_result["model_name"],
        "best_model_metrics": best_result["metrics"],
        "all_results": results,
    }

    joblib.dump(best_bundle, ARTIFACT_DIR / "best_model.joblib")
    (ARTIFACT_DIR / "model_comparison.json").write_text(json.dumps(metadata, indent=2))

    logger.info("Best model selected: %s with F1 %.4f", best_result["model_name"], best_result["metrics"]["f1"])
    return metadata


if __name__ == "__main__":
    run_training_pipeline()
