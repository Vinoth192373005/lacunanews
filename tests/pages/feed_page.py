"""
Page Object for the Main Feed and Synthesized Roundup Reader Modal.
"""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.pages.base_page import BasePage


class FeedPage(BasePage):
    """Page Object covering home feed, category switching, search, and the reader modal."""

    # Topbar & Navigation
    WORDMARK = (By.CSS_SELECTOR, "[data-testid='topbar-wordmark']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-testid='search-input']")
    SEARCH_BTN = (By.CSS_SELECTOR, "[data-testid='search-btn']")
    SETTINGS_BTN = (By.CSS_SELECTOR, "[data-testid='settings-nav-btn']")
    SIDE_MENU_TOGGLE = (By.CSS_SELECTOR, "[data-testid='settings-nav-btn']")

    # Category Pills
    PILL_HOME = (By.CSS_SELECTOR, "[data-testid='pill-home']")
    PILL_BUSINESS = (By.CSS_SELECTOR, "[data-testid='pill-business']")
    PILL_TECH = (By.CSS_SELECTOR, "[data-testid='pill-technology']")
    PILL_SPORTS = (By.CSS_SELECTOR, "[data-testid='pill-sports']")
    PILL_HEALTH = (By.CSS_SELECTOR, "[data-testid='pill-health']")
    PILL_CULTURE = (By.CSS_SELECTOR, "[data-testid='pill-culture']")

    # Story Feed Cards
    STORY_FEED = (By.CSS_SELECTOR, "[data-testid='story-feed']")
    FEED_STATUS = (By.CSS_SELECTOR, "[data-testid='feed-status']")
    HERO_LEAD_CARD = (By.CSS_SELECTOR, "[data-testid='hero-lead-card']")
    HERO_LEAD_TITLE = (By.CSS_SELECTOR, "[data-testid='hero-lead-title']")
    HERO_SIDE_CARD = (By.CSS_SELECTOR, "[data-testid='hero-side-card']")
    HERO_SIDE_TITLE = (By.CSS_SELECTOR, "[data-testid='hero-side-title']")
    CLUSTER_CARD = (By.CSS_SELECTOR, "[data-testid='cluster-card']")
    CLUSTER_TITLE = (By.CSS_SELECTOR, "[data-testid='cluster-title']")
    HERO_SOURCES_BTN = (By.CSS_SELECTOR, "[data-testid='hero-sources-btn']")
    HERO_SOURCES_PANEL = (By.CSS_SELECTOR, "[data-testid='hero-sources-panel']")
    SOURCES_PANEL = (By.CSS_SELECTOR, "[data-testid='sources-panel']")

    # Reader Modal
    READER_MODAL = (By.CSS_SELECTOR, "[data-testid='reader-modal']")
    READER_BACKDROP = (By.CSS_SELECTOR, "[data-testid='reader-backdrop']")
    READER_CLOSE_BTN = (By.CSS_SELECTOR, "[data-testid='reader-close-btn']")
    READER_INNER = (By.CSS_SELECTOR, "[data-testid='reader-inner']")
    READER_LOADING = (By.CSS_SELECTOR, "[data-testid='reader-loading']")
    READER_HEADLINE = (By.CSS_SELECTOR, "[data-testid='reader-headline']")
    READER_ARTICLE = (By.CSS_SELECTOR, "[data-testid='reader-article']")
    READER_SOURCE_CHIP = (By.CSS_SELECTOR, "[data-testid='reader-source-chip']")

    def open_home(self) -> "FeedPage":
        """Navigate to the Home feed page."""
        self.driver.get(f"{self.base_url}/")
        self.find(*self.WORDMARK)
        return self

    def wait_for_feed_loaded(self, timeout: int = 15) -> bool:
        """Wait until stories appear or feed status finishes loading."""
        try:
            self.wait_for(
                lambda d: len(d.find_elements(*self.HERO_LEAD_CARD)) > 0
                or len(d.find_elements(*self.CLUSTER_CARD)) > 0
                or "No stories found" in (d.find_element(*self.FEED_STATUS).text if d.find_elements(*self.FEED_STATUS) else ""),
                timeout=timeout
            )
            return True
        except Exception:
            return False

    def select_category(self, name: str) -> None:
        """Click on a category pill (e.g. 'home', 'business', 'technology', 'sports', 'health', 'culture')."""
        pill_map = {
            "home": self.PILL_HOME,
            "business": self.PILL_BUSINESS,
            "technology": self.PILL_TECH,
            "sports": self.PILL_SPORTS,
            "sport": self.PILL_SPORTS,
            "health": self.PILL_HEALTH,
            "culture": self.PILL_CULTURE,
        }
        loc = pill_map.get(name.lower(), (By.CSS_SELECTOR, f"[data-testid='pill-{name.lower()}']"))
        self.click(*loc)

    def search(self, query: str) -> None:
        """Type query into search bar and click search button."""
        self.type_text(*self.SEARCH_INPUT, query)
        self.click(*self.SEARCH_BTN)

    def get_hero_lead_title(self) -> str:
        """Get title of the lead story card."""
        return self.get_text(*self.HERO_LEAD_TITLE)

    def get_hero_side_titles(self) -> List[str]:
        """Get titles of the supporting hero story cards."""
        elements = self.find_all(*self.HERO_SIDE_TITLE)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_cluster_titles(self) -> List[str]:
        """Get titles of all more-stories cluster cards."""
        elements = self.find_all(*self.CLUSTER_TITLE)
        return [el.text.strip() for el in elements if el.text.strip()]

    def open_hero_sources(self) -> None:
        """Click the sources dropdown button on the hero lead card."""
        self.click(*self.HERO_SOURCES_BTN)

    def is_sources_panel_open(self) -> bool:
        """Check if any sources dropdown panel is currently visible."""
        panels = self.driver.find_elements(By.CSS_SELECTOR, ".sources-panel.open, .hero-sources-panel.open")
        return len(panels) > 0 and panels[0].is_displayed()

    def open_hero_lead_reader(self) -> None:
        """Click on the lead story card to open the reader modal."""
        self.click(*self.HERO_LEAD_CARD)

    def open_first_cluster_reader(self) -> None:
        """Click on the first story card in More Stories."""
        cards = self.find_all(*self.CLUSTER_CARD)
        if cards:
            cards[0].click()

    def is_reader_open(self, timeout: int = 5) -> bool:
        """Check if reader modal is open and visible."""
        return self.is_visible(*self.READER_MODAL, timeout=timeout)

    def wait_for_reader_content(self, timeout: int = 15) -> bool:
        """Wait for article synthesis to complete in reader modal."""
        try:
            self.wait_for(
                lambda d: len(d.find_elements(*self.READER_ARTICLE)) > 0,
                timeout=timeout
            )
            return True
        except Exception:
            return False

    def get_reader_headline(self) -> str:
        """Get the synthesized article headline in the reader modal."""
        return self.get_text(*self.READER_HEADLINE)

    def get_reader_article_text(self) -> str:
        """Get the full synthesized article text in the reader modal."""
        return self.get_text(*self.READER_ARTICLE)

    def get_reader_sources_count(self) -> int:
        """Get number of source chips in the reader modal."""
        chips = self.find_all(*self.READER_SOURCE_CHIP)
        return len(chips)

    def close_reader(self) -> None:
        """Close the reader modal via its close button."""
        self.click(*self.READER_CLOSE_BTN)
        self.wait_until_invisible(*self.READER_MODAL)

    def close_reader_via_escape(self) -> None:
        """Close the reader modal by sending the Escape key."""
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        self.wait_until_invisible(*self.READER_MODAL)
