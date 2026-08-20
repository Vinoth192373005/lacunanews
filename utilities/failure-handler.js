/**
 * Failure Handler Utility
 * Intercepts test failures, captures screenshots, browser console logs,
 * current URL, failure reasons, and stack traces.
 */

const path = require('path');
const fs = require('fs');
const logger = require('./logger');
const appConfig = require('../config/app.config');

class FailureHandler {
  static async handleFailure(testContext, driver) {
    const testTitle = testContext.currentTest ? testContext.currentTest.fullTitle() : (testContext.title || 'Unknown_Test');
    const failureReason = testContext.currentTest && testContext.currentTest.err ? testContext.currentTest.err.message : 'Unknown Failure';
    const stackTrace = testContext.currentTest && testContext.currentTest.err ? testContext.currentTest.err.stack : '';

    logger.error(`[FailureHandler] Test Failed: "${testTitle}"`);
    logger.error(`[FailureHandler] Reason: ${failureReason}`);

    let currentUrl = 'N/A';
    let screenshotPath = 'N/A';
    let browserLogs = 'N/A';

    if (driver) {
      try {
        currentUrl = await driver.getCurrentUrl();
      } catch (e) {
        currentUrl = 'Unable to get URL';
      }

      try {
        const sanitizedTitle = testTitle.replace(/[^a-zA-Z0-9_-]/g, '_');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const failureDir = path.resolve(process.cwd(), appConfig.screenshotsDir);
        if (!fs.existsSync(failureDir)) {
          fs.mkdirSync(failureDir, { recursive: true });
        }
        screenshotPath = path.join(failureDir, `FAIL_${sanitizedTitle}_${timestamp}.png`);
        const imageBase64 = await driver.takeScreenshot();
        fs.writeFileSync(screenshotPath, imageBase64, 'base64');
        logger.info(`[FailureHandler] Saved failure screenshot to: ${screenshotPath}`);
      } catch (e) {
        logger.warn(`[FailureHandler] Screenshot capture failed: ${e.message}`);
      }

      try {
        const logs = await driver.manage().logs().get('browser');
        browserLogs = logs.map(l => `[${l.level.name}] ${l.message}`).join('\n');
      } catch (e) {
        browserLogs = 'Console logs not available';
      }
    }

    const failureRecord = {
      testName: testTitle,
      failureReason,
      screenshotPath,
      url: currentUrl,
      browserLogs,
      stackTrace,
      timestamp: new Date().toISOString()
    };

    // Append to failures.json for Excel reporter
    const failureLogPath = path.resolve(process.cwd(), 'reports/failures/failures_summary.json');
    try {
      let failures = [];
      if (fs.existsSync(failureLogPath)) {
        failures = JSON.parse(fs.readFileSync(failureLogPath, 'utf8'));
      }
      failures.push(failureRecord);
      fs.writeFileSync(failureLogPath, JSON.stringify(failures, null, 2), 'utf8');
    } catch (e) {
      logger.error(`[FailureHandler] Could not record failure json: ${e.message}`);
    }

    return failureRecord;
  }
}

module.exports = FailureHandler;
