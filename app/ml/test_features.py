from pathlib import Path

import pandas as pd

from features import create_features


def main():
    file_path = Path("data/transactions.csv")

    dataframe = pd.read_csv(file_path)

    feature_dataframe = create_features(dataframe)

    print("\n--- Feature DataFrame Shape ---")
    print(feature_dataframe.shape)

    print("\n--- Feature Columns ---")
    print(feature_dataframe.columns.tolist())

    print("\n--- First 5 Feature Rows ---")
    print(feature_dataframe.head())

    print("\n--- Missing Values ---")
    print(feature_dataframe.isnull().sum())


if __name__ == "__main__":
    main()