"""Also kill the base transition additions under reduced motion (exit path)."""
import io

p = 'website/_build/build_help.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = """      html.hc-fs .hc-pager, html.hc-fs .hc-side,
      .hc-cta, .hc-pager, .hc-rail { transition: none !important; }"""
assert s.count(old) == 1, s.count(old)
new = """      html.hc-fs .hc-pager, html.hc-fs .hc-side,
      .hc-cta, .hc-pager, .hc-rail, .hc-progress, .hc-fab,
      .hc-side-reveal { transition: none !important; }"""
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('[ok]', p)
