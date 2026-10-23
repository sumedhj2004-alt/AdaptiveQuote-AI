import pandas as pd


def create_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Create ML features from raw transaction data.
    """

    features = dataframe.copy()

    # Compare current transaction with previous transaction.
    features["amount_change_ratio"] = (
        features["amount"]
        / features["previous_transaction_amount"]
    )

    # Keep only numerical features for our first ML model.
    selected_features = [
        "amount",
        "hour",
        "previous_transaction_amount",
        "transaction_frequency",
        "account_age_days",
        "amount_change_ratio",
    ]

    return features[selected_features]