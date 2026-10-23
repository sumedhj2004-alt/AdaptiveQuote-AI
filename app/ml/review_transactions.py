from pathlib import Path
import joblib
import pandas as pd

from app.ml.features import create_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRANSACTIONS_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "data"
    / "transactions.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "models"
    / "anomaly_model.pkl"
)


def review_transactions():

    transactions = pd.read_csv(TRANSACTIONS_FILE)

    model = joblib.load(MODEL_FILE)

    features = create_features(transactions)

    probabilities = model.predict_proba(features)[:, 1]

    transactions["risk_probability"] = probabilities

    transactions["risk_score"] = probabilities * 100

    transactions["predicted_risk"] = transactions[
        "risk_probability"
    ].apply(
        lambda x:
            "LOW" if x <= 0.30
            else "MEDIUM" if x <= 0.70
            else "HIGH"
    )

    return transactions


if __name__ == "__main__":

    data = review_transactions()

    print("\n--- Transaction Review ---")

    print(
        data[
            [
                "transaction_id",
                "amount",
                "hour",
                "previous_transaction_amount",
                "transaction_frequency",
                "account_age_days",
                "risk_score",
                "predicted_risk"
            ]
        ].head(20).to_string(index=False)
    )