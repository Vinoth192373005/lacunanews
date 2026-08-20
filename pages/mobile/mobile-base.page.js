/**
 * Mobile Base Page Object
 * Extends web base page with touch gestures and mobile viewport helpers
 */

const { By } = require('selenium-webdriver');
const BasePage = require('../base.page');
const GestureUtils = require('../../utilities/gesture-utils');

class MobileBasePage extends BasePage {
  constructor(driver) {
    super(driver);
    this.gestures = new GestureUtils(driver);
    
    // Mobile-specific locators
    this.HAMBURGER_MENU = By.css('.hamburger-menu, #menu-toggle, [aria-label="Open menu"]');
    this.BOTTOM_NAV_BAR = By.css('.bottom-nav, #bottom-navigation, nav.mobile-nav');
    this.SNACKBAR_TOAST = By.css('.snackbar, .toast-mobile, .mobile-alert');
  }

  async setMobileViewport(width = 375, height = 812) {
    if (this.driver && this.driver.manage) {
      await this.driver.manage().window().setRect({ width, height });
    }
  }

  async tapElement(locator) {
    const el = await this.utils.waitForVisible(locator);
    return await this.gestures.tap(el);
  }

  async swipeUp() {
    return await this.gestures.swipe('up');
  }

  async swipeDown() {
    return await this.gestures.swipe('down');
  }

  async hideKeyboard() {
    try {
      if (this.driver.hideKeyboard) {
        await this.driver.hideKeyboard();
      } else {
        await this.driver.executeScript('if (document.activeElement) document.activeElement.blur();');
      }
    } catch (e) {
      // ignore
    }
  }
}

module.exports = MobileBasePage;
