/**
 * Roundup (Briefing Synthesis) Page Object Model
 */

const { By } = require('selenium-webdriver');
const BasePage = require('./base.page');

class RoundupPage extends BasePage {
  constructor(driver) {
    super(driver);

    this.ROUNDUP_CONTAINER = By.css('.roundup-view, .briefing-container, #roundup');
    this.SUMMARY_TEXT = By.css('.briefing-summary, .summary-text, .executive-summary');
    this.KEY_TAKEAWAYS = By.css('.key-takeaways li, .takeaway-item');
    this.SOURCES_LIST = By.css('.sources-list, .source-item');
    this.AUDIO_PLAYER = By.css('audio, .audio-player, #tts-player');
    this.SAVE_ROUNDUP_BTN = By.css('#save-roundup, .btn-save-briefing');
    this.GENERATE_NEW_BTN = By.css('#generate-roundup, .btn-generate');
  }

  async openRoundup() {
    await this.navigateTo('/roundup');
    return this;
  }
}

module.exports = RoundupPage;
