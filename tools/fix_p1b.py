"""Repair the broken P1b block in tools/s20_unified_nav.py (shell mangling)."""
import io

p = 'tools/s20_unified_nav.py'
s = io.open(p, encoding='utf-8', newline='').read()
a = s.find('# ============ P1b:')
b = s.find("print('P1 done')")
assert a != -1 and b != -1 and b > a, (a, b)
block = '''# ============ P1b: right-group Help pill + popover ============
if "nav-menu-pop" not in load(BH):
    p1s = load(BH)
    p1old = """f\\'<a class="nav-link" href="{rel}/help.html">{svg("book")}<span>Help Center</span></a>\\'"""
    assert p1s.count(p1old) == 1, p1s.count(p1old)
    p1new = """f\\'<span class="site-menu-wrap">\\'
            f\\'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" \\'
            f\\'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>\\'
            f\\'{pop}</span>\\'"""
    save(BH, p1s.replace(p1old, p1new, 1))
print('P1 done')
'''
s = s[:a] + block + s[b + len("print('P1 done'):"):]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('p1b fixed')
