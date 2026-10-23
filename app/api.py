from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.database_models import (
    Transaction,
    RiskAssessment,
    AgentInteraction
)
from app.ml.risk_engine import calculate_risk
from app.agent.agent import AdaptiveQuoteAgent


app = FastAPI(
    title="AdaptiveQuote AI API",
    description="API for AdaptiveQuote AI Agent",
    version="1.0.0"
)


# -----------------------------
# Request Models
# -----------------------------

class AgentRequest(BaseModel):
    user_input: str
    transaction_id: int | None = None
    transaction: dict | None = None


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "AdaptiveQuote AI API is running",
        "status": "success"
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -----------------------------
# Risk Prediction
# -----------------------------

@app.post("/risk")
def predict_risk(
    transaction: dict,
    db: Session = Depends(get_db)
):
    try:
        # -----------------------------
        # Validate required fields
        # -----------------------------

        required_fields = [
            "amount",
            "hour"
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in transaction
        ]

        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Missing required transaction fields",
                    "missing_fields": missing_fields
                }
            )

        # -----------------------------
        # Run AI risk prediction
        # -----------------------------

        risk_score, risk_level, model_version = calculate_risk(transaction)        # -----------------------------
        # Save transaction
        # -----------------------------

        db_transaction = Transaction(
            amount=transaction["amount"],
            hour=transaction["hour"],
            previous_transaction_amount=transaction.get(
                "previous_transaction_amount"
            ),
            transaction_frequency=transaction.get(
                "transaction_frequency"
            ),
            account_age_days=transaction.get(
                "account_age_days"
            )
        )

        db.add(db_transaction)

        # Flush so PostgreSQL generates the transaction ID
        db.flush()

        # -----------------------------
        # Save risk assessment
        # -----------------------------

        risk_score = float(risk_score)

        risk_assessment = RiskAssessment(
            transaction_id=db_transaction.id,
            risk_score=round(risk_score, 2),
            risk_level=risk_level,
            model_version=model_version
        )

        db.add(risk_assessment)

        # -----------------------------
        # Commit both records
        # -----------------------------

        db.commit()

        # Refresh objects from database
        db.refresh(db_transaction)
        db.refresh(risk_assessment)

        # -----------------------------
        # API response
        # -----------------------------

        return {
            "transaction_id": db_transaction.id,
            "risk_assessment_id": risk_assessment.id,
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "model_version": model_version,
            "status": "saved"
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Risk assessment failed: {str(e)}"
        )


# -----------------------------
# AI Agent
# -----------------------------

@app.post("/agent")
def run_agent(
    request: AgentRequest,
    db: Session = Depends(get_db)
):
    try:
        # -----------------------------
        # Get transaction
        # -----------------------------

        transaction_id = request.transaction_id
        transaction_data = request.transaction

        if transaction_id is not None:
            transaction = db.get(
                Transaction,
                transaction_id
            )

            if transaction:
                transaction_data = {
                    "transaction_id": transaction.id,
                    "amount": float(transaction.amount),
                    "hour": transaction.hour,
                    "previous_transaction_amount": (
                        float(transaction.previous_transaction_amount)
                        if transaction.previous_transaction_amount is not None
                        else None
                    ),
                    "transaction_frequency": transaction.transaction_frequency,
                    "account_age_days": transaction.account_age_days
                }
            else:
                transaction_id = None

                if transaction:
                    transaction_id = transaction.id

                    transaction_data = {
                        "transaction_id": transaction.id,
                        "amount": float(transaction.amount),
                        "hour": transaction.hour,
                        "previous_transaction_amount": (
                            float(transaction.previous_transaction_amount)
                            if transaction.previous_transaction_amount is not None
                            else None
                        ),
                        "transaction_frequency": transaction.transaction_frequency,
                        "account_age_days": transaction.account_age_days
                    }

        # -----------------------------
        # Run AI Agent
        # -----------------------------

        agent = AdaptiveQuoteAgent()

        response = agent.run(
            request.user_input,
            transaction_data
        )

        # -----------------------------
        # Save Agent Interaction
        # -----------------------------

        interaction = AgentInteraction(
            transaction_id=transaction_id,
            user_input=request.user_input,
            agent_response=response
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        # -----------------------------
        # Return response
        # -----------------------------

        return {
            "interaction_id": interaction.id,
            "transaction_id": transaction_id,
            "response": response,
            "status": "saved"
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Agent interaction failed: {str(e)}"
        )