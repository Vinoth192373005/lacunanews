/**
 * Base Page Object Model Class
 * Common methods for navigation, assertions, wait wrappers, and utilities
 */

const { By } = require('selenium-webdriver');
const SeleniumUtils = require('../utilities/selenium-utils');
const appConfig = require('../config/app.config');
const logger = require('../utilities/logger');

class BasePage {
  constructor(driver, baseUrl = appConfig.baseUrl) {
    this.driver = driver;
    this.baseUrl = baseUrl;
    this.utils = new SeleniumUtils(driver);

    // Common Header / Navigation Locators
    this.BRAND_LOGO = By.css('a[href="/"], .brand, .logo');
    this.SETTINGS_NAV_BTN = By.css('a[href="/settings"], [data-testid="nav-settings"], #nav-settings');
    this.HISTORY_NAV_BTN = By.css('a[href="/history"], [data-testid="nav-history"], #nav-history');
    this.BOOKMARKS_NAV_BTN = By.css('a[href="/bookmarks"], [data-testid="nav-bookmarks"], #nav-bookmarks');
    this.ROUNDUP_NAV_BTN = By.css('a[href="/roundup"], [data-testid="nav-roundup"], #nav-roundup');
    this.LOGIN_NAV_BTN = By.css('a[href="/login"], [data-testid="nav-login"], #nav-login');
    this.LOGOUT_BTN = By.css('form[action="/logout"] button, #logout-btn, .logout-btn');
    this.TOAST_CONTAINER = By.css('.toast, .toast-container, .alert-notification, .notification');
    this.REGION_DROPDOWN = By.css('#region-select, select[name="region"], .region-selector');
    this.THEME_TOGGLE = By.css('#theme-toggle, .theme-toggle-btn, [data-theme-toggle]');
  }

  async navigateTo(path = '') {
    const targetUrl = `${this.baseUrl}${path.startsWith('/') ? path : '/' + path}`;
    logger.info(`[Navigation] Navigating to: ${targetUrl}`);
    await this.driver.get(targetUrl);
    await this.utils.sleep(300);
  }

  async getTitle() {
    return await this.driver.getTitle();
  }

  async getCurrentUrl() {
    return await this.driver.getCurrentUrl();
  }

  async refreshPage() {
    logger.info(`[Navigation] Refreshing page`);
    await this.driver.navigate().refresh();
    await this.utils.sleep(300);
  }

  async goBack() {
    logger.info(`[Navigation] Browser back`);
    await this.driver.navigate().back();
    await this.utils.sleep(300);
  }

  async goForward() {
    logger.info(`[Navigation] Browser forward`);
    await this.driver.navigate().forward();
    await this.utils.sleep(300);
  }

  async isElementVisible(locator) {
    return await this.utils.isDisplayed(locator);
  }

  async getElementText(locator) {
    return await this.utils.getText(locator);
  }

  async clickElement(locator) {
    return await this.utils.safeClick(locator);
  }

  async typeInto(locator, text, clearFirst = true) {
    return await this.utils.safeType(locator, text, clearFirst);
  }

  async getActiveTheme() {
    return await this.driver.executeScript("return document.body.getAttribute('data-theme') || document.documentElement.getAttribute('data-theme') || '';");
  }

  async takeScreenshot(name) {
    return await this.utils.captureScreenshot(name);
  }
}

module.exports = BasePage;
