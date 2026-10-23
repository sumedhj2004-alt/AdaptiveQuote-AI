from pathlib import Path

import joblib

from app.ml.features import create_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "models"
    / "anomaly_model.pkl"
)


def main():

    print("\n--- Model Test ---")

    print("Loading model from:")
    print(MODEL_FILE)

    model = joblib.load(MODEL_FILE)

    print("Model loaded successfully!")

    transaction = {
        "amount": 61029.05,
        "hour": 23,
        "previous_transaction_amount": 3784.03,
        "transaction_frequency": 5,
        "account_age_days": 181,
    }

    import pandas as pd

    dataframe = pd.DataFrame([transaction])

    features = create_features(dataframe)

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    print("\n--- Prediction ---")
    print("Prediction:", prediction)
    print("Risk Probability:", round(probability, 4))
    print("Risk Score:", round(probability * 100, 2))


if __name__ == "__main__":
    main()