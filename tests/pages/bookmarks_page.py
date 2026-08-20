"""
Page Object for the Dedicated Bookmarks Page (/bookmarks).
"""

from typing import List
from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class BookmarksPage(BasePage):
    """Page Object covering the standalone saved bookmarks page."""

    PAGE = (By.CSS_SELECTOR, "[data-testid='bookmarks-page']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='bookmarks-title']")
    COUNT_LABEL = (By.CSS_SELECTOR, "[data-testid='bookmarks-count']")
    CLEAR_ALL_BTN = (By.CSS_SELECTOR, "[data-testid='clear-all-bookmarks-btn']")
    CARDS = (By.CSS_SELECTOR, "[data-testid='bookmark-card']")
    CARD_TITLES = (By.CSS_SELECTOR, "[data-testid='bookmark-card-title']")
    REMOVE_BTNS = (By.CSS_SELECTOR, "[data-testid='remove-bookmark-btn']")
    EMPTY_MSG = (By.CSS_SELECTOR, "[data-testid='empty-bookmarks']")
    BACK_TO_SETTINGS = (By.CSS_SELECTOR, "[data-testid='back-to-settings-btn']")
    BACK_TO_FEED = (By.CSS_SELECTOR, "[data-testid='back-to-feed-btn']")

    def open(self) -> "BookmarksPage":
        """Navigate to the bookmarks page."""
        self.driver.get(f"{self.base_url}/bookmarks")
        self.find(*self.TITLE)
        return self

    def is_at_bookmarks(self) -> bool:
        """Verify the browser is currently at /bookmarks."""
        return "/bookmarks" in self.driver.current_url

    def get_bookmarks_items_count(self) -> int:
        """Get the number of bookmark cards rendered."""
        return len(self.driver.find_elements(*self.CARDS))

    def remove_first_bookmark_item(self) -> None:
        """Click the remove button on the first bookmark item."""
        btns = self.driver.find_elements(*self.REMOVE_BTNS)
        if btns:
            btns[0].click()

    def clear_all(self, accept_alert: bool = True) -> None:
        """Click clear all bookmarks button and handle confirm alert."""
        self.click(*self.CLEAR_ALL_BTN)
        if accept_alert:
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except Exception:
                pass

    def click_first_bookmark(self) -> None:
        """Click the first bookmark card title link to open roundup."""
        titles = self.driver.find_elements(*self.CARD_TITLES)
        if titles:
            titles[0].click()
