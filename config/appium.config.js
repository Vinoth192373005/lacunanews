/**
 * Appium 2.x Configuration for Android Mobile Automation
 * Supports UiAutomator2 and Flutter Driver capabilities
 */

const appConfig = require('./app.config');

module.exports = {
  appiumServer: {
    host: process.env.APPIUM_HOST || '127.0.0.1',
    port: parseInt(process.env.APPIUM_PORT || '4723', 10),
    path: '/'
  },
  androidCapabilities: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': process.env.ANDROID_DEVICE_NAME || 'Android Emulator',
    'appium:platformVersion': process.env.ANDROID_VERSION || '13.0',
    'appium:app': appConfig.apkPath,
    'appium:appPackage': appConfig.appPackage,
    'appium:appActivity': appConfig.appActivity,
    'appium:noReset': false,
    'appium:fullReset': false,
    'appium:autoGrantPermissions': true,
    'appium:newCommandTimeout': 120,
    'appium:connectHardwareKeyboard': true,
    'appium:ensureWebviewsHavePages': true,
    'appium:nativeWebScreenshot': true
  },
  installedAppCapabilities: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': process.env.ANDROID_DEVICE_NAME || 'Android Emulator',
    'appium:appPackage': appConfig.appPackage,
    'appium:appActivity': appConfig.appActivity,
    'appium:noReset': true
  }
};
