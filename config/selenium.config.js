/**
 * Selenium WebDriver Configuration
 * Supports Chrome, Firefox, and Microsoft Edge in Headed & Headless modes
 */

const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const firefox = require('selenium-webdriver/firefox');
const edge = require('selenium-webdriver/edge');
const appConfig = require('./app.config');
const logger = require('../utilities/logger');

class SeleniumConfig {
  static async createDriver(browserName = appConfig.browser, isHeadless = appConfig.headless) {
    logger.info(`[SeleniumConfig] Initializing WebDriver: Browser=${browserName}, Headless=${isHeadless}`);
    const builder = new Builder();

    switch (browserName.toLowerCase()) {
      case 'firefox': {
        const ffOptions = new firefox.Options();
        if (isHeadless) {
          ffOptions.addArguments('-headless');
        }
        ffOptions.setPreference('dom.webnotifications.enabled', false);
        return builder.forBrowser('firefox').setFirefoxOptions(ffOptions).build();
      }

      case 'edge':
      case 'msedge': {
        const edgeOptions = new edge.Options();
        if (isHeadless) {
          edgeOptions.addArguments('--headless=new');
        }
        edgeOptions.addArguments('--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu');
        return builder.forBrowser('MicrosoftEdge').setEdgeOptions(edgeOptions).build();
      }

      case 'chrome':
      default: {
        const chromeOptions = new chrome.Options();
        if (isHeadless) {
          chromeOptions.addArguments('--headless=new');
        }
        chromeOptions.addArguments(
          '--no-sandbox',
          '--disable-dev-shm-usage',
          '--disable-gpu',
          '--window-size=1920,1080',
          '--disable-extensions',
          '--disable-notifications',
          '--remote-allow-origins=*'
        );
        return builder.forBrowser('chrome').setChromeOptions(chromeOptions).build();
      }
    }
  }
}

module.exports = SeleniumConfig;
