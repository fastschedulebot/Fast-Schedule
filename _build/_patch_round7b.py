# -*- coding: utf-8 -*-
"""Patch round 7b (blog hub): help-style search results page.

  - typing does NOT auto-search; Enter opens a full results view
  - results look like the help center's: best-result card + two-column
    rows with category chips and content snippets, <mark> highlighting
  - HelpAI (scripts/help-ai.js) does the ranking: typos, synonyms, intents
  - category filter chips above the results (All + the six blog topics)
  - deep links: #q=<query> opens the results view; #cat=<id> opens the hub
    with that category chip pre-selected
"""
import io

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# ---- 1) results view markup (inside the hub body) --------------------------
rep("""  <p id="blog-empty" class="blog-empty" hidden>No articles match your search — try a different word or pick another topic.</p>""",
    """  <section id="blog-results" class="blog-results" hidden>
    <nav class="hc-crumbs" aria-label="Breadcrumb"><a href="#" id="blog-results-back">Blog</a>{bh.svg('chev')}<span aria-current="page">Search</span></nav>
    <header class="blog-res-head">
      <h2 id="blog-res-title">Search results</h2>
      <p id="blog-res-meta"></p>
    </header>
    <div class="blog-filters" id="blog-res-filters"></div>
    <div class="bento" id="blog-res-grid"></div>
  </section>""")

# ---- 2) results view CSS ---------------------------------------------------
rep("""    .blog-empty { margin: 26px 0; color: var(--text-dim); font-size: .95rem; }""",
    """    .blog-empty { margin: 26px 0; color: var(--text-dim); font-size: .95rem; }

    /* ---------- full search results view (help-center style) ---------- */
    .blog-results[hidden] { display: none; }
    .blog-results { margin-top: 26px; }
    .blog-res-head h2 { margin: 0; font-size: 1.5rem; letter-spacing: -.02em; color: var(--text); }
    .blog-res-head p { margin: 4px 0 0; color: var(--text-dim); font-size: .92rem; }
    .blog-filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 18px; }
    .blog-fchip { font: inherit; font-size: .84rem; font-weight: 650; color: var(--text-dim);
      background: var(--surface); border: 1px solid var(--border); border-radius: 999px;
      padding: 7px 14px; cursor: pointer; transition: color .18s, border-color .18s, background .18s; }
    .blog-fchip:hover { color: var(--green-strong); border-color: color-mix(in srgb, var(--green) 50%, transparent); }
    .blog-fchip.on { color: #fff; background: var(--green-strong); border-color: var(--green-strong); }
    /* result cards reuse .bcard sizing but without images */
    #blog-res-grid { grid-template-columns: repeat(3, 1fr); }
    .bcard-text .bcard-cover { display: none; }
    .bcard-text .bcard-body { padding: 18px 20px; }
    .bcard-text .bcard-desc { display: -webkit-box; -webkit-line-clamp: 4;
      -webkit-box-orient: vertical; overflow: hidden; }
    .bcard-text mark, .blog-results mark { background: color-mix(in srgb, #ffd84d 45%, transparent);
      color: inherit; border-radius: 3px; padding: 0 1px; }
    .blog-nores { padding: 40px 0; text-align: center; color: var(--text-dim); }
    @media (max-width: 1100px) { #blog-res-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 700px) { #blog-res-grid { grid-template-columns: 1fr; } }""")

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] markup + css')
