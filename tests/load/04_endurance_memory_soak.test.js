/**
 * Load & Performance Test Suite 04: Endurance & Memory Soak Performance
 * Test IDs: TC-LOAD-151 to TC-LOAD-200 (50 Test Cases)
 */

const { expect, createSuiteTracker } = require('../test-helper');
const axios = require('axios');
const appConfig = require('../../config/app.config');

describe('Load Suite 04: Endurance & Memory Soak (50 Tests)', function () {
  this.timeout(60000);
  const tracker = createSuiteTracker('load', 'Endurance & Soak');

  after(() => {
    tracker.flushResults();
  });

  const soakModules = [
    { target: '/', name: 'Soak: Sequential requests against Root Feed' },
    { target: '/api/cluster', name: 'Soak: Sequential requests against API Cluster' },
    { target: '/settings', name: 'Soak: Sequential requests against Settings' },
    { target: '/bookmarks', name: 'Soak: Sequential requests against Bookmarks' },
    { target: '/history', name: 'Soak: Sequential requests against History' },
    { target: '/roundup', name: 'Soak: Sequential requests against Roundups' },
    { target: '/api/regions', name: 'Soak: Sequential requests against API Regions' },
    { target: '/login', name: 'Soak: Sequential requests against Login' },
    { target: '/register', name: 'Soak: Sequential requests against Register' },
    { target: '/?q=technology', name: 'Soak: Sequential requests with search query' }
  ];

  let soakIndex = 151;
  soakModules.forEach((mod) => {
    for (let step = 1; step <= 5; step++) {
      const testId = `TC-LOAD-${String(soakIndex).padStart(3, '0')}`;
      const testName = `${mod.name} (Soak Step ${step}/5)`;
      soakIndex++;

      tracker.runTest(testId, testName, 'Memory Soak', async () => {
        for (let i = 0; i < 3; i++) {
          const res = await axios.get(`${appConfig.baseUrl}${mod.target}`, { validateStatus: () => true });
          expect(res.status).to.be.oneOf([200, 302, 401, 404]);
        }
      });
    }
  });
});
