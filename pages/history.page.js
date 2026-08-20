/**
 * Reading History Page Object Model
 */

const { By } = require('selenium-webdriver');
const BasePage = require('./base.page');

class HistoryPage extends BasePage {
  constructor(driver) {
    super(driver);

    this.HISTORY_ITEMS = By.css('.history-item, .history-card, tr.history-row');
    this.CLEAR_ALL_BTN = By.css('#clear-history, .btn-clear-history, [data-action="clear-history"]');
    this.SEARCH_HISTORY_INPUT = By.css('#history-search, input[name="history_query"]');
    this.EMPTY_STATE = By.css('.empty-state, .no-history, #empty-history');
    this.REMOVE_ITEM_BTN = By.css('.btn-remove-history, [data-action="remove-history"]');
  }

  async openHistory() {
    await this.navigateTo('/history');
    return this;
  }

  async getHistoryItemsCount() {
    try {
      const items = await this.driver.findElements(this.HISTORY_ITEMS);
      return items.length;
    } catch (e) {
      return 0;
    }
  }

  async clearAllHistory() {
    if (await this.isElementVisible(this.CLEAR_ALL_BTN)) {
      await this.clickElement(this.CLEAR_ALL_BTN);
      await this.utils.handleAlert(true);
      await this.utils.sleep(400);
    }
  }
}

module.exports = HistoryPage;
