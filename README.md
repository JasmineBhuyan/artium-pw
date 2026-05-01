# Artium Academy – Playwright Automation Framework

A Python-based end-to-end test automation framework for [Artium Academy](https://uatreact.artiumacademy.com/) built with Playwright and pytest.

---

## Problem Statement

**URL:** https://uatreact.artiumacademy.com/

1. Log in to the Chrome browser.
2. Create a student using the "Book a Trial" button.
3. Execute the code and save screenshots once the execution is complete.
4. Commit the framework to GitHub.
5. Share the GitHub project URL.

## Objective

Automate the end-to-end "Book a Trial" student creation flow on the Artium Academy UAT environment, including form submission, OTP verification, and slot confirmation — with auto-generated screenshots and an HTML report at every step.

---

## Prerequisites

Make sure the following are installed before proceeding:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- Google Chrome browser

---

## Setup

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd artium-pw
```

### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browser

```bash
playwright install chromium
```

### 5. Configure environment

Create a `.env` file in the project root:

```
HEADLESS=true
SLOW_MO=800
```

> Set `HEADLESS=false` if you want to watch the browser during test execution.

---

## Running Tests

```bash
# Run all tests
pytest

# Run with detailed output
pytest tests/test_book_trial.py -v

# Run a specific test
pytest tests/test_book_trial.py::TestBookTrial::test_book_trial_end_to_end -v

# Run with console logs visible
pytest tests/test_book_trial.py -v -s
```

---

## Project Structure

```
artium-pw/
├── pages/
│   ├── base_page.py          <- Shared Playwright helpers (base class)
│   └── book_trial_page.py    <- Book a Trial page object
├── tests/
│   └── test_book_trial.py    <- TC_BT_01, TC_BT_02, TC_BT_03
├── utils/
│   └── screenshot_helper.py  <- Auto timestamped screenshot utility
├── screenshots/              <- Generated screenshots per test run
├── reports/
│   └── report.html           <- HTML test report
├── conftest.py               <- Browser fixtures and failure hooks
├── config.py                 <- Centralised configuration
├── pytest.ini                <- pytest settings
├── requirements.txt          <- Python dependencies
├── .env                      <- Local environment config (do not commit)
└── .gitignore
```

---

## Test Cases

| ID | Test | Description | Expected Result |
|---|---|---|---|
| TC_BT_01 | `test_book_trial_end_to_end` | Full booking flow: open form, fill details, OTP, confirm slot | Booking confirmed or fully booked message |
| TC_BT_02 | `test_book_trial_form_visible` | Navigate to `/bookfreetrial` and check form loads | Booking form heading visible |
| TC_BT_03 | `test_book_trial_empty_submission` | Open form without filling any fields | Submit button is disabled |

---

## Reports & Screenshots

After each test run, artefacts are saved automatically:

| Artefact | Location |
|---|---|
| HTML Report | `reports/report.html` |
| Screenshots | `screenshots/*.png` |

Open `reports/report.html` in any browser to view the full test report with pass/fail status.

---

## Author

**Jasmine Bhuyan**
