"""
test_book_trial.py  -  "Book a Trial" tests for Artium Academy.

Test cases
  TC_BT_01  Full end-to-end flow  (open form -> fill -> submit -> success)
  TC_BT_02  Booking form is visible at /bookfreetrial
  TC_BT_03  Empty form submission shows validation  (negative)
"""
from playwright.sync_api import Page
from pages.book_trial_page import BookTrialPage
from utils.screenshot_helper import take_screenshot


class TestBookTrial:

    def test_book_trial_end_to_end(self, page: Page):
        """
        TC_BT_01
        GIVEN  the user opens /bookfreetrial
        WHEN   they fill student details and submit
        THEN   a success / confirmation message is displayed
        """
        print("\n\nTC_BT_01  -  Full Book-a-Trial Flow")

        trial = BookTrialPage(page)

        print("\n  Step 1  -  Open booking form")
        trial.open()
        trial.assert_form_open()
        take_screenshot(page, "TC_BT_01_01_form_visible")

        print("\n  Step 2  -  Set up OTP mock")
        trial.setup_otp_mock()

        print("\n  Step 3  -  Fill student details & submit")
        student = trial.fill_and_submit(screenshot_label="TC_BT_01_03_success_confirmed")

        print(f"\n  Student created:")
        print(f"       Name   : {student['name']}")
        print(f"       Phone  : {student['phone']}")
        print(f"       Age    : {student['age']}")
        print(f"       Course : {student['course']}")

        print("\n  Step 4  -  Handle OTP screen")
        trial.handle_otp_screen(otp="1111")
        take_screenshot(page, "TC_BT_01_04_after_otp")

        print("\n  Step 5  -  Assert success message")
        trial.assert_success()

        print("\n  TC_BT_01  PASSED")

    def test_book_trial_form_visible(self, page: Page):
        """
        TC_BT_02
        GIVEN  the user opens /bookfreetrial
        THEN   the booking form heading is visible
        """
        print("\n\nTC_BT_02  -  Form Visibility")

        trial = BookTrialPage(page)
        trial.open()
        trial.assert_form_open()
        take_screenshot(page, "TC_BT_02_01_form_open")

        print("\n  TC_BT_02  PASSED")

    def test_book_trial_empty_submission(self, page: Page):
        """
        TC_BT_03
        GIVEN  the booking form is open with no fields filled
        WHEN   the user checks the submit button
        THEN   submit button is disabled
        """
        print("\n\nTC_BT_03  -  Empty Submission Validation")

        trial = BookTrialPage(page)
        trial.open()
        trial.assert_form_open()

        take_screenshot(page, "TC_BT_03_01_empty_submit_result")
        assert not trial.is_submit_enabled(), (
            "Submit button should be disabled when form fields are empty"
        )
        print("\n  TC_BT_03  PASSED")
