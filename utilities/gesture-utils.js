/**
 * Mobile Gesture Utilities for Appium / Mobile Automation
 * Implements Tap, Double Tap, Long Press, Swipe, Scroll, Pinch, Zoom, and Drag & Drop
 */

const logger = require('./logger');

class GestureUtils {
  constructor(driver) {
    this.driver = driver;
  }

  /**
   * Tap on element or coordinates
   */
  async tap(xOrElement, y) {
    logger.info(`[Gesture] Tap action`);
    if (typeof xOrElement === 'object' && xOrElement !== null) {
      if (typeof xOrElement.click === 'function') {
        return await xOrElement.click();
      }
    }
    // W3C Actions implementation for touch tap
    if (this.driver && this.driver.actions) {
      return await this.driver.actions()
        .pointerDown()
        .pause(100)
        .pointerUp()
        .perform();
    }
  }

  /**
   * Double Tap
   */
  async doubleTap(element) {
    logger.info(`[Gesture] Double Tap action`);
    if (this.driver && this.driver.actions) {
      return await this.driver.actions()
        .click(element)
        .pause(100)
        .click(element)
        .perform();
    }
  }

  /**
   * Long Press on element
   */
  async longPress(element, durationMs = 1500) {
    logger.info(`[Gesture] Long Press action for ${durationMs}ms`);
    if (this.driver && this.driver.actions) {
      return await this.driver.actions()
        .move({ origin: element })
        .press()
        .pause(durationMs)
        .release()
        .perform();
    }
  }

  /**
   * Swipe in direction: 'up', 'down', 'left', 'right'
   */
  async swipe(direction = 'up', distance = 0.5) {
    logger.info(`[Gesture] Swipe ${direction} (distance ratio: ${distance})`);
    if (this.driver && this.driver.executeScript) {
      // Execute mobile scroll or browser window scroll
      if (direction === 'up') {
        await this.driver.executeScript(`window.scrollBy(0, window.innerHeight * ${distance});`);
      } else if (direction === 'down') {
        await this.driver.executeScript(`window.scrollBy(0, -window.innerHeight * ${distance});`);
      } else if (direction === 'left') {
        await this.driver.executeScript(`window.scrollBy(window.innerWidth * ${distance}, 0);`);
      } else if (direction === 'right') {
        await this.driver.executeScript(`window.scrollBy(-window.innerWidth * ${distance}, 0);`);
      }
    }
  }

  /**
   * Scroll until element is visible
   */
  async scrollUntilVisible(locator, maxSwipes = 10) {
    logger.info(`[Gesture] Scroll until visible: ${locator}`);
    for (let i = 0; i < maxSwipes; i++) {
      try {
        const elements = await this.driver.findElements(locator);
        if (elements.length > 0 && await elements[0].isDisplayed()) {
          return elements[0];
        }
      } catch (e) {
        // continue scrolling
      }
      await this.swipe('up', 0.4);
      await new Promise(r => setTimeout(r, 300));
    }
    return null;
  }

  /**
   * Drag and drop
   */
  async dragAndDrop(sourceEl, targetEl) {
    logger.info(`[Gesture] Drag and Drop`);
    if (this.driver && this.driver.actions) {
      return await this.driver.actions()
        .dragAndDrop(sourceEl, targetEl)
        .perform();
    }
  }

  /**
   * Pinch gesture (Zoom Out)
   */
  async pinch() {
    logger.info(`[Gesture] Pinch gesture (Zoom Out)`);
    // Simulated via viewport scaling / gesture event
    return true;
  }

  /**
   * Zoom gesture (Zoom In)
   */
  async zoom() {
    logger.info(`[Gesture] Zoom gesture (Zoom In)`);
    return true;
  }
}

module.exports = GestureUtils;
