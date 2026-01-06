import os
import time
import joblib
import numpy as np
import pytest
from playwright.sync_api import sync_playwright

# 🔹 Resolve model path safely (CI + local)
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "test_failure_model.pkl")


@pytest.fixture(scope="session")
def ai_model():
    """
    Load ML model once per test session.
    CI-safe: no import-time execution.
    """
    if not os.path.exists(MODEL_PATH):
        pytest.skip("AI model file not available in CI environment")

    return joblib.load(MODEL_PATH)


def predict_test_risk(model, page_load_time, api_response_time):
    """
    Predicts test risk using trained ML model.
    """
    features = np.array([[page_load_time, api_response_time]])
    prediction = model.predict(features)
    return int(prediction[0])  # 0 = PASS, 1 = FAIL


def test_ai_assisted_playwright(ai_model):
    """
    AI-assisted Playwright test with real performance signals.
    Works locally and in CI.
    """

    # 🔹 Headless in CI, headed locally
    HEADLESS = os.getenv("CI", "false").lower() == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context()
        page = context.new_page()

        try:
            # -------- PAGE LOAD TIME --------
            page_start = time.time()
            page.goto("https://example.com", timeout=30_000)
            page.wait_for_load_state("networkidle")
            page_load_time = time.time() - page_start

            # -------- API RESPONSE TIME --------
            api_start = time.time()
            response = page.request.get("https://httpbin.org/delay/1", timeout=30_000)
            assert response.ok
            api_response_time = time.time() - api_start

            # -------- AI PREDICTION --------
            risk = predict_test_risk(
                ai_model, page_load_time, api_response_time
            )

            print("\n=== AI Risk Analysis ===")
            print(f"Page Load Time (sec): {round(page_load_time, 3)}")
            print(f"API Response Time (sec): {round(api_response_time, 3)}")
            print(f"AI Prediction (0=PASS, 1=FAIL): {risk}")

            # -------- ASSERTIONS --------
            assert page.title() == "Example Domain"

            if risk == 1:
                pytest.fail("❌ AI predicted test failure")

        finally:
            context.close()
            browser.close()
