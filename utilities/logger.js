/**
 * Winston Logger Utility
 * Enterprise logging with console and file transports
 */

const winston = require('winston');
const path = require('path');
const fs = require('fs');
const appConfig = require('../config/app.config');

const logDir = path.resolve(process.cwd(), appConfig.logsDir);
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const customFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const metaStr = Object.keys(meta).length ? ` | Meta: ${JSON.stringify(meta)}` : '';
    return `[${timestamp}] [${level.toUpperCase().padEnd(5)}] ${message}${metaStr}`;
  })
);

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: customFormat,
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        customFormat
      )
    }),
    new winston.transports.File({
      filename: path.join(logDir, 'execution.log'),
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5
    }),
    new winston.transports.File({
      filename: path.join(logDir, 'errors.log'),
      level: 'error'
    })
  ]
});

module.exports = logger;
