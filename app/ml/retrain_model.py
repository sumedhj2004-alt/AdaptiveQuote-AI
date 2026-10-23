from datetime import datetime
import json
import math
import os
from pathlib import Path
import shutil

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

from app.ml.features import create_features
from app.database import SessionLocal
from app.models.database_models import ModelVersion


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "app" / "ml" / "data" / "feedback_training.csv"
MODEL_FILE = PROJECT_ROOT / "app" / "ml" / "models" / "anomaly_model.pkl"
VERSIONS_DIR = PROJECT_ROOT / "app" / "ml" / "versions"
REGISTRY_FILE = VERSIONS_DIR / "model_registry.json"

MINIMUM_SAMPLES = 20
REQUIRED_COLUMNS = {
    "amount",
    "hour",
    "previous_transaction_amount",
    "transaction_frequency",
    "account_age_days",
    "human_label",
}


def _metrics(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
    }


def _write_json_atomic(path: Path, contents):
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(contents, file, indent=4)
        file.flush()
        os.fsync(file.fileno())
    os.replace(temporary_path, path)


def retrain_model():
    print("\n--- Self-Learning Model Retraining ---")

    if not DATA_FILE.exists():
        print(f"Feedback dataset not found: {DATA_FILE}")
        print("Generate the feedback dataset first. Existing model will NOT be modified.")
        return False

    dataframe = pd.read_csv(DATA_FILE)
    print(f"Feedback samples: {len(dataframe)}")

    if len(dataframe) < MINIMUM_SAMPLES:
        print("Not enough samples for retraining.")
        print(f"Current samples: {len(dataframe)}; minimum required: {MINIMUM_SAMPLES}.")
        print("Existing model will NOT be modified.")
        return False

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        print(f"Retraining cancelled; dataset is missing columns: {sorted(missing_columns)}")
        print("Existing model will NOT be modified.")
        return False

    labels = pd.to_numeric(dataframe["human_label"], errors="coerce")
    if labels.isna().any() or not set(labels.unique()).issubset({0, 1}):
        print("Retraining cancelled; human_label must contain only 0 and 1.")
        print("Existing model will NOT be modified.")
        return False

    class_counts = labels.value_counts()
    if len(class_counts) < 2 or class_counts.min() < 2:
        print("Retraining cancelled; at least two examples of each label are required.")
        print("Existing model will NOT be modified.")
        return False

    dataframe = dataframe.copy()
    dataframe["human_label"] = labels.astype(int)
    features = create_features(dataframe).replace([np.inf, -np.inf], np.nan)
    if features.isna().any().any():
        print("Retraining cancelled; feature data contains missing or non-finite values.")
        print("Existing model will NOT be modified.")
        return False

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        dataframe["human_label"],
        test_size=0.2,
        random_state=42,
        stratify=dataframe["human_label"],
    )

    candidate = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )
    candidate.fit(X_train, y_train)
    candidate_predictions = candidate.predict(X_test)
    candidate_metrics = _metrics(y_test, candidate_predictions)

    print("\n--- Candidate Evaluation ---")
    print(classification_report(y_test, candidate_predictions, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, candidate_predictions))
    print("Candidate metrics:", candidate_metrics)

    if not MODEL_FILE.exists():
        print("Retraining cancelled; active model file is missing, so comparison is unavailable.")
        print("Existing model will NOT be modified.")
        return False

    try:
        active_model = joblib.load(MODEL_FILE)
        active_predictions = active_model.predict(X_test)
        active_metrics = _metrics(y_test, active_predictions)
    except Exception as error:
        print(f"Retraining cancelled; active model could not be evaluated: {error}")
        print("Existing model will NOT be modified.")
        return False

    print("Active model metrics:", active_metrics)
    promote = (
        candidate_metrics["f1"] > active_metrics["f1"]
        or (
            math.isclose(candidate_metrics["f1"], active_metrics["f1"])
            and candidate_metrics["accuracy"] > active_metrics["accuracy"]
        )
    )
    if not promote:
        print("Candidate did not improve suspicious-class F1 (or accuracy on an F1 tie).")
        print("Candidate was NOT promoted; active model remains unchanged.")
        return False

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_name = f"anomaly_model_{timestamp}"
    version_file = VERSIONS_DIR / f"{version_name}.pkl"
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    temporary_model = MODEL_FILE.with_suffix(MODEL_FILE.suffix + ".tmp")
    backup_model = MODEL_FILE.with_suffix(MODEL_FILE.suffix + ".bak")

    if REGISTRY_FILE.exists():
        with REGISTRY_FILE.open("r", encoding="utf-8") as file:
            registry = json.load(file)
    else:
        registry = {"models": []}
    if not isinstance(registry.get("models"), list):
        raise ValueError("model registry must contain a 'models' list")

    registry["models"].append({
        "version": version_name,
        "model_file": version_file.name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "training_samples": len(dataframe),
        "class_distribution": {
            "legitimate": int((dataframe["human_label"] == 0).sum()),
            "suspicious": int((dataframe["human_label"] == 1).sum()),
        },
        "evaluation": {
            "accuracy": round(candidate_metrics["accuracy"], 4),
            "suspicious_precision": round(candidate_metrics["precision"], 4),
            "suspicious_recall": round(candidate_metrics["recall"], 4),
            "suspicious_f1": round(candidate_metrics["f1"], 4),
        },
        "active_model_evaluation": {
            "accuracy": round(active_metrics["accuracy"], 4),
            "suspicious_f1": round(active_metrics["f1"], 4),
        },
    })

    try:
        joblib.dump(candidate, version_file)
        shutil.copy2(version_file, temporary_model)
        shutil.copy2(MODEL_FILE, backup_model)
        os.replace(temporary_model, MODEL_FILE)
        _write_json_atomic(REGISTRY_FILE, registry)

    except Exception:
        if backup_model.exists():
            os.replace(backup_model, MODEL_FILE)

        if temporary_model.exists():
            temporary_model.unlink()

        raise

    else:
        backup_model.unlink(missing_ok=True)

    # Save model version metrics to PostgreSQL
    db = SessionLocal()

    try:
        model_version = ModelVersion(
            model_name="anomaly_model",
            version=version_name,
            accuracy=round(candidate_metrics["accuracy"], 4),
            precision_score=round(candidate_metrics["precision"], 4),
            recall_score=round(candidate_metrics["recall"], 4),
            f1_score=round(candidate_metrics["f1"], 4),
        )

        db.add(model_version)
        db.commit()

        print("Model version saved to PostgreSQL.")

    except Exception as error:
        db.rollback()
        print(f"Warning: PostgreSQL model version save failed: {error}")

    finally:
        db.close()

    print("\nCandidate promoted.")
    print(f"Active model: {MODEL_FILE}")
    print(f"Version saved: {version_file}")
    print(f"Registry updated: {REGISTRY_FILE}")

    return True


if __name__ == "__main__":
    retrain_model()
