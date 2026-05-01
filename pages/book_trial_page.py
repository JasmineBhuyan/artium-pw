"""
book_trial_page.py  -  Page Object for the "Book a Trial" student creation flow.
"""
from playwright.sync_api import Page, expect, Route, Request
from faker import Faker
from pages.base_page import BasePage
from utils.screenshot_helper import take_screenshot
import config
import json

fake = Faker("en_IN")


class BookTrialPage(BasePage):

    # -- Locators --
    BOOK_TRIAL_BTN  = "#bookAfreeTrial-solid"
    FORM_HEADING    = "h1:has-text('Book Your Free 1:1 Trial Class')"
    STUDENT_NAME    = "#learnerName"
    STUDENT_PHONE   = "#mobileNumber"
    COURSE_SELECT   = "#courseSelect"
    COURSES = [
        "Western Vocal", "Hindustani Classical Vocal", "Carnatic Classical Vocal",
        "Popular & Film Music - Hindi", "Popular & Film Music - Telugu",
        "Popular & Film Music - Tamil", "Popular & Film Music - Kannada",
        "Popular & Film Music - Malayalam", "Hindi Devotional", "South Devotional",
        "Ghazal", "Karaoke - Hindi", "Karaoke - Telugu", "Karaoke - Tamil",
        "Karaoke - Malayalam", "Karaoke - Kannada", "Keyboard & Piano", "Guitar", "Tabla",
    ]
    SUBMIT_BTN      = "button[type='submit']"
    AGE_GROUPS      = ["6-12", "13-21", "22-30", "31-40", "40+"]

    # OTP screen
    OTP_HEADING     = "text=Enter OTP"
    OTP_INPUTS      = "input.otp-inputBat"

    # Post-OTP popups
    FULLY_BOOKED_MSG   = "h1:has-text('Our Teachers Are Fully Booked Right Now')"
    SLOT_SELECTION_MSG = "h1:has-text('Select your Trial class time')"
    CONFIRM_SLOT_BTN   = "button:has-text('Confirm Slot')"

    # -- Helpers --
    @staticmethod
    def generate_student() -> dict:
        return {
            "name":  fake.name(),
            "phone": fake.numerify("1########1"),
            "age":   fake.random_element(["6-12", "13-21", "22-30", "31-40", "40+"]),
            "course": fake.random_element(["Western Vocal", "Hindustani Classical Vocal",
                "Carnatic Classical Vocal", "Popular & Film Music - Hindi", "Guitar",
                "Keyboard & Piano", "Tabla", "Ghazal", "Hindi Devotional"]),
        }

    # -- OTP Mocking --
    def setup_otp_mock(self):
        """Mock OTP send + verify endpoints so no real SMS is needed."""

        def mock_send(route: Route, request: Request):
            print(f"\n  MOCKED send-OTP  ->  {request.url}")
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"success": True, "message": "OTP sent"}),
            )

        def mock_verify(route: Route, request: Request):
            print(f"\n  MOCKED verify-OTP  ->  {request.url}")
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"success": True, "message": "OTP verified"}),
            )

        ctx = self.page.context
        ctx.route("https://uat.artiumacademy.com/api/users/user/otp/register*", mock_send)
        ctx.route("https://uat.artiumacademy.com/api/auth/otpLogin", mock_verify)
        print("  OTP mocks registered  ->  send + verify (context-level)")

    def handle_otp_screen(self, otp: str = "0000"):
        """Wait for OTP screen, fill boxes — auto-verifies on last digit."""
        print(f"\n  OTP Screen  -  entering mock OTP: {otp}")

        self.page.wait_for_selector("text=Enter OTP", timeout=self.timeout)
        take_screenshot(self.page, "otp_screen_appeared")

        otp_inputs = self.page.locator(self.OTP_INPUTS)
        otp_inputs.first.wait_for(state="visible", timeout=self.timeout)
        count = otp_inputs.count()
        print(f"  OTP boxes found: {count}")

        otp_inputs.first.click()
        self.page.keyboard.type(otp.ljust(count, "0")[:count], delay=100)

        self.page.wait_for_load_state("networkidle", timeout=config.NAV_TIMEOUT)
        take_screenshot(self.page, "otp_entered")
        print("  OTP entered  ->  auto-verification triggered")

    # -- Actions --
    def open(self):
        url = config.BASE_URL.rstrip("/") + "/bookfreetrial"
        print(f"\n  Opening  ->  {url}")
        self.goto(url)

    def click_book_trial(self):
        btn = self.page.locator(self.BOOK_TRIAL_BTN).first
        btn.wait_for(state="visible", timeout=self.timeout)
        btn.scroll_into_view_if_needed()
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=config.NAV_TIMEOUT)
        print("  Clicked  ->  'Book a free trial' button")

    def fill_name(self, name: str):
        loc = self.page.locator(self.STUDENT_NAME)
        loc.wait_for(state="visible", timeout=self.timeout)
        loc.clear()
        loc.fill(name)
        print(f"  Name      ->  {name}")

    def fill_phone(self, phone: str):
        loc = self.page.locator(self.STUDENT_PHONE)
        loc.wait_for(state="visible", timeout=self.timeout)
        loc.clear()
        loc.fill(phone)
        print(f"  Phone     ->  {phone}")

    def select_age(self, age: str):
        btn = self.page.locator(f"button:has-text('{age}')").first
        btn.wait_for(state="visible", timeout=self.timeout)
        btn.click()
        print(f"  Age       ->  {age}")

    def select_course(self, course: str):
        trigger = self.page.locator(self.COURSE_SELECT)
        trigger.wait_for(state="visible", timeout=self.timeout)
        trigger.click()
        option = self.page.get_by_role("option", name=course, exact=True)
        option.wait_for(state="visible", timeout=self.timeout)
        option.click()
        print(f"  Course    ->  {course}")

    def is_submit_enabled(self) -> bool:
        btn = self.page.locator(self.SUBMIT_BTN)
        return btn.is_visible() and btn.is_enabled()

    def submit(self, screenshot_label: str = None):
        btn = self.page.locator(self.SUBMIT_BTN)
        btn.wait_for(state="visible", timeout=self.timeout)
        self.page.wait_for_function(
            "document.querySelector('button[type=\"submit\"]').className.includes('e82c86')",
            timeout=self.timeout,
        )
        print("  Button turned pink  ->  form is ready to submit")
        if screenshot_label:
            take_screenshot(self.page, screenshot_label)
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=config.NAV_TIMEOUT)
        print("  Clicked  ->  'Book Your Free Trial' button")

    def fill_and_submit(self, screenshot_label: str = None) -> dict:
        student = self.generate_student()
        self.fill_name(student["name"])
        self.fill_phone(student["phone"])
        self.select_age(student["age"])
        self.select_course(student["course"])
        self.submit(screenshot_label=screenshot_label)
        return student

    # -- Assertions --
    def assert_form_open(self):
        loc = self.page.locator(self.FORM_HEADING)
        loc.wait_for(state="visible", timeout=self.timeout)
        print("  Assertion passed  ->  Booking form is visible")

    def assert_success(self):
        """Handle either post-OTP popup and pass the test."""
        self.page.wait_for_selector(
            f"{self.FULLY_BOOKED_MSG}, {self.SLOT_SELECTION_MSG}",
            timeout=20_000,
        )

        if self.page.locator(self.FULLY_BOOKED_MSG).is_visible():
            take_screenshot(self.page, "TC_BT_01_fully_booked")
            print("  Option 1: Teachers fully booked - booking registered successfully")

        elif self.page.locator(self.SLOT_SELECTION_MSG).is_visible():
            print("  Option 2: Slot selection screen appeared - selecting slot")
            self._select_and_confirm_slot()
            print("  Option 2: Slot confirmed - booking complete")

    def _select_and_confirm_slot(self):
        """Select first available date, first time slot, then confirm."""
        date_btn = self.page.locator("div.flex.gap-1 button, div.flex.gap-2 button").first
        date_btn.wait_for(state="visible", timeout=self.timeout)
        date_btn.click()
        print("  Date selected")
        take_screenshot(self.page, "TC_BT_01_date_selected")

        time_btn = self.page.locator("div.grid button").first
        time_btn.wait_for(state="visible", timeout=self.timeout)
        time_btn.click()
        print("  Time slot selected")
        take_screenshot(self.page, "TC_BT_01_time_selected")

        confirm = self.page.locator(self.CONFIRM_SLOT_BTN)
        confirm.wait_for(state="visible", timeout=self.timeout)
        confirm.click()
        self.page.wait_for_load_state("networkidle", timeout=config.NAV_TIMEOUT)
        take_screenshot(self.page, "TC_BT_01_slot_confirmed")
        print("  Confirm Slot clicked")
