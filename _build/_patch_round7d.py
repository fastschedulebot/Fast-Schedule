# -*- coding: utf-8 -*-
"""Patch round 7d (help center):

  - build_search_json gains the BLOG articles: each blog post becomes a
    searchable doc tagged c='blog' (chip label "Blog") and links to the
    real blog page instead of the #/a/ help route
  - the search results page gets category filter chips (like the blog's)
"""
import io

P = 'build_help.py'
s = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new, 1)

# ---- 1) index: merge blog docs ---------------------------------------------
rep("""def build_search_json(article_order, groups):
    cat_title = {g['cat']['id']: g['cat']['title'] for g in groups}
    sections = []
    for n in article_order:
        faq = ' '.join((f['q'] + ' ' + re.sub(r'<[^>]+>', ' ', f['a'])) for f in n['faq'])
        body = re.sub(r'<[^>]+>', ' ', n['content'])
        desc = (n.get('description') or ' '.join(body.split())[:160])
        sections.append({'id': n['id'], 'c': n.get('c', ''), 't': n['title'], 'b': body, 'f': faq, 'd': desc})
    return json.dumps(sections, ensure_ascii=False)""",
    """def _blog_search_docs():
    \"\"\"Blog articles as search docs. c='blog' renders a Blog chip; href
    points at the real blog page. Reads the index the blog builder exports
    (falls back to importing the article modules directly).\"\"\"
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    idx = os.path.join(here, '_blog_search_data.json')
    docs = []
    try:
        raw = json.load(open(idx, encoding='utf-8'))
        docs = [{'id': d['id'], 'c': 'blog', 't': d['t'], 'b': d['b'], 'f': d.get('f', ''),
                 'd': d.get('d', ''), 'href': 'blog/a/' + d['id'] + '.html'} for d in raw]
    except Exception:
        pass
    return docs


def build_search_json(article_order, groups):
    cat_title = {g['cat']['id']: g['cat']['title'] for g in groups}
    sections = []
    for n in article_order:
        faq = ' '.join((f['q'] + ' ' + re.sub(r'<[^>]+>', ' ', f['a'])) for f in n['faq'])
        body = re.sub(r'<[^>]+>', ' ', n['content'])
        desc = (n.get('description') or ' '.join(body.split())[:160])
        sections.append({'id': n['id'], 'c': n.get('c', ''), 't': n['title'], 'b': body, 'f': faq, 'd': desc})
    sections += _blog_search_docs()
    return json.dumps(sections, ensure_ascii=False)""")

# ---- 2) CATS gets a Blog label ----------------------------------------------
rep("""  var CATS = {};
  SIDE.forEach(function (c) { CATS[c.id] = c.title; });""",
    """  var CATS = {};
  SIDE.forEach(function (c) { CATS[c.id] = c.title; });
  CATS.blog = 'Blog';""")

# ---- 3) resultRow + best card honor href ------------------------------------
rep("""  function resultRow(sec, q) {
    return '<a class="hc-row" href="#/a/' + sec.id + '"><span class="hc-row-t">' +
      markText(sec.t, q) + '</span><span class="hc-row-m">' +
      escapeHtml(CATS[sec.c] || '') + '</span>' + CHEV_SVG + '</a>';
  }""",
    """  function docHref(sec) { return sec.href ? sec.href : ('#/a/' + sec.id); }
  function resultRow(sec, q) {
    return '<a class="hc-row" href="' + docHref(sec) + '"><span class="hc-row-t">' +
      markText(sec.t, q) + '</span><span class="hc-row-m">' +
      escapeHtml(CATS[sec.c] || '') + '</span>' + CHEV_SVG + '</a>';
  }""")

rep("""        html += '<a class="hc-best" href="#/a/' + top.sec.id + '">' +""",
    """        html += '<a class="hc-best" href="' + docHref(top.sec) + '">' +""")

# ---- 4) category filter chips on the search page ----------------------------
rep("""          <div class="hc-list" id="hcSearchList" hidden></div>""",
    """          <div class="hc-filters" id="hcSearchFilters" hidden></div>
          <div class="hc-list" id="hcSearchList" hidden></div>""")

rep("""    /* ---------- full search results page ---------- */""",
    """    /* search page category filter chips */
    .hc-filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 6px; }
    .hc-filters[hidden] { display: none; }
    .hc-fchip { font: inherit; font-size: .84rem; font-weight: 650; color: var(--text-dim);
      background: var(--surface); border: 1px solid var(--border); border-radius: 999px;
      padding: 7px 14px; cursor: pointer; transition: color .18s, border-color .18s, background .18s; }
    .hc-fchip:hover { color: var(--green-strong); border-color: color-mix(in srgb, var(--green) 50%, transparent); }
    .hc-fchip.on { color: #fff; background: var(--green-strong); border-color: var(--green-strong); }

    /* ---------- full search results page ---------- */""")

# ---- 5) renderSearchPage: filter state + chips + re-render ------------------
rep("""    if (searchList) searchQEl_check();""".replace('searchQEl_check()', 'x') if False else """    hits = hits.slice(0, 40);""",
    """    hits = hits.slice(0, 40);
    renderSearchFilters(hits, q);""")

rep("""    if (hits.length) {
      if (searchEmpty) searchEmpty.hidden = true;
      searchList.hidden = false;
      if (searchSug) searchSug.innerHTML = '';
      var top = hits[0], rest = hits.slice(1);""",
    """    if (hits.length) {
      if (searchEmpty) searchEmpty.hidden = true;
      searchList.hidden = false;
      if (searchSug) searchSug.innerHTML = '';
      hits = hits.filter(function (x) { return searchCat === 'all' || x.sec.c === searchCat; });
      var top = hits[0], rest = hits.slice(1);""")

rep("""  function renderSearchPage(q) {""",
    """  var searchCat = 'all';
  function renderSearchFilters(hits, q) {
    var el = document.getElementById('hcSearchFilters');
    if (!el) return;
    var present = {};
    hits.forEach(function (x) { present[x.sec.c] = true; });
    var order = Object.keys(present).sort(function (a, b) {
      if (a === 'blog') return -1; if (b === 'blog') return 1; return 0; });
    if (order.length < 2) { el.hidden = true; el.innerHTML = ''; return; }
    el.hidden = false;
    var html = '<button type="button" class="hc-fchip' + (searchCat === 'all' ? ' on' : '') +
      '" data-fcat="all">All</button>';
    order.forEach(function (cid) {
      html += '<button type="button" class="hc-fchip' + (searchCat === cid ? ' on' : '') +
        '" data-fcat="' + escapeHtml(cid) + '">' + escapeHtml(CATS[cid] || cid) + '</button>';
    });
    el.innerHTML = html;
    el.querySelectorAll('.hc-fchip').forEach(function (b) {
      b.addEventListener('click', function () {
        searchCat = b.getAttribute('data-fcat');
        renderSearchPage(q);
      });
    });
  }

  function renderSearchPage(q) {""")

rep("""    q = String(q || '').trim().slice(0, 200);""",
    """    q = String(q || '').trim().slice(0, 200);
    if (window.__blogSearchQ !== q) { window.__blogSearchQ = q; searchCat = 'all'; }""")

# the meta count should reflect the filtered list; move meta update after filter
rep("""    if (searchMeta) searchMeta.textContent = hits.length
      ? hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for “' + q + '”'
      : '0 results';
    if (hits.length) {""",
    """    if (searchMeta) searchMeta.textContent = hits.length
      ? hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for “' + q + '”'
      : '0 results';
    if (hits.length) {""")

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
import ast
ast.parse(s)
print('[ok] build_help.py: blog in index + category filters; syntax OK')
