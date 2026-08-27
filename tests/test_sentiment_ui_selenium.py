"""
Selenium UI tests for reader feedback comment section,
positivity/negativity percentage badges on the home feed, and roundup sentiment analysis.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.feed_page import FeedPage
from tests.pages.roundup_page import RoundupPage


@pytest.mark.selenium
class TestSentimentUI:
    """Test suite covering home feed sentiment badges and interactive feedback modal & roundup section."""

    def test_homefeed_sentiment_badges_rendered(self, authenticated_driver, live_server):
        """Story cards on the homefeed should display positivity and negativity percentage badges."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()
        feed_page.wait_for_feed_loaded(timeout=10)

        badges = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".story-sentiment-badge"))
        )
        assert len(badges) >= 1, "Expected at least one sentiment badge on story cards"

        first_badge = badges[0]
        pos_tag = first_badge.find_element(By.CSS_SELECTOR, ".pos-tag .sentiment-val")
        neg_tag = first_badge.find_element(By.CSS_SELECTOR, ".neg-tag .sentiment-val")
        split_bar = first_badge.find_element(By.CSS_SELECTOR, ".sentiment-split-bar")

        assert "%" in pos_tag.text
        assert "%" in neg_tag.text
        assert split_bar.is_displayed()

    def test_quick_feedback_modal_flow(self, authenticated_driver, live_server):
        """Clicking a sentiment badge opens the quick feedback modal, allows posting, and updates sentiment."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()
        feed_page.wait_for_feed_loaded(timeout=10)

        badge = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".story-sentiment-badge"))
        )
        badge.click()

        # Modal should open
        modal_backdrop = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "feedback-modal-backdrop"))
        )
        assert "open" in modal_backdrop.get_attribute("class")

        # Check modal dashboard
        dashboard = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "modal-sentiment-dashboard"))
        )
        assert dashboard.is_displayed()

        pos_pct = driver.find_element(By.ID, "modal-pos-pct")
        assert "Pos" in pos_pct.text or "%" in pos_pct.text

        # Submit a new feedback comment
        textarea = driver.find_element(By.ID, "modal-feedback-input")
        textarea.clear()
        textarea.send_keys("Spectacular scientific innovation! Extremely optimistic regarding the transformative results.")

        submit_btn = driver.find_element(By.ID, "modal-feedback-submit")
        submit_btn.click()

        # Wait for form status to indicate success
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "modal-form-status"), "Feedback posted")
        )
        time.sleep(0.5)

        comments = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, ".feedback-comment-item")
        )
        assert len(comments) >= 1
        assert "Spectacular" in comments[0].text or len(comments[0].text) > 0

        # Close modal
        close_btn = driver.find_element(By.ID, "feedback-modal-close")
        close_btn.click()
        time.sleep(0.4)
        assert "open" not in modal_backdrop.get_attribute("class")

    def test_roundup_feedback_and_sentiment_section(self, authenticated_driver, live_server):
        """Roundup article page renders the full Reader Feedback & Semantic Sentiment Analysis section."""
        driver, _ = authenticated_driver
        feed_page = FeedPage(driver, live_server).open_home()
        feed_page.wait_for_feed_loaded(timeout=10)

        hero_cards = driver.find_elements(*feed_page.HERO_LEAD_CARD)
        if hero_cards:
            hero_cards[0].click()
        else:
            pytest.skip("No hero cards found")

        roundup_page = RoundupPage(driver, live_server)
        assert roundup_page.is_at_roundup()
        assert roundup_page.wait_for_roundup_loaded(timeout=15)

        # Feedback Section
        feedback_section = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "roundup-feedback-section"))
        )
        assert feedback_section.is_displayed()

        # Sentiment Card
        sentiment_card = driver.find_element(By.ID, "roundup-sentiment-card")
        assert sentiment_card.is_displayed()

        pos_rate = driver.find_element(By.ID, "stat-pos-rate")
        assert "%" in pos_rate.text

        # Post a comment on the roundup page
        comment_input = driver.find_element(By.ID, "roundup-comment-input")
        comment_input.send_keys("Remarkable editorial coverage and profound technical depth.")

        submit_btn = driver.find_element(By.ID, "roundup-comment-submit")
        submit_btn.click()

        # Wait for posted comment
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "roundup-form-status"), "Feedback posted")
        )
        time.sleep(0.5)

        roundup_comments = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, ".roundup-comment-card")
        )
        assert len(roundup_comments) >= 1
