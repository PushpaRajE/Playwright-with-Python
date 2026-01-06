from playwright.sync_api import sync_playwright, TimeoutError
from ai_self_healing_logic import find_best_match

def test_google_search_ai_self_healing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com")

        # -------- PRIMARY LOCATOR --------
        try:
            page.locator("input[name='q']").fill("cricbuzzz")
            page.keyboard.press("Enter")
            browser.close()
            return
        except TimeoutError:
            print("Primary locator failed → invoking AI self-healing")

        # -------- COLLECT INPUT LABELS FROM DOM --------
        labels = page.evaluate("""
        () => Array.from(document.querySelectorAll("input, textarea"))
              .map(el => el.getAttribute("aria-label"))
              .filter(Boolean)
        """)

        # -------- AI FINDS BEST MATCH --------
        best_label = find_best_match("Search", labels)
        print(f"🤖 AI matched locator text: {best_label}")

        # -------- USE HEALED LOCATOR --------
        page.locator(f"[aria-label='{best_label}']").fill("cricbuzzz")
        page.keyboard.press("Enter")

        browser.close()
