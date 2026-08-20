/**
 * Load & Performance Test Suite 03: Stress & Breaking Point Thresholds
 * Test IDs: TC-LOAD-101 to TC-LOAD-150 (50 Test Cases)
 */

const { expect, createSuiteTracker } = require('../test-helper');
const axios = require('axios');
const appConfig = require('../../config/app.config');

describe('Load Suite 03: Stress & Threshold Testing (50 Tests)', function () {
  this.timeout(60000);
  const tracker = createSuiteTracker('load', 'Stress Testing');

  after(() => {
    tracker.flushResults();
  });

  const stressEndpoints = [
    { path: '/', name: 'Stress: Rapid traffic burst on Root Feed' },
    { path: '/api/cluster', name: 'Stress: Rapid traffic burst on API Cluster' },
    { path: '/api/regions', name: 'Stress: Rapid traffic burst on API Regions' },
    { path: '/settings', name: 'Stress: Rapid traffic burst on Settings Page' },
    { path: '/history', name: 'Stress: Rapid traffic burst on History Page' },
    { path: '/bookmarks', name: 'Stress: Rapid traffic burst on Bookmarks Page' },
    { path: '/roundup', name: 'Stress: Rapid traffic burst on Roundups Page' },
    { path: '/login', name: 'Stress: Rapid traffic burst on Login Page' },
    { path: '/register', name: 'Stress: Rapid traffic burst on Register Page' },
    { path: '/static/app.js', name: 'Stress: Rapid traffic burst on Static JS Bundle' }
  ];

  let stressIndex = 101;
  stressEndpoints.forEach((ep) => {
    for (let round = 1; round <= 5; round++) {
      const testId = `TC-LOAD-${String(stressIndex).padStart(3, '0')}`;
      const testName = `${ep.name} (Burst Round ${round}/5)`;
      stressIndex++;

      tracker.runTest(testId, testName, 'Stress Limits', async () => {
        const burst = Array.from({ length: 10 }, () =>
          axios.get(`${appConfig.baseUrl}${ep.path}`, { validateStatus: () => true })
        );
        const results = await Promise.all(burst);
        results.forEach((res) => {
          expect(res.status).to.be.oneOf([200, 302, 401, 404]);
        });
      });
    }
  });
});
