/**
 * Master Enterprise Test Runner & Excel Orchestrator
 * Executes all 1,200 Automated Tests across Selenium, Appium, Vulnerability, and Load suites.
 * Generates individual and consolidated Master Excel Reports.
 */

const Mocha = require('mocha');
const path = require('path');
const fs = require('fs');
const logger = require('./utilities/logger');
const TestServerManager = require('./utilities/test-server-manager');
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
  logger.info('================================================================================');
  logger.info('🚀 STARTING ENTERPRISE MULTI-ENGINE QA AUTOMATION (1,200 TEST CASES)');
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
      // 1. Generate Individual Excel Reports
      if (globalResultsStore.selenium.length > 0) {
        const selReporter = new ExcelReporter('E2E_Report', 'E2E_Report.xlsx');
        selReporter.testResults = globalResultsStore.selenium;
        selReporter.executionLogs = globalResultsStore.logs.filter(l => l.remarks.includes('Authentication') || l.remarks.includes('Form Validation') || l.remarks.includes('UI Components') || l.remarks.includes('Navigation') || l.remarks.includes('Business Workflows') || l.remarks.includes('Settings & Preferences'));
        await selReporter.generateReport();
      }

      if (globalResultsStore.appium.length > 0) {
        const appReporter = new ExcelReporter('Mobile_E2E_Report', 'Mobile_E2E_Report.xlsx');
        appReporter.testResults = globalResultsStore.appium;
        appReporter.executionLogs = globalResultsStore.logs.filter(l => l.remarks.includes('App Lifecycle') || l.remarks.includes('Mobile Auth') || l.remarks.includes('Touch Gestures') || l.remarks.includes('Mobile Forms') || l.remarks.includes('Mobile Navigation') || l.remarks.includes('Mobile AI & Workflows'));
        await appReporter.generateReport();
      }

      if (globalResultsStore.vulnerability.length > 0) {
        const vulnReporter = new ExcelReporter('Vulnerability_Report', 'Vulnerability_Report.xlsx');
        vulnReporter.testResults = globalResultsStore.vulnerability;
        vulnReporter.executionLogs = globalResultsStore.logs.filter(l => l.remarks.includes('Injection') || l.remarks.includes('Auth & Session') || l.remarks.includes('CORS') || l.remarks.includes('IDOR') || l.remarks.includes('Sanitization') || l.remarks.includes('DoS'));
        await vulnReporter.generateReport();
      }

      if (globalResultsStore.load.length > 0) {
        const loadReporter = new ExcelReporter('Load_Report', 'Load_Report.xlsx');
        loadReporter.testResults = globalResultsStore.load;
        loadReporter.executionLogs = globalResultsStore.logs.filter(l => l.remarks.includes('Baseline') || l.remarks.includes('Concurrency') || l.remarks.includes('Stress') || l.remarks.includes('Endurance') || l.remarks.includes('AI Compute') || l.remarks.includes('DB Transactions'));
        await loadReporter.generateReport();
      }

      // 2. Generate Consolidated Master 1200-Test Report
      await generateMasterReport();

      logger.info('🎉 All Excel Reports successfully compiled in ./reports/excel/');
    } catch (reportErr) {
      logger.error(`Error compiling Excel reports: ${reportErr.message}`);
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
