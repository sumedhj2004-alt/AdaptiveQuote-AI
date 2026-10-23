from datetime import datetime
from pathlib import Path
import csv

from app.database import SessionLocal
from app.models.database_models import (
    HumanFeedback,
    Transaction,
    RiskAssessment
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

FEEDBACK_DIR = PROJECT_ROOT / "app" / "agent" / "data"
FEEDBACK_FILE = FEEDBACK_DIR / "feedback.csv"


def record_feedback(
    transaction_id: str,
    decision: str,
    reviewer: str = "human_reviewer",
    comment: str = ""
):
    """
    Record human feedback in both:
    1. CSV file for the existing self-learning pipeline
    2. PostgreSQL for persistent application storage
    """

    valid_decisions = [
        "suspicious",
        "legitimate",
        "investigate"
    ]

    decision = decision.lower()

    if decision not in valid_decisions:
        raise ValueError(
            f"Invalid decision. Choose from: {valid_decisions}"
        )

    # --------------------------------------------------
    # Convert transaction ID to integer
    # --------------------------------------------------

    try:
        transaction_id_int = int(transaction_id)
    except (TypeError, ValueError):
        raise ValueError(
            "transaction_id must be a valid database transaction ID."
        )

    timestamp = datetime.now().isoformat()

    # --------------------------------------------------
    # Save to CSV
    # --------------------------------------------------

    feedback = {
        "transaction_id": str(transaction_id_int),
        "decision": decision,
        "reviewer": reviewer,
        "comment": comment,
        "timestamp": timestamp
    }

    FEEDBACK_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_exists = FEEDBACK_FILE.exists()

    with open(
        FEEDBACK_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=feedback.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(feedback)

    # --------------------------------------------------
    # Save to PostgreSQL
    # --------------------------------------------------

    db = SessionLocal()

    try:
        # Check transaction exists
        transaction = db.get(
            Transaction,
            transaction_id_int
        )

        if transaction is None:
            raise ValueError(
                f"Transaction {transaction_id_int} does not exist."
            )

        # Find the related risk assessment
        risk_assessment = (
            db.query(RiskAssessment)
            .filter(
                RiskAssessment.transaction_id
                == transaction_id_int
            )
            .order_by(
                RiskAssessment.id.desc()
            )
            .first()
        )

        risk_assessment_id = None

        if risk_assessment:
            risk_assessment_id = risk_assessment.id

        # Store reviewer inside the comment if supplied
        database_comment = comment

        if reviewer:
            database_comment = (
                f"Reviewer: {reviewer}"
                + (
                    f" | {comment}"
                    if comment
                    else ""
                )
            )

        human_feedback = HumanFeedback(
            transaction_id=transaction_id_int,
            risk_assessment_id=risk_assessment_id,
            human_decision=decision,
            corrected_risk_level=None,
            feedback_comment=database_comment
        )

        db.add(human_feedback)

        db.commit()

        db.refresh(human_feedback)

        feedback["database_feedback_id"] = human_feedback.id
        feedback["risk_assessment_id"] = risk_assessment_id

        return feedback

    except Exception:
        db.rollback()

        # Important:
        # The CSV has already been written.
        # Re-raise the error so the caller knows
        # PostgreSQL storage failed.
        raise

    finally:
        db.close()


def get_feedback():
    """
    Retrieve all stored human feedback from CSV.
    """

    if not FEEDBACK_FILE.exists():
        return []

    with open(
        FEEDBACK_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def get_feedback_summary():
    """
    Generate a summary of stored human feedback.
    """

    feedback = get_feedback()

    summary = {
        "total_reviews": len(feedback),
        "suspicious": 0,
        "legitimate": 0,
        "investigate": 0
    }

    for item in feedback:

        decision = item["decision"]

        if decision in summary:
            summary[decision] += 1

    return summary


if __name__ == "__main__":

    summary = get_feedback_summary()

    print("\n--- Human Feedback Summary ---")
    print("Total Reviews:", summary["total_reviews"])
    print("Suspicious:", summary["suspicious"])
    print("Legitimate:", summary["legitimate"])
    print("Investigate:", summary["investigate"])