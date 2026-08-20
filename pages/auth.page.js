/**
 * Authentication Page Object (Login & Register)
 */

const { By } = require('selenium-webdriver');
const BasePage = require('./base.page');
const logger = require('../utilities/logger');

class AuthPage extends BasePage {
  constructor(driver) {
    super(driver);

    // Form Locators
    this.LOGIN_TAB = By.css('button[data-tab="login"], a[href="#login"], #tab-login');
    this.REGISTER_TAB = By.css('button[data-tab="register"], a[href="#register"], #tab-register');
    this.USERNAME_INPUT = By.css('input[name="username"], #username, input[type="text"]');
    this.PASSWORD_INPUT = By.css('input[name="password"], #password, input[type="password"]');
    this.CONFIRM_PASSWORD_INPUT = By.css('input[name="confirm_password"], #confirm_password');
    this.SUBMIT_BTN = By.css('button[type="submit"], input[type="submit"], .auth-submit-btn');
    this.ERROR_MESSAGE = By.css('.error, .alert-danger, .flash-message.error, .auth-error, [role="alert"]');
    this.SUCCESS_MESSAGE = By.css('.success, .alert-success, .flash-message.success');
    this.GOOGLE_LOGIN_BTN = By.css('a[href*="/login/google"], .google-login-btn');
    this.AUTH_CONTAINER = By.css('.auth-card, .auth-container, .login-form');
  }

  async openLogin() {
    await this.navigateTo('/login');
    return this;
  }

  async openRegister() {
    await this.navigateTo('/register');
    return this;
  }

  async switchToLoginTab() {
    if (await this.isElementVisible(this.LOGIN_TAB)) {
      await this.clickElement(this.LOGIN_TAB);
    }
  }

  async switchToRegisterTab() {
    if (await this.isElementVisible(this.REGISTER_TAB)) {
      await this.clickElement(this.REGISTER_TAB);
    }
  }

  async login(username, password) {
    logger.info(`[AuthPage] Attempting login with username: "${username}"`);
    if (username !== null && username !== undefined) {
      await this.typeInto(this.USERNAME_INPUT, username);
    }
    if (password !== null && password !== undefined) {
      await this.typeInto(this.PASSWORD_INPUT, password);
    }
    await this.clickElement(this.SUBMIT_BTN);
    await this.utils.sleep(500);
  }

  async register(username, password, confirmPassword = password) {
    logger.info(`[AuthPage] Attempting registration for username: "${username}"`);
    await this.switchToRegisterTab();
    if (username) await this.typeInto(this.USERNAME_INPUT, username);
    if (password) await this.typeInto(this.PASSWORD_INPUT, password);
    if (await this.isElementVisible(this.CONFIRM_PASSWORD_INPUT) && confirmPassword) {
      await this.typeInto(this.CONFIRM_PASSWORD_INPUT, confirmPassword);
    }
    await this.clickElement(this.SUBMIT_BTN);
    await this.utils.sleep(500);
  }

  async getErrorMessage() {
    if (await this.isElementVisible(this.ERROR_MESSAGE)) {
      return await this.getElementText(this.ERROR_MESSAGE);
    }
    return '';
  }

  async isAuthCardVisible() {
    return await this.isElementVisible(this.AUTH_CONTAINER);
  }
}

module.exports = AuthPage;
