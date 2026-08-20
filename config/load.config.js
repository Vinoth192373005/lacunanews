/**
 * Load & Performance Testing Configuration
 * Thresholds, SLA Limits, Virtual Users, Soak & Burst configurations
 */

module.exports = {
  sla: {
    maxTtfbMs: 300,
    maxPageLoadMs: 1500,
    maxApiLatencyMs: 500,
    maxSynthesisLatencyMs: 3000,
    minSuccessRatePercent: 99.5
  },
  scenarios: {
    baseline: { virtualUsers: 1, iterations: 10 },
    concurrencyLow: { virtualUsers: 5, iterations: 10 },
    concurrencyMed: { virtualUsers: 15, iterations: 5 },
    concurrencyHigh: { virtualUsers: 30, iterations: 3 },
    burst: { burstUsers: 50, durationMs: 2000 },
    endurance: { durationSec: 10, targetRps: 20 }
  },
  targetEndpoints: [
    '/',
    '/login',
    '/settings',
    '/history',
    '/bookmarks',
    '/roundup',
    '/api/cluster',
    '/api/regions',
    '/api/interests'
  ]
};
