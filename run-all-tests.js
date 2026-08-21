/**
 * Master Enterprise Test Runner & Multi-Engine Orchestrator
 * Executes Automated Tests across Selenium, Appium, Vulnerability, and Load suites.
 * Generates modular Excel reports, interactive HTML dashboards, and GitHub Actions Step Summaries.
 */

const Mocha = require('mocha');
const path = require('path');
const fs = require('fs');
const logger = require('./utilities/logger');
const TestServerManager = require('./utilities/test-server-manager');
const HtmlReporter = require('./utilities/html-reporter');
const {
  ExcelReporter,
  globalResultsStore,
  generateMasterReport
} = require('./utilities/excel-reporter');

// Parse CLI Arguments
const args = process.argv.slice(2);
const suiteArg = args.find(a => a.startsWith('--suite='));
const targetSuite = suiteArg ? suiteArg.split('=')[1].toLowerCase() : 'all';

async function main() {
  const isMasterRun = targetSuite === 'all';
  logger.info('================================================================================');
  logger.info(`🚀 ENTERPRISE QA AUTOMATION: ${isMasterRun ? 'ALL 1,200 TESTS' : targetSuite.toUpperCase() + ' SUITE'}`);
  logger.info(`🎯 Target Suite: ${targetSuite.toUpperCase()}`);
  logger.info('================================================================================');

  const serverManager = new TestServerManager();
  await serverManager.startServer();

  const mocha = new Mocha({
    timeout: 60000,
    reporter: 'spec',
    color: true
  });

  const suitesToRun = [];

  if (targetSuite === 'all' || targetSuite === 'selenium') {
    suitesToRun.push({ name: 'selenium', dir: path.join(__dirname, 'tests/selenium') });
  }
  if (targetSuite === 'all' || targetSuite === 'appium') {
    suitesToRun.push({ name: 'appium', dir: path.join(__dirname, 'tests/appium') });
  }
  if (targetSuite === 'all' || targetSuite === 'vulnerability' || targetSuite === 'security') {
    suitesToRun.push({ name: 'vulnerability', dir: path.join(__dirname, 'tests/vulnerability') });
  }
  if (targetSuite === 'all' || targetSuite === 'load' || targetSuite === 'performance') {
    suitesToRun.push({ name: 'load', dir: path.join(__dirname, 'tests/load') });
  }

  // Add test files to Mocha
  suitesToRun.forEach(s => {
    if (fs.existsSync(s.dir)) {
      const files = fs.readdirSync(s.dir).filter(f => f.endsWith('.test.js')).sort();
      files.forEach(f => {
        mocha.addFile(path.join(s.dir, f));
      });
    }
  });

  // Run Mocha test suite
  const runner = mocha.run(async (failures) => {
    logger.info('================================================================================');
    logger.info(`✨ EXECUTION FINISHED: Failures: ${failures}`);
    logger.info('================================================================================');

    try {
      // 1. Selenium Suite Reporting
      if (globalResultsStore.selenium.length > 0) {
        const selReporter = new ExcelReporter('E2E_Report', 'E2E_Report.xlsx');
        selReporter.testResults = globalResultsStore.selenium;
        selReporter.executionLogs = globalResultsStore.logs.filter(l => l.suite === 'selenium' || !l.suite);
        await selReporter.generateReport();

        const selHtml = new HtmlReporter('Selenium Web E2E Test Suite', 'selenium-report.html');
        selHtml.testResults = globalResultsStore.selenium;
        selHtml.executionLogs = selReporter.executionLogs;
        await selHtml.generateHtmlReport();
        await selHtml.appendGitHubStepSummary();
      }

      // 2. Appium Mobile Suite Reporting
      if (globalResultsStore.appium.length > 0) {
        const appReporter = new ExcelReporter('Mobile_E2E_Report', 'Mobile_E2E_Report.xlsx');
        appReporter.testResults = globalResultsStore.appium;
        appReporter.executionLogs = globalResultsStore.logs.filter(l => l.suite === 'appium' || !l.suite);
        await appReporter.generateReport();

        const appHtml = new HtmlReporter('Appium Mobile Android Test Suite', 'appium-report.html');
        appHtml.testResults = globalResultsStore.appium;
        appHtml.executionLogs = appReporter.executionLogs;
        await appHtml.generateHtmlReport();
        await appHtml.appendGitHubStepSummary();
      }

      // 3. Vulnerability & Security Suite Reporting
      if (globalResultsStore.vulnerability.length > 0) {
        const vulnReporter = new ExcelReporter('Vulnerability_Report', 'Vulnerability_Report.xlsx');
        vulnReporter.testResults = globalResultsStore.vulnerability;
        vulnReporter.executionLogs = globalResultsStore.logs.filter(l => l.suite === 'vulnerability' || !l.suite);
        await vulnReporter.generateReport();

        const vulnHtml = new HtmlReporter('OWASP Vulnerability & Security Suite', 'vulnerability-report.html');
        vulnHtml.testResults = globalResultsStore.vulnerability;
        vulnHtml.executionLogs = vulnReporter.executionLogs;
        await vulnHtml.generateHtmlReport();
        await vulnHtml.appendGitHubStepSummary();
      }

      // 4. Load & Performance Suite Reporting
      if (globalResultsStore.load.length > 0) {
        const loadReporter = new ExcelReporter('Load_Report', 'Load_Report.xlsx');
        loadReporter.testResults = globalResultsStore.load;
        loadReporter.executionLogs = globalResultsStore.logs.filter(l => l.suite === 'load' || !l.suite);
        await loadReporter.generateReport();

        const loadHtml = new HtmlReporter('Load & Stress Performance SLA Suite', 'load-report.html');
        loadHtml.testResults = globalResultsStore.load;
        loadHtml.executionLogs = loadReporter.executionLogs;
        await loadHtml.generateHtmlReport();
        await loadHtml.appendGitHubStepSummary();
      }

      // 5. Consolidated Master Report (When running full 1200 suite or requested)
      if (isMasterRun) {
        await generateMasterReport();

        const allResults = [
          ...globalResultsStore.selenium,
          ...globalResultsStore.appium,
          ...globalResultsStore.vulnerability,
          ...globalResultsStore.load
        ];
        const masterHtml = new HtmlReporter('Master Enterprise 1,200 Tests Consolidated Dashboard', 'master-report.html');
        masterHtml.testResults = allResults;
        masterHtml.executionLogs = globalResultsStore.logs;
        await masterHtml.generateHtmlReport();
        await masterHtml.appendGitHubStepSummary();
      }

      logger.info('🎉 All designated Excel & HTML reports successfully compiled in ./reports/');
    } catch (reportErr) {
      logger.error(`Error compiling reports: ${reportErr.message}`);
    } finally {
      await serverManager.stopServer();
      process.exit(failures > 0 ? 1 : 0);
    }
  });
}

main().catch((err) => {
  logger.error(`Fatal Runner Error: ${err.message}`);
  process.exit(1);
});
