import ollama

from app.agent.tools.risk_tool import risk_prediction_tool
from app.agent.tools.policy_tool import policy_search_tool
from app.agent.tools.feedback_tool import (
    record_feedback,
    get_feedback_summary
)
class AdaptiveQuoteAgent:

    def __init__(self):
        print("AdaptiveQuote AI Agent initialized!")

    def submit_feedback(
        self,
        transaction_id,
        decision,
        reviewer="human_reviewer",
        comment=""
    ):
        """
        Record a human review decision.
        """

        return record_feedback(
            transaction_id=transaction_id,
            decision=decision,
            reviewer=reviewer,
            comment=comment
        )

    def get_feedback_summary(self):
        """
        Return a summary of human review decisions.
        """

        return get_feedback_summary()

    def run(self, user_input, transaction=None):

        # Decide whether risk analysis is required
        risk_keywords = [
            "analyze",
            "calculate risk",
            "assess",
            "risk score",
            "risk prediction",
            "detect fraud",
            "detect anomaly"
        ]

        needs_risk_tool = any(
            keyword in user_input.lower()
            for keyword in risk_keywords
        )

        # Run risk tool when required
        risk_result = None

        if needs_risk_tool:

            if transaction is None:
                return "Risk analysis requires transaction data."

            risk_result = risk_prediction_tool(transaction)

        # Retrieve relevant policy
        policy_result = policy_search_tool(user_input)
        context = "\n\n".join(policy_result["results"])

        # Build context for the LLM
        risk_context = ""

        if risk_result:
            risk_context = f"""
RISK TOOL RESULT:
Risk Score: {risk_result["risk_score"]}/100
Risk Level: {risk_result["risk_level"]}
"""

        prompt = f"""
You are AdaptiveQuote AI, an AI assistant for quotation and financial risk analysis.

Use the policy context and risk tool result to answer the user.

POLICY CONTEXT:
{context}

{risk_context}

USER REQUEST:
{user_input}

Rules:
- Do not invent policy rules.
- Do not invent, modify, estimate, or recalculate the ML risk score.
- If a RISK TOOL RESULT is provided, report its exact Risk Score and Risk Level.
- Do not claim that the risk tool was used unless a RISK TOOL RESULT is present.
- Do not invent transaction characteristics or risk indicators that are not present in the tool result or policy context.
- Clearly distinguish ML risk results from policy information.
- If information is insufficient, say what additional information is required.

Provide a concise and useful response.
"""

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]


if __name__ == "__main__":

    agent = AdaptiveQuoteAgent()

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

    response = agent.run(
        "What should happen when a transaction is classified as high risk?"
    )

    print("\nAgent Response:")
    print(response)



