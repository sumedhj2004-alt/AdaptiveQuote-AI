from pathlib import Path
import joblib

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def main():
    # Load dataset
    file_path = Path("data/transactions.csv")
    dataframe = pd.read_csv(file_path)

    # Create ML features
    from features import create_features

    X = create_features(dataframe)

    # Target variable
    y = dataframe["is_anomaly"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("\n--- Dataset Split ---")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Create Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    # Train model
    model.fit(X_train, y_train)

    print("\n--- Model Training ---")
    print("Random Forest model trained successfully!")

    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Evaluate model
    from sklearn.metrics import classification_report

    print("\n--- Model Evaluation ---")
    print(classification_report(y_test, y_pred))

    from sklearn.metrics import confusion_matrix

    matrix = confusion_matrix(y_test, y_pred)

    print("\n--- Confusion Matrix ---")
    print(matrix)

    # Save trained model
    model_directory = Path("models")
    model_directory.mkdir(exist_ok=True)

    model_file = model_directory / "anomaly_model.pkl"

    joblib.dump(model, model_file)

    print("\n--- Model Saving ---")
    print(f"Model saved successfully to: {model_file}")

if __name__ == "__main__":
    main()