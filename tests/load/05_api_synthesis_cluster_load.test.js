/**
 * Load & Performance Test Suite 05: Heavy Compute & AI Synthesis Benchmarks
 * Test IDs: TC-LOAD-201 to TC-LOAD-250 (50 Test Cases)
 */

const { expect, createSuiteTracker } = require('../test-helper');
const axios = require('axios');
const appConfig = require('../../config/app.config');

describe('Load Suite 05: Heavy Compute & AI Synthesis Load (50 Tests)', function () {
  this.timeout(60000);
  const tracker = createSuiteTracker('load', 'AI Compute Load');

  after(() => {
    tracker.flushResults();
  });

  const computeEndpoints = [
    { path: '/api/cluster', method: 'GET', name: 'Compute: Clustering algorithm response time' },
    { path: '/api/regions', method: 'GET', name: 'Compute: Region aggregation response time' },
    { path: '/roundup', method: 'GET', name: 'Compute: Synthesis template rendering load' },
    { path: '/api/interests', method: 'GET', name: 'Compute: User interest weighting retrieval' },
    { path: '/api/history', method: 'GET', name: 'Compute: History query execution benchmark' },
    { path: '/api/bookmarks', method: 'GET', name: 'Compute: Bookmarks query execution benchmark' },
    { path: '/?region=US', method: 'GET', name: 'Compute: Filtered US feed generation' },
    { path: '/?region=UK', method: 'GET', name: 'Compute: Filtered UK feed generation' },
    { path: '/?region=IN', method: 'GET', name: 'Compute: Filtered IN feed generation' },
    { path: '/?region=GLOBAL', method: 'GET', name: 'Compute: Filtered GLOBAL feed generation' }
  ];

  let computeIndex = 201;
  computeEndpoints.forEach((ep) => {
    for (let testNum = 1; testNum <= 5; testNum++) {
      const testId = `TC-LOAD-${String(computeIndex).padStart(3, '0')}`;
      const testName = `${ep.name} (Iteration ${testNum}/5)`;
      computeIndex++;

      tracker.runTest(testId, testName, 'AI Compute', async () => {
        const startTime = Date.now();
        const res = await axios.get(`${appConfig.baseUrl}${ep.path}`, { validateStatus: () => true });
        const latency = Date.now() - startTime;
        expect(res.status).to.be.oneOf([200, 302, 401]);
        expect(latency).to.be.lessThan(2500); // 2.5s compute limit
      });
    }
  });
});
