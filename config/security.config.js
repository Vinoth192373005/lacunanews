/**
 * Security & Vulnerability Testing Configuration
 * Covers OWASP Top 10, Auth Bypass, SQLi, XSS, CSRF, IDOR, Headers
 */

module.exports = {
  sqliPayloads: [
    "' OR '1'='1",
    "' OR 1=1 --",
    "admin' --",
    "' UNION SELECT null, username, password FROM users --",
    "1; DROP TABLE users;--",
    "' OR 'a'='a",
    "\" OR \"1\"=\"1",
    "'; EXEC xp_cmdshell('dir');--",
    "1' ORDER BY 1--+",
    "1' ORDER BY 10--+"
  ],
  xssPayloads: [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "javascript:alert('XSS')",
    "'\"><script>alert(1)</script>",
    "<iframe src=\"javascript:alert(`xss`)\"></iframe>",
    "<body onload=alert('XSS')>",
    "<input autofocus onfocus=alert(1)>",
    "<details open ontoggle=alert(1)>",
    "'\"><img src=x onerror=alert(document.cookie)>"
  ],
  pathTraversalPayloads: [
    "../../../../etc/passwd",
    "..%2f..%2f..%2f..%2fetc%2fpasswd",
    "..\\..\\..\\windows\\win.ini",
    "....//....//....//etc/passwd",
    "/etc/shadow"
  ],
  sstiPayloads: [
    "{{7*7}}",
    "${7*7}",
    "<%= 7*7 %>",
    "{{config.items()}}",
    "{{''.__class__.__mro__[1].__subclasses__()}}"
  ],
  requiredSecurityHeaders: [
    'x-content-type-options',
    'x-frame-options',
    'referrer-policy'
  ]
};
