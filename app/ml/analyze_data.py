from pathlib import Path

import pandas as pd


def main():
    file_path = Path("data/transactions.csv")

    dataframe = pd.read_csv(file_path)

    print("\n--- Normal vs Anomalous Transactions ---")

    amount_summary = (
        dataframe
        .groupby("is_anomaly")["amount"]
        .agg(["count", "mean", "median", "min", "max"])
    )

    print(amount_summary)

    print("\n--- Average Transaction Hour ---")

    hour_summary = (
        dataframe
        .groupby("is_anomaly")["hour"]
        .agg(["mean", "median", "min", "max"])
    )

    print(hour_summary)

    print("\n--- Device Distribution ---")

    device_summary = pd.crosstab(
        dataframe["device_type"],
        dataframe["is_anomaly"],
        normalize="columns"
    ) * 100

    print(device_summary.round(2))

    print("\n--- Location Distribution ---")

    location_summary = pd.crosstab(
        dataframe["location"],
        dataframe["is_anomaly"],
        normalize="columns"
    ) * 100

    print(location_summary.round(2))

    print("\n--- Transaction Amount vs Previous Amount ---")

    dataframe["amount_change_ratio"] = (
        dataframe["amount"]
        / dataframe["previous_transaction_amount"]
    )

    amount_change_summary = (
        dataframe
        .groupby("is_anomaly")["amount_change_ratio"]
        .agg(["mean", "median", "min", "max"])
    )

    print(amount_change_summary.round(2))



if __name__ == "__main__":
    main()