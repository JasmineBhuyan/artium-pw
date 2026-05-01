import os
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL = "https://uatreact.artiumacademy.com/"

BROWSER  = os.getenv("BROWSER",  "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO  = int(os.getenv("SLOW_MO", "800"))

VIEWPORT = {"width": 1920, "height": 1080}

DEFAULT_TIMEOUT = 30_000
NAV_TIMEOUT     = 60_000

SCREENSHOT_DIR = "screenshots"
REPORT_DIR     = "reports"
