"""Apply the missed P1b: Help pill + popover in unified_nav right group."""
import io

p = 'website/_build/build_help.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = """f'<a class="nav-link" href="{rel}/help.html">{svg("book")}<span>Help Center</span></a>'"""
assert s.count(old) == 1, s.count(old)
new = """f'<span class="site-menu-wrap">'
            f'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" '
            f'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>'
            f'{pop}</span>'"""
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('p1c applied')
