import streamlit as st
import requests
import pandas as pd

from sqlalchemy import select, func

from app.database import SessionLocal
from app.models.database_models import (
    Transaction,
    RiskAssessment,
    HumanFeedback,
    AgentInteraction,
)

API_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AdaptiveQuote AI",
    page_icon="🧠",
    layout="wide",
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 AdaptiveQuote AI")
st.caption(
    "AI-Powered Transaction Risk, RAG Policy Intelligence & Human Feedback Platform"
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎛️ Transaction Analysis")

transaction_id = st.sidebar.number_input(
    "Transaction ID",
    min_value=1,
    value=6,
    step=1,
)

user_input = st.sidebar.text_area(
    "Ask AI Agent",
    value="Analyze this transaction and tell me whether it requires human review.",
)

analyze_button = st.sidebar.button(
    "🔍 Analyze Transaction",
    use_container_width=True,
)

# API STATUS

try:
    health = requests.get(f"{API_URL}/health", timeout=5)

    if health.status_code == 200:
        st.sidebar.success("🟢 API Connected")
    else:
        st.sidebar.error("🔴 API Error")

except requests.exceptions.RequestException:
    st.sidebar.error("🔴 API Offline")


# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------

db = SessionLocal()

try:
    transaction_count = db.scalar(
        select(func.count()).select_from(Transaction)
    ) or 0

    assessment_count = db.scalar(
        select(func.count()).select_from(RiskAssessment)
    ) or 0

    feedback_count = db.scalar(
        select(func.count()).select_from(HumanFeedback)
    ) or 0

    interaction_count = db.scalar(
        select(func.count()).select_from(AgentInteraction)
    ) or 0

finally:
    db.close()


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Transactions", transaction_count)

with m2:
    st.metric("Risk Assessments", assessment_count)

with m3:
    st.metric("Human Feedback", feedback_count)

with m4:
    st.metric("AI Interactions", interaction_count)


# --------------------------------------------------
# AI AGENT
# --------------------------------------------------

if analyze_button:

    payload = {
        "user_input": user_input,
        "transaction_id": int(transaction_id),
    }

    try:

        response = requests.post(
            f"{API_URL}/agent",
            json=payload,
            timeout=60,
        )

        if response.status_code == 200:

            data = response.json()

            st.success("✅ AI analysis completed successfully")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Transaction ID",
                    data.get("transaction_id", "N/A"),
                )

            with col2:
                st.metric(
                    "Interaction ID",
                    data.get("interaction_id", "N/A"),
                )

            st.subheader("🤖 AI Agent Analysis")

            st.info(
                data.get(
                    "response",
                    "No response received.",
                )
            )

        else:

            st.error(
                f"Agent API Error: {response.status_code}\n\n"
                f"{response.text}"
            )

    except requests.exceptions.RequestException as e:

        st.error(f"Could not connect to API: {e}")


# --------------------------------------------------
# RISK ANALYSIS
# --------------------------------------------------

st.divider()

st.header("📊 Risk Analysis")

st.caption(
    "Evaluate a transaction using the trained machine-learning risk engine."
)

col1, col2, col3 = st.columns(3)

with col1:

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=18000.0,
    )

    hour = st.number_input(
        "Transaction Hour",
        min_value=0,
        max_value=23,
        value=18,
    )

with col2:

    previous_amount = st.number_input(
        "Previous Transaction Amount",
        min_value=0.0,
        value=5000.0,
    )

    transaction_frequency = st.number_input(
        "Transaction Frequency",
        min_value=0,
        value=10,
    )

with col3:

    account_age = st.number_input(
        "Account Age (Days)",
        min_value=0,
        value=1000,
    )

    risk_button = st.button(
        "⚡ Calculate Risk",
        use_container_width=True,
    )


if risk_button:

    risk_payload = {
        "amount": amount,
        "hour": hour,
        "previous_transaction_amount": previous_amount,
        "transaction_frequency": transaction_frequency,
        "account_age_days": account_age,
    }

    try:

        response = requests.post(
            f"{API_URL}/risk",
            json=risk_payload,
            timeout=30,
        )

        if response.status_code == 200:

            risk_data = response.json()

            st.success("✅ Risk assessment completed")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Risk Score",
                    risk_data.get("risk_score", "N/A"),
                )

            with col2:
                st.metric(
                    "Risk Level",
                    risk_data.get("risk_level", "N/A"),
                )

            with col3:
                st.metric(
                    "Model Version",
                    risk_data.get("model_version", "N/A"),
                )

        else:

            st.error(
                f"Risk API Error: {response.status_code}\n\n"
                f"{response.text}"
            )

    except requests.exceptions.RequestException as e:

        st.error(f"Could not connect to API: {e}")


# --------------------------------------------------
# HUMAN FEEDBACK
# --------------------------------------------------

st.divider()

st.header("👤 Human Review & Feedback")

feedback_col1, feedback_col2 = st.columns(2)

with feedback_col1:

    feedback_transaction_id = st.number_input(
        "Transaction ID for Review",
        min_value=1,
        value=int(transaction_id),
        step=1,
    )

    decision = st.selectbox(
        "Human Decision",
        [
            "legitimate",
            "suspicious",
            "investigate",
        ],
    )

with feedback_col2:

    reviewer = st.text_input(
        "Reviewer",
        value="human_reviewer",
    )

    comment = st.text_area(
        "Review Comment",
        value="Reviewed by human reviewer.",
    )


feedback_button = st.button(
    "💾 Submit Human Feedback",
    use_container_width=True,
)


if feedback_button:

    try:

        from app.agent.tools.feedback_tool import record_feedback

        result = record_feedback(
            str(feedback_transaction_id),
            decision,
            reviewer,
            comment,
        )

        if "error" in result:

            st.error(result["error"])

        else:

            st.success("✅ Human feedback saved successfully")

            st.json(result)

    except Exception as e:

        st.error(f"Feedback error: {e}")


# --------------------------------------------------
# RECENT RISK ASSESSMENTS
# --------------------------------------------------

st.divider()

st.header("📋 Recent Risk Assessments")

db = SessionLocal()

try:

    assessments = db.execute(
        select(
            RiskAssessment.id,
            RiskAssessment.transaction_id,
            RiskAssessment.risk_score,
            RiskAssessment.risk_level,
            RiskAssessment.model_version,
            RiskAssessment.created_at,
        )
        .order_by(RiskAssessment.id.desc())
        .limit(10)
    ).all()

finally:

    db.close()


if assessments:

    assessment_data = [
        {
            "Assessment ID": row.id,
            "Transaction ID": row.transaction_id,
            "Risk Score": float(row.risk_score),
            "Risk Level": row.risk_level,
            "Model Version": row.model_version,
            "Created": row.created_at,
        }
        for row in assessments
    ]

    st.dataframe(
        pd.DataFrame(assessment_data),
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("No risk assessments found.")


# --------------------------------------------------
# HUMAN FEEDBACK HISTORY
# --------------------------------------------------

st.header("📝 Recent Human Feedback")

db = SessionLocal()

try:

    feedback_rows = db.execute(
        select(
            HumanFeedback.id,
            HumanFeedback.transaction_id,
            HumanFeedback.risk_assessment_id,
            HumanFeedback.human_decision,
            HumanFeedback.corrected_risk_level,
            HumanFeedback.feedback_comment,
            HumanFeedback.created_at,
        )
        .order_by(HumanFeedback.id.desc())
        .limit(10)
    ).all()

finally:

    db.close()


if feedback_rows:

    feedback_data = [
        {
            "Feedback ID": row.id,
            "Transaction ID": row.transaction_id,
            "Risk Assessment": row.risk_assessment_id,
            "Decision": row.human_decision,
            "Corrected Risk": row.corrected_risk_level or "-",
            "Comment": row.feedback_comment or "-",
            "Created": row.created_at,
        }
        for row in feedback_rows
    ]

    st.dataframe(
        pd.DataFrame(feedback_data),
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("No human feedback found.")


# --------------------------------------------------
# SYSTEM ARCHITECTURE
# --------------------------------------------------

st.divider()

st.header("🏗️ System Architecture")

st.code(
    """
User / Dashboard
       │
       ▼
   FastAPI API
       │
       ├──────────────► PostgreSQL
       │
       ▼
  ML Risk Engine
       │
       ▼
   Risk Score
       │
       ▼
  AI Agent (Ollama)
       │
       ├──────────────► RAG / ChromaDB
       │
       ▼
Human Review
       │
       ▼
Feedback Dataset
       │
       ▼
Automated Retraining
       │
       ▼
Model Versioning
    """,
    language="text",
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AdaptiveQuote AI • FastAPI • PostgreSQL • Machine Learning • "
    "RAG • Ollama • Human Feedback • Automated Retraining"
)