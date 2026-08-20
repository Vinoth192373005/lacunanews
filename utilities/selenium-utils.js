/**
 * Selenium Utility Layer
 * Provides reusable methods for explicit waits, scrolling, JS execution,
 * window switching, alert handling, retries, and failure screenshots.
 */

const { until, By, Key } = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');
const logger = require('./logger');
const appConfig = require('../config/app.config');

class SeleniumUtils {
  constructor(driver) {
    this.driver = driver;
    this.timeout = appConfig.defaultTimeout;
  }

  /**
   * Explicit wait for element to be located and visible
   */
  async waitForVisible(locator, timeoutMs = this.timeout) {
    logger.debug(`[Wait] Waiting for element visible: ${locator}`);
    const el = await this.driver.wait(until.elementLocated(locator), timeoutMs);
    await this.driver.wait(until.elementIsVisible(el), timeoutMs);
    return el;
  }

  /**
   * Explicit wait for element to be clickable
   */
  async waitForClickable(locator, timeoutMs = this.timeout) {
    logger.debug(`[Wait] Waiting for element clickable: ${locator}`);
    const el = await this.waitForVisible(locator, timeoutMs);
    await this.driver.wait(until.elementIsEnabled(el), timeoutMs);
    return el;
  }

  /**
   * Wait for element to disappear / become invisible
   */
  async waitForInvisible(locator, timeoutMs = this.timeout) {
    logger.debug(`[Wait] Waiting for element invisible: ${locator}`);
    try {
      const el = await this.driver.findElement(locator);
      await this.driver.wait(until.elementIsNotVisible(el), timeoutMs);
      return true;
    } catch (e) {
      return true; // If element doesn't exist, it is invisible
    }
  }

  /**
   * Safe Click with retry and scroll into view fallback
   */
  async safeClick(locator, timeoutMs = this.timeout) {
    try {
      const el = await this.waitForClickable(locator, timeoutMs);
      await this.scrollIntoView(locator);
      await el.click();
    } catch (error) {
      logger.warn(`[Click] Standard click failed for ${locator}, attempting JavaScript click`);
      await this.jsClick(locator);
    }
  }

  /**
   * Safe Type / SendKeys
   */
  async safeType(locator, text, clearFirst = true, timeoutMs = this.timeout) {
    const el = await this.waitForVisible(locator, timeoutMs);
    if (clearFirst) {
      await el.sendKeys(Key.chord(Key.CONTROL, 'a'), Key.BACK_SPACE);
      try {
        await el.clear();
      } catch (e) {
        // Ignore if clear unsupported
      }
    }
    await el.sendKeys(text);
  }

  /**
   * Get element text
   */
  async getText(locator, timeoutMs = this.timeout) {
    const el = await this.waitForVisible(locator, timeoutMs);
    return await el.getText();
  }

  /**
   * Get element attribute
   */
  async getAttribute(locator, attributeName, timeoutMs = this.timeout) {
    const el = await this.waitForVisible(locator, timeoutMs);
    return await el.getAttribute(attributeName);
  }

  /**
   * Check if element is displayed
   */
  async isDisplayed(locator) {
    try {
      const elements = await this.driver.findElements(locator);
      if (elements.length === 0) return false;
      return await elements[0].isDisplayed();
    } catch (e) {
      return false;
    }
  }

  /**
   * Execute JavaScript on page
   */
  async executeScript(script, ...args) {
    return await this.driver.executeScript(script, ...args);
  }

  /**
   * JavaScript click
   */
  async jsClick(locator) {
    const el = await this.driver.findElement(locator);
    await this.driver.executeScript('arguments[0].click();', el);
  }

  /**
   * Scroll element into view
   */
  async scrollIntoView(locator) {
    try {
      const el = await this.driver.findElement(locator);
      await this.driver.executeScript('arguments[0].scrollIntoView({ behavior: "smooth", block: "center" });', el);
      await this.sleep(200);
    } catch (e) {
      // Ignore scroll error
    }
  }

  /**
   * Scroll to top of page
   */
  async scrollToTop() {
    await this.driver.executeScript('window.scrollTo(0, 0);');
  }

  /**
   * Scroll to bottom of page
   */
  async scrollToBottom() {
    await this.driver.executeScript('window.scrollTo(0, document.body.scrollHeight);');
  }

  /**
   * Handle JavaScript alert
   */
  async handleAlert(accept = true) {
    try {
      await this.driver.wait(until.alertIsPresent(), 3000);
      const alert = await this.driver.switchTo().alert();
      const text = await alert.getText();
      if (accept) {
        await alert.accept();
      } else {
        await alert.dismiss();
      }
      return text;
    } catch (e) {
      return null;
    }
  }

  /**
   * Capture Failure Screenshot
   */
  async captureScreenshot(testName) {
    try {
      const sanitizedName = testName.replace(/[^a-zA-Z0-9_-]/g, '_');
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const dir = path.resolve(process.cwd(), appConfig.screenshotsDir);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      const filename = `${sanitizedName}_${timestamp}.png`;
      const filepath = path.join(dir, filename);
      const image = await this.driver.takeScreenshot();
      fs.writeFileSync(filepath, image, 'base64');
      logger.info(`[Screenshot] Captured: ${filepath}`);
      return filepath;
    } catch (err) {
      logger.error(`[Screenshot] Failed to capture screenshot: ${err.message}`);
      return null;
    }
  }

  /**
   * Get Browser Console Logs
   */
  async getBrowserLogs() {
    try {
      const logs = await this.driver.manage().logs().get('browser');
      return logs.map(l => `[${l.level.name}] ${l.message}`).join('\n');
    } catch (e) {
      return 'Console logs unavailable for this driver';
    }
  }

  /**
   * Sleep helper
   */
  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = SeleniumUtils;
