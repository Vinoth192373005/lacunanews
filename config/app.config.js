/**
 * Application Configuration
 * Enterprise QA Automation Framework
 */

require('dotenv').config();

const ENV = process.env.NODE_ENV || 'local';

const config = {
  env: ENV,
  baseUrl: process.env.BASE_URL || 'http://127.0.0.1:5001',
  apiBaseUrl: process.env.API_BASE_URL || 'http://127.0.0.1:5001/api',
  serverPort: parseInt(process.env.TEST_PORT || '5001', 10),
  defaultTimeout: parseInt(process.env.DEFAULT_TIMEOUT || '15000', 10),
  pageLoadTimeout: parseInt(process.env.PAGE_LOAD_TIMEOUT || '30000', 10),
  implicitWait: parseInt(process.env.IMPLICIT_WAIT || '3000', 10),
  retryCount: parseInt(process.env.RETRY_COUNT || '2', 10),
  headless: process.env.HEADLESS !== 'false',
  browser: process.env.BROWSER || 'chrome',
  reportsDir: process.env.REPORTS_DIR || './reports',
  screenshotsDir: process.env.SCREENSHOTS_DIR || './reports/failures',
  excelReportsDir: process.env.EXCEL_REPORTS_DIR || './reports/excel',
  logsDir: process.env.LOGS_DIR || './logs',
  apkPath: process.env.APK_PATH || './lacuna-android/app/build/outputs/apk/debug/app-debug.apk',
  appPackage: process.env.APP_PACKAGE || 'com.lacuna.news',
  appActivity: process.env.APP_ACTIVITY || 'com.lacuna.news.MainActivity'
};

module.exports = config;
