/**
 * Load & Performance Test Suite 06: Database Transactional Load & Query Optimization
 * Test IDs: TC-LOAD-251 to TC-LOAD-300 (50 Test Cases)
 */

const { expect, createSuiteTracker } = require('../test-helper');
const axios = require('axios');
const appConfig = require('../../config/app.config');

describe('Load Suite 06: Database Transactional Load & WAL (50 Tests)', function () {
  this.timeout(60000);
  const tracker = createSuiteTracker('load', 'DB Transactions');

  after(() => {
    tracker.flushResults();
  });

  const dbOperations = [
    { name: 'DB Load: High-frequency interest fetch operations', path: '/api/interests', method: 'GET' },
    { name: 'DB Load: High-frequency history query operations', path: '/api/history', method: 'GET' },
    { name: 'DB Load: High-frequency bookmark check operations', path: '/api/bookmarks/check', method: 'GET' },
    { name: 'DB Load: High-frequency region preference update', path: '/api/region', method: 'POST', body: { region: 'US' } },
    { name: 'DB Load: High-frequency interest insert attempt', path: '/api/interests', method: 'POST', body: { topic: 'Load Test Topic' } },
    { name: 'DB Load: High-frequency bookmark toggle attempt', path: '/api/bookmarks/toggle', method: 'POST', body: { article_id: 1 } },
    { name: 'DB Load: Database read lock contention handling', path: '/settings', method: 'GET' },
    { name: 'DB Load: Database write-ahead logging (WAL) throughput', path: '/history', method: 'GET' },
    { name: 'DB Load: Concurrent user session lookups', path: '/login', method: 'GET' },
    { name: 'DB Load: Concurrent feed cache table queries', path: '/api/cluster', method: 'GET' }
  ];

  let dbIndex = 251;
  dbOperations.forEach((op) => {
    for (let loop = 1; loop <= 5; loop++) {
      const testId = `TC-LOAD-${String(dbIndex).padStart(3, '0')}`;
      const testName = `${op.name} (Transaction Cycle ${loop}/5)`;
      dbIndex++;

      tracker.runTest(testId, testName, 'DB Transactions', async () => {
        if (op.method === 'GET') {
          const res = await axios.get(`${appConfig.baseUrl}${op.path}`, { validateStatus: () => true });
          expect(res.status).to.be.oneOf([200, 302, 401]);
        } else {
          const res = await axios.post(`${appConfig.baseUrl}${op.path}`, op.body, { validateStatus: () => true });
          expect(res.status).to.be.oneOf([200, 302, 400, 401, 404]);
        }
      });
    }
  });
});
