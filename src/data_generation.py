from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

FEATURE_COLUMNS = ["temperature", "humidity", "pressure", "vibration"]
DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "sensor_anomalies_dataset.csv"


def _generate_normal_record(rng: np.random.Generator) -> dict:
    return {
        "temperature": float(rng.normal(25.0, 3.0)),
        "humidity": float(rng.normal(60.0, 8.0)),
        "pressure": float(rng.normal(1013.0, 5.0)),
        "vibration": float(rng.normal(0.5, 0.12)),
    }


def _generate_anomaly_record(rng: np.random.Generator) -> dict:
    anomaly_type = rng.choice(["temperature", "humidity", "pressure", "vibration"])
    record = _generate_normal_record(rng)

    if anomaly_type == "temperature":
        record["temperature"] = float(rng.choice([rng.normal(48.0, 6.0), rng.normal(5.0, 4.0)]))
    elif anomaly_type == "humidity":
        record["humidity"] = float(rng.choice([rng.normal(94.0, 3.0), rng.normal(8.0, 4.0)]))
    elif anomaly_type == "pressure":
        record["pressure"] = float(rng.choice([rng.normal(1055.0, 7.0), rng.normal(970.0, 6.0)]))
    else:
        record["vibration"] = float(rng.normal(2.3, 0.45))

    record["temperature"] = float(np.clip(record["temperature"], -20.0, 80.0))
    record["humidity"] = float(np.clip(record["humidity"], 0.0, 100.0))
    record["pressure"] = float(np.clip(record["pressure"], 900.0, 1100.0))
    record["vibration"] = float(np.clip(record["vibration"], 0.0, 5.0))
    return record


def generate_sensor_dataset(n_rows: int = 25000, anomaly_rate: float = 0.08, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    for _ in range(n_rows):
        if rng.random() < anomaly_rate:
            record = _generate_anomaly_record(rng)
            label = 1
        else:
            record = _generate_normal_record(rng)
            label = 0

        record["label"] = int(label)
        rows.append(record)

    df = pd.DataFrame(rows)
    df = df[["temperature", "humidity", "pressure", "vibration", "label"]]
    return df


def save_dataset(df: pd.DataFrame, output_path: Path = DATASET_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def ensure_dataset_exists(n_rows: int = 25000, anomaly_rate: float = 0.08, seed: int = 42) -> Path:
    path = DATASET_PATH
    if not path.exists():
        dataset = generate_sensor_dataset(n_rows=n_rows, anomaly_rate=anomaly_rate, seed=seed)
        save_dataset(dataset, path)
    return path
