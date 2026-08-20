"""
Page Object for the Dedicated Reading History Page (/history).
"""

from typing import List
from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class HistoryPage(BasePage):
    """Page Object covering the standalone reading history page."""

    PAGE = (By.CSS_SELECTOR, "[data-testid='history-page']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='history-title']")
    COUNT_LABEL = (By.CSS_SELECTOR, "[data-testid='history-count']")
    CLEAR_ALL_BTN = (By.CSS_SELECTOR, "[data-testid='clear-all-history-btn']")
    CARDS = (By.CSS_SELECTOR, "[data-testid='history-card']")
    CARD_TITLES = (By.CSS_SELECTOR, "[data-testid='history-card-title']")
    REMOVE_BTNS = (By.CSS_SELECTOR, "[data-testid='remove-history-btn']")
    EMPTY_MSG = (By.CSS_SELECTOR, "[data-testid='empty-history']")
    BACK_TO_SETTINGS = (By.CSS_SELECTOR, "[data-testid='back-to-settings-btn']")
    BACK_TO_FEED = (By.CSS_SELECTOR, "[data-testid='back-to-feed-btn']")

    def open(self) -> "HistoryPage":
        """Navigate to the history page."""
        self.driver.get(f"{self.base_url}/history")
        self.find(*self.TITLE)
        return self

    def is_at_history(self) -> bool:
        """Verify the browser is currently at /history."""
        return "/history" in self.driver.current_url

    def get_history_items_count(self) -> int:
        """Get the number of history cards rendered."""
        return len(self.driver.find_elements(*self.CARDS))

    def remove_first_history_item(self) -> None:
        """Click the remove button on the first history item."""
        btns = self.driver.find_elements(*self.REMOVE_BTNS)
        if btns:
            btns[0].click()

    def clear_all(self, accept_alert: bool = True) -> None:
        """Click clear all history button and handle confirm alert."""
        self.click(*self.CLEAR_ALL_BTN)
        if accept_alert:
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except Exception:
                pass

    def click_first_roundup(self) -> None:
        """Click the first history card title link to open roundup."""
        titles = self.driver.find_elements(*self.CARD_TITLES)
        if titles:
            titles[0].click()
