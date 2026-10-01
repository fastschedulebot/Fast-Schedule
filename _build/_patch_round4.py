# -*- coding: utf-8 -*-
"""Patch round 4 (2026-09-26):

  build_blog.py
    - real reading time: words/200, min 1 (was max(3, ...) so every card
      said "3 min read" no matter the length)
    - hub search goes deep: cards index title + description + body text
    - multi-word queries: every word must match, so "50 ideas" finds the
      ideas article
    - hub accepts #q= deep links, so an article's "More on this topic"
      link lands on the hub with results already filtered
  hotkeys.js
    - S focuses the blog search field on blog pages (help center keeps its
      own S = search; blog pages load no help-center script)
  build_blog.py article template
    - "More on this topic" chip at the end of every article, deep-linking
      into the hub search
"""
import io

def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, (path, old[:80])
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', path)

# ------------------------------------------------------------- build_blog.py
patch('build_blog.py', [
    # 1) real reading time
    ("""def reading_minutes(art):
    words = len(strip_html(art['content']).split())
    return max(3, round(words / 200))""",
     """def reading_minutes(art):
    \"\"\"Honest reading time: average adult reads ~200 wpm of mixed prose.
    Counts the body text (headings included — readers skim them too) and
    FAQ answers, which live in art['faq']. Minimum 1 minute.\"\"\"
    words = len(strip_html(art['content']).split())
    for f in art.get('faq') or []:
        words += len(strip_html(f['q'] + ' ' + f['a']).split())
    return max(1, round(words / 200))"""),
    # 2) full-text search haystack
    ("""    hay = bh.esc((a['title'] + ' ' + a['description']).lower())""",
     """    hay = bh.esc((a['title'] + ' ' + a['description'] + ' ' +
                  strip_html(a['content'])).lower())"""),
    # 3) multi-word matching + deep links in the hub JS
    ("""  function apply() {
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
  }""",
     """  function apply() {
    var raw = q.value.trim().toLowerCase();
    /* multi-word queries: every word must match somewhere in the card's
       title/description/body text, so "50 ideas" finds the ideas guide and
       "posting time" finds the best-time article */
    var terms = raw.split(/\\s+/).filter(Boolean);
    var shown = 0;
    secs.forEach(function (s) {
      var vis = 0;
      [].forEach.call(s.querySelectorAll('.bcard:not(.bsearch)'), function (c) {
        var hay = c.getAttribute('data-search') || '';
        var ok = (cat === 'all' || s.getAttribute('data-cat') === cat) &&
                 terms.every(function (w) { return hay.indexOf(w) >= 0; });
        c.classList.toggle('off', !ok);
        if (ok) vis++;
      });
      s.style.display = vis ? '' : 'none';
      shown += vis;
    });
    if (empty) empty.hidden = !!shown;
    placeTile();
  }"""),
    ("""  q.addEventListener('input', apply);
})();""",
     """  q.addEventListener('input', apply);
  /* deep links: blog/a/*.html "More on this topic" chips link here as
     ../index.html#q=word+word — land with the search already applied */
  if (location.hash.indexOf('#q=') === 0) {
    try { q.value = decodeURIComponent(location.hash.slice(3)).replace(/\\+/g, ' '); } catch (err) {}
  }
  if (q.value) apply();
})();"""),
    # 4) "More on this topic" chip inside every article
    ("""      <div class="blog-bot-links">""",
     """      <div class="blog-moreq"><a href="../index.html#q={bh.esc(art['category'])}">More on this topic{bh.svg('arrow-r')}</a></div>
      <div class="blog-bot-links">"""),
    # 5) chip styling
    ("""    .blog-bot-links { margin: 22px 0 4px; padding: 14px 18px; border-radius: 14px;""",
     """    .blog-moreq { margin: 20px 0 0; }
    .blog-moreq a { display: inline-flex; align-items: center; gap: 7px; font-size: .9rem;
      font-weight: 650; color: var(--green-strong); text-decoration: none;
      padding: 9px 15px; border: 1px solid color-mix(in srgb, var(--green) 35%, var(--border));
      border-radius: 999px; transition: border-color .18s, background .18s; }
    .blog-moreq a:hover { border-color: var(--green);
      background: color-mix(in srgb, var(--green) 7%, transparent); text-decoration: none; }
    .blog-moreq svg { width: 15px; height: 15px; }
    .blog-bot-links { margin: 22px 0 4px; padding: 14px 18px; border-radius: 14px;"""),
])

# --------------------------------------------------------------- hotkeys.js
patch('../scripts/hotkeys.js', [
    ("""    { key: 'g', sel: 'a.nav-link[href*="blog"], .help-row a[href*="blog"], a[href$="blog/index.html"], a[href$="/blog/"]',
      name: 'Blog', hint: 'rail' },""",
     """    { key: 'g', sel: 'a.nav-link[href*="blog"], .help-row a[href*="blog"], a[href$="blog/index.html"], a[href$="/blog/"]',
      name: 'Blog', hint: 'rail' },
    /* S = search on blog pages: focuses the hub's search field. The help
       center binds its own S (help.html doesn't load that script), and on
       the home page S belongs to the hero search there — both declare the
       key themselves; no selector here would collide. */
    { key: 's', name: 'Search the blog', hint: false, run: function () {
        var f = document.getElementById('blog-q');
        if (f) {
          var tile = document.getElementById('blog-search-tile');
          if (tile && tile.scrollIntoView) tile.scrollIntoView({ block: 'center' });
          f.focus(); f.select();
        }
      },
      blogOnly: true },"""),
])

print('[done] round 4')
