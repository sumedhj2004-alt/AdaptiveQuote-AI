from app.database import engine, Base
from app.models.database_models import (
    Transaction,
    RiskAssessment,
    AgentInteraction,
    HumanFeedback,
    ModelVersion
)

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")