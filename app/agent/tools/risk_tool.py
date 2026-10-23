from app.ml.risk_engine import calculate_risk


def risk_prediction_tool(transaction: dict):
    """
    Agent tool for calculating transaction risk.
    """

    risk_score, risk_level, model_version = calculate_risk(transaction)
    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level
    }


if __name__ == "__main__":

    transaction = {
        "transaction_id": "TX_AGENT_001",
        "customer_id": "CUST0001",
        "amount": 18000.00,
        "merchant_category": "Electronics",
        "transaction_type": "Purchase",
        "location": "Delhi",
        "device_type": "Tablet",
        "hour": 18,
        "account_age_days": 1000,
        "previous_transaction_amount": 5000.00,
        "transaction_frequency": 10,
    }

    result = risk_prediction_tool(transaction)

    print("\n--- Agent Risk Tool ---")
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])