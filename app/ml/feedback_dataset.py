from pathlib import Path

import pandas as pd

from app.database import SessionLocal
from app.models.database_models import HumanFeedback, Transaction


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRANSACTIONS_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "data"
    / "transactions.csv"
)

HISTORICAL_FEEDBACK_FILE = (
    PROJECT_ROOT
    / "app"
    / "agent"
    / "data"
    / "human_review_batch.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "data"
    / "feedback_training.csv"
)


def create_feedback_training_data():

    print("\n--- Creating Feedback Training Dataset ---")

    transactions = pd.read_csv(TRANSACTIONS_FILE)

    # ---------------------------------------------------------
    # 1. Load historical human reviews
    # ---------------------------------------------------------

    historical_feedback = pd.read_csv(HISTORICAL_FEEDBACK_FILE)

    label_mapping = {
        "suspicious": 1,
        "legitimate": 0
    }

    historical_feedback["human_label"] = (
        historical_feedback["human_decision"]
        .map(label_mapping)
    )

    historical_feedback = historical_feedback.dropna(
        subset=["human_label"]
    )

    historical_feedback["human_label"] = (
        historical_feedback["human_label"].astype(int)
    )

    historical_feedback = historical_feedback.drop_duplicates(
        subset=["transaction_id"],
        keep="last"
    )

    historical_labels = historical_feedback[
        ["transaction_id", "human_label"]
    ]

    historical_dataset = transactions.merge(
        historical_labels,
        on="transaction_id",
        how="inner"
    )

    # ---------------------------------------------------------
    # 2. Load new PostgreSQL human feedback
    # ---------------------------------------------------------

    db = SessionLocal()

    try:

        feedback_rows = (
            db.query(HumanFeedback)
            .order_by(HumanFeedback.id.asc())
            .all()
        )

        postgres_data = []

        for feedback in feedback_rows:

            if feedback.human_decision not in [
                "suspicious",
                "legitimate"
            ]:
                continue

            transaction = db.get(
                Transaction,
                feedback.transaction_id
            )

            if transaction is None:
                continue

            human_label = (
                1
                if feedback.human_decision == "suspicious"
                else 0
            )

            postgres_data.append({
                "transaction_id": str(transaction.id),
                "amount": float(transaction.amount),
                "hour": transaction.hour,
                "previous_transaction_amount": (
                    float(transaction.previous_transaction_amount)
                    if transaction.previous_transaction_amount is not None
                    else None
                ),
                "transaction_frequency": transaction.transaction_frequency,
                "account_age_days": transaction.account_age_days,
                "human_label": human_label
            })

    finally:
        db.close()

    postgres_dataset = pd.DataFrame(postgres_data)

    # ---------------------------------------------------------
    # 3. Combine historical + PostgreSQL feedback
    # ---------------------------------------------------------

    if not postgres_dataset.empty:

        historical_dataset["transaction_source"] = "historical"
        postgres_dataset["transaction_source"] = "postgresql"

        combined = pd.concat(
            [
                historical_dataset,
                postgres_dataset
            ],
            ignore_index=True
        )

    else:

        combined = historical_dataset

    # Keep only features required by the ML model
    required_columns = [
        "transaction_id",
        "amount",
        "hour",
        "previous_transaction_amount",
        "transaction_frequency",
        "account_age_days",
        "human_label"
    ]

    combined = combined[required_columns]

    # Remove duplicate transaction IDs.
    # New PostgreSQL feedback takes priority.
    combined = combined.drop_duplicates(
        subset=["transaction_id"],
        keep="last"
    )

    combined.to_csv(
        OUTPUT_FILE,
        index=False
    )

    return combined


if __name__ == "__main__":

    dataset = create_feedback_training_data()

    print("\n--- Feedback Training Dataset ---")

    if dataset.empty:

        print("No matching feedback found.")

    else:

        print("Rows:", len(dataset))

        print("\nLabel distribution:")

        print(
            dataset["human_label"]
            .value_counts()
            .sort_index()
            .rename(
                index={
                    0: "legitimate",
                    1: "suspicious"
                }
            )
        )

        print("\nTraining Data:")

        print(dataset)

        minimum_samples = 20

        print("\n--- Retraining Safety Check ---")

        if len(dataset) < minimum_samples:

            print(
                "Not enough human feedback for retraining."
            )

            print(
                f"Current samples: {len(dataset)}"
            )

            print(
                f"Minimum required: {minimum_samples}"
            )

            print(
                "Existing model will NOT be modified."
            )

        else:

            print(
                "Enough feedback available for retraining."
            )

        print("\nSaved to:")
        print(OUTPUT_FILE)