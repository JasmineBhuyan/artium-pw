"""
screenshot_helper.py  –  Saves timestamped, full-page screenshots.
"""
import os
import time
import config


def take_screenshot(page, name: str) -> str:
    """
    Capture a full-page PNG and save it to the screenshots/ folder.

    Args:
        page : Playwright Page object
        name : Human-readable step label (no extension required)

    Returns:
        Absolute path to the saved file.
    """
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path      = os.path.join(config.SCREENSHOT_DIR, f"{name}_{timestamp}.png")
    page.screenshot(path=path, full_page=True)
    print(f"    📸  Screenshot → {path}")
    return path
