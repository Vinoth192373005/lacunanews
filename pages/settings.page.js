/**
 * Settings and Preferences Page Object Model
 */

const { By } = require('selenium-webdriver');
const BasePage = require('./base.page');

class SettingsPage extends BasePage {
  constructor(driver) {
    super(driver);

    this.SETTINGS_TITLE = By.css('h1, .page-title, #settings-title');
    this.USERNAME_DISPLAY = By.css('#user-name-display, .account-username, .user-badge');
    this.READ_COUNT_STAT = By.css('#stat-read-count, [data-stat="read"]');
    this.BOOKMARKS_COUNT_STAT = By.css('#stat-bookmarks-count, [data-stat="bookmarks"]');
    this.INTEREST_INPUT = By.css('#interest-input, input[name="interest"]');
    this.ADD_INTEREST_BTN = By.css('#add-interest-btn, button[data-action="add-interest"]');
    this.INTEREST_TAGS = By.css('.interest-tag, .badge-interest, .topic-pill');
    this.REMOVE_INTEREST_BTNS = By.css('.btn-remove-interest, [data-action="remove-interest"]');
    this.THEME_SWATCHES = By.css('.theme-swatch, [data-theme-name]');
    this.REGION_SELECT = By.css('#region-preference, select[name="region_pref"]');
    this.BACK_TO_FEED_BTN = By.css('a[href="/"], .back-to-feed, #back-btn');
  }

  async openSettings() {
    await this.navigateTo('/settings');
    return this;
  }

  async addInterest(topic) {
    if (await this.isElementVisible(this.INTEREST_INPUT)) {
      await this.typeInto(this.INTEREST_INPUT, topic);
      if (await this.isElementVisible(this.ADD_INTEREST_BTN)) {
        await this.clickElement(this.ADD_INTEREST_BTN);
      } else {
        await this.driver.findElement(this.INTEREST_INPUT).sendKeys('\n');
      }
      await this.utils.sleep(300);
    }
  }

  async getInterestNames() {
    try {
      const elements = await this.driver.findElements(this.INTEREST_TAGS);
      const names = [];
      for (const el of elements) {
        names.push(await el.getText());
      }
      return names;
    } catch (e) {
      return [];
    }
  }
}

module.exports = SettingsPage;
