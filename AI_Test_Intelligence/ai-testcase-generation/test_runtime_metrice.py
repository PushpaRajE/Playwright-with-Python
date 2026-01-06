from playwright.sync_api import Page, expect
import pytest
from ai_outcome_logic import generate_login_test_cases
from data_provider import get_credentials

REQUIREMENT = "User should be able to login using username and password"


def pytest_generate_tests(metafunc):
    """
    CI-safe dynamic test generation.
    AI logic runs during pytest collection,
    NOT at module import time.
    """
    if "case" in metafunc.fixturenames:
        test_cases = generate_login_test_cases(REQUIREMENT)
        metafunc.parametrize(
            "case",
            test_cases,
            ids=[case["title"] for case in test_cases],
        )


def test_login(page: Page, case):
    """
    AI outcome-based login test using Playwright.
    """

    creds = get_credentials(case["scenario"])

    page.goto("https://the-internet.herokuapp.com/login")

    page.fill("#username", creds["username"])
    page.fill("#password", creds["password"])
    page.click("button[type='submit']")

    flash = page.locator("#flash")

    if case["expected"] == "success":
        expect(flash).to_contain_text("You logged into a secure area!")
    else:
        expect(flash).to_contain_text("is invalid")
