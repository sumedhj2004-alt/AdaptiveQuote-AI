from pathlib import Path
import json
import joblib
import pandas as pd

from app.ml.features import create_features


def get_model_version():
    registry_file = (
        Path(__file__).resolve().parent
        / "versions"
        / "model_registry.json"
    )

    if not registry_file.exists():
        return "unknown"

    try:
        with open(registry_file, "r", encoding="utf-8") as file:
            registry = json.load(file)

        models = registry.get("models", [])

        if not models:
            return "unknown"

        return models[-1]["version"]

    except Exception:
        return "unknown"


def calculate_risk(transaction: dict):

    model_file = (
        Path(__file__).resolve().parent
        / "models"
        / "anomaly_model.pkl"
    )

    model = joblib.load(model_file)

    dataframe = pd.DataFrame([transaction])

    features = create_features(dataframe)

    probability = model.predict_proba(features)[0][1]

    risk_score = float(probability * 100)

    if risk_score <= 30:
        risk_level = "LOW"
    elif risk_score <= 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    model_version = get_model_version()

    return risk_score, risk_level, model_version