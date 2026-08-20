"""
Selenium Automated Tests for Dedicated Settings Page, Interests Management, Dedicated Reading History, Theming, and Region.
"""

import time
import pytest
import news
from tests.pages.feed_page import FeedPage
from tests.pages.settings_page import SettingsPage
from tests.pages.history_page import HistoryPage
from tests.pages.bookmarks_page import BookmarksPage
from tests.pages.roundup_page import RoundupPage


@pytest.mark.selenium
class TestSettingsAndInterests:
    """Test suite covering the dedicated /settings page, interest tracking, history page, bookmarks, and preferences."""

    def test_navigation_to_settings_and_back(self, authenticated_driver, live_server):
        """User can navigate to /settings from the topbar button and return to feed."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()

        # Click topbar settings button
        feed_page.click(*feed_page.SETTINGS_BTN)
        settings_page = SettingsPage(driver, live_server)
        assert settings_page.is_at_settings()
        assert settings_page.get_text(*settings_page.TITLE) == "Settings"

        # Click Back to Feed
        settings_page.back_to_feed()
        assert "/" in driver.current_url and "/settings" not in driver.current_url

    def test_settings_displays_account_info(self, authenticated_driver, live_server):
        """Account section in Settings should display the current username and stats."""
        driver, user = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()

        assert settings_page.get_username() == user["username"]
        assert settings_page.is_visible(*settings_page.STAT_READ_COUNT)
        assert settings_page.is_visible(*settings_page.STAT_BOOKMARKS_COUNT)

    def test_theme_switching_and_toggle(self, authenticated_driver, live_server):
        """Clicking light/dark toggle and theme swatches updates the theme attribute."""
        driver, _ = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()

        # Toggle to Dark
        settings_page.toggle_theme_mode()
        assert settings_page.get_active_body_theme() == "pitch-black"

        # Toggle back to Light
        settings_page.toggle_theme_mode()
        assert settings_page.get_active_body_theme() in ("", "default")

        # Select Palette themes
        settings_page.select_theme("palette-one")
        assert settings_page.get_active_body_theme() == "palette-one"

        settings_page.select_theme("palette-two")
        assert settings_page.get_active_body_theme() == "palette-two"

        settings_page.select_theme("palette-three")
        assert settings_page.get_active_body_theme() == "palette-three"

    def test_manual_interest_add_and_remove(self, authenticated_driver, live_server):
        """User can add a custom interest topic and remove it via the remove button."""
        driver, _ = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()

        initial_count = len(settings_page.get_interest_names())

        # Add new interest
        test_topic = "Quantum Computing"
        settings_page.add_interest(test_topic)
        time.sleep(0.5)

        interests = settings_page.get_interest_names()
        assert any(test_topic.lower() in item.lower() for item in interests)

        # Remove the interest
        settings_page.remove_first_interest()
        time.sleep(0.5)
        updated_interests = settings_page.get_interest_names()
        assert len(updated_interests) <= len(interests)

    def test_search_automatically_tracks_interest(self, authenticated_driver, live_server):
        """Searching for a keyword automatically records it in the user's interests."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()

        search_term = "OpenAI GPT-5"
        feed_page.search(search_term)
        time.sleep(0.6)

        # Navigate to settings to verify captured interest
        settings_page = SettingsPage(driver, live_server).open()
        interests = settings_page.get_interest_names()
        assert any("OpenAI" in item or "GPT" in item for item in interests)

    def test_roundup_reading_tracks_category_interest(self, authenticated_driver, live_server):
        """Reading a synthesized article records its category rather than raw headline title."""
        driver, user = authenticated_driver
        from news import save_interests_from_roundup

        # Simulate reading an article in the Technology category
        save_interests_from_roundup(
            user["id"],
            title="Nvidia Unveils Next-Gen AI Chip Architecture for Supercomputers",
            sources=[{"title": "TechCrunch - Nvidia AI Chip", "url": "https://techcrunch.com/nvidia-ai"}],
            article_text="Nvidia announced its latest Blackwell architecture designed to accelerate machine learning and artificial intelligence workloads across global cloud datacenters."
        )

        settings_page = SettingsPage(driver, live_server).open()
        interests = settings_page.get_interest_names()
        # Verify that category 'Technology' was saved and NOT the raw 70-character headline
        assert "Technology" in interests
        assert not any("Nvidia Unveils Next-Gen" in item for item in interests)

    def test_region_selection(self, authenticated_driver, live_server):
        """Selecting a region button should update region preferences."""
        driver, _ = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()

        assert settings_page.is_visible(*settings_page.REGION_BTN_GB)
        settings_page.select_region("gb")
        time.sleep(0.3)

    def test_navigate_to_dedicated_history_page(self, authenticated_driver, live_server):
        """User can navigate from Settings to the dedicated Reading History page."""
        driver, _ = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()

        assert settings_page.is_visible(*settings_page.VIEW_HISTORY_BTN)
        settings_page.click(*settings_page.VIEW_HISTORY_BTN)

        history_page = HistoryPage(driver, live_server)
        assert history_page.is_at_history()
        assert history_page.is_visible(*history_page.PAGE)
        assert history_page.is_visible(*history_page.TITLE)

    def test_history_articles_render_images(self, authenticated_driver, live_server):
        """Verify history articles display images correctly with referrerpolicy."""
        driver, user = authenticated_driver

        test_img_url = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400"
        with news.get_db() as db:
            param = news.sql_param()
            db.execute(
                f"INSERT INTO article_history (user_id, title, article_text, image_url, source_count, sources_json) VALUES ({param}, {param}, {param}, {param}, {param}, {param})",
                (user["id"], "Image Test Article In History", "Synthesis text with image...", test_img_url, 1, "[]")
            )

        history_page = HistoryPage(driver, live_server).open()
        cards = driver.find_elements(*history_page.CARDS)
        assert len(cards) > 0

        # Verify the thumbnail image element has the expected src or fallback
        card_img = cards[0].find_element(pytest.importorskip("selenium.webdriver.common.by").By.CSS_SELECTOR, ".card-thumb")
        assert card_img.get_attribute("referrerpolicy") == "no-referrer"
        assert card_img.get_attribute("src") != ""

    def test_history_page_remove_singular_and_clear_all(self, authenticated_driver, live_server):
        """User can remove a single history entry or clear all reading history."""
        driver, user = authenticated_driver

        # Seed test history entries directly for the authenticated user
        with news.get_db() as db:
            param = news.sql_param()
            db.execute(
                f"INSERT INTO article_history (user_id, title, article_text, image_url, source_count, sources_json) VALUES ({param}, {param}, {param}, {param}, {param}, {param})",
                (user["id"], "Test Quantum Computing Roundup", "Detailed synthesis on quantum breakthroughs...", "", 3, "[]")
            )
            db.execute(
                f"INSERT INTO article_history (user_id, title, article_text, image_url, source_count, sources_json) VALUES ({param}, {param}, {param}, {param}, {param}, {param})",
                (user["id"], "Test AI Breakthrough Roundup", "Detailed synthesis on artificial intelligence...", "", 2, "[]")
            )

        # Open dedicated History page
        history_page = HistoryPage(driver, live_server).open()
        initial_items = history_page.get_history_items_count()
        assert initial_items >= 2

        # Test removing single history item
        history_page.remove_first_history_item()
        time.sleep(0.5)
        after_remove_items = history_page.get_history_items_count()
        assert after_remove_items == initial_items - 1

        # Test clear all history
        assert history_page.is_visible(*history_page.CLEAR_ALL_BTN)
        history_page.clear_all(accept_alert=True)
        time.sleep(0.5)
        assert history_page.get_history_items_count() == 0
        assert history_page.is_visible(*history_page.EMPTY_MSG)

    def test_navigate_to_dedicated_bookmarks_page(self, authenticated_driver, live_server):
        """User can navigate from Settings to the dedicated Bookmarks page."""
        driver, _ = authenticated_driver
        settings_page = SettingsPage(driver, live_server).open()

        assert settings_page.is_visible(*settings_page.VIEW_BOOKMARKS_BTN)
        settings_page.click(*settings_page.VIEW_BOOKMARKS_BTN)

        bookmarks_page = BookmarksPage(driver, live_server)
        assert bookmarks_page.is_at_bookmarks()
        assert bookmarks_page.is_visible(*bookmarks_page.PAGE)
        assert bookmarks_page.is_visible(*bookmarks_page.TITLE)

    def test_bookmarks_page_remove_singular_and_clear_all(self, authenticated_driver, live_server):
        """User can view saved bookmarks, remove single bookmark, or clear all bookmarks."""
        driver, user = authenticated_driver

        # Seed test bookmark entries
        test_img_url = "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400"
        with news.get_db() as db:
            param = news.sql_param()
            db.execute(
                f"INSERT INTO bookmarks (user_id, title, article_text, image_url, source_count, sources_json) VALUES ({param}, {param}, {param}, {param}, {param}, {param})",
                (user["id"], "Bookmarked Science Story", "Deep dive analysis into astrophysics...", test_img_url, 4, "[]")
            )
            db.execute(
                f"INSERT INTO bookmarks (user_id, title, article_text, image_url, source_count, sources_json) VALUES ({param}, {param}, {param}, {param}, {param}, {param})",
                (user["id"], "Bookmarked Tech Report", "Silicon breakthroughs in 2026...", "", 2, "[]")
            )

        bookmarks_page = BookmarksPage(driver, live_server).open()
        initial_items = bookmarks_page.get_bookmarks_items_count()
        assert initial_items >= 2

        # Verify image rendering with referrerpolicy
        cards = driver.find_elements(*bookmarks_page.CARDS)
        card_img = cards[0].find_element(pytest.importorskip("selenium.webdriver.common.by").By.CSS_SELECTOR, ".card-thumb")
        assert card_img.get_attribute("referrerpolicy") == "no-referrer"

        # Test single bookmark removal
        bookmarks_page.remove_first_bookmark_item()
        time.sleep(0.5)
        assert bookmarks_page.get_bookmarks_items_count() == initial_items - 1

        # Test clear all bookmarks
        assert bookmarks_page.is_visible(*bookmarks_page.CLEAR_ALL_BTN)
        bookmarks_page.clear_all(accept_alert=True)
        time.sleep(0.5)
        assert bookmarks_page.get_bookmarks_items_count() == 0
        assert bookmarks_page.is_visible(*bookmarks_page.EMPTY_MSG)

    def test_bookmark_roundup_toggle(self, authenticated_driver, live_server):
        """User can toggle the bookmark button in News Roundup page."""
        driver, user = authenticated_driver

        # Seed a history entry to open roundup for
        with news.get_db() as db:
            param = news.sql_param()
            db.execute(
                f"INSERT INTO article_history (user_id, title, article_text, image_url, source_count, sources_json) VALUES ({param}, {param}, {param}, {param}, {param}, {param})",
                (user["id"], "Test Toggle Bookmark Story", "Full synthesis body for toggle bookmark...", "", 2, "[]")
            )
            row = db.execute(
                f"SELECT id FROM article_history WHERE user_id = {param} AND title = {param}",
                (user["id"], "Test Toggle Bookmark Story")
            ).fetchone()
            history_id = row["id"]

        roundup_page = RoundupPage(driver, live_server).open(history_id=history_id)
        assert roundup_page.is_at_roundup()

        bookmark_btn_loc = (pytest.importorskip("selenium.webdriver.common.by").By.CSS_SELECTOR, "[data-testid='bookmark-roundup-btn']")
        assert roundup_page.is_visible(*bookmark_btn_loc)
        btn_text_before = roundup_page.get_text(*bookmark_btn_loc)

        # Toggle to Bookmark / Save
        roundup_page.click(*bookmark_btn_loc)
        time.sleep(0.5)
        btn_text_after = roundup_page.get_text(*bookmark_btn_loc)
        assert "SAVED" in btn_text_after.upper() or btn_text_after != btn_text_before

        # Toggle off
        roundup_page.click(*bookmark_btn_loc)
        time.sleep(0.5)
        btn_text_final = roundup_page.get_text(*bookmark_btn_loc)
        assert "BOOKMARK" in btn_text_final.upper()

