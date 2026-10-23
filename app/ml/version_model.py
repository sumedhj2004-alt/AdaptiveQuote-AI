from pathlib import Path
import shutil
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "models"
    / "anomaly_model.pkl"
)

VERSIONS_DIR = (
    PROJECT_ROOT
    / "app"
    / "ml"
    / "versions"
)


def create_model_version():

    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

    if not MODEL_FILE.exists():
        print("Model file not found.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    version_file = (
        VERSIONS_DIR
        / f"anomaly_model_{timestamp}.pkl"
    )

    shutil.copy2(
        MODEL_FILE,
        version_file
    )

    print("\n--- Model Versioning ---")
    print("Current model:")
    print(MODEL_FILE)

    print("\nVersion created:")
    print(version_file)


if __name__ == "__main__":
    create_model_version()