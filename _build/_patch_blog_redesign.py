# -*- coding: utf-8 -*-
"""One-shot patch: redesign the blog hub (bento grid + central search +
category chips + reading time + generated SVG covers) in build_blog.py.

Run:  python _patch_blog_redesign.py
"""
import io

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()
orig_len = len(s)

# ---------------------------------------------------------------------------
# 1) Replace the hub CSS block (keeps article-page + mirrored component CSS)
# ---------------------------------------------------------------------------
CSS_START = '    /* ===== hub cards ===== */'
CSS_END = '    /* ===== components mirrored'
a = s.index(CSS_START)
b = s.index(CSS_END)

NEW_CSS = r'''    /* ===== hub: topic filter chips ===== */
    .blog-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 6px; }
    .blog-chip { font: inherit; font-size: .86rem; font-weight: 650; color: var(--text-dim);
      background: var(--surface); border: 1px solid var(--border); border-radius: 999px;
      padding: 8px 16px; cursor: pointer; transition: color .18s, border-color .18s, background .18s; }
    .blog-chip:hover { color: var(--green-strong);
      border-color: color-mix(in srgb, var(--green) 50%, transparent); }
    .blog-chip.on { color: #fff; background: var(--green-strong); border-color: var(--green-strong); }

    /* ===== hub: bento grid of article cards ===== */
    .blog-sec { margin-top: 34px; }
    .blog-sec h2 { margin: 0 0 4px; font-size: 1.35rem; letter-spacing: -.02em; color: var(--text); }
    .blog-sec-desc { color: var(--text-dim); margin: 0 0 16px; font-size: .95rem; }
    .bento { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; grid-auto-flow: dense; }
    .bcard { display: flex; flex-direction: column; min-width: 0; overflow: hidden;
      background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
      color: var(--text); text-decoration: none;
      transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease; }
    .bcard:hover { border-color: var(--green); box-shadow: var(--shadow-sm);
      text-decoration: none; transform: translateY(-2px); }
    .bcard-cover { display: block; aspect-ratio: 16 / 9; overflow: hidden; background: var(--surface-2); }
    .bcard-cover img { display: block; width: 100%; height: 100%; object-fit: cover; }
    .bcard-body { display: flex; flex-direction: column; gap: 8px; flex: 1; padding: 16px 18px 18px; }
    .bcard-body b { font-size: 1rem; line-height: 1.35; letter-spacing: -.01em; }
    .bcard-desc { display: none; color: var(--text-dim); font-size: .88rem; line-height: 1.5; }
    .bcard-meta { margin-top: auto; padding-top: 4px; font-size: .78rem; color: var(--text-dim); }
    .s-lg, .s-md { grid-column: span 2; }
    .s-lg .bcard-body b { font-size: 1.18rem; }
    .s-lg .bcard-desc, .s-md .bcard-desc {
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .bcard.off { display: none; }

    /* search tile — rendered as a card placed mid-grid */
    .bsearch { grid-column: span 2; justify-content: center; gap: 10px;
      padding: 20px 22px; background: color-mix(in srgb, var(--green) 6%, var(--surface)); }
    .bsearch label { font-size: .72rem; font-weight: 800; letter-spacing: .06em;
      text-transform: uppercase; color: var(--text-dim); }
    .bsearch-row { display: flex; align-items: center; gap: 10px; padding: 11px 14px;
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }
    .bsearch-row:focus-within { border-color: var(--green); }
    .bsearch-row svg { width: 17px; height: 17px; flex: none; color: var(--text-dim); }
    .bsearch-row input { flex: 1; min-width: 0; border: 0; outline: 0; background: transparent;
      font: inherit; font-size: .95rem; color: var(--text); }
    .bsearch-hint { margin: 0; font-size: .8rem; color: var(--text-dim); }

    .blog-empty { margin: 26px 0; color: var(--text-dim); font-size: .95rem; }

    @media (max-width: 1100px) { .bento { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 700px) {
      .bento { grid-template-columns: 1fr; gap: 12px; }
      .s-lg, .s-md, .bsearch { grid-column: auto; }
      .bcard-desc { display: none !important; }
    }
    @media (max-width: 400px) {
      .bento { gap: 10px; }
      .bcard-body { padding: 14px 15px 16px; }
    }
    @media (hover: none) { .bcard:hover { transform: none; } }
    @media (prefers-reduced-motion: reduce) {
      .bcard, .bcard:hover { transition: none; transform: none; }
    }

'''
s = s[:a] + NEW_CSS + s[b:]

# ---------------------------------------------------------------------------
# 2) Replace the hub builder region (adds helpers + new build_hub + HUB_JS)
# ---------------------------------------------------------------------------
HUB_START = '# ------------------------------------------------------------------ hub ----'
HUB_END = '# -------------------------------------------------------------- articles ---'
a = s.index(HUB_START)
b = s.index(HUB_END)

NEW_HUB = r"""# ------------------------------------------------------------------ hub ----
CAT_ICON = {'growth': 'gauge', 'content': 'book', 'tools': 'bot',
            'platform': 'globe', 'money': 'crown'}
COVER_COLORS = {
    'growth':   ('#3e9d76', '#1d5c44'),
    'content':  ('#6d7ff3', '#3d3f86'),
    'tools':    ('#4f8cc9', '#2b4a72'),
    'platform': ('#4aa9c9', '#275a6e'),
    'money':    ('#d9a441', '#8a6420'),
}


def _hash(s):
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h


def reading_minutes(art):
    words = len(strip_html(art['content']).split())
    return max(3, round(words / 200))


def size_for(art, i):
    # Deterministic per-slug size mix: stable builds, varied bento layouts.
    pool = ('lg', 'sm', 'sm', 'md', 'sm', 'sm')
    return pool[(i + _hash(art['id'])) % len(pool)]


def cover_svg(art):
    c1, c2 = COVER_COLORS.get(art['category'], ('#4bb98b', '#256d4f'))
    h = _hash(art['id'])
    icon = bh.ICONS[CAT_ICON.get(art['category'], 'book')]
    x1, y1 = 90 + h % 200, 70 + (h >> 3) % 110
    r1 = 80 + (h >> 5) % 70
    x2, y2 = 640 - (h >> 7) % 180, 330 + (h >> 9) % 70
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
        '</linearGradient></defs>'
        '<rect width="800" height="450" fill="url(#g)"/>'
        '<g fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1.5">'
        f'<circle cx="{x1}" cy="{y1}" r="{r1}"/>'
        f'<circle cx="{x2}" cy="{y2}" r="{r1 + 45}"/>'
        f'<circle cx="{x2}" cy="{y1 + 30}" r="{r1 // 2}" fill="rgba(255,255,255,.07)" stroke="none"/>'
        '</g>'
        '<g transform="translate(340,165) scale(5)" stroke="rgba(255,255,255,.92)" fill="none" '
        f'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{icon}</g>'
        '</svg>')


def card_html(a, size, minutes):
    desc = a['description']
    if len(desc) > 140:
        desc = desc[:140].rstrip() + '…'
    hay = bh.esc((a['title'] + ' ' + a['description']).lower())
    return (f'<a class="bcard s-{size}" href="a/{bh.esc(a["id"])}.html" data-search="{hay}">'
            f'<span class="bcard-cover"><img src="img/{bh.esc(a["id"])}.svg" alt="" '
            f'width="800" height="450" loading="lazy"></span>'
            f'<span class="bcard-body"><b>{bh.esc(a["title"])}</b>'
            f'<span class="bcard-desc">{bh.esc(desc)}</span>'
            f'<span class="bcard-meta">{minutes} min read · {fmt_date(a["date"])}</span>'
            f'</span></a>')


SEARCH_TILE = ('<div class="bcard bsearch" id="blog-search-tile">'
               '<label for="blog-q">Search the blog</label>'
               '<div class="bsearch-row">' + bh.svg('search') +
               '<input id="blog-q" type="search" placeholder="Search articles…" '
               'autocomplete="off" spellcheck="false"></div>'
               '<p class="bsearch-hint">Titles, topics, tools — e.g. “posting times” '
               'or “ControllerBot”.</p>'
               '</div>')

HUB_JS = '''<script>
(function () {
  var q = document.getElementById('blog-q');
  if (!q) return;
  var tile = document.getElementById('blog-search-tile'),
      chips = [].slice.call(document.querySelectorAll('.blog-chip')),
      secs = [].slice.call(document.querySelectorAll('.blog-sec')),
      empty = document.getElementById('blog-empty'),
      cat = 'all';
  function placeTile() {
    if (!tile) return;
    var sec = null;
    for (var i = 0; i < secs.length; i++) {
      if (secs[i].style.display !== 'none') { sec = secs[i]; break; }
    }
    if (!sec) return;
    var grid = sec.querySelector('.bento');
    if (!grid) return;
    var vis = [].filter.call(grid.querySelectorAll('.bcard:not(.bsearch)'), function (c) {
      return !c.classList.contains('off');
    });
    var mid = vis[Math.floor(vis.length / 2)];
    if (mid) grid.insertBefore(tile, mid); else grid.appendChild(tile);
  }
  function apply() {
    var t = q.value.trim().toLowerCase(), shown = 0;
    secs.forEach(function (s) {
      var vis = 0;
      [].forEach.call(s.querySelectorAll('.bcard:not(.bsearch)'), function (c) {
        var ok = (cat === 'all' || s.getAttribute('data-cat') === cat) &&
                 (!t || (c.getAttribute('data-search') || '').indexOf(t) >= 0);
        c.classList.toggle('off', !ok);
        if (ok) vis++;
      });
      s.style.display = vis ? '' : 'none';
      shown += vis;
    });
    if (empty) empty.hidden = !!shown;
    placeTile();
  }
  chips.forEach(function (ch) {
    ch.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.toggle('on', c === ch); });
      cat = ch.getAttribute('data-cat') || 'all';
      apply();
    });
  });
  q.addEventListener('input', apply);
})();
</script>'''


def build_hub(groups):
    n = sum(len(k) for k in groups.values())
    ntopics = len([c for c in groups if groups[c]])
    lead = ('Field notes on growing Telegram channels — written for channel owners, '
            'not for search engines. No fluff, no “10 hacks” lists: just what works, '
            'from people who schedule posts for a living.')
    order = ('growth', 'content', 'tools', 'platform', 'money')
    chips = ''.join(
        f'<button type="button" class="blog-chip{" on" if cid == "all" else ""}" '
        f'data-cat="{cid}">{bh.esc(label)}</button>'
        for cid, label in
        [('all', 'All topics')] + [(c, CATEGORIES[c]['title']) for c in order if groups.get(c)])
    secs = []
    first = True
    for cid in order:
        arts = groups.get(cid)
        if not arts:
            continue
        meta = CATEGORIES[cid]
        cards = [card_html(a, size_for(a, i), reading_minutes(a))
                 for i, a in enumerate(arts)]
        if first:
            # the search tile sits centrally among the article blocks
            cards.insert(len(cards) // 2, SEARCH_TILE)
            first = False
        secs.append(
            f'<section class="blog-sec" data-cat="{cid}"><h2>{bh.esc(meta["title"])}</h2>'
            f'<p class="blog-sec-desc">{bh.esc(meta["desc"])}</p>'
            f'<div class="bento">{"".join(cards)}</div></section>')

    body = f'''<div class="blog-wrap">
  <nav class="hc-crumbs" aria-label="Breadcrumb"><a href="../index.html">Fast Scheduler</a>{bh.svg('chev')}<span aria-current="page">Blog</span></nav>
  <header class="blog-hero">
    <h1>Blog</h1>
    <p class="lead">{lead}</p>
    <p class="blog-byline">{n} in-depth guides across {ntopics} topics — new pieces added regularly.</p>
  </header>
  <div class="blog-chips">{chips}</div>
  {''.join(secs)}
  <p id="blog-empty" class="blog-empty" hidden>No articles match your search — try a different word or pick another topic.</p>
  <div class="hc-cta"><div><b>Own a Telegram channel?</b><p>The scheduling bot this blog is written around — free to start, runs your whole publishing pipeline.</p></div>
  <a class="btn btn-primary" href="{BOT_URL}" target="_blank" rel="noopener noreferrer">{bh.svg('send')} Open Fast Scheduler</a></div>
</div>'''
    title = 'Blog — Growing Telegram Channels: Guides & Field Notes | Fast Scheduler'
    desc = ('In-depth guides on Telegram channel growth, content systems, bots and '
            f'monetization. {n} long-form articles from the Fast Scheduler team.')
    canonical = f'{SITE}/blog/'
    ld = jsonld({
        '@context': 'https://schema.org', '@type': 'Blog',
        'name': 'Fast Scheduler Blog',
        'description': desc, 'url': canonical,
        'publisher': {'@type': 'Organization', 'name': 'Fast Scheduler', 'url': SITE},
        'blogPost': [{'@type': 'BlogPosting', 'headline': a['title'],
                      'url': f'{SITE}/blog/a/{a["id"]}.html',
                      'image': f'{SITE}/blog/img/{a["id"]}.svg',
                      'datePublished': a['date']} for a in ARTICLES],
    })
    head = page_head(title, desc, canonical, extra_ld=ld + '\n' + breadcrumb_ld([
        ('Fast Scheduler', SITE + '/'), ('Blog', canonical)]), og_type='website')
    return page_shell(head, body, extra_js=HUB_JS)


"""
s = s[:a] + NEW_HUB + s[b:]

# ---------------------------------------------------------------------------
# 3) Article pages: cover image in JSON-LD, reading time in the byline
# ---------------------------------------------------------------------------
s = s.replace("'mainEntityOfPage': canon,",
              "'image': f'{SITE}/blog/img/{art[\"id\"]}.svg',\n            "
              "'mainEntityOfPage': canon,", 1)
s = s.replace("heads = headings_of(art['content'])",
              "heads = headings_of(art['content'])\n        mins = reading_minutes(art)", 1)
s = s.replace('<p class="blog-byline">{cat["title"]} · {fmt_date(art["date"])} · Fast Scheduler team</p>',
              '<p class="blog-byline">{cat["title"]} · {fmt_date(art["date"])} · {mins} min read · Fast Scheduler team</p>', 1)

# ---------------------------------------------------------------------------
# 4) main(): write the generated SVG covers next to the hub
# ---------------------------------------------------------------------------
OLD_MAIN = """    io.open(os.path.join(BLOG_DIR, 'index.html'), 'w', encoding='utf-8',
            newline='\\n').write(build_hub(groups))
"""
NEW_MAIN = """    io.open(os.path.join(BLOG_DIR, 'index.html'), 'w', encoding='utf-8',
            newline='\\n').write(build_hub(groups))

    # generated preview covers (royalty-free: drawn at build time, no external assets)
    img_dir = os.path.join(BLOG_DIR, 'img')
    os.makedirs(img_dir, exist_ok=True)
    for art in ARTICLES:
        io.open(os.path.join(img_dir, art['id'] + '.svg'), 'w', encoding='utf-8',
                newline='\\n').write(cover_svg(art))
"""
assert OLD_MAIN in s, 'main() anchor not found'
s = s.replace(OLD_MAIN, NEW_MAIN, 1)

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print(f'[ok] patched {P}: {orig_len} -> {len(s)} chars')
