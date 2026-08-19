const REGIONS = window.REGIONS || {};
const THEMES = new Set(['default', 'pitch-black', 'palette-one', 'palette-two', 'palette-three']);

let currentRegion = (localStorage.getItem('lacuna_region') || localStorage.getItem('newsRegion') || window.USER_REGION || 'US').toUpperCase();
let currentTheme  = localStorage.getItem('lacuna_theme') || localStorage.getItem('newsTheme') || 'default';
let currentQuery  = '__home__';
let currentCategoryName = 'Home';

function applyTheme(theme) {
    currentTheme = THEMES.has(theme) ? theme : 'default';
    if (currentTheme === 'default') {
        document.body.removeAttribute('data-theme');
    } else {
        document.body.setAttribute('data-theme', currentTheme);
    }
    document.querySelectorAll('[data-theme-option]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.themeOption === currentTheme);
    });
}

function setTheme(theme) {
    const t = THEMES.has(theme) ? theme : 'default';
    localStorage.setItem('lacuna_theme', t);
    localStorage.setItem('newsTheme', t);
    applyTheme(t);
}

document.querySelectorAll('[data-theme-option]').forEach(btn => {
    btn.addEventListener('click', () => setTheme(btn.dataset.themeOption));
});

function buildRegionGrid() {
    const grids = [
        document.getElementById('region-grid')
    ].filter(Boolean);

    grids.forEach(grid => {
        grid.innerHTML = '';
        Object.entries(REGIONS).forEach(([code, label]) => {
            const btn = document.createElement('button');
            btn.className = 'region-option' + (code === currentRegion ? ' active' : '');
            btn.type = 'button';
            btn.dataset.code = code;
            btn.dataset.testid = 'region-option-' + code.toLowerCase();
            btn.innerHTML = `<span class="region-code-badge">${code}</span>${label}`;
            btn.addEventListener('click', () => selectRegion(code));
            grid.appendChild(btn);
        });
    });
}

function selectRegion(code) {
    const changed = (code !== currentRegion);
    currentRegion = code.toUpperCase();
    localStorage.setItem('newsRegion', currentRegion);
    localStorage.setItem('lacuna_region', currentRegion.toLowerCase());
    fetch('/api/region', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region: currentRegion })
    }).catch(() => {});
    buildRegionGrid();
    if (changed) {
        loadQuery(currentQuery, currentCategoryName);
    }
}

function timeAgo(dateString) {
    if (!dateString) return '';
    try {
        const date = new Date(dateString);
        const now = new Date();
        const seconds = Math.floor((now - date) / 1000);
        if (seconds < 60) return 'Just now';
        const minutes = Math.floor(seconds / 60);
        if (minutes < 60) return `${minutes}m ago`;
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        const days = Math.floor(hours / 24);
        if (days < 7) return `${days}d ago`;
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    } catch(e) {
        return '';
    }
}

function loadAccountDetails() {
    const regEl = document.getElementById('stat-region-code');
    if (regEl) regEl.textContent = currentRegion;

    fetch('/api/account')
        .then(r => r.ok ? r.json() : null)
        .then(data => {
            if (!data) return;
            if (data.username) {
                const uEl = document.getElementById('side-account-username');
                if (uEl) uEl.textContent = data.username;
            }
            if (typeof data.email !== 'undefined') {
                const emailEl = document.getElementById('side-account-email');
                if (emailEl) emailEl.textContent = data.email || '';
            }
            if (data.created_at) {
                const d = new Date(data.created_at);
                const metaEl = document.getElementById('account-meta-date');
                if (metaEl && !isNaN(d.getTime())) {
                    metaEl.textContent = 'Member since ' + d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
                }
            }
            if (typeof data.history_count !== 'undefined') {
                const countEl = document.getElementById('stat-read-count');
                if (countEl) countEl.textContent = data.history_count;
            }
            if (data.preferred_region) {
                const prev = currentRegion;
                currentRegion = data.preferred_region.toUpperCase();
                localStorage.setItem('lacuna_region', currentRegion.toLowerCase());
                localStorage.setItem('newsRegion', currentRegion);
                if (regEl) regEl.textContent = currentRegion;
                if (prev !== currentRegion) {
                    buildRegionGrid();
                    loadQuery(currentQuery, currentCategoryName);
                }
            }
        })
        .catch(() => {});
}

function loadReadingHistory() {
    const list = document.getElementById('side-history-list');
    const countEl = document.getElementById('side-history-count');
    if (!list) return;

    fetch('/api/history')
        .then(r => r.ok ? r.json() : [])
        .then(items => {
            list.innerHTML = '';
            if (!items || !items.length) {
                list.innerHTML = '<div class="side-empty-history">No reading history yet. Synthesized roundups will appear here.</div>';
                if (countEl) countEl.textContent = '0 roundups';
                return;
            }
            if (countEl) countEl.textContent = `${items.length} recent roundup${items.length === 1 ? '' : 's'}`;

            const statReadEl = document.getElementById('stat-read-count');
            if (statReadEl) {
                const cur = parseInt(statReadEl.textContent || '0', 10);
                if (items.length > cur) statReadEl.textContent = items.length;
            }

            items.forEach(item => {
                const card = document.createElement('div');
                card.className = 'side-history-card';
                card.dataset.testid = 'side-history-card';
                card.title = 'Click to open roundup';

                const img = document.createElement('img');
                img.className = 'side-history-thumb';
                img.src = item.image || getFallbackImage(item.title);
                img.alt = '';
                img.loading = 'lazy';
                img.referrerPolicy = 'no-referrer';
                img.onerror = () => { img.onerror = null; img.src = getFallbackImage(item.title); };

                const details = document.createElement('div');
                details.className = 'side-history-details';

                const title = document.createElement('div');
                title.className = 'side-history-title';
                title.dataset.testid = 'side-history-title';
                title.textContent = item.title;

                const meta = document.createElement('div');
                meta.className = 'side-history-meta';
                const time = timeAgo(item.created_at);
                const srcCount = item.source_count || (item.sources ? item.sources.length : 0);
                meta.innerHTML = `<span>${time || 'Recent'}</span>${srcCount ? `<span>·</span><span>${srcCount} src</span>` : ''}`;

                details.appendChild(title);
                details.appendChild(meta);
                card.appendChild(img);
                card.appendChild(details);

                card.addEventListener('click', () => {
                    openHistoryArticle(item);
                });

                list.appendChild(card);
            });
        })
        .catch(() => {
            list.innerHTML = '<div class="side-empty-history">[Error] Could not load history.</div>';
        });
}

function openHistoryArticle(historyItem) {
    closeSideMenu();
    const modal = document.getElementById('reader-modal');
    const backdrop = document.getElementById('reader-backdrop');
    const inner = document.getElementById('reader-inner');

    modal.style.display = 'flex';
    backdrop.classList.add('open');
    document.body.style.overflow = 'hidden';

    const nd = {
        cluster_title: historyItem.title,
        cluster_image: historyItem.image,
        articles: (historyItem.sources && historyItem.sources.length) ? historyItem.sources : [{
            title: historyItem.title,
            url: '#',
            published: historyItem.created_at,
            source: 'Lacuna Archive'
        }]
    };

    renderReaderContent(inner, nd, historyItem.article || 'Archive content.');
}

function clearReadingHistory() {
    if (!confirm('Clear your reading history?')) return;
    fetch('/api/history/clear', { method: 'POST' })
        .then(r => r.json())
        .then(() => {
            loadReadingHistory();
            const statReadEl = document.getElementById('stat-read-count');
            if (statReadEl) statReadEl.textContent = '0';
        })
        .catch(() => alert('Failed to clear history.'));
}

    function hostname(url) {
        try { return new URL(url).hostname.replace(/^www\./, ''); } catch(e) { return ''; }
    }
    function formatSource(a) {
        if (!a) return 'NEWS';
        if (a.domain && !a.domain.toLowerCase().includes('google.com')) {
            return a.domain.toUpperCase();
        }
        if (a.source_url) {
            const h = hostname(a.source_url);
            if (h && !h.toLowerCase().includes('google.com')) return h.toUpperCase();
        }
        if (a.source && !a.source.toLowerCase().includes('google')) {
            return a.source.toUpperCase();
        }
        const h = hostname(a.url);
        if (h && !h.toLowerCase().includes('google.com')) {
            return h.toUpperCase();
        }
        return (a.source || 'NEWS').toUpperCase();
    }
    function formatDate(d) {
        if (!d) return '';
        try { return new Date(d).toLocaleDateString('en-US', {month:'short', day:'numeric'}); }
        catch(e) { return ''; }
    }

    function getFallbackImage(title) {
        const clean = (title || 'News').trim().slice(0, 48);
        const hash = [...clean].reduce((acc, c) => (acc * 31 + c.charCodeAt(0)) | 0, 0);
        const hue = Math.abs(hash) % 360;
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
            <defs>
                <linearGradient id="g${hue}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="hsl(${hue}, 35%, 14%)"/>
                    <stop offset="100%" stop-color="hsl(${(hue + 40) % 360}, 30%, 8%)"/>
                </linearGradient>
            </defs>
            <rect width="800" height="500" fill="url(#g${hue})"/>
            <rect x="24" y="24" width="752" height="452" fill="none" stroke="hsl(${hue}, 40%, 35%)" stroke-width="2" opacity="0.35"/>
            <circle cx="400" cy="200" r="130" fill="hsl(${hue}, 50%, 25%)" opacity="0.25"/>
            <path d="M120 400 Q 400 280 680 410" stroke="hsl(${hue}, 55%, 45%)" stroke-width="6" fill="none" opacity="0.35"/>
            <text x="400" y="240" fill="hsl(${hue}, 35%, 85%)" font-family="Glacial Indifference, Helvetica Neue, Helvetica, Arial, sans-serif" font-size="24" font-weight="700" text-anchor="middle" letter-spacing="2">${clean.replace(/[<>&"]/g, '')}</text>
        </svg>`;
        return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    }

    /* ── HERO BUILDERS ── */
    function buildHeroLead(nd) {
        const { articles, cluster_image, cluster_title, consensus_summary } = nd;
        const art = articles[0];
        const title = cluster_title || art.title || '';
        const el = document.createElement('div');
        el.className = 'hero-lead';
        el.dataset.testid = 'hero-lead-card';
        el.addEventListener('click', () => openReader(nd));

        const media = document.createElement('div');
        media.className = 'hero-lead-media';
        media.dataset.testid = 'hero-lead-media';
        const img = document.createElement('img');
        img.className = 'hero-lead-img';
        img.src = cluster_image || getFallbackImage(title);
        img.alt = '';
        img.loading = 'lazy';
        img.referrerPolicy = 'no-referrer';
        img.onerror = () => {
            img.onerror = null;
            img.src = getFallbackImage(title);
        };
        media.appendChild(img);
        el.appendChild(media);

        const body = document.createElement('div');
        body.className = 'hero-lead-body';
        const n = articles.length;

        const attr = document.createElement('div');
        attr.className = 'hero-lead-attr';
        attr.textContent = (n >= 8 ? 'Trending' : n >= 4 ? 'Top Story' : 'Story') + (art.published ? '  ·  ' + formatDate(art.published) : '');
        body.appendChild(attr);

        const titleEl = document.createElement('div');
        titleEl.className = 'hero-lead-title';
        titleEl.dataset.testid = 'hero-lead-title';
        titleEl.textContent = title;
        body.appendChild(titleEl);

        if (consensus_summary) {
            const sum = document.createElement('div');
            sum.className = 'hero-lead-summary';
            sum.dataset.testid = 'hero-lead-summary';
            sum.textContent = consensus_summary;
            body.appendChild(sum);
        }

        body.appendChild(buildHeroSourcesMenu(articles));

        const related = articles
            .slice(1)
            .map(a => a.title)
            .filter(t => t && t !== title)
            .slice(0, 4);
        if (related.length) {
            const list = document.createElement('div');
            list.className = 'hero-lead-list';
            related.forEach(text => {
                const item = document.createElement('div');
                item.className = 'hero-lead-item';
                item.textContent = text.length > 118 ? text.slice(0, 115) + '...' : text;
                list.appendChild(item);
            });
            body.appendChild(list);
        }

        el.appendChild(body);
        return el;
    }

    function buildHeroSide(nd) {
        const { articles, cluster_image, cluster_title, consensus_summary } = nd;
        const art = articles[0];
        const title = cluster_title || art.title || '';
        const el = document.createElement('div');
        el.className = 'hero-side';
        el.dataset.testid = 'hero-side-card';
        el.addEventListener('click', () => openReader(nd));

        const img = document.createElement('img');
        img.className = 'hero-side-img';
        img.src = cluster_image || getFallbackImage(title);
        img.alt = '';
        img.loading = 'lazy';
        img.referrerPolicy = 'no-referrer';
        img.onerror = () => {
            img.onerror = null;
            img.src = getFallbackImage(title);
        };
        el.appendChild(img);

        const body = document.createElement('div');
        body.className = 'hero-side-body';

        const attr = document.createElement('div');
        attr.className = 'hero-side-attr';
        attr.textContent = formatDate(art.published);
        body.appendChild(attr);

        const titleEl = document.createElement('div');
        titleEl.className = 'hero-side-title';
        titleEl.dataset.testid = 'hero-side-title';
        titleEl.textContent = cluster_title || art.title;
        body.appendChild(titleEl);

        if (consensus_summary) {
            const sum = document.createElement('div');
            sum.className = 'hero-side-summary';
            sum.dataset.testid = 'hero-side-summary';
            sum.textContent = consensus_summary.length > 150 ? consensus_summary.slice(0, 147) + '...' : consensus_summary;
            body.appendChild(sum);
        }

        body.appendChild(buildHeroSourcesMenu(articles));

        el.appendChild(body);
        return el;
    }

    function buildHeroSourcesMenu(articles) {
        const wrap = document.createElement('div');
        wrap.className = 'hero-sources';
        wrap.addEventListener('click', e => e.stopPropagation());

        const btn = document.createElement('button');
        btn.className = 'hero-sources-btn';
        btn.dataset.testid = 'hero-sources-btn';
        btn.type = 'button';
        btn.innerHTML = `${articles.length} source${articles.length === 1 ? '' : 's'} <span class="sarrow">▼</span>`;

        const panel = buildSourcesPanel(articles);
        panel.classList.add('hero-sources-panel');

        btn.addEventListener('click', e => {
            e.stopPropagation();
            const isCurrentlyOpen = panel.classList.contains('open');
            document.querySelectorAll('.hero-sources-panel.open, .sources-panel.open').forEach(openPanel => {
                openPanel.classList.remove('open');
            });
            document.querySelectorAll('.hero-sources-btn.open, .cr-sources-btn.open').forEach(openBtn => {
                openBtn.classList.remove('open');
            });
            document.querySelectorAll('.hero-side').forEach(card => card.style.zIndex = '');
            if (!isCurrentlyOpen) {
                panel.classList.add('open');
                btn.classList.add('open');
                const parentCard = wrap.closest('.hero-side');
                if (parentCard) parentCard.style.zIndex = '250';
            }
        });
        panel.addEventListener('click', e => e.stopPropagation());

        wrap.appendChild(btn);
        wrap.appendChild(panel);
        return wrap;
    }

    function buildCompact(nd) {
        const { articles, cluster_image, cluster_title, consensus_summary } = nd;
        const art = articles[0];
        const title = cluster_title || art.title || '';
        const n = articles.length;

        const card = document.createElement('div');
        card.className = 'cluster-row';
        card.dataset.testid = 'cluster-card';
        card.addEventListener('click', () => openReader(nd));

        card.appendChild(buildImageCol(cluster_image, title));
        card.appendChild(buildTextCol(cluster_title, art, consensus_summary));

        const metaCol = document.createElement('div');
        metaCol.className = 'cr-meta-col';

        const badge = document.createElement('div');
        badge.className = 'cr-badge';
        badge.textContent = n >= 8 ? 'Trending' : n >= 4 ? 'Top Story' : 'Story';
        metaCol.appendChild(badge);

        const date = document.createElement('div');
        date.className = 'cr-date';
        date.textContent = formatDate(art.published).toUpperCase();
        metaCol.appendChild(date);

        const btn = document.createElement('button');
        btn.className = 'cr-sources-btn';
        btn.dataset.testid = 'cr-sources-btn';
        btn.type = 'button';
        btn.innerHTML = `${n} source${n === 1 ? '' : 's'} <span class="sarrow">▼</span>`;

        const panel = buildSourcesPanel(articles);

        btn.addEventListener('click', e => {
            e.stopPropagation();
            const isCurrentlyOpen = panel.classList.contains('open');
            document.querySelectorAll('.hero-sources-panel.open, .sources-panel.open').forEach(openPanel => {
                openPanel.classList.remove('open');
            });
            document.querySelectorAll('.hero-sources-btn.open, .cr-sources-btn.open').forEach(openBtn => {
                openBtn.classList.remove('open');
            });
            if (!isCurrentlyOpen) {
                panel.classList.add('open');
                btn.classList.add('open');
            }
        });
        panel.addEventListener('click', e => e.stopPropagation());

        metaCol.appendChild(btn);
        card.appendChild(metaCol);
        card.appendChild(panel);

        return card;
    }

    function buildImageCol(cluster_image, title) {
        const imgCol = document.createElement('div');
        imgCol.className = 'cr-img-col';

        const img = document.createElement('img');
        img.className = 'cr-img';
        img.src = cluster_image || getFallbackImage(title);
        img.alt = '';
        img.loading = 'lazy';
        img.referrerPolicy = 'no-referrer';
        img.onerror = () => {
            img.onerror = null;
            img.src = getFallbackImage(title);
        };
        imgCol.appendChild(img);

        return imgCol;
    }

    function buildTextCol(cluster_title, art, consensus_summary) {
        const textCol = document.createElement('div');
        textCol.className = 'cr-text-col';

        const titleEl = document.createElement('div');
        titleEl.className = 'cr-title';
        titleEl.dataset.testid = 'cluster-title';
        titleEl.textContent = cluster_title || art.title;
        textCol.appendChild(titleEl);

        if (consensus_summary) {
            const sum = document.createElement('div');
            sum.className = 'cr-summary';
            sum.dataset.testid = 'cluster-summary';
            sum.textContent = consensus_summary;
            textCol.appendChild(sum);
        }

        return textCol;
    }

    function openReader(nd) {
        try {
            sessionStorage.setItem('active_roundup', JSON.stringify(nd));
        } catch(e) {
            console.error("Could not set active roundup", e);
        }
        window.location.href = '/roundup';
    }

    document.addEventListener('click', () => {
        document.querySelectorAll('.hero-sources-panel.open, .sources-panel.open').forEach(openPanel => {
            openPanel.classList.remove('open');
        });
        document.querySelectorAll('.hero-sources-btn.open, .cr-sources-btn.open').forEach(openBtn => {
            openBtn.classList.remove('open');
        });
        document.querySelectorAll('.hero-side').forEach(card => card.style.zIndex = '');
    });

    function buildSourcesPanel(articles) {
        const panel = document.createElement('div');
        panel.className = 'sources-panel';
        panel.dataset.testid = 'sources-panel';
        articles.forEach(src => {
            const item = document.createElement('div');
            item.className = 'source-item';
            const lnk = document.createElement('a');
            lnk.className = 'source-link';
            lnk.dataset.testid = 'source-link';
            lnk.href = src.url;
            lnk.target = '_blank';
            lnk.rel = 'noopener';
            lnk.textContent = src.title;
            lnk.addEventListener('click', e => e.stopPropagation());
            const dom = document.createElement('span');
            dom.className = 'source-domain';
            dom.textContent = formatSource(src);
            item.appendChild(lnk);
            item.appendChild(dom);
            panel.appendChild(item);
        });
        return panel;
    }

    function renderClusters(data) {
        const feed = document.getElementById('story-feed');
        feed.innerHTML = '';
        const entries = Object.entries(data);
        if (!entries.length) { feed.innerHTML = '<div class="status">No stories found.</div>'; return; }

        const sorted = entries.sort((a, b) => {
            const scoreDiff = (b[1].query_score || 0) - (a[1].query_score || 0);
            if (Math.abs(scoreDiff) > 0.01) return scoreDiff;
            return b[1].articles.length - a[1].articles.length;
        });

        // ── Hero section: lead story with three supporting stories ──
        const heroCount = Math.min(4, sorted.length);
        if (heroCount >= 1) {
            const heroSection = document.createElement('div');
            heroSection.className = 'hero-section';
            const heroGrid = document.createElement('div');
            heroGrid.className = 'hero-grid';

            heroGrid.appendChild(buildHeroLead(sorted[0][1]));
            sorted.slice(1, heroCount).forEach(([, nd]) => heroGrid.appendChild(buildHeroSide(nd)));

            heroSection.appendChild(heroGrid);
            feed.appendChild(heroSection);
        }

        // ── Remaining stories ──
        const rest = sorted.slice(heroCount);
        if (rest.length > 0) {
            const moreSection = document.createElement('div');
            moreSection.className = 'more-section';
            const moreLabel = document.createElement('div');
            moreLabel.className = 'more-label';
            moreLabel.textContent = '// More Stories';
            moreSection.appendChild(moreLabel);
            rest.forEach(([, nd]) => moreSection.appendChild(buildCompact(nd)));
            feed.appendChild(moreSection);
        }
    }

    function loadQuery(query, categoryName) {
        currentQuery = query;
        currentCategoryName = categoryName;
        document.getElementById('story-feed').innerHTML = '<div class="status blink">Loading...</div>';
        const regionParam = `&region=${encodeURIComponent(currentRegion)}`;
        fetch(`/api/cluster?q=${encodeURIComponent(query)}${regionParam}`)
            .then(r => r.json())
            .then(data => renderClusters(data))
            .catch(() => { document.getElementById('story-feed').innerHTML = '<div class="status">[Error] Failed to load.</div>'; });
    }

    function triggerSearch() {
        const q = document.getElementById('search-input').value.trim();
        if (!q) return;
        document.querySelectorAll('.pill-item').forEach(el => el.classList.remove('active'));
        loadQuery(q, q);
    }

    document.querySelectorAll('.pill-item').forEach(pill => {
        pill.addEventListener('click', () => {
            document.querySelectorAll('.pill-item').forEach(el => el.classList.remove('active'));
            pill.classList.add('active');
            document.getElementById('search-input').value = '';
            loadQuery(pill.dataset.query, pill.textContent.trim());
        });
    });

    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', e => { if (e.key === 'Enter') triggerSearch(); });
    }

    window.addEventListener('storage', e => {
        if (e.key === 'lacuna_region' || e.key === 'newsRegion') {
            const next = (e.newValue || 'US').toUpperCase();
            if (next && next !== currentRegion) {
                currentRegion = next;
                buildRegionGrid();
                loadQuery(currentQuery, currentCategoryName);
            }
        }
    });

    applyTheme(currentTheme);
    buildRegionGrid();
    loadAccountDetails();
    loadQuery('__home__', 'Home');
