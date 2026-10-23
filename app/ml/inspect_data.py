from pathlib import Path

import pandas as pd


def main():
    file_path = Path("data/transactions.csv")

    dataframe = pd.read_csv(file_path)

    print("\n--- Dataset Shape ---")
    print(dataframe.shape)

    print("\n--- Columns ---")
    print(dataframe.columns.tolist())

    print("\n--- First 5 Transactions ---")
    print(dataframe.head())

    print("\n--- Data Types ---")
    print(dataframe.dtypes)

    print("\n--- Missing Values ---")
    print(dataframe.isnull().sum())

    print("\n--- Basic Statistics ---")
    print(dataframe.describe())


if __name__ == "__main__":
    main()