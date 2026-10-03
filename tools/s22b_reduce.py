"""OS reduced-motion: fullscreen chrome hides instantly (like the header)."""
import io

p = 'website/_build/build_help.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = """    @media (min-width: 1021px) {
      html.hc-fs .hc-side { margin-left: -284px; }
    }"""
assert s.count(old) == 1, s.count(old)
new = old + """
    /* OS-level reduced motion: instant hide (the navbar is already covered
       by the shared reduced-motion block; this covers the fs fades). */
    @media (prefers-reduced-motion: reduce) {
      html.hc-fs .hc-progress, html.hc-fs .hc-fab, html.hc-fs .hc-rail,
      html.hc-fs .hc-side-reveal, html.hc-fs footer.site, html.hc-fs .hc-cta,
      html.hc-fs .hc-pager, html.hc-fs .hc-side,
      .hc-cta, .hc-pager, .hc-rail { transition: none !important; }
    }"""
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('[ok]', p)
