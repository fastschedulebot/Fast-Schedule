"""Navbar order: brand to far right; gear just left of Blog pill.

Left group: [page extras] Open-Bot CTA.
Right group: gear, Blog pill, Help pill (+quick-search popover),
Open-Bot CTA, brand.
"""
import io

p = 'website/_build/build_help.py'
s = io.open(p, encoding='utf-8', newline='').read()

old_doc = """    Left group: Open Bot CTA + settings gear + brand. Right group: Blog and
    Help Center pills + Open Bot CTA. Page-specific extras slot into
    left_extra (help sidebar burger) and center_extra (help search, legal
    doc tabs); brand_extra appends to the brand (help "Help Center" suffix);"""
assert s.count(old_doc) == 1, s.count(old_doc)
new_doc = """    Left group: page-specific left_extra (help sidebar burger) + Open Bot
    CTA. Right group: settings gear, Blog and Help Center pills, a second
    Open Bot CTA, then the brand at the far right. center_extra holds
    page extras (help search, legal doc tabs); brand_extra appends to the
    brand (help "Help Center" suffix);"""
s = s.replace(old_doc, new_doc, 1)

old_ret = """    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{left_extra}{cta}{gear}{brand}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<span class="site-menu-wrap">'
            f'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" '
            f'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>'
            f'{pop}</span>'
            f'{cta}</div></div></header>')"""
assert s.count(old_ret) == 1, s.count(old_ret)
new_ret = """    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{left_extra}{cta}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">{gear}'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<span class="site-menu-wrap">'
            f'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" '
            f'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>'
            f'{pop}</span>'
            f'{cta}{brand}</div></div></header>')"""
s = s.replace(old_ret, new_ret, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('[ok]', p)
