/**
 * Load & Performance Test Suite 01: Baseline Latency & Throughput Benchmarks
 * Test IDs: TC-LOAD-001 to TC-LOAD-050 (50 Test Cases)
 */

const { expect, createSuiteTracker } = require('../test-helper');
const axios = require('axios');
const appConfig = require('../../config/app.config');

describe('Load Suite 01: Baseline Latency & Throughput (50 Tests)', function () {
  this.timeout(60000);
  const tracker = createSuiteTracker('load', 'Baseline Latency');

  after(() => {
    tracker.flushResults();
  });

  // Endpoints to benchmark for baseline TTFB & Latency
  const baselineEndpoints = [
    { path: '/', name: 'Feed Home Root /' },
    { path: '/login', name: 'Login Page /login' },
    { path: '/register', name: 'Register Page /register' },
    { path: '/settings', name: 'Settings Page /settings' },
    { path: '/history', name: 'History Page /history' },
    { path: '/bookmarks', name: 'Bookmarks Page /bookmarks' },
    { path: '/roundup', name: 'Roundups Page /roundup' },
    { path: '/api/cluster', name: 'API Cluster /api/cluster' },
    { path: '/api/regions', name: 'API Regions /api/regions' },
    { path: '/favicon.ico', name: 'Favicon Asset /favicon.ico' }
  ];

  // TC-LOAD-001 to TC-LOAD-050: 5 iterations per endpoint = 50 tests
  let loadIndex = 1;
  baselineEndpoints.forEach((ep) => {
    for (let iter = 1; iter <= 5; iter++) {
      const testId = `TC-LOAD-${String(loadIndex).padStart(3, '0')}`;
      const testName = `Latency SLA: ${ep.name} (Iteration ${iter}/5)`;
      loadIndex++;

      tracker.runTest(testId, testName, 'Baseline SLA', async () => {
        const startTime = Date.now();
        const res = await axios.get(`${appConfig.baseUrl}${ep.path}`, { validateStatus: () => true });
        const latencyMs = Date.now() - startTime;
        expect(res.status).to.be.oneOf([200, 204, 302, 401, 404]);
        expect(latencyMs).to.be.lessThan(1000); // 1000ms SLA limit
      });
    }
  });
});
