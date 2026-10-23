from pathlib import Path
import pandas as pd
import joblib

from app.ml.features import create_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRANSACTIONS_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "data"
    / "transactions.csv"
)

REVIEW_FILE = (
    PROJECT_ROOT
    / "app"
    / "agent"
    / "data"
    / "human_review_batch.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "models"
    / "anomaly_model.pkl"
)


def load_review_batch():

    transactions = pd.read_csv(TRANSACTIONS_FILE)
    review_batch = pd.read_csv(REVIEW_FILE)

    model = joblib.load(MODEL_FILE)

    features = create_features(transactions)

    probabilities = model.predict_proba(features)[:, 1]

    transactions["risk_score"] = probabilities * 100

    transactions["predicted_risk"] = transactions[
        "risk_score"
    ].apply(
        lambda x:
            "LOW" if x <= 30
            else "MEDIUM" if x <= 70
            else "HIGH"
    )

    merged = review_batch.merge(
        transactions,
        on="transaction_id",
        how="left"
    )

    return merged


def save_review(transaction_id, decision, reviewer, comment):


    review_batch = pd.read_csv(
        REVIEW_FILE,
        dtype=str
    )

    index = review_batch[
        review_batch["transaction_id"] == transaction_id
    ].index

    if len(index) == 0:
        return

    review_batch.loc[index, "human_decision"] = decision
    review_batch.loc[index, "reviewer"] = reviewer
    review_batch.loc[index, "comment"] = comment

    review_batch.to_csv(
        REVIEW_FILE,
        index=False
    )


if __name__ == "__main__":

    data = load_review_batch()

    reviewer = input("Enter reviewer name: ").strip()

    for _, transaction in data.iterrows():

        if pd.notna(transaction["human_decision"]):
            continue

        print("\n" + "=" * 60)

        print("Transaction ID:", transaction["transaction_id"])
        print("Amount:", transaction["amount"])
        print("Hour:", transaction["hour"])
        print(
            "Previous Amount:",
            transaction["previous_transaction_amount"]
        )
        print(
            "Transaction Frequency:",
            transaction["transaction_frequency"]
        )
        print(
            "Account Age:",
            transaction["account_age_days"]
        )

        print(
            "AI Risk Score:",
            f"{transaction['risk_score']:.2f}"
        )

        print(
            "AI Predicted Risk:",
            transaction["predicted_risk"]
        )

        print("\nHuman Decision:")
        print("1. suspicious")
        print("2. legitimate")
        print("3. investigate")

        choice = input("Enter choice: ").strip()

        decision_map = {
            "1": "suspicious",
            "2": "legitimate",
            "3": "investigate"
        }

        if choice not in decision_map:
            print("Invalid choice. Skipping transaction.")
            continue

        decision = decision_map[choice]

        comment = input("Review comment: ").strip()

        save_review(
            transaction_id=transaction["transaction_id"],
            decision=decision,
            reviewer=reviewer,
            comment=comment
        )

        print("✓ Review saved.")