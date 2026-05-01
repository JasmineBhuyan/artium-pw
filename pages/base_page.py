"""
base_page.py  –  Shared Playwright helpers inherited by every Page-Object.
"""
from playwright.sync_api import Page, expect
import config


class BasePage:
    def __init__(self, page: Page):
        self.page    = page
        self.timeout = config.DEFAULT_TIMEOUT

    # ── Navigation ────────────────────────────────────────────────────────────
    def goto(self, url: str = config.BASE_URL):
        self.page.goto(url, wait_until="networkidle", timeout=config.NAV_TIMEOUT)

    # ── Smart wait helpers ─────────────────────────────────────────────────────
    def wait_visible(self, selector: str, timeout: int = None):
        loc = self.page.locator(selector).first
        loc.wait_for(state="visible", timeout=timeout or self.timeout)
        return loc

    def wait_clickable(self, selector: str, timeout: int = None):
        loc = self.page.locator(selector).first
        loc.wait_for(state="visible", timeout=timeout or self.timeout)
        expect(loc).to_be_enabled(timeout=timeout or self.timeout)
        return loc

    # ── Actions ───────────────────────────────────────────────────────────────
    def click(self, selector: str):
        self.wait_clickable(selector).click()

    def fill(self, selector: str, text: str):
        loc = self.wait_visible(selector)
        loc.clear()
        loc.fill(text)

    def select_option(self, selector: str, value: str):
        self.page.locator(selector).first.select_option(value)

    # ── Assertions ─────────────────────────────────────────────────────────────
    def assert_visible(self, selector: str, timeout: int = None):
        expect(
            self.page.locator(selector).first
        ).to_be_visible(timeout=timeout or self.timeout)
