/**
 * Test Server Manager
 * Manages background Python/Flask test server lifecycle for local & CI test execution
 */

const { spawn } = require('child_process');
const axios = require('axios');
const path = require('path');
const fs = require('fs');
const logger = require('./logger');
const appConfig = require('../config/app.config');

class TestServerManager {
  constructor(port = appConfig.serverPort) {
    this.port = port;
    this.baseUrl = `http://127.0.0.1:${port}`;
    this.serverProcess = null;
  }

  /**
   * Check if server is already responding
   */
  async isServerRunning() {
    try {
      const res = await axios.get(this.baseUrl, { timeout: 1500, validateStatus: () => true });
      return res.status < 500;
    } catch (e) {
      return false;
    }
  }

  /**
   * Start Flask Server if not already active
   */
  async startServer() {
    if (await this.isServerRunning()) {
      logger.info(`[ServerManager] Live server already active at: ${this.baseUrl}`);
      return this.baseUrl;
    }

    logger.info(`[ServerManager] Starting background Flask test server on port ${this.port}...`);
    
    // Choose python executable (.venv/bin/python if present)
    let pythonExe = 'python3';
    const venvPython = path.resolve(process.cwd(), '.venv/bin/python');
    const venvWindowsPython = path.resolve(process.cwd(), '.venv/Scripts/python.exe');

    if (fs.existsSync(venvPython)) {
      pythonExe = venvPython;
    } else if (fs.existsSync(venvWindowsPython)) {
      pythonExe = venvWindowsPython;
    } else if (process.platform === 'win32') {
      pythonExe = 'python';
    }

    const serverScript = path.resolve(__dirname, 'start_test_server.py');

    this.serverProcess = spawn(pythonExe, [serverScript, '--port', String(this.port)], {
      cwd: process.cwd(),
      env: {
        ...process.env,
        PORT: String(this.port),
        FLASK_ENV: 'testing',
        SECRET_KEY: 'test-secret-key-enterprise-qa'
      },
      detached: false,
      stdio: 'pipe'
    });

    this.serverProcess.stdout.on('data', (data) => {
      logger.debug(`[Flask stdout] ${data.toString().trim()}`);
    });

    this.serverProcess.stderr.on('data', (data) => {
      logger.debug(`[Flask stderr] ${data.toString().trim()}`);
    });

    // Wait for server to become healthy (max 15s)
    const startTime = Date.now();
    while (Date.now() - startTime < 15000) {
      if (await this.isServerRunning()) {
        logger.info(`[ServerManager] Flask test server successfully started and verified at: ${this.baseUrl}`);
        return this.baseUrl;
      }
      await new Promise(r => setTimeout(r, 400));
    }

    logger.warn(`[ServerManager] Server did not respond within timeout, proceeding with default base url: ${this.baseUrl}`);
    return this.baseUrl;
  }

  /**
   * Stop background server
   */
  async stopServer() {
    if (this.serverProcess) {
      logger.info(`[ServerManager] Terminating background Flask test server...`);
      try {
        this.serverProcess.kill('SIGTERM');
      } catch (e) {
        // ignore
      }
      this.serverProcess = null;
    }
  }
}

module.exports = TestServerManager;
