/**
 * Dynamic Form & Route Discovery Utility
 * Automatically traverses routes, discovers forms, detects input fields,
 * and extracts validation constraints (required, minlength, pattern, etc.)
 */

const axios = require('axios');
const appConfig = require('../config/app.config');
const logger = require('./logger');

class DynamicFormDiscovery {
  constructor(baseUrl = appConfig.baseUrl) {
    this.baseUrl = baseUrl;
    this.discoveredRoutes = [];
    this.discoveredForms = [];
  }

  /**
   * Crawl known application routes
   */
  async crawlRoutes() {
    const candidateRoutes = [
      '/',
      '/login',
      '/register',
      '/settings',
      '/roundup',
      '/history',
      '/bookmarks',
      '/api/cluster',
      '/api/regions',
      '/api/interests'
    ];

    logger.info(`[Discovery] Starting dynamic route & form discovery across ${candidateRoutes.length} endpoints`);

    for (const route of candidateRoutes) {
      try {
        const url = `${this.baseUrl}${route}`;
        const res = await axios.get(url, { validateStatus: () => true, timeout: 5000 });
        this.discoveredRoutes.push({
          route,
          url,
          status: res.status,
          contentType: res.headers['content-type'] || 'unknown',
          isHtml: (res.headers['content-type'] || '').includes('text/html')
        });

        if (typeof res.data === 'string' && res.data.includes('<form')) {
          this.parseForms(route, res.data);
        }
      } catch (err) {
        logger.warn(`[Discovery] Route ${route} unavailable: ${err.message}`);
      }
    }

    logger.info(`[Discovery] Discovered ${this.discoveredRoutes.length} routes and ${this.discoveredForms.length} active forms.`);
    return {
      routes: this.discoveredRoutes,
      forms: this.discoveredForms
    };
  }

  /**
   * Parse HTML form elements and extract rules
   */
  parseForms(route, htmlContent) {
    const formRegex = /<form([^>]*?)>([\s\S]*?)<\/form>/gi;
    let match;

    while ((match = formRegex.exec(htmlContent)) !== null) {
      const formAttrs = match[1];
      const formInner = match[2];

      const actionMatch = /action=["']([^"']*)["']/i.exec(formAttrs);
      const methodMatch = /method=["']([^"']*)["']/i.exec(formAttrs);
      const idMatch = /id=["']([^"']*)["']/i.exec(formAttrs);

      const action = actionMatch ? actionMatch[1] : route;
      const method = methodMatch ? methodMatch[1].toUpperCase() : 'GET';
      const formId = idMatch ? idMatch[1] : `form_${route.replace(/[^a-zA-Z0-9]/g, '_')}`;

      // Discover input fields
      const inputs = [];
      const inputRegex = /<input([^>]*?)\/?>/gi;
      let inputMatch;
      while ((inputMatch = inputRegex.exec(formInner)) !== null) {
        const attrs = inputMatch[1];
        const nameMatch = /name=["']([^"']*)["']/i.exec(attrs);
        const typeMatch = /type=["']([^"']*)["']/i.exec(attrs);
        const required = /required/i.test(attrs);
        const minLengthMatch = /minlength=["'](\d+)["']/i.exec(attrs);
        const maxLengthMatch = /maxlength=["'](\d+)["']/i.exec(attrs);
        const patternMatch = /pattern=["']([^"']*)["']/i.exec(attrs);

        if (nameMatch) {
          inputs.push({
            name: nameMatch[1],
            type: typeMatch ? typeMatch[1] : 'text',
            required,
            minLength: minLengthMatch ? parseInt(minLengthMatch[1], 10) : null,
            maxLength: maxLengthMatch ? parseInt(maxLengthMatch[1], 10) : null,
            pattern: patternMatch ? patternMatch[1] : null
          });
        }
      }

      this.discoveredForms.push({
        route,
        formId,
        action,
        method,
        fields: inputs
      });
    }
  }
}

module.exports = DynamicFormDiscovery;
