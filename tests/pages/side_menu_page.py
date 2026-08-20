"""
Page Object for the Pop-up Side Drawer (Settings & Account).
"""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.base_page import BasePage


class SideMenuPage(BasePage):
    """Page Object covering the settings and account drawer."""

    # Selectors
    TOGGLE_BTN = (By.CSS_SELECTOR, "[data-testid='side-menu-toggle-btn']")
    DRAWER = (By.CSS_SELECTOR, "[data-testid='side-menu-drawer']")
    BACKDROP = (By.CSS_SELECTOR, "[data-testid='side-menu-backdrop']")
    CLOSE_BTN = (By.CSS_SELECTOR, "[data-testid='side-menu-close-btn']")

    # Account Section
    USERNAME = (By.CSS_SELECTOR, "[data-testid='side-account-username']")
    STAT_READ_COUNT = (By.CSS_SELECTOR, "[data-testid='stat-read-count']")
    STAT_REGION_CODE = (By.CSS_SELECTOR, "[data-testid='stat-region-code']")
    LOGOUT_BTN = (By.CSS_SELECTOR, "[data-testid='side-logout-btn']")

    # History Section
    HISTORY_LIST = (By.CSS_SELECTOR, "[data-testid='side-history-list']")
    HISTORY_CARDS = (By.CSS_SELECTOR, "[data-testid='side-history-card']")
    CLEAR_HISTORY_BTN = (By.CSS_SELECTOR, "[data-testid='side-clear-history-btn']")

    # Themes
    THEME_DEFAULT = (By.CSS_SELECTOR, "[data-testid='theme-option-default']")
    THEME_PITCH_BLACK = (By.CSS_SELECTOR, "[data-testid='theme-option-pitch-black']")
    THEME_PALETTE_ONE = (By.CSS_SELECTOR, "[data-testid='theme-option-palette-one']")
    THEME_PALETTE_TWO = (By.CSS_SELECTOR, "[data-testid='theme-option-palette-two']")
    THEME_PALETTE_THREE = (By.CSS_SELECTOR, "[data-testid='theme-option-palette-three']")

    def open(self) -> "SideMenuPage":
        """Open the side menu drawer."""
        if not self.is_open():
            self.click(*self.TOGGLE_BTN)
            self.wait_for(lambda d: "open" in (d.find_element(*self.DRAWER).get_attribute("class") or ""))
        return self

    def close(self) -> None:
        """Close the side menu drawer via its close button."""
        if self.is_open():
            self.click(*self.CLOSE_BTN)
            self.wait_for(lambda d: "open" not in (d.find_element(*self.DRAWER).get_attribute("class") or ""))

    def close_via_backdrop(self) -> None:
        """Close the side menu drawer by clicking the backdrop overlay."""
        if self.is_open():
            # Use JS click to ensure click reaches the backdrop overlay
            backdrop = self.find_present(*self.BACKDROP)
            self.driver.execute_script("arguments[0].click();", backdrop)
            self.wait_for(lambda d: "open" not in (d.find_element(*self.DRAWER).get_attribute("class") or ""))

    def close_via_escape(self) -> None:
        """Close the side menu drawer by sending the Escape key."""
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        self.wait_for(lambda d: "open" not in (d.find_element(*self.DRAWER).get_attribute("class") or ""))

    def is_open(self) -> bool:
        """Check if drawer is currently open."""
        try:
            drawer = self.find_present(*self.DRAWER, timeout=2)
            classes = drawer.get_attribute("class") or ""
            return "open" in classes
        except Exception:
            return False

    def get_username(self) -> str:
        """Get the username displayed in the account section."""
        return self.get_text(*self.USERNAME)

    def get_read_count(self) -> str:
        """Get the roundups read count in stats."""
        return self.get_text(*self.STAT_READ_COUNT)

    def get_region_code(self) -> str:
        """Get the feed region code in stats."""
        return self.get_text(*self.STAT_REGION_CODE)

    def select_theme(self, theme_name: str) -> None:
        """Select a theme option (e.g. 'default', 'pitch-black', 'palette-one', etc.)."""
        theme_map = {
            "default": self.THEME_DEFAULT,
            "light": self.THEME_DEFAULT,
            "pitch-black": self.THEME_PITCH_BLACK,
            "dark": self.THEME_PITCH_BLACK,
            "palette-one": self.THEME_PALETTE_ONE,
            "blue": self.THEME_PALETTE_ONE,
            "palette-two": self.THEME_PALETTE_TWO,
            "red": self.THEME_PALETTE_TWO,
            "palette-three": self.THEME_PALETTE_THREE,
            "gold": self.THEME_PALETTE_THREE,
        }
        loc = theme_map.get(theme_name.lower(), (By.CSS_SELECTOR, f"[data-testid='theme-option-{theme_name.lower()}']"))
        self.click(*loc)

    def get_active_body_theme(self) -> str:
        """Get current data-theme attribute on <body>."""
        return self.get_body_attribute("data-theme")

    def select_region(self, code: str) -> None:
        """Select a region option button (e.g. 'us', 'gb', 'in')."""
        loc = (By.CSS_SELECTOR, f"[data-testid='region-option-{code.lower()}']")
        self.click(*loc)

    def get_history_items(self) -> List[str]:
        """Get titles of all reading history items in the drawer."""
        elements = self.find_all(*self.HISTORY_CARDS)
        return [el.text.strip() for el in elements if el.text.strip()]

    def clear_history(self, accept_alert: bool = True) -> None:
        """Click clear reading history and handle the browser confirmation dialog."""
        self.click(*self.CLEAR_HISTORY_BTN)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            if accept_alert:
                alert.accept()
            else:
                alert.dismiss()
        except Exception:
            pass

    def logout(self, timeout: int = 10) -> None:
        """Click the logout button inside the side drawer and wait for redirect."""
        self.click(*self.LOGOUT_BTN)
        self.wait_for(lambda d: "/login" in d.current_url, timeout=timeout)
