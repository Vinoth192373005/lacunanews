"""
Page Object for the Dedicated News Roundup Page (/roundup).
"""

from typing import List
from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage


class RoundupPage(BasePage):
    """Page Object covering the standalone synthesized news roundup page."""

    PAGE = (By.CSS_SELECTOR, "[data-testid='roundup-page']")
    HEADLINE = (By.CSS_SELECTOR, "[data-testid='roundup-headline']")
    META = (By.CSS_SELECTOR, "[data-testid='roundup-meta']")
    ARTICLE = (By.CSS_SELECTOR, "[data-testid='roundup-article']")
    HERO_IMG = (By.CSS_SELECTOR, "[data-testid='roundup-hero-img']")
    SOURCES_CONTAINER = (By.CSS_SELECTOR, "[data-testid='roundup-sources']")
    SOURCE_CHIPS = (By.CSS_SELECTOR, "[data-testid='roundup-source-chip']")
    BACK_TO_FEED = (By.CSS_SELECTOR, "[data-testid='back-to-feed-btn']")
    SETTINGS_BTN = (By.CSS_SELECTOR, "[data-testid='settings-nav-btn']")
    BOOKMARK_BTN = (By.CSS_SELECTOR, "[data-testid='bookmark-roundup-btn']")
    LOADING = (By.CSS_SELECTOR, "[data-testid='roundup-loading']")

    def open(self, history_id: int = None) -> "RoundupPage":
        """Navigate directly to the roundup page."""
        url = f"{self.base_url}/roundup" if not history_id else f"{self.base_url}/roundup/{history_id}"
        self.driver.get(url)
        return self

    def is_at_roundup(self) -> bool:
        """Verify the browser is currently at the /roundup page."""
        return "/roundup" in self.driver.current_url

    def wait_for_roundup_loaded(self, timeout: int = 15) -> bool:
        """Wait until the synthesized article text is loaded."""
        try:
            self.wait_for(
                lambda d: len(d.find_elements(*self.ARTICLE)) > 0
                and d.find_element(*self.ARTICLE).is_displayed()
                and len(d.find_element(*self.ARTICLE).text.strip()) > 10,
                timeout=timeout
            )
            return True
        except Exception:
            return False

    def get_headline(self) -> str:
        """Get the main story headline."""
        return self.get_text(*self.HEADLINE)

    def get_article_text(self) -> str:
        """Get the full synthesis body text."""
        return self.get_text(*self.ARTICLE)

    def get_source_count(self) -> int:
        """Get the number of source citation chips rendered."""
        return len(self.driver.find_elements(*self.SOURCE_CHIPS))

    def back_to_feed(self) -> None:
        """Click Back to Feed button."""
        self.click(*self.BACK_TO_FEED)
