"""
Page Object for the Settings Page (/settings).
"""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.pages.base_page import BasePage


class SettingsPage(BasePage):
    """Page Object covering Appearance, Interests, Region, and Account settings."""

    # Page container & Header
    PAGE = (By.CSS_SELECTOR, "[data-testid='settings-page']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='settings-title']")
    BACK_TO_FEED = (By.CSS_SELECTOR, "[data-testid='back-to-feed-btn']")
    WORDMARK = (By.CSS_SELECTOR, "[data-testid='topbar-wordmark']")

    # Appearance
    THEME_TOGGLE_BTN = (By.CSS_SELECTOR, "[data-testid='theme-toggle-btn']")
    THEME_DEFAULT = (By.CSS_SELECTOR, "[data-testid='theme-option-default']")
    THEME_PITCH_BLACK = (By.CSS_SELECTOR, "[data-testid='theme-option-pitch-black']")
    THEME_PALETTE_ONE = (By.CSS_SELECTOR, "[data-testid='theme-option-palette-one']")
    THEME_PALETTE_TWO = (By.CSS_SELECTOR, "[data-testid='theme-option-palette-two']")
    THEME_PALETTE_THREE = (By.CSS_SELECTOR, "[data-testid='theme-option-palette-three']")

    # Interests
    INTEREST_CHIPS = (By.CSS_SELECTOR, "[data-testid='interest-chip']")
    REMOVE_INTEREST_BTNS = (By.CSS_SELECTOR, "[data-testid='remove-interest-btn']")
    NEW_INTEREST_INPUT = (By.CSS_SELECTOR, "[data-testid='new-interest-input']")
    ADD_INTEREST_BTN = (By.CSS_SELECTOR, "[data-testid='add-interest-btn']")
    CLEAR_INTERESTS_BTN = (By.CSS_SELECTOR, "[data-testid='clear-interests-btn']")
    EMPTY_INTERESTS = (By.CSS_SELECTOR, "[data-testid='empty-interests']")

    # Region
    REGION_BTN_US = (By.CSS_SELECTOR, "[data-testid='region-btn-us']")
    REGION_BTN_GB = (By.CSS_SELECTOR, "[data-testid='region-btn-gb']")
    REGION_BTN_IN = (By.CSS_SELECTOR, "[data-testid='region-btn-in']")

    # Account & Logout
    ACCOUNT_USERNAME = (By.CSS_SELECTOR, "[data-testid='account-username']")
    ACCOUNT_EMAIL = (By.CSS_SELECTOR, "[data-testid='account-email']")
    STAT_READ_COUNT = (By.CSS_SELECTOR, "[data-testid='stat-read-count']")
    VIEW_HISTORY_BTN = (By.CSS_SELECTOR, "[data-testid='view-history-btn']")
    CLEAR_HISTORY_BTN = (By.CSS_SELECTOR, "[data-testid='clear-history-btn']")
    STAT_BOOKMARKS_COUNT = (By.CSS_SELECTOR, "[data-testid='stat-bookmarks-count']")
    VIEW_BOOKMARKS_BTN = (By.CSS_SELECTOR, "[data-testid='view-bookmarks-btn']")
    CLEAR_BOOKMARKS_BTN = (By.CSS_SELECTOR, "[data-testid='clear-bookmarks-btn']")
    LOGOUT_BTN = (By.CSS_SELECTOR, "[data-testid='settings-logout-btn']")

    def open(self) -> "SettingsPage":
        """Navigate directly to the settings page."""
        self.driver.get(f"{self.base_url}/settings")
        self.find(*self.TITLE)
        return self

    def is_at_settings(self) -> bool:
        """Verify the browser is currently at the settings page."""
        return "/settings" in self.driver.current_url

    def get_username(self) -> str:
        """Get the displayed username."""
        return self.get_text(*self.ACCOUNT_USERNAME)

    def get_email(self) -> str:
        """Get the displayed email."""
        return self.get_text(*self.ACCOUNT_EMAIL)

    def get_read_count(self) -> str:
        """Get the roundups read stat."""
        return self.get_text(*self.STAT_READ_COUNT)

    def toggle_theme_mode(self) -> None:
        """Click the main light/dark mode switch button."""
        self.click(*self.THEME_TOGGLE_BTN)

    def select_theme(self, theme_name: str) -> None:
        """Select a theme swatch."""
        theme_map = {
            "default": self.THEME_DEFAULT,
            "light": self.THEME_DEFAULT,
            "pitch-black": self.THEME_PITCH_BLACK,
            "dark": self.THEME_PITCH_BLACK,
            "palette-one": self.THEME_PALETTE_ONE,
            "palette-two": self.THEME_PALETTE_TWO,
            "palette-three": self.THEME_PALETTE_THREE,
        }
        if theme_name in theme_map:
            self.click(*theme_map[theme_name])

    def get_active_body_theme(self) -> str:
        """Get the data-theme attribute on <body>."""
        body = self.driver.find_element(By.TAG_NAME, "body")
        return body.get_attribute("data-theme") or ""

    def select_region(self, region_code: str) -> None:
        """Select a region button."""
        selector = (By.CSS_SELECTOR, f"[data-testid='region-btn-{region_code.lower()}']")
        self.click(*selector)

    def get_interest_names(self) -> List[str]:
        """Get all interest chip texts."""
        chips = self.driver.find_elements(*self.INTEREST_CHIPS)
        return [c.text.replace("×", "").strip() for c in chips]

    def add_interest(self, topic: str) -> None:
        """Add a new interest via input."""
        self.type_text(*self.NEW_INTEREST_INPUT, topic)
        self.click(*self.ADD_INTEREST_BTN)
        self.wait_for(lambda d: topic.lower() in " ".join([c.text.lower() for c in d.find_elements(*self.INTEREST_CHIPS)]))

    def remove_first_interest(self) -> None:
        """Remove the first interest chip."""
        btns = self.driver.find_elements(*self.REMOVE_INTEREST_BTNS)
        if btns:
            btns[0].click()

    def clear_reading_history(self) -> None:
        """Click clear reading history."""
        self.click(*self.CLEAR_HISTORY_BTN)

    def back_to_feed(self) -> None:
        """Click the Back to Feed button."""
        self.click(*self.BACK_TO_FEED)

    def logout(self) -> None:
        """Click the Log Out button."""
        self.click(*self.LOGOUT_BTN)
