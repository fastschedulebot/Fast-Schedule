# -*- coding: utf-8 -*-
"""Patch round 6 (2026-09-26):

  - hub: delete the hero image; replace the search-in-grid tile with a real
    search bar placed ABOVE the category chips (sticky, upgraded styling)
  - S hotkey now just focuses that bar and STAYS focused (old code focused,
    then a second global dispatcher re-resolved and the browser default ate
    the focus — also removed the scrollIntoView that fought the focus)
  - fix: pressing S while already typing in a text field must not hijack
  - articles' "More on this topic" -> hub deep links verified to auto-apply
"""
import io

def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, (path, old[:80])
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', path)

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()

# 1) remove hero image markup
old = ("  <figure class=\"blog-hero-img\"><img src=\"img/hero.jpg\" "
       "alt=\"Workspace with a phone showing a Telegram channel\" "
       "width=\"1600\" height=\"600\" loading=\"eager\"></figure>\n")
assert old in s
s = s.replace(old, "", 1)

# 2) remove hero image CSS
old = """    .blog-hero-img { margin: 18px 0 4px; border-radius: 18px; overflow: hidden;
      border: 1px solid var(--border); box-shadow: var(--shadow-sm); }
    .blog-hero-img img { display: block; width: 100%; height: clamp(180px, 26vw, 300px);
      object-fit: cover; }
"""
assert old in s
s = s.replace(old, "", 1)

# 3) search bar markup replaces the grid tile
old = """SEARCH_TILE = ('<div class="bcard bsearch" id="blog-search-tile">'
               '<label for="blog-q">Search the blog</label>'
               '<div class="bsearch-row">' + bh.svg('search') +
               '<input id="blog-q" type="search" placeholder="Search articles…" '
               'autocomplete="off" spellcheck="false"></div>'
               '<p class="bsearch-hint">Titles, topics, tools — e.g. “posting times” '
               'or “ControllerBot”.</p>'
               '</div>')"""
new = """SEARCH_BAR = ('<div class="blog-search" id="blog-search-bar">'
              '<div class="bsearch-row">' + bh.svg('search') +
              '<input id="blog-q" type="search" placeholder="Search all 60 articles — titles, topics, tools…" '
              'autocomplete="off" spellcheck="false">'
              '<kbd class="blog-search-kbd" aria-hidden="true">S</kbd></div>'
              '</div>')"""
assert old in s
s = s.replace(old, new, 1)

# 4) place the bar above the chips in the body; drop tile insertion + placeTile
old = """  <div class="blog-chips">{chips}</div>
  {''.join(secs)}"""
new = """  {SEARCH_BAR}
  <div class="blog-chips">{chips}</div>
  {''.join(secs)}"""
assert old in s
s = s.replace(old, new, 1)

old = """        cards = [card_html(a, size_for(a, i), reading_minutes(a))
                 for i, a in enumerate(arts)]
        if first:
            # the search tile sits centrally among the article blocks
            cards.insert(len(cards) // 2, SEARCH_TILE)
            first = False
        secs.append("""
new = """        cards = [card_html(a, size_for(a, i), reading_minutes(a))
                 for i, a in enumerate(arts)]
        secs.append("""
assert old in s
s = s.replace(old, new, 1)

old = """    secs = []
    first = True
    for cid in order:"""
new = """    secs = []
    for cid in order:"""
assert old in s
s = s.replace(old, new, 1)

# 5) rewrite the HUB_JS: no tile placement; focus-keeping; deep links stay
start = s.index("HUB_JS = '''<script>")
end = s.index("'''", start + 20) + 3
new_js = '''HUB_JS = \'<script>
(function () {
  var q = document.getElementById(\\'blog-q\\');
  if (!q) return;
  var bar = document.getElementById(\\'blog-search-bar\\'),
      chips = [].slice.call(document.querySelectorAll(\\'.blog-chip\\')),
      secs = [].slice.call(document.querySelectorAll(\\'.blog-sec\\')),
      empty = document.getElementById(\\'blog-empty\\'),
      cat = \\'all\\';
  function apply() {
    var raw = q.value.trim().toLowerCase();
    var terms = raw.split(/\\\\s+/).filter(Boolean);
    var shown = 0;
    secs.forEach(function (s) {
      var vis = 0;
      [].forEach.call(s.querySelectorAll(\\'.bcard:not(.bsearch)\\'), function (c) {
        var hay = c.getAttribute(\\'data-search\\') || \\'\\';
        var ok = (cat === \\'all\\' || s.getAttribute(\\'data-cat\\') === cat) &&
                 terms.every(function (w) { return hay.indexOf(w) >= 0; });
        c.classList.toggle(\\'off\\', !ok);
        if (ok) vis++;
      });
      s.style.display = vis ? \\'\\' : \\'none\\';
      shown += vis;
    });
    if (empty) empty.hidden = !!shown;
  }
  chips.forEach(function (ch) {
    ch.addEventListener(\\'click\\', function () {
      chips.forEach(function (c) { c.classList.toggle(\\'on\\', c === ch); });
      cat = ch.getAttribute(\\'data-cat\\') || \\'all\\';
      apply();
    });
  });
  /* keep focus in the field: the S hotkey focuses once; nothing here steals
     it back. Re-applying the filter on every input does NOT touch focus. */
  q.addEventListener(\\'input\\', apply);
  /* deep links: article pages link here as ../index.html#q=term+term */
  if (location.hash.indexOf(\\'#q=\\') === 0) {
    try { q.value = decodeURIComponent(location.hash.slice(3)).replace(/\\\\+/g, \\' \\'); } catch (err) {}
  }
  if (q.value) apply();
})();
</script>\''''
s = s[:start] + new_js + s[end:]

# 6) upgraded search bar CSS (sticky under the header)
old = """    /* search tile — rendered as a card placed mid-grid */
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
    .bsearch-hint { margin: 0; font-size: .8rem; color: var(--text-dim); }"""
new = """    /* search bar — sticky above the topic chips */
    .blog-search { position: sticky; top: 8px; z-index: 40; margin: 14px 0 2px; }
    .bsearch-row { display: flex; align-items: center; gap: 10px; padding: 12px 16px;
      background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
      box-shadow: var(--shadow-sm); transition: border-color .18s, box-shadow .18s; }
    .bsearch-row:focus-within { border-color: var(--green);
      box-shadow: 0 0 0 3px color-mix(in srgb, var(--green) 18%, transparent); }
    .bsearch-row svg { width: 18px; height: 18px; flex: none; color: var(--text-dim); }
    .bsearch-row input { flex: 1; min-width: 0; border: 0; outline: 0; background: transparent;
      font: inherit; font-size: .98rem; color: var(--text); }
    .bsearch-row input::placeholder { color: var(--text-dim); }
    .blog-search-kbd { font-family: inherit; font-size: .74rem; font-weight: 700;
      color: var(--text-dim); border: 1px solid var(--border); border-radius: 6px;
      padding: 2px 7px; background: var(--surface-2); }
    @media (max-width: 700px) { .blog-search-kbd { display: none; } }"""
assert old in s
s = s.replace(old, new, 1)

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok]', P)

# ---------------------------------------------------------------- hotkeys.js
patch('../scripts/hotkeys.js', [
    ("""    /* S = search on blog pages: focuses the hub's search field. The help
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
      blogOnly: true },""",
     """    /* S = search on blog pages: focuses the sticky search bar. Pressing S
       while already typing stands down (allow() normally guards this, but
       the field itself must not steal focus back mid-typing). */
    { key: 's', name: 'Search the blog', hint: false, run: function () {
        var f = document.getElementById('blog-q');
        if (!f) return;
        if (window.FS_KEYS && FS_KEYS.typing()) return;
        f.focus();
        try { f.setSelectionRange(f.value.length, f.value.length); } catch (err) {}
      } },"""),
])

print('[done] round 6')
