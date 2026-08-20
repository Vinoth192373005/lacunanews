# 📑 Master Test Case Catalog (1,200 Automated Test Cases)

This document contains the complete directory of all **1,200 Automated Test Cases** included in the **Master Enterprise QA Report** (`Master_Enterprise_1200_Report.xlsx`).

---

## 📑 Summary of Suites

1. **Selenium Web E2E Suite**: `TC-SEL-001` to `TC-SEL-300` (300 Tests)
2. **Appium Mobile Android Suite**: `TC-APP-001` to `TC-APP-300` (300 Tests)
3. **Vulnerability & Security Suite**: `TC-SEC-001` to `TC-SEC-300` (300 Tests)
4. **Load & Performance Suite**: `TC-LOAD-001` to `TC-LOAD-300` (300 Tests)

---

# 1. 🌐 Selenium Web E2E Test Suite (300 Tests)

### Module 1: Authentication & Session Management (TC-SEL-001 to TC-SEL-050)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEL-001 | Authentication | Redirect user to homepage dashboard on valid authentication |
| TC-SEL-002 | Authentication | Block redirect. Display 'Invalid credentials' error message on empty credentials |
| TC-SEL-003 | Authentication | Redirect user to homepage dashboard on successful user registration |
| TC-SEL-004 | Authentication | Block redirect. Display 'Invalid credentials' on empty password submission |
| TC-SEL-005 | Authentication | Redirect user to homepage dashboard on session cookie persistence |
| TC-SEL-006 | Authentication | Block redirect. Display 'Invalid credentials' on non-existent username |
| TC-SEL-007 | Authentication | Redirect user to homepage dashboard on remembered session state |
| TC-SEL-008 | Authentication | Block redirect. Display 'Invalid credentials' on whitespace credentials |
| TC-SEL-009 | Authentication | Redirect user to homepage dashboard on Google OAuth SSO fallback |
| TC-SEL-010 | Authentication | Block redirect. Display 'Invalid credentials' on password mismatch |
| TC-SEL-011 | Authentication | Block redirect. Display 'Invalid credentials' on empty username |
| TC-SEL-012 | Authentication | Block redirect. Display 'Invalid credentials' on username under minimum length |
| TC-SEL-013 | Authentication | Block redirect. Display 'Invalid credentials' on username exceeding maximum length |
| TC-SEL-014 | Authentication | Block redirect. Display 'Invalid credentials' on single-character password |
| TC-SEL-015 | Authentication | Block redirect. Display 'Invalid credentials' on special symbol username |
| TC-SEL-016 | Authentication | Block redirect. Display 'Invalid credentials' on SQL injection attempt |
| TC-SEL-017 | Authentication | Block redirect. Display 'Invalid credentials' on script tag payload |
| TC-SEL-018 | Authentication | Block redirect. Display 'Invalid credentials' on null literal string |
| TC-SEL-019 | Authentication | Block redirect. Display 'Invalid credentials' on undefined payload |
| TC-SEL-020 | Authentication | Block redirect. Display 'Invalid credentials' on wrong password for existing user |
| TC-SEL-021 | Authentication | Register new user with valid alphanumeric credentials |
| TC-SEL-022 | Authentication | Block registration on duplicate username with user friendly warning |
| TC-SEL-023 | Authentication | Register new user with underscore and dot in username |
| TC-SEL-024 | Authentication | Register new user with complex password containing symbols |
| TC-SEL-025 | Authentication | Block registration on mismatched confirm password |
| TC-SEL-026 | Authentication | Register new user and trim leading/trailing whitespace |
| TC-SEL-027 | Authentication | Register new user and verify empty reading history initialization |
| TC-SEL-028 | Authentication | Register new user and verify empty bookmarks list initialization |
| TC-SEL-029 | Authentication | Register new user and verify default theme preference |
| TC-SEL-030 | Authentication | Register new user and redirect immediately to personalized feed |
| TC-SEL-031 | Authentication | Authenticate valid user and verify session cookie issuance |
| TC-SEL-032 | Authentication | Verify session cookie contains HttpOnly security flag |
| TC-SEL-033 | Authentication | Verify session cookie contains SameSite=Lax/Strict attribute |
| TC-SEL-034 | Authentication | Verify authenticated user can access protected /settings |
| TC-SEL-035 | Authentication | Verify authenticated user can access protected /bookmarks |
| TC-SEL-036 | Authentication | Verify authenticated user can access protected /history |
| TC-SEL-037 | Authentication | Block unauthenticated direct access to /settings |
| TC-SEL-038 | Authentication | Block unauthenticated direct access to /bookmarks |
| TC-SEL-039 | Authentication | Verify session persistence across multiple HTTP requests |
| TC-SEL-040 | Authentication | Verify session state remains valid on page reload |
| TC-SEL-041 | Authentication | Verify /logout POST request invalidates active user session |
| TC-SEL-042 | Authentication | Redirect user to /login or / after successful logout |
| TC-SEL-043 | Authentication | Block back-button caching of protected session pages after logout |
| TC-SEL-044 | Authentication | Verify session cookie is cleared or expired upon logout |
| TC-SEL-045 | Authentication | Verify calling /api/account after logout returns 401 unauthenticated |
| TC-SEL-046 | Authentication | Verify concurrent user logins handled gracefully |
| TC-SEL-047 | Authentication | Verify Google OAuth mock callback handles state parameter |
| TC-SEL-048 | Authentication | Verify password hashing algorithm uses modern cryptography |
| TC-SEL-049 | Authentication | Verify password is never echoed in plain text in response HTML |
| TC-SEL-050 | Authentication | Verify auth headers in response prevent unauthorized caching |

### Module 2: Form Validation & Field Rules (TC-SEL-051 to TC-SEL-100)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEL-051 | Form Validation | Dynamic Crawler: Discover and index root page forms |
| TC-SEL-052 | Form Validation | Dynamic Crawler: Discover and index /login forms |
| TC-SEL-053 | Form Validation | Dynamic Crawler: Discover and index /register forms |
| TC-SEL-054 | Form Validation | Dynamic Crawler: Discover and index /settings forms |
| TC-SEL-055 | Form Validation | Dynamic Crawler: Discover and index /history search forms |
| TC-SEL-056 | Form Validation | Dynamic Crawler: Discover and index /bookmarks search forms |
| TC-SEL-057 | Form Validation | Dynamic Crawler: Discover and index /roundup synthesis forms |
| TC-SEL-058 | Form Validation | Dynamic Crawler: Verify all discovered forms specify valid action URI |
| TC-SEL-059 | Form Validation | Dynamic Crawler: Verify all discovered forms specify valid HTTP method |
| TC-SEL-060 | Form Validation | Dynamic Crawler: Verify all input elements have name attributes |
| TC-SEL-061 | Form Validation | Required validation: Missing username on registration |
| TC-SEL-062 | Form Validation | Required validation: Missing password on registration |
| TC-SEL-063 | Form Validation | Required validation: Missing username on login submit |
| TC-SEL-064 | Form Validation | Required validation: Missing password on login submit |
| TC-SEL-065 | Form Validation | Required validation: Empty search query handled gracefully |
| TC-SEL-066 | Form Validation | Required validation: Empty interest topic submission |
| TC-SEL-067 | Form Validation | Required validation: Empty region code submission |
| TC-SEL-068 | Form Validation | Required validation: Missing cluster ID in synthesis request |
| TC-SEL-069 | Form Validation | Required validation: Null payload in JSON post to /api/interests |
| TC-SEL-070 | Form Validation | Required validation: Null payload in JSON post to /api/bookmarks/toggle |
| TC-SEL-071 | Form Validation | Boundary: Username with minimum 3 characters accepted |
| TC-SEL-072 | Form Validation | Boundary: Username with 2 characters rejected or handled |
| TC-SEL-073 | Form Validation | Boundary: Username with maximum 30 characters accepted |
| TC-SEL-074 | Form Validation | Boundary: Username with 31+ characters rejected or truncated |
| TC-SEL-075 | Form Validation | Boundary: Password with minimum 6 characters accepted |
| TC-SEL-076 | Form Validation | Boundary: Password with 5 characters rejected |
| TC-SEL-077 | Form Validation | Boundary: Password with 128 characters accepted |
| TC-SEL-078 | Form Validation | Boundary: Interest topic with 50 characters accepted |
| TC-SEL-079 | Form Validation | Boundary: Interest topic with 51+ characters handled |
| TC-SEL-080 | Form Validation | Boundary: Search query with 255 characters handled gracefully |
| TC-SEL-081 | Form Validation | Dropdown: Region selector contains US option |
| TC-SEL-082 | Form Validation | Dropdown: Region selector contains UK option |
| TC-SEL-083 | Form Validation | Dropdown: Region selector contains IN option |
| TC-SEL-084 | Form Validation | Dropdown: Region selector contains GLOBAL option |
| TC-SEL-085 | Form Validation | Dropdown: Rejection of invalid region code |
| TC-SEL-086 | Form Validation | Checkbox: Theme dark mode toggle state persistence |
| TC-SEL-087 | Form Validation | Checkbox: Auto-refresh feed checkbox state toggling |
| TC-SEL-088 | Form Validation | Radio: Digest frequency selection (daily / weekly) |
| TC-SEL-089 | Form Validation | Color Swatch: Theme palette one selection |
| TC-SEL-090 | Form Validation | Color Swatch: Theme palette two selection |
| TC-SEL-091 | Form Validation | Accessibility: Form input labels associated via for attribute |
| TC-SEL-092 | Form Validation | Accessibility: Form inputs possess aria-label or title |
| TC-SEL-093 | Form Validation | Accessibility: Submit buttons have accessible name |
| TC-SEL-094 | Form Validation | Accessibility: Error alerts have role="alert" |
| TC-SEL-095 | Form Validation | Validation: Browser native HTML5 constraint validation |
| TC-SEL-096 | Form Validation | Validation: Keyboard Tab navigation reaches all form inputs |
| TC-SEL-097 | Form Validation | Validation: Enter key triggers form submission |
| TC-SEL-098 | Form Validation | Validation: Form reset restores default values |
| TC-SEL-099 | Form Validation | Validation: Disabled form buttons prevent double submit |
| TC-SEL-100 | Form Validation | Validation: Form submission indicators show loading state |

### Module 3: UI Components & Design System (TC-SEL-101 to TC-SEL-150)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEL-101 | UI Components | UI: Brand header contains logo and application title |
| TC-SEL-102 | UI Components | UI: Navigation bar renders Feed link |
| TC-SEL-103 | UI Components | UI: Navigation bar renders Roundups link |
| TC-SEL-104 | UI Components | UI: Navigation bar renders History link |
| TC-SEL-105 | UI Components | UI: Navigation bar renders Bookmarks link |
| TC-SEL-106 | UI Components | UI: Navigation bar renders Settings link |
| TC-SEL-107 | UI Components | UI: Navigation bar renders Login / User profile button |
| TC-SEL-108 | UI Components | UI: Search bar input contains magnifying glass icon / placeholder |
| TC-SEL-109 | UI Components | UI: Region selector dropdown displayed in header |
| TC-SEL-110 | UI Components | UI: Header remains sticky or fixed at top on scroll |
| TC-SEL-111 | UI Components | UI: News cards contain article headline |
| TC-SEL-112 | UI Components | UI: News cards contain source badge |
| TC-SEL-113 | UI Components | UI: News cards contain published timestamp |
| TC-SEL-114 | UI Components | UI: News cards contain summary excerpt |
| TC-SEL-115 | UI Components | UI: News cards contain bookmark action button |
| TC-SEL-116 | UI Components | UI: News cards contain synthesize action button |
| TC-SEL-117 | UI Components | UI: News cards render fallback image when image unavailable |
| TC-SEL-118 | UI Components | UI: Card hover state shows elevation / border highlight |
| TC-SEL-119 | UI Components | UI: Category pills render with distinct badge colors |
| TC-SEL-120 | UI Components | UI: Font family adheres to modern typography design system |
| TC-SEL-121 | UI Components | UI: Login modal renders with dark backdrop overlay |
| TC-SEL-122 | UI Components | UI: Modal closes on backdrop click |
| TC-SEL-123 | UI Components | UI: Modal closes on Escape key press |
| TC-SEL-124 | UI Components | UI: Modal contains distinct close (X) button |
| TC-SEL-125 | UI Components | UI: Modal traps keyboard focus within its dialog |
| TC-SEL-126 | UI Components | UI: Confirmation dialog for Clear All History action |
| TC-SEL-127 | UI Components | UI: Confirmation dialog for Clear All Bookmarks action |
| TC-SEL-128 | UI Components | UI: Delete interest confirmation popup |
| TC-SEL-129 | UI Components | UI: Synthesis progress dialog / overlay displays during AI generation |
| TC-SEL-130 | UI Components | UI: Dialog animations use smooth CSS transitions |
| TC-SEL-131 | UI Components | UI: Toast notification appears on bookmark toggle |
| TC-SEL-132 | UI Components | UI: Toast auto-dismisses after 3-5 seconds |
| TC-SEL-133 | UI Components | UI: Toast contains icon matching alert level |
| TC-SEL-134 | UI Components | UI: Error toast displays on network failure |
| TC-SEL-135 | UI Components | UI: Success toast displays on settings saved |
| TC-SEL-136 | UI Components | UI: Loading spinner renders during async feed fetch |
| TC-SEL-137 | UI Components | UI: Skeleton placeholder cards render before news loads |
| TC-SEL-138 | UI Components | UI: Tooltip appears on theme mode toggle hover |
| TC-SEL-139 | UI Components | UI: Tooltip appears on bookmark icon hover |
| TC-SEL-140 | UI Components | UI: Empty state graphic displays when bookmarks list is empty |
| TC-SEL-141 | UI Components | UI: Desktop viewport (1920x1080) multi-column grid layout |
| TC-SEL-142 | UI Components | UI: Laptop viewport (1366x768) 2-column layout |
| TC-SEL-143 | UI Components | UI: Tablet viewport (768x1024) single-column responsive layout |
| TC-SEL-144 | UI Components | UI: Mobile viewport (375x812) header collapses to hamburger menu |
| TC-SEL-145 | UI Components | UI: Pitch-Black dark mode background color #000000 or #0a0a0a |
| TC-SEL-146 | UI Components | UI: Pitch-Black dark mode text color high contrast #ededed |
| TC-SEL-147 | UI Components | UI: Palette one theme CSS custom properties applied |
| TC-SEL-148 | UI Components | UI: Palette two theme CSS custom properties applied |
| TC-SEL-149 | UI Components | UI: Palette three theme CSS custom properties applied |
| TC-SEL-150 | UI Components | UI: CSS media query prefers-color-scheme support |

### Module 4: Navigation, Routing & History (TC-SEL-151 to TC-SEL-200)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEL-151 | Navigation | Navigation: Direct URL navigation to Feed root / |
| TC-SEL-152 | Navigation | Navigation: Direct URL navigation to /login |
| TC-SEL-153 | Navigation | Navigation: Direct URL navigation to /register |
| TC-SEL-154 | Navigation | Navigation: Direct URL navigation to /settings |
| TC-SEL-155 | Navigation | Navigation: Direct URL navigation to /history |
| TC-SEL-156 | Navigation | Navigation: Direct URL navigation to /bookmarks |
| TC-SEL-157 | Navigation | Navigation: Direct URL navigation to /roundup |
| TC-SEL-158 | Navigation | Navigation: Favicon asset responds with HTTP 200 or 204 |
| TC-SEL-159 | Navigation | Navigation: 404 page returns proper HTTP 404 status |
| TC-SEL-160 | Navigation | Navigation: API cluster endpoint reachable |
| TC-SEL-161 | Navigation | Nav: Active link class applied on Home page |
| TC-SEL-162 | Navigation | Nav: Active link class applied on Roundups page |
| TC-SEL-163 | Navigation | Nav: Active link class applied on History page |
| TC-SEL-164 | Navigation | Nav: Active link class applied on Bookmarks page |
| TC-SEL-165 | Navigation | Nav: Active link class applied on Settings page |
| TC-SEL-166 | Navigation | Nav: Brand logo click navigates to Home from /settings |
| TC-SEL-167 | Navigation | Nav: Brand logo click navigates to Home from /history |
| TC-SEL-168 | Navigation | Nav: Brand logo click navigates to Home from /bookmarks |
| TC-SEL-169 | Navigation | Nav: Brand logo click navigates to Home from /roundup |
| TC-SEL-170 | Navigation | Nav: Brand logo click navigates to Home from /login |
| TC-SEL-171 | Navigation | History: Browser back from /settings returns to / |
| TC-SEL-172 | Navigation | History: Browser forward after back returns to /settings |
| TC-SEL-173 | Navigation | History: Page refresh preserves current theme |
| TC-SEL-174 | Navigation | History: Page refresh preserves active category tab |
| TC-SEL-175 | Navigation | History: Page refresh on /roundup preserves synthesized state |
| TC-SEL-176 | Navigation | History: Page refresh on /history maintains reading entries |
| TC-SEL-177 | Navigation | History: Page refresh on /bookmarks maintains saved items |
| TC-SEL-178 | Navigation | History: PushState updates URL without full page reload |
| TC-SEL-179 | Navigation | History: PopState event updates UI components cleanly |
| TC-SEL-180 | Navigation | History: Scroll position preserved on back navigation |
| TC-SEL-181 | Navigation | Deep Link: Search query via URL /?q=technology |
| TC-SEL-182 | Navigation | Deep Link: Region filter via URL /?region=US |
| TC-SEL-183 | Navigation | Deep Link: Category filter via URL /?cat=business |
| TC-SEL-184 | Navigation | Deep Link: Direct link to specific roundup /roundup/1 |
| TC-SEL-185 | Navigation | Deep Link: Direct link to history search /history?q=space |
| TC-SEL-186 | Navigation | Deep Link: Direct link to bookmarks category /bookmarks?cat=tech |
| TC-SEL-187 | Navigation | Deep Link: Auth return URL parameter /login?next=/settings |
| TC-SEL-188 | Navigation | Deep Link: Escaped special characters in query string |
| TC-SEL-189 | Navigation | Deep Link: Multiple query parameters combined /?q=ai&region=UK |
| TC-SEL-190 | Navigation | Deep Link: Empty query parameter handled as default view |
| TC-SEL-191 | Navigation | Sidebar: Hamburger toggle opens mobile sidebar |
| TC-SEL-192 | Navigation | Sidebar: Clicking backdrop closes sidebar |
| TC-SEL-193 | Navigation | Sidebar: Clicking close button closes sidebar |
| TC-SEL-194 | Navigation | Sidebar: Selecting link in sidebar navigates and closes drawer |
| TC-SEL-195 | Navigation | Sidebar: Swiping from left edge opens sidebar |
| TC-SEL-196 | Navigation | Sidebar: Swiping left closes sidebar |
| TC-SEL-197 | Navigation | Sidebar: Body scroll lock when sidebar is open |
| TC-SEL-198 | Navigation | Sidebar: User info card displayed at top of sidebar |
| TC-SEL-199 | Navigation | Sidebar: Theme toggle switcher inside sidebar |
| TC-SEL-200 | Navigation | Sidebar: Version & copyright footer inside sidebar |

### Module 5: Business Workflows & AI Synthesis (TC-SEL-201 to TC-SEL-250)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEL-201 | Business Workflows | E2E Journey: Anonymous user views feed and reads top story |
| TC-SEL-202 | Business Workflows | E2E Journey: Anonymous user searches for news topic |
| TC-SEL-203 | Business Workflows | E2E Journey: Anonymous user switches region to US |
| TC-SEL-204 | Business Workflows | E2E Journey: Anonymous user switches theme to Pitch-Black |
| TC-SEL-205 | Business Workflows | E2E Journey: User registers account -> Lands on personalized feed |
| TC-SEL-206 | Business Workflows | E2E Journey: Logged in user bookmarks article -> Verified in Bookmarks page |
| TC-SEL-207 | Business Workflows | E2E Journey: Logged in user removes bookmark -> Verified removed |
| TC-SEL-208 | Business Workflows | E2E Journey: Reading article logs entry to Reading History |
| TC-SEL-209 | Business Workflows | E2E Journey: User deletes single history item |
| TC-SEL-210 | Business Workflows | E2E Journey: User clears entire reading history |
| TC-SEL-211 | Business Workflows | Synthesis: Trigger AI briefing synthesis for top news cluster |
| TC-SEL-212 | Business Workflows | Synthesis: Verify executive summary text generation |
| TC-SEL-213 | Business Workflows | Synthesis: Verify bulleted key takeaways list |
| TC-SEL-214 | Business Workflows | Synthesis: Verify multi-source attribution badges |
| TC-SEL-215 | Business Workflows | Synthesis: Verify sentiment / stance analysis indicator |
| TC-SEL-216 | Business Workflows | Synthesis: Verify timeline chronological progression |
| TC-SEL-217 | Business Workflows | Synthesis: Save synthesized briefing to Roundups library |
| TC-SEL-218 | Business Workflows | Synthesis: Audio TTS player controls playback |
| TC-SEL-219 | Business Workflows | Synthesis: Export briefing summary to clipboard |
| TC-SEL-220 | Business Workflows | Synthesis: Share briefing via Web Share API |
| TC-SEL-221 | Business Workflows | Bookmarks: Add article to bookmarks via card button |
| TC-SEL-222 | Business Workflows | Bookmarks: Button icon toggles to filled bookmark state |
| TC-SEL-223 | Business Workflows | Bookmarks: Navigate to /bookmarks and verify item presence |
| TC-SEL-224 | Business Workflows | Bookmarks: Filter bookmarks by category pill |
| TC-SEL-225 | Business Workflows | Bookmarks: Search within saved bookmarks |
| TC-SEL-226 | Business Workflows | Bookmarks: Remove bookmark from bookmarks page |
| TC-SEL-227 | Business Workflows | Bookmarks: Undo bookmark deletion toast action |
| TC-SEL-228 | Business Workflows | Bookmarks: Clear all bookmarks with confirmation dialog |
| TC-SEL-229 | Business Workflows | Bookmarks: Verify empty state illustration when 0 bookmarks |
| TC-SEL-230 | Business Workflows | Bookmarks: Export bookmarks to JSON / OPML |
| TC-SEL-231 | Business Workflows | History: Click article opens modal/link and records history |
| TC-SEL-232 | Business Workflows | History: History entry contains accurate read timestamp |
| TC-SEL-233 | Business Workflows | History: Repeated reads update latest timestamp without duplicates |
| TC-SEL-234 | Business Workflows | History: Group history by date (Today, Yesterday, Older) |
| TC-SEL-235 | Business Workflows | History: Filter history entries by keyword |
| TC-SEL-236 | Business Workflows | History: Delete individual history entry |
| TC-SEL-237 | Business Workflows | History: Clear entire history via API endpoint |
| TC-SEL-238 | Business Workflows | History: History stats counter on Settings page decrements to 0 |
| TC-SEL-239 | Business Workflows | History: Pause reading history tracking option in Settings |
| TC-SEL-240 | Business Workflows | History: Resume reading history tracking |
| TC-SEL-241 | Business Workflows | Sync: Bookmark added in Tab 1 reflects in Tab 2 on focus |
| TC-SEL-242 | Business Workflows | Sync: Theme changed in Tab 1 reflects in Tab 2 |
| TC-SEL-243 | Business Workflows | Sync: User logout in Tab 1 updates session state in Tab 2 |
| TC-SEL-244 | Business Workflows | Sync: LocalStorage updates trigger window storage listener |
| TC-SEL-245 | Business Workflows | Sync: Offline service worker caches latest top stories |
| TC-SEL-246 | Business Workflows | Sync: Online reconnect toast displays when network restored |
| TC-SEL-247 | Business Workflows | Sync: Failed network request shows retry banner |
| TC-SEL-248 | Business Workflows | Sync: Auto-refresh timer fetches latest news in background |
| TC-SEL-249 | Business Workflows | Sync: Unread badge counter updates when new cluster appears |
| TC-SEL-250 | Business Workflows | Sync: Tab title flashes notification on urgent breaking news |

### Module 6: Settings, Preferences & Personalization (TC-SEL-251 to TC-SEL-300)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEL-251 | Settings & Preferences | Settings: Account section displays username badge |
| TC-SEL-252 | Settings & Preferences | Settings: Read count statistic card displays numeric count |
| TC-SEL-253 | Settings & Preferences | Settings: Bookmarks count statistic card displays numeric count |
| TC-SEL-254 | Settings & Preferences | Settings: Account creation date displayed formatted |
| TC-SEL-255 | Settings & Preferences | Settings: User role / subscription tier badge visible |
| TC-SEL-256 | Settings & Preferences | Settings: Back to Feed navigation button returns to home |
| TC-SEL-257 | Settings & Preferences | Settings: Change password form fields render correctly |
| TC-SEL-258 | Settings & Preferences | Settings: Change password enforces old password verification |
| TC-SEL-259 | Settings & Preferences | Settings: Export personal data download JSON button |
| TC-SEL-260 | Settings & Preferences | Settings: Delete account button with confirmation modal |
| TC-SEL-261 | Settings & Preferences | Interests: Add new interest topic "Artificial Intelligence" |
| TC-SEL-262 | Settings & Preferences | Interests: Add new interest topic "Quantum Computing" |
| TC-SEL-263 | Settings & Preferences | Interests: Add new interest topic "Renewable Energy" |
| TC-SEL-264 | Settings & Preferences | Interests: Verify added interest renders as tag badge |
| TC-SEL-265 | Settings & Preferences | Interests: Reject duplicate interest topic entry |
| TC-SEL-266 | Settings & Preferences | Interests: Remove individual interest tag via (X) button |
| TC-SEL-267 | Settings & Preferences | Interests: Clear all interests via clear button |
| TC-SEL-268 | Settings & Preferences | Interests: Interest topics influence feed recommendation weighting |
| TC-SEL-269 | Settings & Preferences | Interests: Pre-populated suggested interest chips |
| TC-SEL-270 | Settings & Preferences | Interests: Click suggested interest chip adds it immediately |
| TC-SEL-271 | Settings & Preferences | Theme: Toggle from Light mode to Pitch-Black dark mode |
| TC-SEL-272 | Settings & Preferences | Theme: Body data-theme attribute set to "pitch-black" |
| TC-SEL-273 | Settings & Preferences | Theme: Toggle back from Pitch-Black to Light mode |
| TC-SEL-274 | Settings & Preferences | Theme: Select Palette One theme swatch |
| TC-SEL-275 | Settings & Preferences | Theme: Body data-theme attribute set to "palette-one" |
| TC-SEL-276 | Settings & Preferences | Theme: Select Palette Two theme swatch |
| TC-SEL-277 | Settings & Preferences | Theme: Body data-theme attribute set to "palette-two" |
| TC-SEL-278 | Settings & Preferences | Theme: Select Palette Three theme swatch |
| TC-SEL-279 | Settings & Preferences | Theme: Body data-theme attribute set to "palette-three" |
| TC-SEL-280 | Settings & Preferences | Theme: Selected theme persists across page reload in localStorage |
| TC-SEL-281 | Settings & Preferences | Region: Select United States (US) region preference |
| TC-SEL-282 | Settings & Preferences | Region: Select United Kingdom (UK) region preference |
| TC-SEL-283 | Settings & Preferences | Region: Select India (IN) region preference |
| TC-SEL-284 | Settings & Preferences | Region: Select Global (GLOBAL) region preference |
| TC-SEL-285 | Settings & Preferences | Region: POST /api/region updates active session preference |
| TC-SEL-286 | Settings & Preferences | Region: Feed updates article sources matching selected region |
| TC-SEL-287 | Settings & Preferences | Region: Region flag / code badge rendered in header |
| TC-SEL-288 | Settings & Preferences | Region: Auto-detect region from browser locale fallback |
| TC-SEL-289 | Settings & Preferences | Region: Invalid region code falls back to default region |
| TC-SEL-290 | Settings & Preferences | Region: Region switch preserved across browser restarts |
| TC-SEL-291 | Settings & Preferences | Prefs: Toggle daily email digest notification preference |
| TC-SEL-292 | Settings & Preferences | Prefs: Toggle breaking news browser push notifications |
| TC-SEL-293 | Settings & Preferences | Prefs: Font size preference selection (Small, Medium, Large) |
| TC-SEL-294 | Settings & Preferences | Prefs: Reading speed WPM setting for estimated read times |
| TC-SEL-295 | Settings & Preferences | Prefs: High contrast mode toggle for accessibility |
| TC-SEL-296 | Settings & Preferences | Prefs: Reduce animations toggle for prefers-reduced-motion |
| TC-SEL-297 | Settings & Preferences | Prefs: Auto-synthesis enable / disable toggle |
| TC-SEL-298 | Settings & Preferences | Prefs: Clear browsing cache button in settings |
| TC-SEL-299 | Settings & Preferences | Prefs: Save Preferences button displays confirmation toast |
| TC-SEL-300 | Settings & Preferences | Prefs: Reset all settings to factory default values |

---

# 2. 📱 Appium Mobile Android E2E Suite (300 Tests)

### Module 1: App Launch, Lifecycle & APK (TC-APP-001 to TC-APP-050)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-APP-001 | App Lifecycle | Mobile: Dynamic connected device discovery (Emulator / Real Device) |
| TC-APP-002 | App Lifecycle | Mobile: Android version detection (Android 10 - 15) |
| TC-APP-003 | App Lifecycle | Mobile: APK package integrity verification com.lacuna.news |
| TC-APP-004 | App Lifecycle | Mobile: Main Activity validation .MainActivity |
| TC-APP-005 | App Lifecycle | Mobile: Automated APK installation via adb / Appium |
| TC-APP-006 | App Lifecycle | Mobile: Support pre-installed application launch |
| TC-APP-007 | App Lifecycle | Mobile: Android permission auto-grant verification |
| TC-APP-008 | App Lifecycle | Mobile: Hardware acceleration enabled in AndroidManifest |
| TC-APP-009 | App Lifecycle | Mobile: Target SDK version 33+ compatibility |
| TC-APP-010 | App Lifecycle | Mobile: App cold start latency within benchmark (< 2.5s) |
| TC-APP-011 | App Lifecycle | Lifecycle: App launches into foreground view |
| TC-APP-012 | App Lifecycle | Lifecycle: App sends to background for 5s and returns to foreground |
| TC-APP-013 | App Lifecycle | Lifecycle: App state preserved after backgrounding |
| TC-APP-014 | App Lifecycle | Lifecycle: App force-stop and cold relaunch |
| TC-APP-015 | App Lifecycle | Lifecycle: Splash screen displays and fades smoothly |
| TC-APP-016 | App Lifecycle | Lifecycle: WebView component loads without crash |
| TC-APP-017 | App Lifecycle | Lifecycle: ProgressBar displays during initial page load |
| TC-APP-018 | App Lifecycle | Lifecycle: ProgressBar hides upon onPageFinished event |
| TC-APP-019 | App Lifecycle | Lifecycle: Device sleep / wake cycle maintains app state |
| TC-APP-020 | App Lifecycle | Lifecycle: App handles low memory warning without termination |
| TC-APP-021 | App Lifecycle | Display: Default portrait mode orientation 1080x2400 |
| TC-APP-022 | App Lifecycle | Display: Rotate device to Landscape mode (90 degrees) |
| TC-APP-023 | App Lifecycle | Display: Web content reflows responsively in landscape |
| TC-APP-024 | App Lifecycle | Display: Rotate device back to Portrait mode |
| TC-APP-025 | App Lifecycle | Display: FitsSystemWindows root layout prevents status bar overlap |
| TC-APP-026 | App Lifecycle | Display: Navigation bar safe insets handling |
| TC-APP-027 | App Lifecycle | Display: Display cutout / notch area padding verification |
| TC-APP-028 | App Lifecycle | Display: High DPI (xxhdpi/xxxhdpi) asset rendering clarity |
| TC-APP-029 | App Lifecycle | Display: Multi-window / Split-screen mode layout test |
| TC-APP-030 | App Lifecycle | Display: Picture-in-picture / floating window resilience |
| TC-APP-031 | App Lifecycle | Network: WiFi connectivity active state validation |
| TC-APP-032 | App Lifecycle | Network: Cellular (4G/5G) mobile data validation |
| TC-APP-033 | App Lifecycle | Network: Airplane mode simulation / network disconnect |
| TC-APP-034 | App Lifecycle | Network: Offline banner displays when connection lost |
| TC-APP-035 | App Lifecycle | Network: Cached articles accessible while offline |
| TC-APP-036 | App Lifecycle | Network: Connection restore triggers automatic sync |
| TC-APP-037 | App Lifecycle | Network: Slow 3G network latency simulation |
| TC-APP-038 | App Lifecycle | Network: Timeout handling on unreachable host |
| TC-APP-039 | App Lifecycle | Network: SSL / TLS certificate validation in WebView |
| TC-APP-040 | App Lifecycle | Network: Cookie synchronization across native & WebView contexts |
| TC-APP-041 | App Lifecycle | Telemetry: App launch time under 2000ms |
| TC-APP-042 | App Lifecycle | Telemetry: CPU utilization during scrolling < 25% |
| TC-APP-043 | App Lifecycle | Telemetry: Native memory consumption < 150MB |
| TC-APP-044 | App Lifecycle | Telemetry: Frame rate maintains smooth 60fps scrolling |
| TC-APP-045 | App Lifecycle | Telemetry: Android logcat capture on test failure |
| TC-APP-046 | App Lifecycle | Telemetry: Anomaly / ANR (Application Not Responding) detection |
| TC-APP-047 | App Lifecycle | Telemetry: Battery drain optimization check |
| TC-APP-048 | App Lifecycle | Telemetry: Native crash dumps saved to reports/failures |
| TC-APP-049 | App Lifecycle | Telemetry: Clean logcat output with zero Fatal Exceptions |
| TC-APP-050 | App Lifecycle | Telemetry: App cleanly uninstalls on teardown if requested |

### Module 2: Mobile Authentication & Session (TC-APP-051 to TC-APP-100)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-APP-051 | Mobile Auth | Mobile Auth: Tap username field brings up virtual soft keyboard |
| TC-APP-052 | Mobile Auth | Mobile Auth: Virtual keyboard auto-capitalization disabled for username |
| TC-APP-053 | Mobile Auth | Mobile Auth: Virtual keyboard shows "Next" action key on username |
| TC-APP-054 | Mobile Auth | Mobile Auth: Tapping "Next" shifts focus to password input |
| TC-APP-055 | Mobile Auth | Mobile Auth: Password input shows password keyboard with mask bullets |
| TC-APP-056 | Mobile Auth | Mobile Auth: Password reveal eye icon toggles clear text visibility |
| TC-APP-057 | Mobile Auth | Mobile Auth: Virtual keyboard shows "Done" / "Go" action key on password |
| TC-APP-058 | Mobile Auth | Mobile Auth: Hiding soft keyboard does not alter form values |
| TC-APP-059 | Mobile Auth | Mobile Auth: Tapping outside form dismisses virtual keyboard |
| TC-APP-060 | Mobile Auth | Mobile Auth: Viewport scrolls up to keep focused input above keyboard |
| TC-APP-061 | Mobile Auth | Mobile Auth: Submit valid mobile user credentials |
| TC-APP-062 | Mobile Auth | Mobile Auth: Reject empty mobile login form |
| TC-APP-063 | Mobile Auth | Mobile Auth: Display validation error tooltip above mobile button |
| TC-APP-064 | Mobile Auth | Mobile Auth: Reject invalid username on mobile |
| TC-APP-065 | Mobile Auth | Mobile Auth: Reject wrong password on mobile |
| TC-APP-066 | Mobile Auth | Mobile Auth: Single-tap login submission |
| TC-APP-067 | Mobile Auth | Mobile Auth: Double-tap on submit button does not duplicate POST |
| TC-APP-068 | Mobile Auth | Mobile Auth: Mobile registration tab switch via touch tap |
| TC-APP-069 | Mobile Auth | Mobile Auth: Register new user on mobile device |
| TC-APP-070 | Mobile Auth | Mobile Auth: Auto-fill credentials via Android autofill service |
| TC-APP-071 | Mobile Auth | Mobile Session: Android CookieManager accepts session cookie |
| TC-APP-072 | Mobile Auth | Mobile Session: Third-party cookies handled per policy |
| TC-APP-073 | Mobile Auth | Mobile Session: Session retained after navigating to external link |
| TC-APP-074 | Mobile Auth | Mobile Session: Session retained after app background / resume |
| TC-APP-075 | Mobile Auth | Mobile Session: Session retained across app relaunch |
| TC-APP-076 | Mobile Auth | Mobile Session: Mobile logout clears local WebView cookies |
| TC-APP-077 | Mobile Auth | Mobile Session: Mobile logout redirects to guest feed |
| TC-APP-078 | Mobile Auth | Mobile Session: Biometric touch ID / face unlock mock prompt |
| TC-APP-079 | Mobile Auth | Mobile Session: Session expiration displays re-auth dialog |
| TC-APP-080 | Mobile Auth | Mobile Session: Secure storage of local auth tokens |
| TC-APP-081 | Mobile Auth | Mobile SSO: Tap Google SSO button on mobile screen |
| TC-APP-082 | Mobile Auth | Mobile SSO: Custom tabs / OAuth webview intent launched |
| TC-APP-083 | Mobile Auth | Mobile SSO: Deep link redirect callback to app scheme |
| TC-APP-084 | Mobile Auth | Mobile SSO: OAuth token exchange completes successfully |
| TC-APP-085 | Mobile Auth | Mobile SSO: User profile auto-populated from OAuth profile |
| TC-APP-086 | Mobile Auth | Mobile SSO: Cancel OAuth return gracefully to login screen |
| TC-APP-087 | Mobile Auth | Mobile SSO: No internet during OAuth displays retry prompt |
| TC-APP-088 | Mobile Auth | Mobile SSO: OAuth error handling on invalid state token |
| TC-APP-089 | Mobile Auth | Mobile SSO: Multiple account chooser dialog |
| TC-APP-090 | Mobile Auth | Mobile SSO: Account linking between password and SSO login |
| TC-APP-091 | Mobile Auth | Mobile Security: Screenshot prevention in secure app mode |
| TC-APP-092 | Mobile Auth | Mobile Security: Clear cache on user logout |
| TC-APP-093 | Mobile Auth | Mobile Security: Clear DOM storage on user logout |
| TC-APP-094 | Mobile Auth | Mobile Security: Jailbreak / Root detection warning check |
| TC-APP-095 | Mobile Auth | Mobile Security: WebView JavaScript interface isolation |
| TC-APP-096 | Mobile Auth | Mobile Security: In-app PIN code lock entry |
| TC-APP-097 | Mobile Auth | Mobile Security: 5 failed PIN attempts locks for 30 seconds |
| TC-APP-098 | Mobile Auth | Mobile Security: Mask app thumbnail in Android recent apps switcher |
| TC-APP-099 | Mobile Auth | Mobile Security: TLS 1.3 encryption for all network traffic |
| TC-APP-100 | Mobile Auth | Mobile Security: Encrypted SharedPreferences validation |

### Module 3: Touch Gestures & Interactivity (TC-APP-101 to TC-APP-150)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-APP-101 | Touch Gestures | Gestures: Single tap on news card opens article modal / detail |
| TC-APP-102 | Touch Gestures | Gestures: Single tap on bookmark icon toggles bookmark |
| TC-APP-103 | Touch Gestures | Gestures: Single tap on region dropdown opens bottom sheet picker |
| TC-APP-104 | Touch Gestures | Gestures: Double tap on article card triggers quick like / bookmark |
| TC-APP-105 | Touch Gestures | Gestures: Double tap on image triggers zoom in 2x |
| TC-APP-106 | Touch Gestures | Gestures: Double tap on zoomed image triggers zoom reset |
| TC-APP-107 | Touch Gestures | Gestures: Long press (800ms) on news card opens context menu |
| TC-APP-108 | Touch Gestures | Gestures: Long press context menu contains "Read Later", "Share", "Hide" |
| TC-APP-109 | Touch Gestures | Gestures: Long press on interest tag enters edit / reorder mode |
| TC-APP-110 | Touch Gestures | Gestures: Touch feedback / ripple animation on button press |
| TC-APP-111 | Touch Gestures | Gestures: Swipe Up (Fling scroll down) through 20 articles |
| TC-APP-112 | Touch Gestures | Gestures: Fast fling scrolling maintains smooth 60fps frame rate |
| TC-APP-113 | Touch Gestures | Gestures: Momentum scrolling deceleration physics |
| TC-APP-114 | Touch Gestures | Gestures: Swipe Down at top of feed triggers Pull-to-Refresh |
| TC-APP-115 | Touch Gestures | Gestures: Pull-to-refresh spinner rotates smoothly |
| TC-APP-116 | Touch Gestures | Gestures: Pull-to-refresh releases and updates feed with fresh articles |
| TC-APP-117 | Touch Gestures | Gestures: Scroll-to-top floating FAB button appears after scrolling 500px |
| TC-APP-118 | Touch Gestures | Gestures: Tap scroll-to-top FAB smoothly scrolls back to top |
| TC-APP-119 | Touch Gestures | Gestures: Infinite scroll threshold loads next page when near bottom |
| TC-APP-120 | Touch Gestures | Gestures: Scroll position restored when returning from article view |
| TC-APP-121 | Touch Gestures | Gestures: Swipe Left on category tab bar switches category |
| TC-APP-122 | Touch Gestures | Gestures: Swipe Right on category tab bar returns to previous category |
| TC-APP-123 | Touch Gestures | Gestures: Swipe Left on article card in history removes item |
| TC-APP-124 | Touch Gestures | Gestures: Swipe Right on article card reveals bookmark shortcut |
| TC-APP-125 | Touch Gestures | Gestures: Horizontal carousel swiping between top briefing stories |
| TC-APP-126 | Touch Gestures | Gestures: Carousel pagination dots update on swipe |
| TC-APP-127 | Touch Gestures | Gestures: Edge swipe from left screen bezel opens navigation drawer |
| TC-APP-128 | Touch Gestures | Gestures: Edge swipe from right screen bezel triggers Android back |
| TC-APP-129 | Touch Gestures | Gestures: Tab bar auto-scrolls to keep selected category centered |
| TC-APP-130 | Touch Gestures | Gestures: Snapping behavior on carousel item alignment |
| TC-APP-131 | Touch Gestures | Gestures: Two-finger Pinch Out (Zoom In) on infographic |
| TC-APP-132 | Touch Gestures | Gestures: Two-finger Pinch In (Zoom Out) to fit viewport |
| TC-APP-133 | Touch Gestures | Gestures: Multi-touch rejection of unintended palm contacts |
| TC-APP-134 | Touch Gestures | Gestures: Pan across zoomed image with single finger |
| TC-APP-135 | Touch Gestures | Gestures: Zoom scale clamped between 1.0x and 4.0x |
| TC-APP-136 | Touch Gestures | Gestures: Pinch-to-close on expanded modal dialog |
| TC-APP-137 | Touch Gestures | Gestures: Multi-finger gesture support in canvas / chart views |
| TC-APP-138 | Touch Gestures | Gestures: Text selection handles draggable on mobile |
| TC-APP-139 | Touch Gestures | Gestures: Copy text to Android clipboard via selection toolbar |
| TC-APP-140 | Touch Gestures | Gestures: Share selected text intent via Android share sheet |
| TC-APP-141 | Touch Gestures | Gestures: Long press and drag interest topic tag to reorder |
| TC-APP-142 | Touch Gestures | Gestures: Drag topic card into priority feed zone |
| TC-APP-143 | Touch Gestures | Gestures: Drag article card into reading list folder |
| TC-APP-144 | Touch Gestures | Gestures: Drag to dismiss snackbar notification |
| TC-APP-145 | Touch Gestures | Gestures: Drag bottom sheet handle up to expand full screen |
| TC-APP-146 | Touch Gestures | Gestures: Drag bottom sheet handle down to half-expanded state |
| TC-APP-147 | Touch Gestures | Gestures: Drag bottom sheet down past threshold to close |
| TC-APP-148 | Touch Gestures | Gestures: Touch target minimum size satisfies 48x48dp standard |
| TC-APP-149 | Touch Gestures | Gestures: Haptic feedback vibration on successful drag drop |
| TC-APP-150 | Touch Gestures | Gestures: Smooth spring animations upon gesture release |

### Module 4: Mobile Form Validation & Rules (TC-APP-151 to TC-APP-200)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-APP-151 | Mobile Forms | Mobile Form: Required field validation indicator displayed on mobile |
| TC-APP-152 | Mobile Forms | Mobile Form: Input field focus border color changes to accent blue |
| TC-APP-153 | Mobile Forms | Mobile Form: Clear text (X) icon inside mobile search input |
| TC-APP-154 | Mobile Forms | Mobile Form: Tapping clear (X) icon empties search field |
| TC-APP-155 | Mobile Forms | Mobile Form: Number keyboard triggered on numeric inputs |
| TC-APP-156 | Mobile Forms | Mobile Form: Email keyboard with @ key triggered on email inputs |
| TC-APP-157 | Mobile Forms | Mobile Form: URL keyboard with .com key triggered on URL inputs |
| TC-APP-158 | Mobile Forms | Mobile Form: Search keyboard with search magnifying icon on enter |
| TC-APP-159 | Mobile Forms | Mobile Form: Auto-correction disabled for password and code fields |
| TC-APP-160 | Mobile Forms | Mobile Form: Maxlength constraint enforces character limit on mobile |
| TC-APP-161 | Mobile Forms | Mobile Form: Invalid form submission displays bottom Snackbar |
| TC-APP-162 | Mobile Forms | Mobile Form: Snackbar stays anchored above bottom navigation bar |
| TC-APP-163 | Mobile Forms | Mobile Form: Snackbar contains "DISMISS" action button |
| TC-APP-164 | Mobile Forms | Mobile Form: Inline error label beneath invalid input field |
| TC-APP-165 | Mobile Forms | Mobile Form: Input border turns red on validation failure |
| TC-APP-166 | Mobile Forms | Mobile Form: Typing valid text immediately clears error state |
| TC-APP-167 | Mobile Forms | Mobile Form: Shake animation on failed form submission |
| TC-APP-168 | Mobile Forms | Mobile Form: Screen reader reads error description via TalkBack |
| TC-APP-169 | Mobile Forms | Mobile Form: Error alert does not clip on small screens (320px) |
| TC-APP-170 | Mobile Forms | Mobile Form: Auto-scroll to first invalid input field |
| TC-APP-171 | Mobile Forms | Mobile Form: Native / Web date picker dialog for history filter |
| TC-APP-172 | Mobile Forms | Mobile Form: Select date range in mobile calendar sheet |
| TC-APP-173 | Mobile Forms | Mobile Form: Confirm date selection updates list immediately |
| TC-APP-174 | Mobile Forms | Mobile Form: Cancel date selection preserves previous range |
| TC-APP-175 | Mobile Forms | Mobile Form: Region selection bottom sheet modal |
| TC-APP-176 | Mobile Forms | Mobile Form: Radio button tap target satisfies touch accessibility |
| TC-APP-177 | Mobile Forms | Mobile Form: Toggle switch for dark mode with haptic feedback |
| TC-APP-178 | Mobile Forms | Mobile Form: Toggle switch for push notifications |
| TC-APP-179 | Mobile Forms | Mobile Form: Font size slider adjustment on mobile |
| TC-APP-180 | Mobile Forms | Mobile Form: Slider value label updates dynamically on drag |
| TC-APP-181 | Mobile Forms | Mobile Form: Input emoji characters in search query 🚀 📰 |
| TC-APP-182 | Mobile Forms | Mobile Form: Input accented characters (é, ü, ñ, ç) |
| TC-APP-183 | Mobile Forms | Mobile Form: Input Asian characters (Japanese, Chinese, Korean) |
| TC-APP-184 | Mobile Forms | Mobile Form: Input Right-to-Left (Arabic, Hebrew) text |
| TC-APP-185 | Mobile Forms | Mobile Form: Input mathematical symbols (∑, √, π) |
| TC-APP-186 | Mobile Forms | Mobile Form: Input currency symbols (€, £, ¥, ₹) |
| TC-APP-187 | Mobile Forms | Mobile Form: Pasting text from Android clipboard into input |
| TC-APP-188 | Mobile Forms | Mobile Form: Cutting text to Android clipboard |
| TC-APP-189 | Mobile Forms | Mobile Form: Multiline textarea expands gracefully with text |
| TC-APP-190 | Mobile Forms | Mobile Form: Max lines limit on textarea with scroll bar |
| TC-APP-191 | Mobile Forms | Mobile Form: Submit form under poor network connection |
| TC-APP-192 | Mobile Forms | Mobile Form: Submit button disabled and shows spinner during POST |
| TC-APP-193 | Mobile Forms | Mobile Form: Network timeout during submit shows retry dialog |
| TC-APP-194 | Mobile Forms | Mobile Form: Backgrounding app during form POST resumes cleanly |
| TC-APP-195 | Mobile Forms | Mobile Form: Rotating device while filling form preserves input state |
| TC-APP-196 | Mobile Forms | Mobile Form: Form draft saved locally in IndexedDB / localStorage |
| TC-APP-197 | Mobile Forms | Mobile Form: App crash recovery restores unsaved form draft |
| TC-APP-198 | Mobile Forms | Mobile Form: Discard draft button clears local storage form cache |
| TC-APP-199 | Mobile Forms | Mobile Form: Form success toast with checkmark icon |
| TC-APP-200 | Mobile Forms | Mobile Form: Reset form clears all validation error states |

### Module 5: Mobile Navigation, Drawer & Views (TC-APP-201 to TC-APP-250)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-APP-201 | Mobile Navigation | Bottom Nav: Bottom navigation bar visible at base of mobile screen |
| TC-APP-202 | Mobile Navigation | Bottom Nav: Feed icon and label in bottom bar |
| TC-APP-203 | Mobile Navigation | Bottom Nav: Roundups icon and label in bottom bar |
| TC-APP-204 | Mobile Navigation | Bottom Nav: Bookmarks icon and label in bottom bar |
| TC-APP-205 | Mobile Navigation | Bottom Nav: History icon and label in bottom bar |
| TC-APP-206 | Mobile Navigation | Bottom Nav: Settings icon and label in bottom bar |
| TC-APP-207 | Mobile Navigation | Bottom Nav: Tap Feed icon transitions view to Main Feed |
| TC-APP-208 | Mobile Navigation | Bottom Nav: Tap Roundups icon transitions view to Roundups |
| TC-APP-209 | Mobile Navigation | Bottom Nav: Tap Bookmarks icon transitions view to Bookmarks |
| TC-APP-210 | Mobile Navigation | Bottom Nav: Tap History icon transitions view to History |
| TC-APP-211 | Mobile Navigation | Drawer: Tap hamburger button slides out side navigation drawer |
| TC-APP-212 | Mobile Navigation | Drawer: Drawer scrim darkens background view |
| TC-APP-213 | Mobile Navigation | Drawer: Drawer header displays current user profile / avatar |
| TC-APP-214 | Mobile Navigation | Drawer: Drawer contains links to all primary application sections |
| TC-APP-215 | Mobile Navigation | Drawer: Quick region switcher embedded in navigation drawer |
| TC-APP-216 | Mobile Navigation | Drawer: Quick theme toggle embedded in navigation drawer |
| TC-APP-217 | Mobile Navigation | Drawer: Tap backdrop scrim closes drawer with slide-out animation |
| TC-APP-218 | Mobile Navigation | Drawer: Swipe left anywhere on drawer closes drawer |
| TC-APP-219 | Mobile Navigation | Drawer: Selecting any drawer link navigates and closes drawer |
| TC-APP-220 | Mobile Navigation | Drawer: Version number and terms link displayed at bottom of drawer |
| TC-APP-221 | Mobile Navigation | Hardware Back: Press Android back button closes open modal dialog |
| TC-APP-222 | Mobile Navigation | Hardware Back: Press Android back button closes open drawer |
| TC-APP-223 | Mobile Navigation | Hardware Back: Press Android back button closes open search keyboard |
| TC-APP-224 | Mobile Navigation | Hardware Back: Press Android back button from Settings returns to Feed |
| TC-APP-225 | Mobile Navigation | Hardware Back: Press Android back button from Bookmarks returns to Feed |
| TC-APP-226 | Mobile Navigation | Hardware Back: Press Android back button from History returns to Feed |
| TC-APP-227 | Mobile Navigation | Hardware Back: Press Android back button on Home feed shows "Press back again to exit" toast |
| TC-APP-228 | Mobile Navigation | Hardware Back: Double tap Android back within 2s minimizes app |
| TC-APP-229 | Mobile Navigation | Hardware Back: Edge back gesture on Android 10+ navigates back |
| TC-APP-230 | Mobile Navigation | Hardware Back: WebView canGoBack history stack integrity |
| TC-APP-231 | Mobile Navigation | Deep Links: Launch app with intent scheme lacuna://feed |
| TC-APP-232 | Mobile Navigation | Deep Links: Launch app with intent scheme lacuna://roundup/1 |
| TC-APP-233 | Mobile Navigation | Deep Links: Launch app with intent scheme lacuna://settings |
| TC-APP-234 | Mobile Navigation | Deep Links: Launch app with intent scheme lacuna://bookmarks |
| TC-APP-235 | Mobile Navigation | Deep Links: Launch app with HTTPS app link https://lacuna.app/roundup |
| TC-APP-236 | Mobile Navigation | Deep Links: Handle invalid deep link with fallback to Home feed |
| TC-APP-237 | Mobile Navigation | Deep Links: Deep link with query parameter opens filtered view |
| TC-APP-238 | Mobile Navigation | Deep Links: Deep link while unauthenticated prompts login then redirects |
| TC-APP-239 | Mobile Navigation | Deep Links: adb shell am start -d intent verification |
| TC-APP-240 | Mobile Navigation | Deep Links: Android App Links domain verification (assetlinks.json) |
| TC-APP-241 | Mobile Navigation | Transitions: Shared element transition from card thumbnail to article view |
| TC-APP-242 | Mobile Navigation | Transitions: Slide right transition on forward page navigation |
| TC-APP-243 | Mobile Navigation | Transitions: Slide left transition on back navigation |
| TC-APP-244 | Mobile Navigation | Transitions: Fade transition between bottom navigation tabs |
| TC-APP-245 | Mobile Navigation | Transitions: Elevation shadow on active navigation bar |
| TC-APP-246 | Mobile Navigation | Transitions: Tab badge indicator displays number of unread items |
| TC-APP-247 | Mobile Navigation | Transitions: Tab badge clears upon tapping the tab |
| TC-APP-248 | Mobile Navigation | Transitions: Smooth collapse of topbar on scroll down |
| TC-APP-249 | Mobile Navigation | Transitions: Immediate expansion of topbar on scroll up |
| TC-APP-250 | Mobile Navigation | Transitions: 60fps frame timing verification during transitions |

### Module 6: Mobile AI Discovery & Workflows (TC-APP-251 to TC-APP-300)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-APP-251 | Mobile AI & Workflows | Smart AI: Traversal of Android view hierarchy XML tree |
| TC-APP-252 | Mobile AI & Workflows | Smart AI: Automated identification of interactive Button elements |
| TC-APP-253 | Mobile AI & Workflows | Smart AI: Automated identification of editable EditText / Input elements |
| TC-APP-254 | Mobile AI & Workflows | Smart AI: Automated identification of RecyclerView / ListView items |
| TC-APP-255 | Mobile AI & Workflows | Smart AI: Automated identification of Modal Dialogs & Sheets |
| TC-APP-256 | Mobile AI & Workflows | Smart AI: Dynamic test scenario generation from discovered form fields |
| TC-APP-257 | Mobile AI & Workflows | Smart AI: Automatic detection of missing accessibility labels (contentDescription) |
| TC-APP-258 | Mobile AI & Workflows | Smart AI: Automatic detection of touch targets smaller than 48dp |
| TC-APP-259 | Mobile AI & Workflows | Smart AI: Automatic navigation path graph generation |
| TC-APP-260 | Mobile AI & Workflows | Smart AI: Flutter widget finder integration (byValueKey, bySemanticsLabel) |
| TC-APP-261 | Mobile AI & Workflows | Mobile E2E: Launch App -> Guest Feed -> Read Article -> Background App |
| TC-APP-262 | Mobile AI & Workflows | Mobile E2E: Resume App -> Register New Account -> Land on Feed |
| TC-APP-263 | Mobile AI & Workflows | Mobile E2E: Search news by keyword -> Tap result -> Add Bookmark |
| TC-APP-264 | Mobile AI & Workflows | Mobile E2E: Open Bookmarks tab -> Verify saved article displays |
| TC-APP-265 | Mobile AI & Workflows | Mobile E2E: Open Settings -> Add Interest "Aerospace" -> Verify tag |
| TC-APP-266 | Mobile AI & Workflows | Mobile E2E: Open Roundups tab -> Trigger AI synthesis -> Read briefing |
| TC-APP-267 | Mobile AI & Workflows | Mobile E2E: Share synthesized briefing via Android Intent Share Sheet |
| TC-APP-268 | Mobile AI & Workflows | Mobile E2E: Open History tab -> Remove single history item via swipe |
| TC-APP-269 | Mobile AI & Workflows | Mobile E2E: Toggle OLED Pitch-Black dark mode in Settings |
| TC-APP-270 | Mobile AI & Workflows | Mobile E2E: Logout from Settings -> Return to Guest Feed state |
| TC-APP-271 | Mobile AI & Workflows | Mobile Storage: Local database cache initializes upon first run |
| TC-APP-272 | Mobile AI & Workflows | Mobile Storage: Latest 50 articles cached for offline reading |
| TC-APP-273 | Mobile AI & Workflows | Mobile Storage: Offline bookmarks queued for sync when reconnecting |
| TC-APP-274 | Mobile AI & Workflows | Mobile Storage: Offline reading history logs timestamp locally |
| TC-APP-275 | Mobile AI & Workflows | Mobile Storage: Network reconnect syncs offline bookmarks with server |
| TC-APP-276 | Mobile AI & Workflows | Mobile Storage: Network reconnect syncs reading history with server |
| TC-APP-277 | Mobile AI & Workflows | Mobile Storage: Conflict resolution favors newest timestamp |
| TC-APP-278 | Mobile AI & Workflows | Mobile Storage: Clear local cache frees internal storage space |
| TC-APP-279 | Mobile AI & Workflows | Mobile Storage: Storage quota limit management (< 50MB footprint) |
| TC-APP-280 | Mobile AI & Workflows | Mobile Storage: Corrupt cache auto-recovery mechanism |
| TC-APP-281 | Mobile AI & Workflows | Mobile Media: Audio player initializes for synthesized news briefings |
| TC-APP-282 | Mobile AI & Workflows | Mobile Media: Tap play starts TTS audio playback |
| TC-APP-283 | Mobile AI & Workflows | Mobile Media: Tap pause pauses audio playback |
| TC-APP-284 | Mobile AI & Workflows | Mobile Media: Audio seekbar drag updates current position |
| TC-APP-285 | Mobile AI & Workflows | Mobile Media: Audio playback speed control (1x, 1.25x, 1.5x, 2x) |
| TC-APP-286 | Mobile AI & Workflows | Mobile Media: Background audio playback continues when screen locked |
| TC-APP-287 | Mobile AI & Workflows | Mobile Media: Lock screen media notification with controls |
| TC-APP-288 | Mobile AI & Workflows | Mobile Media: Audio focus handling when phone call received |
| TC-APP-289 | Mobile AI & Workflows | Mobile Media: Bluetooth headset connect/disconnect pause behavior |
| TC-APP-290 | Mobile AI & Workflows | Mobile Media: Audio completion event resets player to beginning |
| TC-APP-291 | Mobile AI & Workflows | Mobile Push: Request notification permission on Android 13+ |
| TC-APP-292 | Mobile AI & Workflows | Mobile Push: FCM registration token generated successfully |
| TC-APP-293 | Mobile AI & Workflows | Mobile Push: Receive breaking news push notification in notification shade |
| TC-APP-294 | Mobile AI & Workflows | Mobile Push: Tap notification opens associated article detail view |
| TC-APP-295 | Mobile AI & Workflows | Mobile Push: Notification channel categories (Breaking, Daily Digest) |
| TC-APP-296 | Mobile AI & Workflows | Mobile Push: User can mute specific notification channels in Settings |
| TC-APP-297 | Mobile AI & Workflows | Mobile Push: Rich notification with image preview banner |
| TC-APP-298 | Mobile AI & Workflows | Mobile Push: Quick action buttons on notification ("Save", "Read") |
| TC-APP-299 | Mobile AI & Workflows | Mobile Push: App badge counter updates with unread notifications |
| TC-APP-300 | Mobile AI & Workflows | Mobile Push: Notification dismissal does not affect unread status |

---

# 3. 🛡️ Vulnerability & Security Test Suite (300 Tests)

### Module 1: OWASP Injection Attacks (TC-SEC-001 to TC-SEC-050)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEC-001 | SQL Injection | SQLi Test: Login Username with payload "' OR '1'='1" |
| TC-SEC-002 | SQL Injection | SQLi Test: Login Username with payload "' OR 1=1 --" |
| TC-SEC-003 | SQL Injection | SQLi Test: Login Username with payload "admin' --" |
| TC-SEC-004 | SQL Injection | SQLi Test: Login Username with payload "' UNION SELECT null, username, password FROM users --" |
| TC-SEC-005 | SQL Injection | SQLi Test: Login Username with payload "1; DROP TABLE users;--" |
| TC-SEC-006 | SQL Injection | SQLi Test: Login Password with payload "' OR '1'='1" |
| TC-SEC-007 | SQL Injection | SQLi Test: Login Password with payload "' OR 1=1 --" |
| TC-SEC-008 | SQL Injection | SQLi Test: Login Password with payload "admin' --" |
| TC-SEC-009 | SQL Injection | SQLi Test: Login Password with payload "' UNION SELECT null, username, password FROM users --" |
| TC-SEC-010 | SQL Injection | SQLi Test: Login Password with payload "1; DROP TABLE users;--" |
| TC-SEC-011 | SQL Injection | SQLi Test: Search Query with payload "' OR '1'='1" |
| TC-SEC-012 | SQL Injection | SQLi Test: Search Query with payload "' OR 1=1 --" |
| TC-SEC-013 | SQL Injection | SQLi Test: Search Query with payload "admin' --" |
| TC-SEC-014 | SQL Injection | SQLi Test: Search Query with payload "' UNION SELECT null, username, password FROM users --" |
| TC-SEC-015 | SQL Injection | SQLi Test: Search Query with payload "1; DROP TABLE users;--" |
| TC-SEC-016 | SQL Injection | SQLi Test: API Cluster Filter with payload "' OR '1'='1" |
| TC-SEC-017 | SQL Injection | SQLi Test: API Cluster Filter with payload "' OR 1=1 --" |
| TC-SEC-018 | SQL Injection | SQLi Test: API Cluster Filter with payload "admin' --" |
| TC-SEC-019 | SQL Injection | SQLi Test: API Cluster Filter with payload "' UNION SELECT null, username, password FROM users --" |
| TC-SEC-020 | SQL Injection | SQLi Test: API Cluster Filter with payload "1; DROP TABLE users;--" |
| TC-SEC-021 | SQL Injection | SQLi Test: History Delete ID with payload "' OR '1'='1" |
| TC-SEC-022 | SQL Injection | SQLi Test: History Delete ID with payload "' OR 1=1 --" |
| TC-SEC-023 | SQL Injection | SQLi Test: History Delete ID with payload "admin' --" |
| TC-SEC-024 | SQL Injection | SQLi Test: History Delete ID with payload "' UNION SELECT null, username, password FROM users --" |
| TC-SEC-025 | SQL Injection | SQLi Test: History Delete ID with payload "1; DROP TABLE users;--" |
| TC-SEC-026 | XSS & Template Injection | XSS / SSTI Test: Search Param Reflected XSS with payload "<script>alert('XSS')</script>" |
| TC-SEC-027 | XSS & Template Injection | XSS / SSTI Test: Search Param Reflected XSS with payload "<img src=x onerror=alert('XSS')>" |
| TC-SEC-028 | XSS & Template Injection | XSS / SSTI Test: Search Param Reflected XSS with payload "<svg onload=alert('XSS')>" |
| TC-SEC-029 | XSS & Template Injection | XSS / SSTI Test: Search Param Reflected XSS with payload "javascript:alert('XSS')" |
| TC-SEC-030 | XSS & Template Injection | XSS / SSTI Test: Search Param Reflected XSS with payload "'\"><script>alert(1)</script>" |
| TC-SEC-031 | XSS & Template Injection | XSS / SSTI Test: Interest Topic Stored XSS with payload "<script>alert('XSS')</script>" |
| TC-SEC-032 | XSS & Template Injection | XSS / SSTI Test: Interest Topic Stored XSS with payload "<img src=x onerror=alert('XSS')>" |
| TC-SEC-033 | XSS & Template Injection | XSS / SSTI Test: Interest Topic Stored XSS with payload "<svg onload=alert('XSS')>" |
| TC-SEC-034 | XSS & Template Injection | XSS / SSTI Test: Interest Topic Stored XSS with payload "javascript:alert('XSS')" |
| TC-SEC-035 | XSS & Template Injection | XSS / SSTI Test: Interest Topic Stored XSS with payload "'\"><script>alert(1)</script>" |
| TC-SEC-036 | XSS & Template Injection | XSS / SSTI Test: Region Code Injection with payload "<script>alert('XSS')</script>" |
| TC-SEC-037 | XSS & Template Injection | XSS / SSTI Test: Region Code Injection with payload "<img src=x onerror=alert('XSS')>" |
| TC-SEC-038 | XSS & Template Injection | XSS / SSTI Test: Region Code Injection with payload "<svg onload=alert('XSS')>" |
| TC-SEC-039 | XSS & Template Injection | XSS / SSTI Test: Region Code Injection with payload "javascript:alert('XSS')" |
| TC-SEC-040 | XSS & Template Injection | XSS / SSTI Test: Region Code Injection with payload "'\"><script>alert(1)</script>" |
| TC-SEC-041 | XSS & Template Injection | XSS / SSTI Test: Register Username XSS with payload "<script>alert('XSS')</script>" |
| TC-SEC-042 | XSS & Template Injection | XSS / SSTI Test: Register Username XSS with payload "<img src=x onerror=alert('XSS')>" |
| TC-SEC-043 | XSS & Template Injection | XSS / SSTI Test: Register Username XSS with payload "<svg onload=alert('XSS')>" |
| TC-SEC-044 | XSS & Template Injection | XSS / SSTI Test: Register Username XSS with payload "javascript:alert('XSS')" |
| TC-SEC-045 | XSS & Template Injection | XSS / SSTI Test: Register Username XSS with payload "'\"><script>alert(1)</script>" |
| TC-SEC-046 | XSS & Template Injection | XSS / SSTI Test: Bookmark Notes XSS with payload "<script>alert('XSS')</script>" |
| TC-SEC-047 | XSS & Template Injection | XSS / SSTI Test: Bookmark Notes XSS with payload "<img src=x onerror=alert('XSS')>" |
| TC-SEC-048 | XSS & Template Injection | XSS / SSTI Test: Bookmark Notes XSS with payload "<svg onload=alert('XSS')>" |
| TC-SEC-049 | XSS & Template Injection | XSS / SSTI Test: Bookmark Notes XSS with payload "javascript:alert('XSS')" |
| TC-SEC-050 | XSS & Template Injection | XSS / SSTI Test: Bookmark Notes XSS with payload "'\"><script>alert(1)</script>" |

### Module 2: Authentication & Session Security (TC-SEC-051 to TC-SEC-100)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEC-051 | Cookie Flags | Cookie Security: Session cookie has HttpOnly flag enabled |
| TC-SEC-052 | Cookie Flags | Cookie Security: Session cookie has SameSite=Lax or SameSite=Strict |
| TC-SEC-053 | Cookie Flags | Cookie Security: Cookie path scoped to root / |
| TC-SEC-054 | Cookie Flags | Cookie Security: Cookie domain does not expose wildcard subdomains |
| TC-SEC-055 | Cookie Flags | Cookie Security: Session cookie expires on browser close or reasonable TTL |
| TC-SEC-056 | Cookie Flags | Cookie Security: Cookie value has sufficient entropy (min 128 bits) |
| TC-SEC-057 | Cookie Flags | Cookie Security: Multiple Set-Cookie headers do not conflict |
| TC-SEC-058 | Cookie Flags | Cookie Security: Session cookie overwritten upon new authentication |
| TC-SEC-059 | Cookie Flags | Cookie Security: Cookie manipulation / tampering triggers session invalidation |
| TC-SEC-060 | Cookie Flags | Cookie Security: Client-side JS (document.cookie) cannot read HttpOnly session |
| TC-SEC-061 | Brute Force Defense | Brute Force: 10 rapid failed login attempts handled without crash |
| TC-SEC-062 | Brute Force Defense | Brute Force: Account lockout or incremental delay simulation |
| TC-SEC-063 | Brute Force Defense | Brute Force: Constant-time password comparison prevents timing attacks |
| TC-SEC-064 | Brute Force Defense | Brute Force: Generic error message on failed login (no username enumeration) |
| TC-SEC-065 | Brute Force Defense | Brute Force: Registration endpoint rejects automated dictionary spam |
| TC-SEC-066 | Brute Force Defense | Brute Force: CAPTCHA / Proof of work token presence under high failure rate |
| TC-SEC-067 | Brute Force Defense | Brute Force: IP rate limiter headers present |
| TC-SEC-068 | Brute Force Defense | Brute Force: Failed attempts log security audit event |
| TC-SEC-069 | Brute Force Defense | Brute Force: Password reset rate limit protection |
| TC-SEC-070 | Brute Force Defense | Brute Force: Concurrent session limit enforcement |
| TC-SEC-071 | Session Fixation | Session Fixation: Pre-session ID discarded upon successful login |
| TC-SEC-072 | Session Fixation | Session Fixation: Brand new session token generated upon login |
| TC-SEC-073 | Session Fixation | Session Fixation: Session token does not leak in Referer header |
| TC-SEC-074 | Session Fixation | Session Fixation: Session token not accepted via URL query parameter |
| TC-SEC-075 | Session Fixation | Session Fixation: Session binding to User-Agent family |
| TC-SEC-076 | Session Fixation | Session Fixation: Replay attack with expired session token rejected |
| TC-SEC-077 | Session Fixation | Session Fixation: Logout invalidates session immediately on server |
| TC-SEC-078 | Session Fixation | Session Fixation: Invalidate all other active sessions upon password change |
| TC-SEC-079 | Session Fixation | Session Fixation: Session timeout after 30 minutes of inactivity |
| TC-SEC-080 | Session Fixation | Session Fixation: Forced re-authentication for critical account modifications |
| TC-SEC-081 | Cryptographic Security | Crypto: Passwords hashed with PBKDF2, Argon2, Scrypt, or Bcrypt |
| TC-SEC-082 | Cryptographic Security | Crypto: Unique cryptographic salt used for every user password |
| TC-SEC-083 | Cryptographic Security | Crypto: Hash work factor / cost parameter meets current NIST recommendations |
| TC-SEC-084 | Cryptographic Security | Crypto: Passwords never stored in plaintext in SQLite / Postgres |
| TC-SEC-085 | Cryptographic Security | Crypto: Database dumps do not expose decryptable reversible passwords |
| TC-SEC-086 | Cryptographic Security | Crypto: Secret key used for session signing is cryptographically random |
| TC-SEC-087 | Cryptographic Security | Crypto: Session signature verification prevents payload tampering |
| TC-SEC-088 | Cryptographic Security | Crypto: TLS cipher suites adhere to modern Forward Secrecy |
| TC-SEC-089 | Cryptographic Security | Crypto: Sensitive environment variables excluded from source code |
| TC-SEC-090 | Cryptographic Security | Crypto: API keys hashed / masked in application logs |
| TC-SEC-091 | Access Control | Access Control: Anonymous access to /settings |
| TC-SEC-092 | Access Control | Access Control: Anonymous access to /bookmarks |
| TC-SEC-093 | Access Control | Access Control: Anonymous access to /history |
| TC-SEC-094 | Access Control | Access Control: Anonymous access to /api/account |
| TC-SEC-095 | Access Control | Access Control: Anonymous access to /api/bookmarks |
| TC-SEC-096 | Access Control | Access Control: Anonymous access to /api/history |
| TC-SEC-097 | Access Control | Access Control: Anonymous access to /api/interests |
| TC-SEC-098 | Access Control | Access Control: Anonymous POST to /api/history/clear |
| TC-SEC-099 | Access Control | Access Control: Anonymous POST to /api/bookmarks/clear |
| TC-SEC-100 | Access Control | Access Control: Anonymous POST to /api/interests/clear |

### Module 3: CSRF, CORS & Security Headers (TC-SEC-101 to TC-SEC-150)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEC-101 | Security Headers | Headers: X-Content-Type-Options is set to nosniff |
| TC-SEC-102 | Security Headers | Headers: X-Frame-Options set to DENY or SAMEORIGIN (Clickjacking defense) |
| TC-SEC-103 | Security Headers | Headers: Referrer-Policy is present and restrictive |
| TC-SEC-104 | Security Headers | Headers: Content-Security-Policy (CSP) restricts unauthorized scripts |
| TC-SEC-105 | Security Headers | Headers: Strict-Transport-Security (HSTS) configured for production |
| TC-SEC-106 | Security Headers | Headers: Server header does not disclose exact OS or framework versions |
| TC-SEC-107 | Security Headers | Headers: X-Powered-By header is removed or masked |
| TC-SEC-108 | Security Headers | Headers: Permissions-Policy restricts sensitive device APIs |
| TC-SEC-109 | Security Headers | Headers: Cache-Control on authenticated pages set to no-store |
| TC-SEC-110 | Security Headers | Headers: Pragma: no-cache included on sensitive responses |
| TC-SEC-111 | CORS Validation | CORS: Unauthorized origin receives no Access-Control-Allow-Origin header |
| TC-SEC-112 | CORS Validation | CORS: Access-Control-Allow-Origin: * is forbidden on authenticated endpoints |
| TC-SEC-113 | CORS Validation | CORS: Access-Control-Allow-Credentials: true not combined with wildcard origin |
| TC-SEC-114 | CORS Validation | CORS: Preflight OPTIONS request returns valid Allowed-Methods |
| TC-SEC-115 | CORS Validation | CORS: Preflight OPTIONS request validates Allowed-Headers |
| TC-SEC-116 | CORS Validation | CORS: Origin with null header is rejected on sensitive APIs |
| TC-SEC-117 | CORS Validation | CORS: Subdomain reflection attack prevented |
| TC-SEC-118 | CORS Validation | CORS: Protocol downgrade (HTTP vs HTTPS) origin rejected |
| TC-SEC-119 | CORS Validation | CORS: Access-Control-Max-Age header has reasonable caching duration |
| TC-SEC-120 | CORS Validation | CORS: Exposed headers restricted to non-sensitive values |
| TC-SEC-121 | CSRF Defense | CSRF: State changing POST to /login without credentials rejected |
| TC-SEC-122 | CSRF Defense | CSRF: State changing POST to /register validates origin/referer |
| TC-SEC-123 | CSRF Defense | CSRF: State changing POST to /api/bookmarks/toggle checks session |
| TC-SEC-124 | CSRF Defense | CSRF: State changing POST to /api/history/clear checks session |
| TC-SEC-125 | CSRF Defense | CSRF: State changing POST to /api/interests checks session |
| TC-SEC-126 | CSRF Defense | CSRF: State changing DELETE to /api/bookmarks/1 checks session |
| TC-SEC-127 | CSRF Defense | CSRF: State changing DELETE to /api/history/1 checks session |
| TC-SEC-128 | CSRF Defense | CSRF: Cross-site image tag GET request cannot trigger state changes |
| TC-SEC-129 | CSRF Defense | CSRF: SameSite=Lax cookie attribute blocks cross-site POST form delivery |
| TC-SEC-130 | CSRF Defense | CSRF: Custom X-Requested-With header verification on AJAX calls |
| TC-SEC-131 | Clickjacking Protection | Clickjacking: Framing /login page inside iframe is blocked |
| TC-SEC-132 | Clickjacking Protection | Clickjacking: Framing /settings page inside iframe is blocked |
| TC-SEC-133 | Clickjacking Protection | Clickjacking: Framing /bookmarks page inside iframe is blocked |
| TC-SEC-134 | Clickjacking Protection | Clickjacking: Framing /history page inside iframe is blocked |
| TC-SEC-135 | Clickjacking Protection | Clickjacking: CSP frame-ancestors directive set to none or self |
| TC-SEC-136 | Clickjacking Protection | Clickjacking: Frame busting script fallback validation |
| TC-SEC-137 | Clickjacking Protection | Clickjacking: Transparent overlay click hijacking prevention |
| TC-SEC-138 | Clickjacking Protection | Clickjacking: Modal backdrop prevents background interaction |
| TC-SEC-139 | Clickjacking Protection | Clickjacking: Double click hijacking prevention on submit buttons |
| TC-SEC-140 | Clickjacking Protection | Clickjacking: CSS pointer-events disabled on inactive layers |
| TC-SEC-141 | Information Leak Prevention | Info Leak: 404 page does not leak server file system paths |
| TC-SEC-142 | Information Leak Prevention | Info Leak: 500 internal server error masks Python tracebacks in production |
| TC-SEC-143 | Information Leak Prevention | Info Leak: Directory listing is disabled across all static folders |
| TC-SEC-144 | Information Leak Prevention | Info Leak: /static/ folder does not expose source code or .py files |
| TC-SEC-145 | Information Leak Prevention | Info Leak: /.git/ directory is inaccessible via HTTP |
| TC-SEC-146 | Information Leak Prevention | Info Leak: /.env file is inaccessible via HTTP |
| TC-SEC-147 | Information Leak Prevention | Info Leak: Database file (*.db, *.sqlite) is inaccessible via HTTP |
| TC-SEC-148 | Information Leak Prevention | Info Leak: Verbose debug banners disabled in response headers |
| TC-SEC-149 | Information Leak Prevention | Info Leak: Robots.txt does not reveal secret admin endpoints |
| TC-SEC-150 | Information Leak Prevention | Info Leak: Source maps disabled or restricted in production assets |

### Module 4: IDOR & Access Control (TC-SEC-151 to TC-SEC-200)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEC-151 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/bookmarks/1 |
| TC-SEC-152 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/bookmarks/2 |
| TC-SEC-153 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/bookmarks/99 |
| TC-SEC-154 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/bookmarks/9999 |
| TC-SEC-155 | IDOR & Access Control | IDOR: Negative ID input on /api/bookmarks/-1 |
| TC-SEC-156 | IDOR & Access Control | IDOR: Zero ID input on /api/bookmarks/0 |
| TC-SEC-157 | IDOR & Access Control | IDOR: Non-integer string ID input on /api/bookmarks/abc |
| TC-SEC-158 | IDOR & Access Control | IDOR: Float ID input on /api/bookmarks/1.5 |
| TC-SEC-159 | IDOR & Access Control | IDOR: Integer overflow ID input on /api/bookmarks/ |
| TC-SEC-160 | IDOR & Access Control | IDOR: Cross-user bookmark deletion attempt rejected |
| TC-SEC-161 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/history/1 |
| TC-SEC-162 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/history/2 |
| TC-SEC-163 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/history/99 |
| TC-SEC-164 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/history/9999 |
| TC-SEC-165 | IDOR & Access Control | IDOR: Negative ID input on /api/history/-1 |
| TC-SEC-166 | IDOR & Access Control | IDOR: Zero ID input on /api/history/0 |
| TC-SEC-167 | IDOR & Access Control | IDOR: String null ID input on /api/history/null |
| TC-SEC-168 | IDOR & Access Control | IDOR: String undefined ID input on /api/history/undefined |
| TC-SEC-169 | IDOR & Access Control | IDOR: Large integer ID input on /api/history/999999999 |
| TC-SEC-170 | IDOR & Access Control | IDOR: Cross-user reading history wipe attempt rejected |
| TC-SEC-171 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/interests/1 |
| TC-SEC-172 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/interests/2 |
| TC-SEC-173 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/interests/99 |
| TC-SEC-174 | IDOR & Access Control | IDOR: Unauthorized user attempting DELETE /api/interests/9999 |
| TC-SEC-175 | IDOR & Access Control | IDOR: Negative ID input on /api/interests/-1 |
| TC-SEC-176 | IDOR & Access Control | IDOR: Zero ID input on /api/interests/0 |
| TC-SEC-177 | IDOR & Access Control | IDOR: String test ID input on /api/interests/test |
| TC-SEC-178 | IDOR & Access Control | IDOR: NaN ID input on /api/interests/NaN |
| TC-SEC-179 | IDOR & Access Control | IDOR: 1M ID input on /api/interests/1000000 |
| TC-SEC-180 | IDOR & Access Control | IDOR: Cross-user interest deletion attempt rejected |
| TC-SEC-181 | IDOR & Access Control | PrivEsc: Regular user cannot elevate role to admin via profile update |
| TC-SEC-182 | IDOR & Access Control | PrivEsc: Mass assignment vulnerability check on user registration |
| TC-SEC-183 | IDOR & Access Control | PrivEsc: Role parameter injected in JSON POST ignored by backend |
| TC-SEC-184 | IDOR & Access Control | PrivEsc: Is_admin flag in request body ignored by backend |
| TC-SEC-185 | IDOR & Access Control | PrivEsc: Modifying user ID in cookie session signature rejected |
| TC-SEC-186 | IDOR & Access Control | PrivEsc: Accessing admin metrics without admin privileges forbidden |
| TC-SEC-187 | IDOR & Access Control | PrivEsc: Vertical privilege escalation from guest to user prevented |
| TC-SEC-188 | IDOR & Access Control | PrivEsc: Horizontal privilege escalation between distinct users prevented |
| TC-SEC-189 | IDOR & Access Control | PrivEsc: Impersonation token creation rejected |
| TC-SEC-190 | IDOR & Access Control | PrivEsc: Backend verifies session ownership for all database queries |
| TC-SEC-191 | IDOR & Access Control | IDOR: Accessing specific saved roundup /roundup/1 |
| TC-SEC-192 | IDOR & Access Control | IDOR: Accessing specific saved roundup /roundup/2 |
| TC-SEC-193 | IDOR & Access Control | IDOR: Accessing non-existent roundup /roundup/9999 |
| TC-SEC-194 | IDOR & Access Control | IDOR: Accessing negative roundup /roundup/-1 |
| TC-SEC-195 | IDOR & Access Control | IDOR: Accessing alphabetic roundup /roundup/abc |
| TC-SEC-196 | IDOR & Access Control | IDOR: Accessing zero roundup /roundup/0 |
| TC-SEC-197 | IDOR & Access Control | IDOR: Accessing large integer roundup /roundup/9999999999 |
| TC-SEC-198 | IDOR & Access Control | IDOR: Unauthorized deletion of roundup /roundup/1/delete |
| TC-SEC-199 | IDOR & Access Control | IDOR: Unauthorized export of private roundup |
| TC-SEC-200 | IDOR & Access Control | IDOR: Unauthorized modification of private roundup |

### Module 5: Input Boundary & Sanitization (TC-SEC-201 to TC-SEC-250)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEC-201 | Input Sanitization | Path Traversal: ../../../../etc/passwd |
| TC-SEC-202 | Input Sanitization | Path Traversal: URL encoded ..%2f |
| TC-SEC-203 | Input Sanitization | Path Traversal: Windows backslash traversal |
| TC-SEC-204 | Input Sanitization | Path Traversal: Nested slash bypass attempt |
| TC-SEC-205 | Input Sanitization | Path Traversal: Double URL encoded |
| TC-SEC-206 | Input Sanitization | Path Traversal: Absolute path to /etc/shadow |
| TC-SEC-207 | Input Sanitization | Path Traversal: Absolute path to /proc/self/environ |
| TC-SEC-208 | Input Sanitization | Path Traversal: Log poisoning path check |
| TC-SEC-209 | Input Sanitization | Path Traversal: Source file retrieval via static handler |
| TC-SEC-210 | Input Sanitization | Path Traversal: SQLite DB retrieval attempt |
| TC-SEC-211 | Input Sanitization | Null Byte: %00 in static filename |
| TC-SEC-212 | Input Sanitization | Null Byte: \u0000 in username input |
| TC-SEC-213 | Input Sanitization | Null Byte: Hex \x00 in password |
| TC-SEC-214 | Input Sanitization | CRLF Injection in interest topic input |
| TC-SEC-215 | Input Sanitization | CRLF Injection in search query |
| TC-SEC-216 | Input Sanitization | Control Characters: Form feeds and backspaces |
| TC-SEC-217 | Input Sanitization | URL Encoded CRLF in path parameter |
| TC-SEC-218 | Input Sanitization | ANSI Escape Sequence injection |
| TC-SEC-219 | Input Sanitization | Unicode Byte Order Mark (BOM) handling |
| TC-SEC-220 | Input Sanitization | Right-to-Left Override spoofing character |
| TC-SEC-221 | Input Sanitization | Payload Size: 10KB string in search query |
| TC-SEC-222 | Input Sanitization | Payload Size: 50KB string in registration username |
| TC-SEC-223 | Input Sanitization | Payload Size: 100KB string in interest topic POST |
| TC-SEC-224 | Input Sanitization | Payload Size: 500KB JSON body to /api/bookmarks/toggle |
| TC-SEC-225 | Input Sanitization | Payload Size: 1MB JSON body payload handled without crash |
| TC-SEC-226 | Input Sanitization | Payload Size: Deeply nested JSON object (100 levels) |
| TC-SEC-227 | Input Sanitization | Payload Size: Array with 5000 items in JSON body |
| TC-SEC-228 | Input Sanitization | Payload Size: Massive header value (8KB header line) |
| TC-SEC-229 | Input Sanitization | Payload Size: 100 duplicate query parameters (?q=1&q=2...) |
| TC-SEC-230 | Input Sanitization | Payload Size: Zero-length content body with Content-Length: 1000 |
| TC-SEC-231 | Input Sanitization | MIME: Send text with application/json header |
| TC-SEC-232 | Input Sanitization | MIME: Send XML to JSON API endpoint |
| TC-SEC-233 | Input Sanitization | MIME: Send HTML body to API endpoint |
| TC-SEC-234 | Input Sanitization | MIME: Malformed multipart boundary |
| TC-SEC-235 | Input Sanitization | MIME: Send JSON with urlencoded header |
| TC-SEC-236 | Input Sanitization | MIME: Plain text body to POST route |
| TC-SEC-237 | Input Sanitization | MIME: Binary payload to JSON endpoint |
| TC-SEC-238 | Input Sanitization | MIME: Missing Content-Type header on POST |
| TC-SEC-239 | Input Sanitization | MIME: UTF-7 charset XSS evasion attempt |
| TC-SEC-240 | Input Sanitization | MIME: Invalid charset parameter |
| TC-SEC-241 | Input Sanitization | Unicode: NFKC normalization on registration username |
| TC-SEC-242 | Input Sanitization | Unicode: Cyrillic homograph character in username (а vs a) |
| TC-SEC-243 | Input Sanitization | Unicode: Full-width characters in search query (ＡＩ) |
| TC-SEC-244 | Input Sanitization | Unicode: Zero-width space (\u200B) stripping in usernames |
| TC-SEC-245 | Input Sanitization | Unicode: Emoji characters safely stored and retrieved in UTF-8 |
| TC-SEC-246 | Input Sanitization | Unicode: Non-BMP 4-byte UTF-8 character handling (utf8mb4) |
| TC-SEC-247 | Input Sanitization | Unicode: Combining diacritical marks in interest tags |
| TC-SEC-248 | Input Sanitization | Unicode: Ligature characters (ﬁ, ﬂ) decomposed correctly |
| TC-SEC-249 | Input Sanitization | Unicode: Math monospace characters in input |
| TC-SEC-250 | Input Sanitization | Unicode: Inverted exclamation and question marks |

### Module 6: DoS Defense & Rate Limiting (TC-SEC-251 to TC-SEC-300)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-SEC-251 | DoS & Rate Limiting | ReDoS: Catastrophic backtracking in email regex |
| TC-SEC-252 | DoS & Rate Limiting | ReDoS: Catastrophic backtracking in phone regex |
| TC-SEC-253 | DoS & Rate Limiting | ReDoS: Catastrophic backtracking in URL regex |
| TC-SEC-254 | DoS & Rate Limiting | ReDoS: Deep domain nesting regex check |
| TC-SEC-255 | DoS & Rate Limiting | ReDoS: Username regex complexity check |
| TC-SEC-256 | DoS & Rate Limiting | ReDoS: Interest tag regex complexity check |
| TC-SEC-257 | DoS & Rate Limiting | ReDoS: Search query tokenizer regex check |
| TC-SEC-258 | DoS & Rate Limiting | ReDoS: HTML parser regex check |
| TC-SEC-259 | DoS & Rate Limiting | ReDoS: Data URL regex check |
| TC-SEC-260 | DoS & Rate Limiting | ReDoS: Date format regex check |
| TC-SEC-261 | DoS & Rate Limiting | Compute: Rapid consecutive calls to /api/synthesize handled gracefully |
| TC-SEC-262 | DoS & Rate Limiting | Compute: Rate limiter restricts excessive AI synthesis per user |
| TC-SEC-263 | DoS & Rate Limiting | Compute: Concurrent synthesis queue limit prevents thread starvation |
| TC-SEC-264 | DoS & Rate Limiting | Compute: Synthesis timeout enforces maximum 30s processing window |
| TC-SEC-265 | DoS & Rate Limiting | Compute: Large cluster synthesis payload size limit |
| TC-SEC-266 | DoS & Rate Limiting | Compute: Background worker health check endpoint active |
| TC-SEC-267 | DoS & Rate Limiting | Compute: TF-IDF matrix dimension capped for memory safety |
| TC-SEC-268 | DoS & Rate Limiting | Compute: DBSCAN clustering max samples threshold |
| TC-SEC-269 | DoS & Rate Limiting | Compute: Async job cancellation frees CPU resources |
| TC-SEC-270 | DoS & Rate Limiting | Compute: Graceful 429 response when compute quota reached |
| TC-SEC-271 | DoS & Rate Limiting | Flood: 20 simultaneous HTTP connections from single client |
| TC-SEC-272 | DoS & Rate Limiting | Flood: Partial HTTP header delay timeout enforcement |
| TC-SEC-273 | DoS & Rate Limiting | Flood: Max keep-alive requests per TCP connection capped |
| TC-SEC-274 | DoS & Rate Limiting | Flood: Keep-alive timeout closes idle sockets after 5s |
| TC-SEC-275 | DoS & Rate Limiting | Flood: Half-open connection reaping mechanism |
| TC-SEC-276 | DoS & Rate Limiting | Flood: Rapid TCP reset (RST) flood handling |
| TC-SEC-277 | DoS & Rate Limiting | Flood: Large header buffer limit (max 16KB per request) |
| TC-SEC-278 | DoS & Rate Limiting | Flood: Chunked transfer encoding validation |
| TC-SEC-279 | DoS & Rate Limiting | Flood: Max concurrent requests per IP limit |
| TC-SEC-280 | DoS & Rate Limiting | Flood: Server retains responsive status during connection bursts |
| TC-SEC-281 | DoS & Rate Limiting | Memory: Node / Python process memory usage stable after 50 requests |
| TC-SEC-282 | DoS & Rate Limiting | Memory: Unclosed database cursor leak prevention |
| TC-SEC-283 | DoS & Rate Limiting | Memory: Garbage collection effectively reclaims cluster data |
| TC-SEC-284 | DoS & Rate Limiting | Memory: File descriptor count stable after static asset serving |
| TC-SEC-285 | DoS & Rate Limiting | Memory: Static file caching bounds memory consumption |
| TC-SEC-286 | DoS & Rate Limiting | Memory: Session store prune task removes expired sessions |
| TC-SEC-287 | DoS & Rate Limiting | Memory: Temp files cleaned up after report / PDF exports |
| TC-SEC-288 | DoS & Rate Limiting | Memory: Max socket backlog queue limit prevents heap blowup |
| TC-SEC-289 | DoS & Rate Limiting | Memory: Process limits (max RSS) configured |
| TC-SEC-290 | DoS & Rate Limiting | Memory: Health check reports memory status green |
| TC-SEC-291 | DoS & Rate Limiting | Audit: Failed authentication events logged with IP and timestamp |
| TC-SEC-292 | DoS & Rate Limiting | Audit: Privilege escalation attempts logged with user ID |
| TC-SEC-293 | DoS & Rate Limiting | Audit: SQL injection payload detection logged at WARN level |
| TC-SEC-294 | DoS & Rate Limiting | Audit: XSS payload detection logged at WARN level |
| TC-SEC-295 | DoS & Rate Limiting | Audit: Rate limit threshold breach logged with client identifier |
| TC-SEC-296 | DoS & Rate Limiting | Audit: Security logs do not contain raw user passwords |
| TC-SEC-297 | DoS & Rate Limiting | Audit: Security logs do not contain session tokens |
| TC-SEC-298 | DoS & Rate Limiting | Audit: Security logs formatted as structured JSON / Winston |
| TC-SEC-299 | DoS & Rate Limiting | Audit: Log file rotation configured to prevent disk fill-up |
| TC-SEC-300 | DoS & Rate Limiting | Audit: High severity events trigger alert notification hook |

---

# 4. ⚡ Load & Performance Test Suite (300 Tests)

### Module 1: Baseline Latency Benchmarks (TC-LOAD-001 to TC-LOAD-050)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-LOAD-001 to 005 | Baseline SLA | Latency SLA: Feed Home Root / (Iterations 1-5) |
| TC-LOAD-006 to 010 | Baseline SLA | Latency SLA: Login Page /login (Iterations 1-5) |
| TC-LOAD-011 to 015 | Baseline SLA | Latency SLA: Register Page /register (Iterations 1-5) |
| TC-LOAD-016 to 020 | Baseline SLA | Latency SLA: Settings Page /settings (Iterations 1-5) |
| TC-LOAD-021 to 025 | Baseline SLA | Latency SLA: History Page /history (Iterations 1-5) |
| TC-LOAD-026 to 030 | Baseline SLA | Latency SLA: Bookmarks Page /bookmarks (Iterations 1-5) |
| TC-LOAD-031 to 035 | Baseline SLA | Latency SLA: Roundups Page /roundup (Iterations 1-5) |
| TC-LOAD-036 to 040 | Baseline SLA | Latency SLA: API Cluster /api/cluster (Iterations 1-5) |
| TC-LOAD-041 to 045 | Baseline SLA | Latency SLA: API Regions /api/regions (Iterations 1-5) |
| TC-LOAD-046 to 050 | Baseline SLA | Latency SLA: Favicon Asset /favicon.ico (Iterations 1-5) |

### Module 2: Concurrency & Virtual User Burst (TC-LOAD-051 to TC-LOAD-100)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-LOAD-051 to 055 | VU Concurrency | Concurrency: 5 VU Concurrent Feed Requests (Cycles 1-5) |
| TC-LOAD-056 to 060 | VU Concurrency | Concurrency: 10 VU Concurrent Feed Requests (Cycles 1-5) |
| TC-LOAD-061 to 065 | VU Concurrency | Concurrency: 15 VU Concurrent Feed Requests (Cycles 1-5) |
| TC-LOAD-066 to 070 | VU Concurrency | Concurrency: 20 VU Concurrent Feed Requests (Cycles 1-5) |
| TC-LOAD-071 to 075 | VU Concurrency | Concurrency: 25 VU Concurrent Feed Requests (Cycles 1-5) |
| TC-LOAD-076 to 080 | VU Concurrency | Concurrency: 5 VU Concurrent /api/cluster Requests (Cycles 1-5) |
| TC-LOAD-081 to 085 | VU Concurrency | Concurrency: 10 VU Concurrent /api/cluster Requests (Cycles 1-5) |
| TC-LOAD-086 to 090 | VU Concurrency | Concurrency: 15 VU Concurrent /api/regions Requests (Cycles 1-5) |
| TC-LOAD-091 to 095 | VU Concurrency | Concurrency: 20 VU Concurrent /settings Requests (Cycles 1-5) |
| TC-LOAD-096 to 100 | VU Concurrency | Concurrency: 25 VU Concurrent /login Requests (Cycles 1-5) |

### Module 3: Stress & Threshold Testing (TC-LOAD-101 to TC-LOAD-150)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-LOAD-101 to 105 | Stress Limits | Stress: Rapid traffic burst on Root Feed (Rounds 1-5) |
| TC-LOAD-106 to 110 | Stress Limits | Stress: Rapid traffic burst on API Cluster (Rounds 1-5) |
| TC-LOAD-111 to 115 | Stress Limits | Stress: Rapid traffic burst on API Regions (Rounds 1-5) |
| TC-LOAD-116 to 120 | Stress Limits | Stress: Rapid traffic burst on Settings Page (Rounds 1-5) |
| TC-LOAD-121 to 125 | Stress Limits | Stress: Rapid traffic burst on History Page (Rounds 1-5) |
| TC-LOAD-126 to 130 | Stress Limits | Stress: Rapid traffic burst on Bookmarks Page (Rounds 1-5) |
| TC-LOAD-131 to 135 | Stress Limits | Stress: Rapid traffic burst on Roundups Page (Rounds 1-5) |
| TC-LOAD-136 to 140 | Stress Limits | Stress: Rapid traffic burst on Login Page (Rounds 1-5) |
| TC-LOAD-141 to 145 | Stress Limits | Stress: Rapid traffic burst on Register Page (Rounds 1-5) |
| TC-LOAD-146 to 150 | Stress Limits | Stress: Rapid traffic burst on Static JS Bundle (Rounds 1-5) |

### Module 4: Endurance & Memory Soak (TC-LOAD-151 to TC-LOAD-200)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-LOAD-151 to 155 | Memory Soak | Soak: Sequential requests against Root Feed (Steps 1-5) |
| TC-LOAD-156 to 160 | Memory Soak | Soak: Sequential requests against API Cluster (Steps 1-5) |
| TC-LOAD-161 to 165 | Memory Soak | Soak: Sequential requests against Settings (Steps 1-5) |
| TC-LOAD-166 to 170 | Memory Soak | Soak: Sequential requests against Bookmarks (Steps 1-5) |
| TC-LOAD-171 to 175 | Memory Soak | Soak: Sequential requests against History (Steps 1-5) |
| TC-LOAD-176 to 180 | Memory Soak | Soak: Sequential requests against Roundups (Steps 1-5) |
| TC-LOAD-181 to 185 | Memory Soak | Soak: Sequential requests against API Regions (Steps 1-5) |
| TC-LOAD-186 to 190 | Memory Soak | Soak: Sequential requests against Login (Steps 1-5) |
| TC-LOAD-191 to 195 | Memory Soak | Soak: Sequential requests against Register (Steps 1-5) |
| TC-LOAD-196 to 200 | Memory Soak | Soak: Sequential requests with search query (Steps 1-5) |

### Module 5: AI Compute & Synthesis Load (TC-LOAD-201 to TC-LOAD-250)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-LOAD-201 to 205 | AI Compute | Compute: Clustering algorithm response time (Iterations 1-5) |
| TC-LOAD-206 to 210 | AI Compute | Compute: Region aggregation response time (Iterations 1-5) |
| TC-LOAD-211 to 215 | AI Compute | Compute: Synthesis template rendering load (Iterations 1-5) |
| TC-LOAD-216 to 220 | AI Compute | Compute: User interest weighting retrieval (Iterations 1-5) |
| TC-LOAD-221 to 225 | AI Compute | Compute: History query execution benchmark (Iterations 1-5) |
| TC-LOAD-226 to 230 | AI Compute | Compute: Bookmarks query execution benchmark (Iterations 1-5) |
| TC-LOAD-231 to 235 | AI Compute | Compute: Filtered US feed generation (Iterations 1-5) |
| TC-LOAD-236 to 240 | AI Compute | Compute: Filtered UK feed generation (Iterations 1-5) |
| TC-LOAD-241 to 245 | AI Compute | Compute: Filtered IN feed generation (Iterations 1-5) |
| TC-LOAD-246 to 250 | AI Compute | Compute: Filtered GLOBAL feed generation (Iterations 1-5) |

### Module 6: Database Transactional Load (TC-LOAD-251 to TC-LOAD-300)
| Test ID | Module | Test Name |
| :--- | :--- | :--- |
| TC-LOAD-251 to 255 | DB Transactions | DB Load: High-frequency interest fetch operations (Cycles 1-5) |
| TC-LOAD-256 to 260 | DB Transactions | DB Load: High-frequency history query operations (Cycles 1-5) |
| TC-LOAD-261 to 265 | DB Transactions | DB Load: High-frequency bookmark check operations (Cycles 1-5) |
| TC-LOAD-266 to 270 | DB Transactions | DB Load: High-frequency region preference update (Cycles 1-5) |
| TC-LOAD-271 to 275 | DB Transactions | DB Load: High-frequency interest insert attempt (Cycles 1-5) |
| TC-LOAD-276 to 280 | DB Transactions | DB Load: High-frequency bookmark toggle attempt (Cycles 1-5) |
| TC-LOAD-281 to 285 | DB Transactions | DB Load: Database read lock contention handling (Cycles 1-5) |
| TC-LOAD-286 to 290 | DB Transactions | DB Load: Database write-ahead logging (WAL) throughput (Cycles 1-5) |
| TC-LOAD-291 to 295 | DB Transactions | DB Load: Concurrent user session lookups (Cycles 1-5) |
| TC-LOAD-296 to 300 | DB Transactions | DB Load: Concurrent feed cache table queries (Cycles 1-5) |
