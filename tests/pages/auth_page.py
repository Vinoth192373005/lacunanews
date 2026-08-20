"""
Page Object for Authentication (Login and Registration).
"""

from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class AuthPage(BasePage):
    """Page Object covering /login and /register flows."""

    # Selectors
    WORDMARK = (By.CSS_SELECTOR, "[data-testid='auth-wordmark']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='auth-title']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-testid='email-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='password-input']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='confirm-password-input']")
    SUBMIT_BTN = (By.CSS_SELECTOR, "[data-testid='auth-submit-btn']")
    GOOGLE_BTN = (By.CSS_SELECTOR, "[data-testid='google-login-btn']")
    FLASH_MSG = (By.CSS_SELECTOR, "[data-testid='flash-message']")
    SWITCH_LINK = (By.CSS_SELECTOR, "[data-testid='auth-switch-link']")

    def open_login(self) -> "AuthPage":
        """Navigate directly to the Login page."""
        self.driver.get(f"{self.base_url}/login")
        self.find(*self.TITLE)
        return self

    def open_register(self) -> "AuthPage":
        """Navigate directly to the Register page."""
        self.driver.get(f"{self.base_url}/register")
        self.find(*self.TITLE)
        return self

    def get_title_text(self) -> str:
        """Get the h1 title on the auth form."""
        return self.get_text(*self.TITLE)

    def fill_email(self, email: str) -> "AuthPage":
        """Fill email input field."""
        self.type_text(*self.EMAIL_INPUT, email)
        return self

    def fill_password(self, password: str) -> "AuthPage":
        """Fill password input field."""
        self.type_text(*self.PASSWORD_INPUT, password)
        return self

    def fill_confirm_password(self, confirm_password: str) -> "AuthPage":
        """Fill confirm password input field (register mode)."""
        self.type_text(*self.CONFIRM_PASSWORD_INPUT, confirm_password)
        return self

    def submit(self) -> None:
        """Click the submit button."""
        self.click(*self.SUBMIT_BTN)

    def click_google_login(self) -> None:
        """Click the Google OAuth login button."""
        self.click(*self.GOOGLE_BTN)

    def login(self, email: str, password: str) -> None:
        """Convenience method to fill and submit the login form."""
        self.fill_email(email)
        self.fill_password(password)
        self.submit()

    def register(self, email: str, password: str = "Password123!", confirm_password: str = None) -> None:
        """Convenience method to fill and submit the registration form."""
        user_confirm = confirm_password if confirm_password is not None else password

        self.fill_email(email)
        self.fill_password(password)
        self.fill_confirm_password(user_confirm)
        self.submit()

    def get_flash_message(self, timeout: int = 5) -> str:
        """Get text of the flash error or success message."""
        return self.get_text(*self.FLASH_MSG, timeout=timeout)

    def has_flash_message(self, timeout: int = 2) -> bool:
        """Check if a flash message is present on the page."""
        return self.is_visible(*self.FLASH_MSG, timeout=timeout)

    def click_switch_link(self) -> None:
        """Click the toggle link to switch between Login and Register."""
        self.click(*self.SWITCH_LINK)

    def is_at_login(self, timeout: int = 5) -> bool:
        """Check if currently on the Login page."""
        try:
            self.wait_for(lambda d: "/login" in d.current_url, timeout=timeout)
            return True
        except Exception:
            return False

    def is_at_register(self, timeout: int = 5) -> bool:
        """Check if currently on the Register page."""
        try:
            self.wait_for(lambda d: "/register" in d.current_url, timeout=timeout)
            return True
        except Exception:
            return False
