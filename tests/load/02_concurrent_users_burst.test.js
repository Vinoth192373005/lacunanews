/**
 * Load & Performance Test Suite 02: Concurrency & Virtual User (VU) Ramping
 * Test IDs: TC-LOAD-051 to TC-LOAD-100 (50 Test Cases)
 */

const { expect, createSuiteTracker } = require('../test-helper');
const axios = require('axios');
const appConfig = require('../../config/app.config');

describe('Load Suite 02: Concurrency & Virtual User Burst (50 Tests)', function () {
  this.timeout(60000);
  const tracker = createSuiteTracker('load', 'Concurrency & VU');

  after(() => {
    tracker.flushResults();
  });

  // Concurrency scenarios with varying Virtual Users (5 VU to 30 VU)
  const concurrencyTiers = [
    { vu: 5, path: '/', name: '5 VU Concurrent Feed Requests' },
    { vu: 10, path: '/', name: '10 VU Concurrent Feed Requests' },
    { vu: 15, path: '/', name: '15 VU Concurrent Feed Requests' },
    { vu: 20, path: '/', name: '20 VU Concurrent Feed Requests' },
    { vu: 25, path: '/', name: '25 VU Concurrent Feed Requests' },
    { vu: 5, path: '/api/cluster', name: '5 VU Concurrent /api/cluster Requests' },
    { vu: 10, path: '/api/cluster', name: '10 VU Concurrent /api/cluster Requests' },
    { vu: 15, path: '/api/regions', name: '15 VU Concurrent /api/regions Requests' },
    { vu: 20, path: '/settings', name: '20 VU Concurrent /settings Requests' },
    { vu: 25, path: '/login', name: '25 VU Concurrent /login Requests' }
  ];

  let vuIndex = 51;
  concurrencyTiers.forEach((tier) => {
    for (let cycle = 1; cycle <= 5; cycle++) {
      const testId = `TC-LOAD-${String(vuIndex).padStart(3, '0')}`;
      const testName = `Concurrency: ${tier.name} (Batch Cycle ${cycle}/5)`;
      vuIndex++;

      tracker.runTest(testId, testName, 'VU Concurrency', async () => {
        const promises = Array.from({ length: tier.vu }, () =>
          axios.get(`${appConfig.baseUrl}${tier.path}`, { validateStatus: () => true })
        );
        const responses = await Promise.all(promises);
        responses.forEach((res) => {
          expect(res.status).to.be.oneOf([200, 302, 401, 404]);
        });
      });
    }
  });
});
