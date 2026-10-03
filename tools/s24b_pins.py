"""Bump hotkeys.js + hotkeys-modal.js pins (selectors changed)."""
import io

files = ['website/_build/build_blog.py', 'website/_build/build_help.py',
         'website/_build/build_site.py', 'website/_build/build_static.py',
         'website/index.html', 'index.html']
for p in files:
    s = io.open(p, encoding='utf-8', newline='').read()
    n1 = s.count('hotkeys.js?v=20260930a1')
    n2 = s.count('hotkeys-modal.js?v=20260930a1')
    if n1 or n2:
        s = s.replace('hotkeys.js?v=20260930a1', 'hotkeys.js?v=20260930a2')
        s = s.replace('hotkeys-modal.js?v=20260930a1', 'hotkeys-modal.js?v=20260930a2')
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print('[ok]', p, n1, n2)
