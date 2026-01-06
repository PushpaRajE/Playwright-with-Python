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
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    - Logs test result
    - Takes screenshot ONLY on failure
    - Attaches screenshot to pytest-html
    - Works correctly in Jenkins
    """

    outcome = yield
    rep = outcome.get_result()

    # ---- SETUP PHASE ----
    if rep.when == "setup":
        print(f"\nSETUP: {item.nodeid}")

    # ---- CALL PHASE (TEST EXECUTION) ----
    if rep.when == "call":

        if rep.passed:
            print(f"PASS: {item.nodeid}")

        elif rep.failed:
            print(f"FAIL: {item.nodeid}")

            # Get Playwright page object
            page = item.funcargs.get("page", None)

            if page:
                # Use RELATIVE directory (important for Jenkins)
                screenshots_dir = "screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_test_name = (
                    item.nodeid.replace("::", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )

                # Relative path (for pytest-html)
                relative_path = os.path.join(
                    screenshots_dir,
                    f"{safe_test_name}_{timestamp}.png"
                )

                # Absolute path (for saving file)
                absolute_path = os.path.join(os.getcwd(), relative_path)

                # Take screenshot
                page.screenshot(path=absolute_path, full_page=True)
                print(f"Screenshot saved: {absolute_path}")

                # Attach screenshot to pytest-html
                rep.extra = getattr(rep, "extra", [])
                rep.extra.append(extras.image(relative_path))

        elif rep.skipped:
            print(f"SKIP: {item.nodeid}")

    # ---- TEARDOWN PHASE ----
    if rep.when == "teardown":
        print(f"TEARDOWN: {item.nodeid}")
