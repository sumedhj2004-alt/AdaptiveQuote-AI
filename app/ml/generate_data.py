import random
from pathlib import Path

import pandas as pd


random.seed(42)

NUM_TRANSACTIONS = 5000
NUM_CUSTOMERS = 500


MERCHANT_CATEGORIES = [
    "Grocery",
    "Electronics",
    "Fuel",
    "Travel",
    "Restaurant",
    "Healthcare",
    "Online Shopping",
]


LOCATIONS = [
    "Mumbai",
    "Pune",
    "Nashik",
    "Nagpur",
    "Delhi",
    "Bangalore",
]


DEVICE_TYPES = [
    "Mobile",
    "Laptop",
    "Tablet",
]


TRANSACTION_TYPES = [
    "Purchase",
    "Online Payment",
    "ATM Withdrawal",
]


def create_customer_profiles():
    profiles = {}

    for customer_number in range(1, NUM_CUSTOMERS + 1):
        profiles[customer_number] = {
            "typical_amount": random.uniform(1000, 10000),
            "preferred_location": random.choice(LOCATIONS),
            "preferred_device": random.choice(DEVICE_TYPES),
            "normal_start_hour": random.randint(7, 10),
            "normal_end_hour": random.randint(19, 22),
            "account_age_days": random.randint(30, 3000),
        }

    return profiles


def generate_transaction(transaction_number, profiles):
    customer_number = random.randint(1, NUM_CUSTOMERS)

    profile = profiles[customer_number]

    is_anomaly = random.random() < 0.05

    if is_anomaly:
        amount = profile["typical_amount"] * random.uniform(5, 15)
        location = random.choice(
            [
                location
                for location in LOCATIONS
                if location != profile["preferred_location"]
            ]
        )
        device = random.choice(
            [
                device
                for device in DEVICE_TYPES
                if device != profile["preferred_device"]
            ]
        )
        hour = random.choice([0, 1, 2, 3, 4, 23])

    else:
        amount = profile["typical_amount"] * random.uniform(0.5, 1.5)
        location = profile["preferred_location"]
        device = profile["preferred_device"]
        hour = random.randint(
            profile["normal_start_hour"],
            profile["normal_end_hour"],
        )

    previous_transaction_amount = profile["typical_amount"] * random.uniform(
        0.5, 1.5
    )

    transaction_frequency = random.randint(1, 20)

    return {
        "transaction_id": f"TX{transaction_number:05d}",
        "customer_id": f"CUST{customer_number:04d}",
        "amount": round(amount, 2),
        "merchant_category": random.choice(MERCHANT_CATEGORIES),
        "transaction_type": random.choice(TRANSACTION_TYPES),
        "location": location,
        "device_type": device,
        "hour": hour,
        "account_age_days": profile["account_age_days"],
        "previous_transaction_amount": round(
            previous_transaction_amount, 2
        ),
        "transaction_frequency": transaction_frequency,
        "is_anomaly": is_anomaly,
    }


def main():
    customer_profiles = create_customer_profiles()

    transactions = [
        generate_transaction(i, customer_profiles)
        for i in range(1, NUM_TRANSACTIONS + 1)
    ]

    dataframe = pd.DataFrame(transactions)

    output_directory = Path("data")
    output_directory.mkdir(exist_ok=True)

    output_file = output_directory / "transactions.csv"

    dataframe.to_csv(output_file, index=False)

    print("Behavioral dataset generated successfully!")
    print(f"Number of transactions: {len(dataframe)}")
    print(f"Number of anomalies: {dataframe['is_anomaly'].sum()}")
    print(
        f"Anomaly rate: "
        f"{dataframe['is_anomaly'].mean() * 100:.2f}%"
    )
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()