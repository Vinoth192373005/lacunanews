/**
 * Bookmarks Page Object Model
 */

const { By } = require('selenium-webdriver');
const BasePage = require('./base.page');

class BookmarksPage extends BasePage {
  constructor(driver) {
    super(driver);

    this.BOOKMARK_ITEMS = By.css('.bookmark-card, .bookmark-item, .saved-article');
    this.CLEAR_ALL_BTN = By.css('#clear-bookmarks, .btn-clear-bookmarks');
    this.REMOVE_BOOKMARK_BTN = By.css('.btn-remove-bookmark, [data-action="remove-bookmark"]');
    this.CATEGORY_FILTER = By.css('#bookmark-filter, .bookmark-categories');
    this.EMPTY_STATE = By.css('.empty-bookmarks, .no-bookmarks');
  }

  async openBookmarks() {
    await this.navigateTo('/bookmarks');
    return this;
  }

  async getBookmarksCount() {
    try {
      const items = await this.driver.findElements(this.BOOKMARK_ITEMS);
      return items.length;
    } catch (e) {
      return 0;
    }
  }
}

module.exports = BookmarksPage;
