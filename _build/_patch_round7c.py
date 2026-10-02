# -*- coding: utf-8 -*-
"""Patch round 7c: replace HUB_JS with the Enter-driven help-style search.
Also embeds the search index JSON, loads help-ai.js on the hub, and updates
page_shell usage so the hub gets the script tag.
"""
import io

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()

start = s.index("HUB_JS = '''<script>")
end = s.index("</script>'''", start) + len("</script>'''")

js = """HUB_JS = '''<script>
/* Blog search: Enter opens a help-style results view (no live filtering).
   Ranking via window.HelpAI (scripts/help-ai.js): typo tolerance, synonyms,
   intent matching — the same engine the help center uses. */
(function () {
  var q = document.getElementById('blog-q');
  if (!q) return;
  var form = q.closest('form') || q.closest('.bsearch-row'),
      bar = document.getElementById('blog-search-bar'),
      chips = [].slice.call(document.querySelectorAll('.blog-chip')),
      secs = [].slice.call(document.querySelectorAll('.blog-sec')),
      view = document.getElementById('blog-results'),
      grid = document.getElementById('blog-res-grid'),
      meta = document.getElementById('blog-res-meta'),
      title = document.getElementById('blog-res-title'),
      filtersEl = document.getElementById('blog-res-filters'),
      backBtn = document.getElementById('blog-results-back');
  var CATS = {};
  chips.forEach(function (c) { CATS[c.getAttribute('data-cat')] = c.textContent.trim(); });
  var CAT_ORDER = ['all', 'growth', 'content', 'tools', 'premium', 'platform', 'money'];
  var DOCS = [];
  try { DOCS = JSON.parse(document.getElementById('blogSearchData').textContent); } catch (e) {}
  DOCS.forEach(function (d) { d.intent = d.c; });
  var state = { q: '', cat: 'all' };

  function esc(x) {
    return String(x == null ? '' : x).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function mark(raw, term) {
    if (!term) return esc(raw);
    var out = '', low = String(raw).toLowerCase(), i = 0, idx;
    while ((idx = low.indexOf(term, i)) !== -1) {
      out += esc(raw.slice(i, idx)) + '<mark>' + esc(raw.slice(idx, idx + term.length)) + '</mark>';
      i = idx + term.length;
    }
    return out + esc(raw.slice(i));
  }
  function snippet(text, term) {
    var low = String(text).toLowerCase(), i = low.indexOf(term);
    if (i === -1) return String(text).slice(0, 150) + '\\u2026';
    var startT = Math.max(0, i - 50);
    return (startT > 0 ? '\\u2026' : '') + text.slice(startT, startT + 160) + '\\u2026';
  }

  function runSearch() {
    var raw = q.value.trim();
    state.q = raw.toLowerCase();
    if (!raw) { showHub(); return; }
    var hits = DOCS.slice();
    if (window.HelpAI) {
      var ranked = window.HelpAI.scoreAll(raw, DOCS).map(function (x) { return { doc: x.doc, s: x.score }; });
      var seen = {};
      ranked.forEach(function (r) { seen[r.doc.id] = true; });
      DOCS.forEach(function (d) {
        if (seen[d.id]) return;
        var low = (d.t + ' ' + d.d + ' ' + d.b + ' ' + d.f).toLowerCase();
        if (state.q && low.indexOf(state.q) !== -1) ranked.push({ doc: d, s: 10 });
      });
      hits = ranked.filter(function (r) { return r.s > 0; }).sort(function (a, b) { return b.s - a.s; })
        .map(function (r) { return r.doc; });
    } else {
      hits = DOCS.filter(function (d) {
        var low = (d.t + ' ' + d.d + ' ' + d.b + ' ' + d.f).toLowerCase();
        return state.q.split(/\\s+/).every(function (w) { return low.indexOf(w) !== -1; });
      });
    }
    renderResults(hits, raw);
  }

  function renderResults(hits, raw) {
    secs.forEach(function (s) { s.style.display = 'none'; });
    chips.forEach(function (c) { c.classList.remove('on'); });
    bar.style.display = 'none';
    view.hidden = false;
    title.textContent = 'Search results';
    meta.textContent = hits.length
      ? hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for \\u201c' + raw + '\\u201d'
      : '0 results for \\u201c' + raw + '\\u201d';
    /* category filter chips */
    var present = {};
    hits.forEach(function (h) { present[h.c] = true; });
    var fhtml = '';
    CAT_ORDER.forEach(function (cid) {
      if (cid !== 'all' && !present[cid]) return;
      fhtml += '<button type="button" class="blog-fchip' + (cid === state.cat ? ' on' : '') +
        '" data-fcat="' + cid + '">' + esc(CATS[cid] || 'All') + '</button>';
    });
    filtersEl.innerHTML = fhtml;
    filtersEl.querySelectorAll('.blog-fchip').forEach(function (b) {
      b.addEventListener('click', function () {
        state.cat = b.getAttribute('data-fcat');
        filtersEl.querySelectorAll('.blog-fchip').forEach(function (x) {
          x.classList.toggle('on', x.getAttribute('data-fcat') === state.cat);
        });
        paintGrid(hits, raw);
      });
    });
    paintGrid(hits, raw);
    try { history.replaceState(null, '', '#q=' + encodeURIComponent(raw)); } catch (e) {}
    window.scrollTo(0, 0);
  }

  function paintGrid(hits, raw) {
    var shown = hits.filter(function (h) { return state.cat === 'all' || h.c === state.cat; });
    if (!shown.length) {
      grid.innerHTML = '<p class="blog-nores">Nothing in this category — try \\u201cAll\\u201d.</p>';
      return;
    }
    grid.innerHTML = shown.map(function (d) {
      return '<a class="bcard bcard-text" href="a/' + esc(d.id) + '.html">' +
        '<span class="bcard-body"><b>' + mark(d.t, state.q) + '</b>' +
        '<span class="bcard-desc">' + mark(snippet(d.d + ' ' + d.b, state.q), state.q) + '</span>' +
        '<span class="bcard-meta">' + esc(CATS[d.c] || '') + '</span></span></a>';
    }).join('');
  }

  function showHub() {
    view.hidden = true;
    bar.style.display = '';
    secs.forEach(function (s) { s.style.display = ''; });
    try { history.replaceState(null, '', location.pathname); } catch (e) {}
  }

  /* Enter-only search; Esc or the breadcrumb returns to the hub */
  if (form) {
    form.addEventListener('submit', function (e) { e.preventDefault(); runSearch(); });
  }
  q.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { q.value = ''; showHub(); q.blur(); }
  });
  if (backBtn) backBtn.addEventListener('click', function (e) { e.preventDefault(); showHub(); });

  /* deep links:
     #q=<query>  -> open results view for that query
     #cat=<id>   -> hub with that category chip active ("More on this topic") */
  function applyHash() {
    var h = location.hash || '';
    if (h.indexOf('#q=') === 0) {
      var query = '';
      try { query = decodeURIComponent(h.slice(3)).replace(/\\+/g, ' '); } catch (err) {}
      if (query) { q.value = query; runSearch(); return true; }
    }
    if (h.indexOf('#cat=') === 0) {
      var cid = h.slice(5);
      var chip = chips.filter(function (c) { return c.getAttribute('data-cat') === cid; })[0];
      if (chip) { chip.click(); window.scrollTo(0, 0); return true; }
    }
    return false;
  }
  window.addEventListener('hashchange', function () { if (applyHash()) { /* handled */ } });
  if (applyHash()) { /* deep link took over */ }
})();
</script>'''"""

s = s[:start] + js + s[end:]

# ---- embed the index JSON + load help-ai.js on the hub ---------------------
rep_blog = io.open(P, encoding='utf-8').read()

old = "    return page_shell(head, body, extra_js=HUB_JS)"
new = ("    search_json = _search_docs()\n"
       "    data_tag = f'<script id=\"blogSearchData\" type=\"application/json\">{search_json}</script>'\n"
       "    ai_tag = f'<script src=\"{{rel}}/scripts/help-ai.js?v=20260930a1\"></script>'\n"
       "    return page_shell(head, body, extra_js=data_tag + ai_tag + HUB_JS)")
assert old in rep_blog
rep_blog = rep_blog.replace(old, new, 1)

# page_shell puts extra_js before </body> — fine, but the data tag must come
# before HUB_JS (it does). help-ai.js path: hub is at blog/, so rel='..'
rep_blog = rep_blog.replace(
    "    ai_tag = f'<script src=\"{rel}/scripts/help-ai.js?v=20260930a1\"></script>'",
    "    ai_tag = '<script src=\"../scripts/help-ai.js?v=20260930a1\"></script>'", 1)

io.open(P, 'w', encoding='utf-8', newline='\n').write(rep_blog)

import ast
ast.parse(rep_blog)
print('[ok] HUB_JS + data tag + help-ai wired; syntax OK')
