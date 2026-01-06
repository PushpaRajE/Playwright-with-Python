import os
import pytest
from datetime import datetime
from pytest_html import extras


# =========================
# SESSION LEVEL LOGS
# =========================
def pytest_sessionstart(session):
    print("\n==============================")
    print("=== Pytest Session Started ===")
    print("==============================\n")


def pytest_sessionfinish(session, exitstatus):
    print("\n==============================")
    print("=== Pytest Session Finished ===")
    print(f"Exit status: {exitstatus}")
    print("==============================\n")


# =========================
# TEST REPORT + SCREENSHOT
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    - Logs test result
    - Takes screenshot on failure
    - Attaches screenshot to pytest-html
    """

    outcome = yield
    rep = outcome.get_result()

    # ---- SETUP PHASE ----
    if rep.when == "setup":
        print(f"\nSETUP: {item.nodeid}")


    # ---- CALL PHASE (TEST EXECUTION) ----
    if rep.when == "call":
        if rep.passed:
            print(f"✅ PASS: {item.nodeid}")

        elif rep.failed:
            print(f"❌ FAIL: {item.nodeid}")

            # Get Playwright page object (from fixture)
            page = item.funcargs.get("page", None)

            if page:
                # Create screenshots directory
                screenshots_dir = os.path.join(os.getcwd(), "screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)

                # Unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_test_name = (
                    item.nodeid.replace("::", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )

                screenshot_path = os.path.join(
                    screenshots_dir,
                    f"{safe_test_name}_{timestamp}.png"
                )

                # Take screenshot
                page.screenshot(path=screenshot_path, full_page=True)

                print(f"📸 Screenshot saved: {screenshot_path}")

                # Attach screenshot to pytest-html report
                if hasattr(rep, "extra"):
                    rep.extra.append(extras.image(screenshot_path))
                else:
                    rep.extra = [extras.image(screenshot_path)]

        elif rep.skipped:
            print(f"⏭️ SKIP: {item.nodeid}")

    # ---- TEARDOWN PHASE ----
    if rep.when == "teardown":
        print(f"◀ TEARDOWN: {item.nodeid}")
