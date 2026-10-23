from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(
        Numeric(15, 2),
        nullable=False
    )

    hour = Column(
        Integer,
        nullable=False
    )

    previous_transaction_amount = Column(
        Numeric(15, 2),
        nullable=True
    )

    transaction_frequency = Column(
        Integer,
        nullable=True
    )

    account_age_days = Column(
        Integer,
        nullable=True
    )

    risk_assessment = relationship(
        "RiskAssessment",
        back_populates="transaction",
        uselist=False
    )

    agent_interactions = relationship(
        "AgentInteraction",
        back_populates="transaction"
    )

    human_feedback = relationship(
        "HumanFeedback",
        back_populates="transaction"
    )


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        Integer,
        ForeignKey(
            "transactions.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    risk_score = Column(
        Numeric(5, 2),
        nullable=False
    )

    risk_level = Column(
        String(20),
        nullable=False
    )

    model_version = Column(
        String(50),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    transaction = relationship(
        "Transaction",
        back_populates="risk_assessment"
    )

    human_feedback = relationship(
        "HumanFeedback",
        back_populates="risk_assessment"
    )


class AgentInteraction(Base):
    __tablename__ = "agent_interactions"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        Integer,
        ForeignKey(
            "transactions.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    user_input = Column(
        Text,
        nullable=False
    )

    agent_response = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    transaction = relationship(
        "Transaction",
        back_populates="agent_interactions"
    )


class HumanFeedback(Base):
    __tablename__ = "human_feedback"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        Integer,
        ForeignKey(
            "transactions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    risk_assessment_id = Column(
        Integer,
        ForeignKey(
            "risk_assessments.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    human_decision = Column(
        String(30),
        nullable=False
    )

    corrected_risk_level = Column(
        String(20),
        nullable=True
    )

    feedback_comment = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    transaction = relationship(
        "Transaction",
        back_populates="human_feedback"
    )

    risk_assessment = relationship(
        "RiskAssessment",
        back_populates="human_feedback"
    )


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)

    model_name = Column(
        String(100),
        nullable=False
    )

    version = Column(
        String(50),
        nullable=False
    )

    accuracy = Column(
        Numeric(6, 4),
        nullable=True
    )

    precision_score = Column(
        Numeric(6, 4),
        nullable=True
    )

    recall_score = Column(
        Numeric(6, 4),
        nullable=True
    )

    f1_score = Column(
        Numeric(6, 4),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
