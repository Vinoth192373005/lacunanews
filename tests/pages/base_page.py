"""
Base Page Object for Selenium Tests.
Provides reusable methods for element location, explicit waits, typing, clicking, and assertions.
"""

from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base class for all page objects with common Selenium utilities."""

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def wait_for(self, condition, timeout: int = None):
        """Wait for an expected condition to be met."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(condition)

    def find(self, by: By, locator: str, timeout: int = None) -> WebElement:
        """Find an element waiting for its visibility."""
        return self.wait_for(EC.visibility_of_element_located((by, locator)), timeout=timeout)

    def find_present(self, by: By, locator: str, timeout: int = None) -> WebElement:
        """Find an element present in the DOM (even if not visible)."""
        return self.wait_for(EC.presence_of_element_located((by, locator)), timeout=timeout)

    def find_all(self, by: By, locator: str, timeout: int = None) -> List[WebElement]:
        """Find all elements matching locator."""
        try:
            self.wait_for(EC.presence_of_element_located((by, locator)), timeout=timeout)
            return self.driver.find_elements(by, locator)
        except TimeoutException:
            return []

    def find_by_testid(self, testid: str, timeout: int = None) -> WebElement:
        """Find an element by its data-testid attribute."""
        return self.find(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def find_present_by_testid(self, testid: str, timeout: int = None) -> WebElement:
        """Find an element present in the DOM by its data-testid attribute."""
        return self.find_present(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def find_all_by_testid(self, testid: str, timeout: int = None) -> List[WebElement]:
        """Find all elements by data-testid attribute."""
        return self.find_all(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def click(self, by: By, locator: str, timeout: int = None) -> None:
        """Wait for element to be clickable and click it."""
        element = self.wait_for(EC.element_to_be_clickable((by, locator)), timeout=timeout)
        element.click()

    def click_testid(self, testid: str, timeout: int = None) -> None:
        """Click an element identified by data-testid."""
        self.click(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def type_text(self, by: By, locator: str, text: str, clear: bool = True, timeout: int = None) -> None:
        """Type text into an input element."""
        element = self.find(by, locator, timeout=timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    def type_text_by_testid(self, testid: str, text: str, clear: bool = True, timeout: int = None) -> None:
        """Type text into an input identified by data-testid."""
        self.type_text(By.CSS_SELECTOR, f"[data-testid='{testid}']", text=text, clear=clear, timeout=timeout)

    def get_text(self, by: By, locator: str, timeout: int = None) -> str:
        """Get visible text from an element."""
        element = self.find(by, locator, timeout=timeout)
        return element.text.strip()

    def get_text_by_testid(self, testid: str, timeout: int = None) -> str:
        """Get visible text from element by data-testid."""
        return self.get_text(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def is_visible(self, by: By, locator: str, timeout: int = 2) -> bool:
        """Check if an element is visible on the page."""
        try:
            self.find(by, locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_testid_visible(self, testid: str, timeout: int = 2) -> bool:
        """Check if an element with data-testid is visible."""
        return self.is_visible(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def wait_until_invisible(self, by: By, locator: str, timeout: int = None) -> bool:
        """Wait until an element is not visible or removed from the DOM."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(EC.invisibility_of_element_located((by, locator)))

    def wait_until_testid_invisible(self, testid: str, timeout: int = None) -> bool:
        """Wait until element with data-testid is invisible."""
        return self.wait_until_invisible(By.CSS_SELECTOR, f"[data-testid='{testid}']", timeout=timeout)

    def get_attribute(self, by: By, locator: str, attribute: str, timeout: int = None) -> str:
        """Get attribute value of an element."""
        element = self.find_present(by, locator, timeout=timeout)
        return element.get_attribute(attribute)

    def get_body_attribute(self, attribute: str) -> str:
        """Get attribute value of <body> tag."""
        body = self.driver.find_element(By.TAG_NAME, "body")
        return body.get_attribute(attribute) or ""

    def scroll_into_view(self, element: WebElement) -> None:
        """Scroll an element into view using JavaScript."""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
