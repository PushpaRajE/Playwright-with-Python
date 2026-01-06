import time
import random
import os
from playwright.sync_api import sync_playwright
from ai_flaky_logic import detect_flakiness


def test_flaky_behavior():
    """
    This test runs the same scenario multiple times,
    collects results & execution time,
    and detects flakiness using AI logic.
    """

    results = []
    times = []

    # 🔹 Make test deterministic in CI
    random.seed(42)

    # 🔹 Headless in CI, headed locally
    HEADLESS = os.getenv("CI", "false").lower() == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        for run in range(5):  # run same test 5 times
            start = time.time()

            page.goto("https://example.com")

            # 🔹 Deterministic flakiness simulation
            if run % 2 == 0:
                results.append("PASS")
            else:
                results.append("FAIL")

            exec_time = time.time() - start
            times.append(exec_time)

        browser.close()

    # 🔹 Analyze flakiness
    is_flaky, failure_ratio, variance = detect_flakiness(results, times)

    # 🔹 Logs visible in Jenkins console
    print("\n=== Flaky Test Analysis ===")
    print("Results:", results)
    print("Execution Times:", times)
    print("Failure Ratio:", failure_ratio)
    print("Time Variance:", variance)

    if is_flaky:
        print("TEST IS FLAKY")
    else:
        print("TEST IS STABLE")

    # 🔹 Optional assertion (kept soft for demo)
    assert isinstance(is_flaky, bool)
