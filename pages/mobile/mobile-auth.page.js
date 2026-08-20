/**
 * Mobile Authentication, Feed, Navigation & Settings Page Objects
 */

const { By } = require('selenium-webdriver');
const MobileBasePage = require('./mobile-base.page');

class MobileAuthPage extends MobileBasePage {
  constructor(driver) {
    super(driver);
    this.MOBILE_USERNAME = By.css('input[name="username"], #username');
    this.MOBILE_PASSWORD = By.css('input[name="password"], #password');
    this.MOBILE_LOGIN_BTN = By.css('button[type="submit"], .auth-submit-btn');
  }

  async mobileLogin(username, password) {
    await this.navigateTo('/login');
    await this.typeInto(this.MOBILE_USERNAME, username);
    await this.typeInto(this.MOBILE_PASSWORD, password);
    await this.hideKeyboard();
    await this.clickElement(this.MOBILE_LOGIN_BTN);
  }
}

class MobileFeedPage extends MobileBasePage {
  constructor(driver) {
    super(driver);
    this.MOBILE_CARDS = By.css('.cluster-card, .article-card, article');
    this.PULL_REFRESH_INDICATOR = By.css('.pull-to-refresh, .refresh-spinner');
  }

  async openMobileFeed() {
    await this.navigateTo('/');
    return this;
  }
}

class MobileNavPage extends MobileBasePage {
  constructor(driver) {
    super(driver);
    this.DRAWER_MENU = By.css('.side-drawer, .nav-drawer, #sidebar');
    this.DRAWER_FEED_LINK = By.css('.drawer-link[href="/"], nav a[href="/"]');
    this.DRAWER_SETTINGS_LINK = By.css('.drawer-link[href="/settings"], nav a[href="/settings"]');
  }

  async openDrawer() {
    if (await this.isElementVisible(this.HAMBURGER_MENU)) {
      await this.clickElement(this.HAMBURGER_MENU);
      await this.utils.sleep(300);
    }
  }
}

class MobileSettingsPage extends MobileBasePage {
  constructor(driver) {
    super(driver);
    this.MOBILE_THEME_BTN = By.css('.theme-swatch, #theme-toggle');
  }
}

module.exports = {
  MobileAuthPage,
  MobileFeedPage,
  MobileNavPage,
  MobileSettingsPage
};
