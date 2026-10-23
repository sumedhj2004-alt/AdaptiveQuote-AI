from pydantic import ValidationError

from schemas import Transaction


try:
    transaction = Transaction(
        transaction_id="TX10001",
        customer_id="CUST502",
        amount=84500.00,
        merchant_category="Electronics",
        transaction_type="Purchase",
        location="Mumbai",
        device_type="Mobile",
        hour=2,
        account_age_days=850,
        previous_transaction_amount=5200.00,
        transaction_frequency=4
    )

    print("Transaction validated successfully!")
    print(transaction)

except ValidationError as error:
    print("Transaction validation failed!")
    print(error)