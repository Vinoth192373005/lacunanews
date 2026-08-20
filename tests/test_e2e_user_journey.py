"""
End-to-End User Journey Selenium Test.
Tests a complete real-world user scenario from registration to feed interaction,
search interest capture, settings page navigation, theming, and logout.
"""

import time
import pytest
from tests.pages.auth_page import AuthPage
from tests.pages.feed_page import FeedPage
from tests.pages.settings_page import SettingsPage


@pytest.mark.selenium
def test_complete_user_journey(driver, live_server):
    """
    Complete E2E Journey:
    1. Register a new user account.
    2. Land on feed and switch categories.
    3. Perform keyword search (which automatically tracks user interest).
    4. Open the Settings page via topbar.
    5. Verify account details and captured search interest.
    6. Switch UI theme to Dark mode.
    7. Log out from Settings and verify redirection back to login.
    """
    username = "journey_user_99"
    password = "SuperPassword123!"

    # 1. Register
    auth_page = AuthPage(driver, live_server).open_register()
    auth_page.register("journey@example.com", password=password, confirm_password=password)

    # 2. Verify Home Feed loaded
    feed_page = FeedPage(driver, live_server)
    assert feed_page.is_visible(*feed_page.WORDMARK, timeout=6)

    # 3. Category Navigation
    feed_page.select_category("technology")
    tech_pill = feed_page.find(*feed_page.PILL_TECH)
    assert "active" in (tech_pill.get_attribute("class") or "")

    # 4. Search
    feed_page.search("Artificial Intelligence")
    time.sleep(0.5)

    # 5. Open Settings Page & Verify Account
    feed_page.click(*feed_page.SETTINGS_BTN)
    settings_page = SettingsPage(driver, live_server)
    assert settings_page.is_at_settings()
    assert settings_page.get_email() == "journey@example.com"

    # 6. Verify tracked interests include the search topic
    interests = settings_page.get_interest_names()
    assert any("Artificial Intelligence" in item or "Intelligence" in item for item in interests)

    # 7. Change Theme to Pitch Black
    settings_page.select_theme("pitch-black")
    assert settings_page.get_active_body_theme() == "pitch-black"

    # 8. Logout
    settings_page.logout()
    assert auth_page.is_at_login()
    assert auth_page.is_visible(*auth_page.EMAIL_INPUT)

