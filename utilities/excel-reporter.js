/**
 * ExcelJS Report Generator
 * Generates Enterprise 4-Sheet Excel Workbooks for QA Test Suites
 * Sheet 1: Summary
 * Sheet 2: Test Cases (Styled identically to enterprise specification)
 * Sheet 3: Failed Tests
 * Sheet 4: Execution Logs
 */

const ExcelJS = require('exceljs');
const path = require('path');
const fs = require('fs');
const logger = require('./logger');
const appConfig = require('../config/app.config');

class ExcelReporter {
  constructor(reportTitle = 'E2E_Report', outputFileName = 'E2E_Report.xlsx') {
    this.reportTitle = reportTitle;
    this.outputFileName = outputFileName;
    this.testResults = [];
    this.executionLogs = [];
    this.failedTests = [];
    this.startTime = new Date();
  }

  /**
   * Log a test step into the execution logs collector
   */
  logStep(testName, stepDescription, result = 'PASSED', remarks = '') {
    this.executionLogs.push({
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
      testName,
      stepDescription,
      result,
      remarks
    });
  }

  /**
   * Record a completed test result
   */
  recordResult({
    testId,
    module,
    scenarioName,
    browser = 'Google Chrome',
    status = 'PASSED',
    startTime = new Date(),
    endTime = new Date(),
    duration = '0.05s',
    failureReason = '',
    screenshotPath = '',
    url = ''
  }) {
    const resultObj = {
      testId,
      module,
      scenarioName,
      browser,
      status,
      startTime: typeof startTime === 'string' ? startTime : startTime.toISOString().replace('T', ' ').substring(0, 19),
      endTime: typeof endTime === 'string' ? endTime : endTime.toISOString().replace('T', ' ').substring(0, 19),
      duration
    };
    this.testResults.push(resultObj);

    if (status === 'FAILED') {
      this.failedTests.push({
        testName: `${testId}: ${scenarioName}`,
        failureReason,
        screenshotPath,
        browser,
        url
      });
    }

    this.logStep(`${testId}: ${scenarioName}`, `Completed execution with status: ${status}`, status, failureReason ? `Failure: ${failureReason}` : 'Executed successfully');
  }

  /**
   * Generate and write Excel Workbook to disk
   */
  async generateReport(targetPath = null) {
    const workbook = new ExcelJS.Workbook();
    workbook.creator = 'Senior QA Automation Architect';
    workbook.created = new Date();
    workbook.properties.date1904 = false;

    const outDir = path.resolve(process.cwd(), appConfig.excelReportsDir);
    if (!fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }
    const finalPath = targetPath || path.join(outDir, this.outputFileName);

    const totalTests = this.testResults.length;
    const passed = this.testResults.filter(t => t.status === 'PASSED').length;
    const failed = this.testResults.filter(t => t.status === 'FAILED').length;
    const skipped = this.testResults.filter(t => t.status === 'SKIPPED').length;
    const passPercentage = totalTests > 0 ? `${((passed / totalTests) * 100).toFixed(2)}%` : '100.00%';
    const totalDurationSec = ((new Date() - this.startTime) / 1000).toFixed(2);
    const executionDuration = `${totalDurationSec}s`;

    // -------------------------------------------------------------
    // SHEET 1: SUMMARY
    // -------------------------------------------------------------
    const summarySheet = workbook.addWorksheet('Summary', {
      views: [{ showGridLines: true }]
    });

    // Title Banner
    summarySheet.mergeCells('A1:H2');
    const titleCell = summarySheet.getCell('A1');
    titleCell.value = `📊 ${this.reportTitle.toUpperCase().replace(/_/g, ' ')} - AUTOMATION EXECUTION SUMMARY`;
    titleCell.font = { name: 'Segoe UI', size: 16, bold: true, color: { argb: 'FFFFFFFF' } };
    titleCell.alignment = { horizontal: 'center', vertical: 'middle' };
    titleCell.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FF1E40AF' } // Deep Royal Blue
    };

    // Subtitle / Date
    summarySheet.mergeCells('A3:H3');
    const subCell = summarySheet.getCell('A3');
    subCell.value = `Execution Date: ${new Date().toISOString().split('T')[0]} | Environment: ${appConfig.env.toUpperCase()} | Suite: ${this.reportTitle}`;
    subCell.font = { name: 'Segoe UI', size: 11, italic: true, color: { argb: 'FF475569' } };
    subCell.alignment = { horizontal: 'center', vertical: 'middle' };

    // KPI Summary Table Headers
    const summaryHeaders = [
      'Execution Date',
      'Environment',
      'Total Tests',
      'Passed',
      'Failed',
      'Skipped',
      'Pass Percentage',
      'Execution Duration'
    ];

    summarySheet.getRow(5).values = summaryHeaders;
    const headerRow = summarySheet.getRow(5);
    headerRow.height = 30;
    headerRow.font = { name: 'Segoe UI', size: 11, bold: true, color: { argb: 'FFFFFFFF' } };
    headerRow.alignment = { horizontal: 'center', vertical: 'middle' };
    headerRow.eachCell((cell) => {
      cell.fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF3B82F6' } // Enterprise Blue
      };
      cell.border = {
        top: { style: 'thin', color: { argb: 'FFCBD5E1' } },
        bottom: { style: 'medium', color: { argb: 'FF1E3A8A' } },
        left: { style: 'thin', color: { argb: 'FFCBD5E1' } },
        right: { style: 'thin', color: { argb: 'FFCBD5E1' } }
      };
    });

    // Summary Data Row
    const summaryData = [
      new Date().toISOString().split('T')[0],
      appConfig.env.toUpperCase(),
      totalTests,
      passed,
      failed,
      skipped,
      passPercentage,
      executionDuration
    ];

    summarySheet.addRow(summaryData);
    const dataRow = summarySheet.getRow(6);
    dataRow.height = 28;
    dataRow.font = { name: 'Segoe UI', size: 12, bold: true };
    dataRow.alignment = { horizontal: 'center', vertical: 'middle' };
    dataRow.eachCell((cell, colNumber) => {
      cell.border = {
        top: { style: 'thin', color: { argb: 'FFCBD5E1' } },
        bottom: { style: 'thin', color: { argb: 'FFCBD5E1' } },
        left: { style: 'thin', color: { argb: 'FFCBD5E1' } },
        right: { style: 'thin', color: { argb: 'FFCBD5E1' } }
      };
      if (colNumber === 4 || colNumber === 7) {
        cell.font = { name: 'Segoe UI', size: 12, bold: true, color: { argb: 'FF166534' } };
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCFCE7' } };
      }
      if (colNumber === 5 && failed > 0) {
        cell.font = { name: 'Segoe UI', size: 12, bold: true, color: { argb: 'FF991B1B' } };
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFEE2E2' } };
      }
    });

    summarySheet.columns = [
      { width: 20 },
      { width: 18 },
      { width: 16 },
      { width: 14 },
      { width: 14 },
      { width: 14 },
      { width: 20 },
      { width: 22 }
    ];

    // -------------------------------------------------------------
    // SHEET 2: TEST CASES (EXACTLY MATCHING USER SCREENSHOT)
    // -------------------------------------------------------------
    const testCasesSheet = workbook.addWorksheet('Test Cases', {
      views: [{ showGridLines: true }]
    });

    const tcHeaders = [
      'Test ID',
      'Module',
      'Test Name',
      'Browser / Device',
      'Status',
      'Start Time',
      'End Time',
      'Duration'
    ];

    testCasesSheet.getRow(1).values = tcHeaders;
    const tcHeaderRow = testCasesSheet.getRow(1);
    tcHeaderRow.height = 32;
    tcHeaderRow.font = { name: 'Segoe UI', size: 12, bold: true, color: { argb: 'FFFFFFFF' } };
    tcHeaderRow.alignment = { horizontal: 'center', vertical: 'middle' };
    tcHeaderRow.eachCell((cell, colNumber) => {
      cell.fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF3B82F6' } // Exact Blue from screenshot
      };
      cell.border = {
        top: { style: 'thin', color: { argb: 'FF93C5FD' } },
        bottom: { style: 'medium', color: { argb: 'FF1D4ED8' } },
        left: { style: 'thin', color: { argb: 'FF93C5FD' } },
        right: { style: 'thin', color: { argb: 'FF93C5FD' } }
      };
      if (colNumber === 1) cell.alignment = { horizontal: 'left', vertical: 'middle', indent: 1 };
      if (colNumber === 2) cell.alignment = { horizontal: 'left', vertical: 'middle', indent: 1 };
      if (colNumber === 3) cell.alignment = { horizontal: 'left', vertical: 'middle', indent: 1 };
    });

    this.testResults.forEach((tr, index) => {
      const row = testCasesSheet.addRow([
        tr.testId,
        tr.module,
        tr.scenarioName,
        tr.browser,
        tr.status,
        tr.startTime,
        tr.endTime,
        tr.duration
      ]);
      row.height = 24;
      row.alignment = { vertical: 'middle' };

      const bgColor = index % 2 === 0 ? 'FFFFFFFF' : 'FFF8FAFC';
      row.eachCell((cell, colNumber) => {
        cell.font = { name: 'Segoe UI', size: 10.5 };
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgColor } };
        cell.border = {
          top: { style: 'thin', color: { argb: 'FFE2E8F0' } },
          bottom: { style: 'thin', color: { argb: 'FFE2E8F0' } },
          left: { style: 'thin', color: { argb: 'FFE2E8F0' } },
          right: { style: 'thin', color: { argb: 'FFE2E8F0' } }
        };

        if (colNumber === 1) {
          cell.font = { name: 'Segoe UI', size: 10.5, bold: true, color: { argb: 'FF1E293B' } };
          cell.alignment = { horizontal: 'left', vertical: 'middle', indent: 1 };
        } else if (colNumber === 2) {
          cell.font = { name: 'Segoe UI', size: 10.5, color: { argb: 'FF334155' } };
          cell.alignment = { horizontal: 'left', vertical: 'middle', indent: 1 };
        } else if (colNumber === 3) {
          cell.font = { name: 'Segoe UI', size: 10.5, color: { argb: 'FF0F172A' } };
          cell.alignment = { horizontal: 'left', vertical: 'middle', indent: 1 };
        } else if (colNumber === 5) {
          cell.alignment = { horizontal: 'center', vertical: 'middle' };
          if (tr.status === 'PASSED') {
            cell.font = { name: 'Segoe UI', size: 10.5, bold: true, color: { argb: 'FF15803D' } };
            cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCFCE7' } };
          } else if (tr.status === 'FAILED') {
            cell.font = { name: 'Segoe UI', size: 10.5, bold: true, color: { argb: 'FFB91C1C' } };
            cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFEE2E2' } };
          }
        } else {
          cell.alignment = { horizontal: 'center', vertical: 'middle' };
        }
      });
    });

    testCasesSheet.columns = [
      { width: 16 }, // Test ID
      { width: 28 }, // Module
      { width: 65 }, // Test Name
      { width: 24 }, // Browser / Device
      { width: 14 }, // Status
      { width: 22 }, // Start Time
      { width: 22 }, // End Time
      { width: 14 }  // Duration
    ];

    // -------------------------------------------------------------
    // SHEET 3: FAILED TESTS
    // -------------------------------------------------------------
    const failedSheet = workbook.addWorksheet('Failed Tests', {
      views: [{ showGridLines: true }]
    });

    const failedHeaders = [
      'Test Name',
      'Failure Reason',
      'Screenshot Path',
      'Browser / Device',
      'URL / Activity'
    ];

    failedSheet.getRow(1).values = failedHeaders;
    const failedHeaderRow = failedSheet.getRow(1);
    failedHeaderRow.height = 30;
    failedHeaderRow.font = { name: 'Segoe UI', size: 11, bold: true, color: { argb: 'FFFFFFFF' } };
    failedHeaderRow.alignment = { horizontal: 'center', vertical: 'middle' };
    failedHeaderRow.eachCell((cell) => {
      cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDC2626' } };
    });

    if (this.failedTests.length === 0) {
      const row = failedSheet.addRow([
        'None - 100% Passed',
        'No failures occurred during this test execution.',
        'N/A',
        'All Browsers/Devices',
        'All URLs verified'
      ]);
      row.height = 26;
      row.font = { name: 'Segoe UI', size: 11, italic: true, color: { argb: 'FF15803D' } };
    } else {
      this.failedTests.forEach(ft => {
        const row = failedSheet.addRow([
          ft.testName,
          ft.failureReason,
          ft.screenshotPath,
          ft.browser,
          ft.url
        ]);
        row.height = 24;
      });
    }

    failedSheet.columns = [
      { width: 35 },
      { width: 40 },
      { width: 35 },
      { width: 20 },
      { width: 30 }
    ];

    // -------------------------------------------------------------
    // SHEET 4: EXECUTION LOGS
    // -------------------------------------------------------------
    const logsSheet = workbook.addWorksheet('Execution Logs', {
      views: [{ showGridLines: true }]
    });

    const logHeaders = [
      'Timestamp',
      'Test Name',
      'Step Description',
      'Result',
      'Remarks'
    ];

    logsSheet.getRow(1).values = logHeaders;
    const logHeaderRow = logsSheet.getRow(1);
    logHeaderRow.height = 30;
    logHeaderRow.font = { name: 'Segoe UI', size: 11, bold: true, color: { argb: 'FFFFFFFF' } };
    logHeaderRow.alignment = { horizontal: 'center', vertical: 'middle' };
    logHeaderRow.eachCell((cell) => {
      cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF475569' } };
    });

    this.executionLogs.forEach((log, index) => {
      const row = logsSheet.addRow([
        log.timestamp,
        log.testName,
        log.stepDescription,
        log.result,
        log.remarks
      ]);
      row.height = 22;
      const bgColor = index % 2 === 0 ? 'FFFFFFFF' : 'FFF8FAFC';
      row.eachCell((cell, colNumber) => {
        cell.font = { name: 'Segoe UI', size: 10 };
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgColor } };
        cell.border = {
          top: { style: 'thin', color: { argb: 'FFE2E8F0' } },
          bottom: { style: 'thin', color: { argb: 'FFE2E8F0' } },
          left: { style: 'thin', color: { argb: 'FFE2E8F0' } },
          right: { style: 'thin', color: { argb: 'FFE2E8F0' } }
        };
        if (colNumber === 4) {
          cell.alignment = { horizontal: 'center' };
          if (log.result === 'PASSED') {
            cell.font = { name: 'Segoe UI', size: 10, bold: true, color: { argb: 'FF15803D' } };
          } else if (log.result === 'FAILED') {
            cell.font = { name: 'Segoe UI', size: 10, bold: true, color: { argb: 'FFB91C1C' } };
          }
        }
      });
    });

    logsSheet.columns = [
      { width: 22 },
      { width: 35 },
      { width: 50 },
      { width: 14 },
      { width: 40 }
    ];

    await workbook.xlsx.writeFile(finalPath);
    logger.info(`[ExcelReporter] Successfully generated report at: ${finalPath}`);
    return finalPath;
  }
}

// Global Singleton Store for Master Consolidation
const globalResultsStore = {
  selenium: [],
  appium: [],
  vulnerability: [],
  load: [],
  logs: []
};

function addSuiteResults(suiteName, results, logs = []) {
  if (globalResultsStore[suiteName]) {
    globalResultsStore[suiteName].push(...results);
  }
  if (logs.length > 0) {
    globalResultsStore.logs.push(...logs);
  }
}

async function generateMasterReport() {
  const masterReporter = new ExcelReporter('Master_Enterprise_1200_Report', 'Master_Enterprise_1200_Report.xlsx');
  
  const allResults = [
    ...globalResultsStore.selenium,
    ...globalResultsStore.appium,
    ...globalResultsStore.vulnerability,
    ...globalResultsStore.load
  ];

  masterReporter.testResults = allResults;
  masterReporter.executionLogs = globalResultsStore.logs;
  
  const outPath = await masterReporter.generateReport();
  logger.info(`[MasterReporter] Master Consolidated 1200-Test Report generated: ${outPath}`);
  return outPath;
}

module.exports = {
  ExcelReporter,
  addSuiteResults,
  generateMasterReport,
  globalResultsStore
};
