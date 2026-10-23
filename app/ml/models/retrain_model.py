from pathlib import Path
from datetime import datetime
import json
import shutil
from app.database import SessionLocal
from app.models.database_models import ModelVersion

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from app.ml.features import create_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "data"
    / "feedback_training.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "models"
    / "anomaly_model.pkl"
)

VERSIONS_DIR = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "versions"
)

REGISTRY_FILE = (
    VERSIONS_DIR
    / "model_registry.json"
)

MINIMUM_SAMPLES = 20


def retrain_model():

    print("\n--- Self-Learning Model Retraining ---")

    dataframe = pd.read_csv(DATA_FILE)

    print(f"Feedback samples: {len(dataframe)}")

    if len(dataframe) < MINIMUM_SAMPLES:
        print("Not enough samples for retraining.")
        print(f"Current samples: {len(dataframe)}")
        print(f"Minimum required: {MINIMUM_SAMPLES}")
        print("Existing model will NOT be modified.")
        return

    X = create_features(dataframe)
    y = dataframe["human_label"]

    if y.nunique() < 2:
        print("Retraining cancelled.")
        print("Both legitimate and suspicious labels are required.")
        print("Existing model will NOT be modified.")
        return

    print("\nClass distribution:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    print("\nNew model trained successfully!")

    y_pred = model.predict(X_test)

    print("\n--- Model Evaluation ---")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    print("\n--- Confusion Matrix ---")
    print(confusion_matrix(y_test, y_pred))

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        pos_label=1,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        pos_label=1,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        pos_label=1,
        zero_division=0
    )

    MODEL_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    VERSIONS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save active model
    joblib.dump(
        model,
        MODEL_FILE
    )

    # Create timestamped version
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    version_name = f"anomaly_model_{timestamp}"

    version_file = (
        VERSIONS_DIR
        / f"{version_name}.pkl"
    )

    shutil.copy2(
        MODEL_FILE,
        version_file
    )

    # Load registry
    if REGISTRY_FILE.exists():

        with open(
            REGISTRY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            registry = json.load(file)

    else:

        registry = {
            "models": []
        }

    model_metadata = {
        "version": version_name,
        "model_file": version_file.name,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "training_samples": len(dataframe),
        "class_distribution": {
            "legitimate": int((y == 0).sum()),
            "suspicious": int((y == 1).sum())
        },
        "evaluation": {
            "accuracy": round(accuracy, 4),
            "suspicious_precision": round(precision, 4),
            "suspicious_recall": round(recall, 4),
            "suspicious_f1": round(f1, 4)
        }
    }

    registry["models"].append(
        model_metadata
    )

    with open(
        REGISTRY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )

    print("\n--- Model Saving ---")
    print("Active model:")
    print(MODEL_FILE)

    print("\nVersion created:")
    print(version_file)

    print("\nModel registry updated:")
    print(REGISTRY_FILE)


if __name__ == "__main__":
    retrain_model()