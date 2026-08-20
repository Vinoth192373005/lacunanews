/**
 * Universal Test Helper
 * Provides suite registration, result tracking, assertions, and Excel reporting hooks
 */

const { expect } = require('chai');
const { addSuiteResults } = require('../utilities/excel-reporter');
const logger = require('../utilities/logger');

function createSuiteTracker(suiteName, defaultModule = 'General') {
  const results = [];
  const logs = [];

  const runTest = (testId, scenarioName, moduleName, testFn) => {
    it(`[${testId}] ${scenarioName}`, async function () {
      const startTime = new Date();
      let status = 'PASSED';
      let failureReason = '';

      logs.push({
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
        testName: `[${testId}] ${scenarioName}`,
        stepDescription: `Starting execution for scenario: ${scenarioName}`,
        result: 'IN_PROGRESS',
        remarks: `Module: ${moduleName || defaultModule}`
      });

      try {
        await testFn.call(this);
      } catch (err) {
        status = 'FAILED';
        failureReason = err.message || String(err);
        logger.error(`[${testId}] Failure: ${failureReason}`);
        throw err;
      } finally {
        const endTime = new Date();
        const durationSec = ((endTime - startTime) / 1000).toFixed(2);
        
        results.push({
          testId,
          module: moduleName || defaultModule,
          scenarioName,
          browser: suiteName.includes('mobile') || suiteName.includes('appium') ? 'Android UiAutomator2' : 'Chrome (Headless)',
          status,
          startTime: startTime.toISOString().replace('T', ' ').substring(0, 19),
          endTime: endTime.toISOString().replace('T', ' ').substring(0, 19),
          duration: `${durationSec}s`,
          failureReason
        });

        logs.push({
          timestamp: endTime.toISOString().replace('T', ' ').substring(0, 19),
          testName: `[${testId}] ${scenarioName}`,
          stepDescription: `Finished execution with status: ${status}`,
          result: status,
          remarks: failureReason ? `Error: ${failureReason}` : `Completed in ${durationSec}s`
        });
      }
    });
  };

  const flushResults = () => {
    addSuiteResults(suiteName, results, logs);
    return { results, logs };
  };

  return {
    runTest,
    flushResults,
    results,
    logs
  };
}

module.exports = {
  expect,
  createSuiteTracker
};
