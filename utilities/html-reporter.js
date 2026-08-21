/**
 * HTML & GitHub Actions Step Summary Report Generator
 * Generates standalone interactive HTML visual dashboards and GitHub Actions Markdown summaries
 */

const fs = require('fs');
const path = require('path');
const logger = require('./logger');

class HtmlReporter {
  constructor(suiteName, outputFileName) {
    this.suiteName = suiteName;
    this.outputFileName = outputFileName || `${suiteName.toLowerCase().replace(/[^a-z0-9]/g, '-')}-report.html`;
    this.testResults = [];
    this.executionLogs = [];
    this.startTime = new Date();
  }

  /**
   * Generates a standalone interactive HTML dashboard
   */
  async generateHtmlReport(targetDir = null) {
    const htmlDir = targetDir || path.resolve(process.cwd(), 'reports/html');
    if (!fs.existsSync(htmlDir)) {
      fs.mkdirSync(htmlDir, { recursive: true });
    }

    const finalPath = path.join(htmlDir, this.outputFileName);
    const total = this.testResults.length;
    const passed = this.testResults.filter(t => t.status === 'PASSED').length;
    const failed = this.testResults.filter(t => t.status === 'FAILED').length;
    const skipped = this.testResults.filter(t => t.status === 'SKIPPED').length;
    const passRate = total > 0 ? ((passed / total) * 100).toFixed(2) : '100.00';
    const totalDurationSec = ((new Date() - this.startTime) / 1000).toFixed(2);

    // Group by modules
    const modules = {};
    this.testResults.forEach(t => {
      const mod = t.module || 'General';
      if (!modules[mod]) {
        modules[mod] = { total: 0, passed: 0, failed: 0, skipped: 0 };
      }
      modules[mod].total++;
      if (t.status === 'PASSED') modules[mod].passed++;
      else if (t.status === 'FAILED') modules[mod].failed++;
      else modules[mod].skipped++;
    });

    const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${this.suiteName} - QA Automation Report</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #3b82f6;
      --accent-glow: rgba(59, 130, 246, 0.25);
      --success: #10b981;
      --success-bg: rgba(16, 185, 129, 0.15);
      --danger: #ef4444;
      --danger-bg: rgba(239, 68, 68, 0.15);
      --warning: #f59e0b;
      --warning-bg: rgba(245, 158, 11, 0.15);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 2rem;
    }
    .container { max-width: 1400px; margin: 0 auto; }
    
    /* Header */
    .header {
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 2rem;
      margin-bottom: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .header h1 {
      font-size: 1.75rem;
      font-weight: 800;
      background: linear-gradient(to right, #60a5fa, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }
    .header p { color: var(--text-muted); font-size: 0.95rem; }
    .badge-pill {
      background: var(--success-bg);
      color: var(--success);
      border: 1px solid var(--success);
      padding: 0.5rem 1.25rem;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    /* KPI Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }
    .kpi-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
      transition: transform 0.2s, border-color 0.2s;
    }
    .kpi-card:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
    }
    .kpi-label { font-size: 0.85rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600; letter-spacing: 0.05em; }
    .kpi-value { font-size: 2.25rem; font-weight: 800; margin-top: 0.25rem; font-family: 'JetBrains Mono', monospace; }
    .kpi-value.total { color: #60a5fa; }
    .kpi-value.passed { color: var(--success); }
    .kpi-value.failed { color: var(--danger); }
    .kpi-value.rate { color: #a855f7; }
    .kpi-value.duration { color: var(--warning); }

    /* Module Breakdown */
    .section-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; color: #e2e8f0; }
    .module-table-wrapper {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 2rem;
    }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }
    th { background: #1e293b; padding: 1rem; font-weight: 600; color: #cbd5e1; border-bottom: 2px solid var(--card-border); }
    td { padding: 0.85rem 1rem; border-bottom: 1px solid var(--card-border); color: #e2e8f0; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(255, 255, 255, 0.02); }

    /* Controls */
    .controls {
      display: flex;
      gap: 1rem;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
    }
    .search-input, .filter-select {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      font-size: 0.95rem;
      outline: none;
    }
    .search-input { flex: 1; min-width: 250px; }
    .search-input:focus, .filter-select:focus { border-color: var(--accent); }

    /* Test Case Status Tags */
    .status-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
    }
    .status-badge.passed { background: var(--success-bg); color: var(--success); }
    .status-badge.failed { background: var(--danger-bg); color: var(--danger); }
    .status-badge.skipped { background: var(--warning-bg); color: var(--warning); }
    .mono { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <h1>📊 ${this.suiteName}</h1>
        <p>Enterprise Multi-Engine QA Automation Report | Executed on ${new Date().toISOString().replace('T', ' ').substring(0, 19)} UTC</p>
      </div>
      <div class="badge-pill">
        <span>✓</span> ${passRate}% PASSED
      </div>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Total Tests</div>
        <div class="kpi-value total">${total}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Passed</div>
        <div class="kpi-value passed">${passed}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Failed</div>
        <div class="kpi-value failed">${failed}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Pass Rate</div>
        <div class="kpi-value rate">${passRate}%</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Duration</div>
        <div class="kpi-value duration">${totalDurationSec}s</div>
      </div>
    </div>

    <h2 class="section-title">📦 Module Coverage Summary</h2>
    <div class="module-table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Module Name</th>
            <th style="text-align: center;">Total Tests</th>
            <th style="text-align: center;">Passed</th>
            <th style="text-align: center;">Failed</th>
            <th style="text-align: center;">Pass Rate</th>
          </tr>
        </thead>
        <tbody>
          ${Object.entries(modules).map(([mod, stats]) => `
          <tr>
            <td style="font-weight: 600;">${mod}</td>
            <td style="text-align: center;" class="mono">${stats.total}</td>
            <td style="text-align: center; color: var(--success);" class="mono">${stats.passed}</td>
            <td style="text-align: center; color: ${stats.failed > 0 ? 'var(--danger)' : 'inherit'};" class="mono">${stats.failed}</td>
            <td style="text-align: center; font-weight: 700; color: var(--success);" class="mono">${((stats.passed / stats.total) * 100).toFixed(1)}%</td>
          </tr>
          `).join('')}
        </tbody>
      </table>
    </div>

    <h2 class="section-title">🧪 Test Case Execution Details</h2>
    <div class="controls">
      <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search test ID, name, or scenario..." onkeyup="filterTests()">
      <select id="moduleFilter" class="filter-select" onchange="filterTests()">
        <option value="ALL">All Modules</option>
        ${Object.keys(modules).map(m => `<option value="${m}">${m}</option>`).join('')}
      </select>
    </div>

    <div class="module-table-wrapper">
      <table id="testTable">
        <thead>
          <tr>
            <th style="width: 140px;">Test ID</th>
            <th style="width: 220px;">Module</th>
            <th>Scenario Name</th>
            <th style="width: 180px;">Browser / Engine</th>
            <th style="width: 100px; text-align: center;">Status</th>
            <th style="width: 100px; text-align: center;">Duration</th>
          </tr>
        </thead>
        <tbody>
          ${this.testResults.map(t => `
          <tr data-module="${t.module || 'General'}" data-text="${(t.testId + ' ' + t.scenarioName + ' ' + (t.module || '')).toLowerCase()}">
            <td class="mono" style="font-weight: 700; color: #60a5fa;">${t.testId}</td>
            <td>${t.module || 'General'}</td>
            <td>${t.scenarioName}</td>
            <td class="mono" style="color: var(--text-muted);">${t.browser || 'Engine'}</td>
            <td style="text-align: center;">
              <span class="status-badge ${t.status.toLowerCase()}">${t.status}</span>
            </td>
            <td style="text-align: center;" class="mono">${t.duration || '0.01s'}</td>
          </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  </div>

  <script>
    function filterTests() {
      const query = document.getElementById('searchInput').value.toLowerCase();
      const selectedModule = document.getElementById('moduleFilter').value;
      const rows = document.querySelectorAll('#testTable tbody tr');

      rows.forEach(row => {
        const text = row.getAttribute('data-text');
        const mod = row.getAttribute('data-module');
        const matchesQuery = !query || text.includes(query);
        const matchesModule = selectedModule === 'ALL' || mod === selectedModule;
        row.style.display = (matchesQuery && matchesModule) ? '' : 'none';
      });
    }
  </script>
</body>
</html>`;

    fs.writeFileSync(finalPath, htmlContent, 'utf-8');
    logger.info(`[HtmlReporter] Standalone HTML report generated at: ${finalPath}`);
    return finalPath;
  }

  /**
   * Appends a Markdown summary table to $GITHUB_STEP_SUMMARY
   */
  async appendGitHubStepSummary() {
    const summaryFile = process.env.GITHUB_STEP_SUMMARY;
    if (!summaryFile) {
      return;
    }

    const total = this.testResults.length;
    const passed = this.testResults.filter(t => t.status === 'PASSED').length;
    const failed = this.testResults.filter(t => t.status === 'FAILED').length;
    const skipped = this.testResults.filter(t => t.status === 'SKIPPED').length;
    const passRate = total > 0 ? ((passed / total) * 100).toFixed(2) : '100.00';
    const totalDurationSec = ((new Date() - this.startTime) / 1000).toFixed(2);

    // Group by modules
    const modules = {};
    this.testResults.forEach(t => {
      const mod = t.module || 'General';
      if (!modules[mod]) {
        modules[mod] = { total: 0, passed: 0, failed: 0, skipped: 0 };
      }
      modules[mod].total++;
      if (t.status === 'PASSED') modules[mod].passed++;
      else if (t.status === 'FAILED') modules[mod].failed++;
      else modules[mod].skipped++;
    });

    const statusBadge = failed === 0 ? '🟢 **PASSED (100%)**' : `🔴 **FAILED (${failed} Failures)**`;

    let md = `\n## 📊 ${this.suiteName} Execution Summary\n\n`;
    md += `| Total Tests | Passed | Failed | Skipped | Pass Rate | Duration | Status |\n`;
    md += `| :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n`;
    md += `| **${total}** | **${passed}** | **${failed}** | **${skipped}** | **${passRate}%** | **${totalDurationSec}s** | ${statusBadge} |\n\n`;

    md += `### 📦 Module Breakdown\n\n`;
    md += `| Module | Total | Passed | Failed | Pass Rate |\n`;
    md += `| :--- | :---: | :---: | :---: | :---: |\n`;
    for (const [mod, stats] of Object.entries(modules)) {
      const rate = ((stats.passed / stats.total) * 100).toFixed(1);
      const icon = stats.failed === 0 ? '✅' : '❌';
      md += `| ${icon} **${mod}** | ${stats.total} | ${stats.passed} | ${stats.failed} | **${rate}%** |\n`;
    }
    md += `\n`;

    if (failed > 0) {
      md += `### ❌ Failed Test Cases\n\n`;
      md += `| Test ID | Module | Scenario | Failure Reason |\n`;
      md += `| :--- | :--- | :--- | :--- |\n`;
      this.testResults.filter(t => t.status === 'FAILED').forEach(ft => {
        md += `| \`${ft.testId}\` | ${ft.module} | ${ft.scenarioName} | ${ft.failureReason || 'Unknown error'} |\n`;
      });
      md += `\n`;
    }

    try {
      fs.appendFileSync(summaryFile, md, 'utf-8');
      logger.info(`[HtmlReporter] Successfully appended Step Summary to $GITHUB_STEP_SUMMARY`);
    } catch (err) {
      logger.error(`[HtmlReporter] Failed to append Step Summary: ${err.message}`);
    }
  }
}

module.exports = HtmlReporter;
