"""
Selenium Automated Tests for Email and Google Authentication (Register, Login, Google OAuth, Validation, Logout).
"""

import pytest
from tests.pages.auth_page import AuthPage
from tests.pages.feed_page import FeedPage
from tests.pages.settings_page import SettingsPage


@pytest.mark.selenium
@pytest.mark.auth
class TestAuthentication:
    """Test suite covering email-only registration and login, Google OAuth, logout, and validations."""

    def test_register_page_renders_expected_elements(self, driver, live_server):
        """Verify register page renders title, wordmark, google button, email and password inputs, and switch link."""
        auth_page = AuthPage(driver, live_server).open_register()

        assert auth_page.get_title_text() == "Create account"
        assert auth_page.is_visible(*auth_page.GOOGLE_BTN)
        assert auth_page.is_visible(*auth_page.EMAIL_INPUT)
        assert auth_page.is_visible(*auth_page.PASSWORD_INPUT)
        assert auth_page.is_visible(*auth_page.CONFIRM_PASSWORD_INPUT)
        assert auth_page.is_visible(*auth_page.SUBMIT_BTN)
        assert auth_page.is_visible(*auth_page.SWITCH_LINK)

    def test_successful_registration_with_email(self, driver, live_server):
        """Registering with valid email and password should succeed and redirect to home feed."""
        auth_page = AuthPage(driver, live_server).open_register()
        auth_page.register("newuser@example.com", "ValidPass123!", "ValidPass123!")

        feed_page = FeedPage(driver, live_server)
        assert feed_page.is_visible(*feed_page.WORDMARK, timeout=6)
        assert "/" in driver.current_url

    def test_registration_validation_invalid_email(self, driver, live_server):
        """Invalid email address format should trigger a validation error."""
        auth_page = AuthPage(driver, live_server).open_register()
        auth_page.register("not-an-email", "Password123!", "Password123!")

        assert auth_page.has_flash_message()
        assert "valid email address" in auth_page.get_flash_message()

    def test_registration_validation_duplicate_email(self, driver, live_server, create_test_user):
        """Registering with an already registered email should display error."""
        create_test_user(email="common@example.com", password="Password123!")

        auth_page = AuthPage(driver, live_server).open_register()
        auth_page.register("common@example.com", "Password123!", "Password123!")

        assert auth_page.has_flash_message()
        assert "email is already registered" in auth_page.get_flash_message()

    def test_registration_validation_password_mismatch(self, driver, live_server):
        """Mismatched passwords should show an error flash message."""
        auth_page = AuthPage(driver, live_server).open_register()
        auth_page.register("mismatch@example.com", "Password123!", "Different123!")

        assert auth_page.has_flash_message()
        assert "Passwords do not match" in auth_page.get_flash_message()

    def test_registration_validation_short_password(self, driver, live_server):
        """Password shorter than 8 chars should show a validation error."""
        auth_page = AuthPage(driver, live_server).open_register()
        auth_page.register("short@example.com", "short", "short")

        assert auth_page.has_flash_message()
        assert "at least 8 characters" in auth_page.get_flash_message()

    def test_login_page_renders_expected_elements(self, driver, live_server):
        """Verify login page renders title, google button, email input, password input, and login button."""
        auth_page = AuthPage(driver, live_server).open_login()

        assert auth_page.get_title_text() == "Welcome back"
        assert auth_page.is_visible(*auth_page.GOOGLE_BTN)
        assert auth_page.is_visible(*auth_page.EMAIL_INPUT)
        assert auth_page.is_visible(*auth_page.PASSWORD_INPUT)
        assert not auth_page.is_visible(*auth_page.CONFIRM_PASSWORD_INPUT, timeout=1)
        assert auth_page.is_visible(*auth_page.SUBMIT_BTN)

    def test_successful_login_with_email(self, driver, live_server, create_test_user):
        """Logging in with registered email and password should redirect to home feed."""
        create_test_user(email="myemail@example.com", password="ValidPassword123!")

        auth_page = AuthPage(driver, live_server).open_login()
        auth_page.login("myemail@example.com", "ValidPassword123!")

        feed_page = FeedPage(driver, live_server)
        assert feed_page.is_visible(*feed_page.WORDMARK, timeout=6)

    def test_login_invalid_credentials(self, driver, live_server, create_test_user):
        """Logging in with wrong password should display invalid email or password error."""
        create_test_user(email="active@example.com", password="ValidPassword123!")

        auth_page = AuthPage(driver, live_server).open_login()
        auth_page.login("active@example.com", "WrongPassword!")

        assert auth_page.has_flash_message()
        assert "Invalid email or password" in auth_page.get_flash_message()

    def test_google_login_flow(self, driver, live_server):
        """Clicking Google sign-in should authenticate user and redirect to home feed."""
        auth_page = AuthPage(driver, live_server).open_login()
        auth_page.click_google_login()

        feed_page = FeedPage(driver, live_server)
        assert feed_page.is_visible(*feed_page.WORDMARK, timeout=6)

        # Check that user details in Settings show Google username and email
        settings_page = SettingsPage(driver, live_server).open()
        assert "tester@gmail.com" in settings_page.get_email()

    def test_auth_switch_link_navigation(self, driver, live_server):
        """Clicking switch link on login goes to register, and vice versa."""
        auth_page = AuthPage(driver, live_server).open_login()
        auth_page.click_switch_link()
        assert auth_page.is_at_register()

        auth_page.click_switch_link()
        assert auth_page.is_at_login()

    def test_logout_redirects_to_login(self, authenticated_driver, live_server):
        """Clicking logout in Settings should log the user out and redirect to /login."""
        driver, _ = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()
        settings_page.logout()

        auth_page = AuthPage(driver, live_server)
        assert auth_page.is_at_login()
        assert auth_page.is_visible(*auth_page.EMAIL_INPUT)
