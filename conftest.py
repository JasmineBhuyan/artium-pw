"""
conftest.py  –  Pytest fixtures and hooks for the Artium automation suite.
"""
import os
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from utils.screenshot_helper import take_screenshot
import config as app_config


# ── Browser (session-scoped) ──────────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as pw:
        launcher = getattr(pw, app_config.BROWSER)
        browser: Browser = launcher.launch(
            headless=app_config.HEADLESS,
            slow_mo=app_config.SLOW_MO,
            args=["--start-maximized"],
        )
        yield browser
        browser.close()


# ── Context (function-scoped – isolated per test) ─────────────────────────────
@pytest.fixture(scope="function")
def context(browser_instance: Browser):
    ctx: BrowserContext = browser_instance.new_context(
        viewport=app_config.VIEWPORT,
        ignore_https_errors=True,
    )
    yield ctx
    ctx.close()


# ── Page (function-scoped) ────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    pg: Page = context.new_page()
    pg.set_default_timeout(app_config.DEFAULT_TIMEOUT)
    pg.set_default_navigation_timeout(app_config.NAV_TIMEOUT)
    yield pg
    pg.close()


# ── Auto-screenshot on failure ────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep     = outcome.get_result()

    if rep.when == "call" and rep.failed:
        pg = item.funcargs.get("page")
        if pg:
            take_screenshot(pg, f"FAILED__{item.name}")


# ── HTML report metadata ───────────────────────────────────────────────────────
def pytest_html_report_title(report):
    report.title = "Artium Academy  –  Playwright Automation Report"


def pytest_configure(config):
    os.makedirs(app_config.REPORT_DIR, exist_ok=True)
    os.makedirs(app_config.SCREENSHOT_DIR, exist_ok=True)
