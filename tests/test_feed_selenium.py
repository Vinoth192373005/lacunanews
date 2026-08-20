"""
Selenium Automated Tests for Story Feed, Categories, Search, and Dedicated News Roundup Page.
"""

import time
import pytest
from tests.pages.feed_page import FeedPage
from tests.pages.roundup_page import RoundupPage


@pytest.mark.selenium
@pytest.mark.feed
class TestFeedAndRoundup:
    """Test suite covering news feed navigation, category switching, and dedicated roundup page."""

    def test_topbar_and_navigation_pills_rendered(self, authenticated_driver, live_server):
        """Verify topbar, wordmark, search bar, and all category pills are rendered."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()

        assert feed_page.is_visible(*feed_page.WORDMARK)
        assert feed_page.is_visible(*feed_page.SEARCH_INPUT)
        assert feed_page.is_visible(*feed_page.SEARCH_BTN)
        assert feed_page.is_visible(*feed_page.PILL_HOME)
        assert feed_page.is_visible(*feed_page.PILL_BUSINESS)
        assert feed_page.is_visible(*feed_page.PILL_TECH)
        assert feed_page.is_visible(*feed_page.PILL_SPORTS)
        assert feed_page.is_visible(*feed_page.PILL_HEALTH)
        assert feed_page.is_visible(*feed_page.PILL_CULTURE)

    def test_category_navigation_pill_activation(self, authenticated_driver, live_server):
        """Clicking category pills should toggle the active class."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()

        # Switch to Technology
        feed_page.select_category("technology")
        tech_pill = feed_page.find(*feed_page.PILL_TECH)
        assert "active" in (tech_pill.get_attribute("class") or "")

        # Switch to Business
        feed_page.select_category("business")
        biz_pill = feed_page.find(*feed_page.PILL_BUSINESS)
        assert "active" in (biz_pill.get_attribute("class") or "")

    def test_search_input_clears_pill_active_and_triggers_feed(self, authenticated_driver, live_server):
        """Performing a search should deselect category pills and trigger query."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()

        feed_page.search("Artificial Intelligence")
        time.sleep(0.5)

        # Pills should no longer be active
        home_pill = feed_page.find(*feed_page.PILL_HOME)
        assert "active" not in (home_pill.get_attribute("class") or "")

    def test_feed_story_cards_or_status_displayed(self, authenticated_driver, live_server):
        """Story feed should display either story cards or valid loaded status."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()
        feed_loaded = feed_page.wait_for_feed_loaded(timeout=10)

        assert feed_loaded is True

    def test_open_roundup_page_from_story_card(self, authenticated_driver, live_server):
        """Clicking a story card navigates to the dedicated /roundup page with headline and article."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()
        feed_page.wait_for_feed_loaded(timeout=10)

        hero_cards = driver.find_elements(*feed_page.HERO_LEAD_CARD)
        cluster_cards = driver.find_elements(*feed_page.CLUSTER_CARD)

        if hero_cards:
            hero_cards[0].click()
        elif cluster_cards:
            cluster_cards[0].click()
        else:
            pytest.skip("No news feed cards loaded in current test run")

        roundup_page = RoundupPage(driver, live_server)
        assert roundup_page.is_at_roundup()
        assert roundup_page.is_visible(*roundup_page.PAGE)
        assert roundup_page.is_visible(*roundup_page.HEADLINE)

        # Wait for article text to load
        assert roundup_page.wait_for_roundup_loaded(timeout=15)
        assert len(roundup_page.get_headline()) > 0
        assert len(roundup_page.get_article_text()) > 10

        # Verify back to feed navigation
        roundup_page.back_to_feed()
        assert "/" in driver.current_url and "/roundup" not in driver.current_url

    def test_roundup_page_direct_access_or_history(self, authenticated_driver, live_server):
        """Accessing /roundup directly renders topbar and container cleanly."""
        driver, _ = authenticated_driver
        driver.get(f"{live_server}/roundup")

        roundup_page = RoundupPage(driver, live_server)
        assert roundup_page.is_at_roundup()
        assert roundup_page.is_visible(*roundup_page.PAGE)
        assert roundup_page.is_visible(*roundup_page.BACK_TO_FEED)
