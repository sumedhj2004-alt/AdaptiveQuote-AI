from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    customer_id: str

    amount: float = Field(gt=0)
    merchant_category: str
    transaction_type: str

    location: str
    device_type: str

    hour: int = Field(ge=0, le=23)

    account_age_days: int = Field(gt=0)
    previous_transaction_amount: float = Field(ge=0)
    transaction_frequency: int = Field(gt=0)