/**
 * Main Feed Page Object Model
 */

const { By } = require('selenium-webdriver');
const BasePage = require('./base.page');
const logger = require('../utilities/logger');

class FeedPage extends BasePage {
  constructor(driver) {
    super(driver);

    // Feed Locators
    this.FEED_CONTAINER = By.css('.feed-container, #feed, main, .articles-grid');
    this.ARTICLE_CARDS = By.css('.cluster-card, .article-card, .news-item, article');
    this.SEARCH_INPUT = By.css('#search-input, input[name="q"], input[type="search"], .search-box input');
    this.SEARCH_SUBMIT = By.css('#search-btn, button[type="submit"], .search-box button');
    this.SYNTHESIZE_BTN = By.css('#synthesize-btn, [data-action="synthesize"], .btn-synthesize');
    this.CATEGORY_PILLS = By.css('.category-pill, .tag, .filter-chip, [data-category]');
    this.BOOKMARK_TOGGLE_BTN = By.css('.bookmark-btn, [data-action="bookmark"], .btn-bookmark');
    this.PAGINATION_NEXT = By.css('.pagination-next, [aria-label="Next page"], .btn-next');
    this.LOADING_SPINNER = By.css('.spinner, .loading-indicator, #loading');
  }

  async openFeed() {
    await this.navigateTo('/');
    return this;
  }

  async getArticleCardsCount() {
    try {
      const elements = await this.driver.findElements(this.ARTICLE_CARDS);
      return elements.length;
    } catch (e) {
      return 0;
    }
  }

  async searchNews(query) {
    logger.info(`[FeedPage] Searching for: "${query}"`);
    if (await this.isElementVisible(this.SEARCH_INPUT)) {
      await this.typeInto(this.SEARCH_INPUT, query);
      if (await this.isElementVisible(this.SEARCH_SUBMIT)) {
        await this.clickElement(this.SEARCH_SUBMIT);
      } else {
        await this.driver.findElement(this.SEARCH_INPUT).sendKeys('\n');
      }
      await this.utils.sleep(400);
    }
  }

  async clickFirstArticle() {
    const cards = await this.driver.findElements(this.ARTICLE_CARDS);
    if (cards.length > 0) {
      await cards[0].click();
      await this.utils.sleep(300);
    }
  }

  async toggleFirstBookmark() {
    if (await this.isElementVisible(this.BOOKMARK_TOGGLE_BTN)) {
      await this.clickElement(this.BOOKMARK_TOGGLE_BTN);
      await this.utils.sleep(300);
    }
  }
}

module.exports = FeedPage;
