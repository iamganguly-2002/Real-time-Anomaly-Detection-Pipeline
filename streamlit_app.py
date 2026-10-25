import json
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_BASE = st.sidebar.text_input(
    "Backend URL",
    value="http://127.0.0.1:8001",
    help="The FastAPI backend that hosts the anomaly detection model.",
)

st.set_page_config(page_title="Anomaly Detection Demo", page_icon="📊", layout="wide")

st.title("Anomaly Detection Demo")
st.caption("IoT sensor anomaly classifier using the best trained model")


@st.cache_data(ttl=60)
def get_model_info() -> dict[str, Any]:
    try:
        response = requests.get(f"{API_BASE}/model-info", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as exc:  # pragma: no cover
        return {"error": str(exc)}


st.sidebar.markdown("### Backend status")
health_response = None
try:
    health_response = requests.get(f"{API_BASE}/health", timeout=10)
    health_response.raise_for_status()
    st.sidebar.success("Backend is online")
except Exception as exc:
    st.sidebar.error(f"Backend offline: {exc}")

model_info = get_model_info()
if "error" in model_info:
    st.warning("Model info is not available. Make sure the backend is running.")
else:
    st.sidebar.write(f"Model: {model_info.get('model_name', 'unknown')}")
    st.sidebar.write(f"Features: {model_info.get('feature_columns', [])}")

st.markdown("---")
st.subheader("Model comparison")
model_results = []
metadata = model_info.get("metadata", {}) if isinstance(model_info, dict) else {}
for result in metadata.get("all_results", []):
    metrics = result.get("metrics", {})
    model_results.append(
        {
            "Model": result.get("model_name", "Unknown"),
            "Accuracy": metrics.get("accuracy", 0.0),
            "Precision": metrics.get("precision", 0.0),
            "Recall": metrics.get("recall", 0.0),
            "F1 Score": metrics.get("f1", 0.0),
        }
    )

if model_results:
    comparison_df = pd.DataFrame(model_results).sort_values("F1 Score", ascending=False)
    st.dataframe(comparison_df, width="stretch")
    st.bar_chart(comparison_df.set_index("Model")["F1 Score"])
else:
    st.info("Model comparison data is not available yet. Run the training pipeline first.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.number_input("Temperature", min_value=-50.0, max_value=100.0, value=25.0, step=0.1)
        humidity = st.number_input("Humidity", min_value=0.0, max_value=100.0, value=55.0, step=0.1)
    with col2:
        pressure = st.number_input("Pressure", min_value=900.0, max_value=1100.0, value=1013.0, step=0.1)
        vibration = st.number_input("Vibration", min_value=0.0, max_value=5.0, value=0.5, step=0.1)

    submitted = st.form_submit_button("Predict anomaly")

if submitted:
    payload = {
        "records": [
            {
                "temperature": float(temperature),
                "humidity": float(humidity),
                "pressure": float(pressure),
                "vibration": float(vibration),
            }
        ]
    }

    try:
        result = requests.post(
            f"{API_BASE}/predict",
            json=payload,
            timeout=15,
        )
        result.raise_for_status()
        data = result.json()

        prediction = data["predictions"][0]
        status = prediction["status"]
        anomaly = prediction["anomaly"]

        if anomaly:
            st.error(f"Prediction: {status.upper()} - anomaly detected")
        else:
            st.success(f"Prediction: {status.upper()} - sensor reading is normal")

        st.json({
            "model_name": data["model_name"],
            "prediction": prediction,
        })
    except Exception as exc:
        st.error(f"Prediction request failed: {exc}")


st.markdown("---")
st.subheader("Project summary")
st.markdown(
    """
    This dashboard compares multiple anomaly detection algorithms, selects the best-performing model,
    and exposes predictions through a FastAPI backend. It is designed as a clean, interview-ready demo.
    """
)
