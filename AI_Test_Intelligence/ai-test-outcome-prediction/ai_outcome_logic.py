import os
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib


def train_and_save_model(output_path: str):
    """
    Trains a simple ML model to predict test failure risk
    and saves it to disk.

    This function is SAFE for CI and reusable.
    """

    # 🔹 Sample historical test execution data
    # [page_load_time, api_response_time]
    X = np.array([
        [2.1, 200],
        [3.5, 500],
        [1.8, 180],
        [4.2, 700],
        [2.5, 300],
        [5.0, 900]
    ])

    # Labels: 0 = PASS, 1 = FAIL
    y = np.array([0, 1, 0, 1, 0, 1])

    model = LogisticRegression()
    model.fit(X, y)

    # 🔹 Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    joblib.dump(model, output_path)
    print(f"✅ AI model trained & saved at: {output_path}")


if __name__ == "__main__":
    """
    This block ensures training runs ONLY when executed directly,
    NOT during pytest collection or Jenkins import.
    """

    BASE_DIR = os.path.dirname(__file__)
    MODEL_PATH = os.path.join(BASE_DIR, "test_failure_model.pkl")

    train_and_save_model(MODEL_PATH)
