# s19a: upgrade unified_nav (popover off Help pill, brand_extra, cta_html).
import io
p = 'website/_build/build_help.py'
s = io.open(p, encoding='utf-8').read()

a1 = "def unified_nav(rel, bot_url, menu_inner, left_extra='', center_extra=''):"
b1 = ("def unified_nav(rel, bot_url, menu_inner, left_extra='', center_extra='',\n"
      "                brand_extra='', cta_html=None):")
assert s.count(a1) == 1
s = s.replace(a1, b1, 1)

a2 = '''    doc tabs). The main page (index) keeps its own navbar.
    """'''
b2 = '''    doc tabs); brand_extra appends to the brand (help "Help Center" suffix);
    cta_html overrides the default CTA (legal tooltip CTA). The Help
    quick-search popover (#siteMenu, owned by help-search.js) hangs off the
    Help Center pill — NOT inside the settings menu. The main page (index)
    keeps its own navbar.
    """'''
assert s.count(a2) == 1
s = s.replace(a2, b2, 1)

a3 = '''    cta = (f'<a class="btn btn-primary nav-cta" href="{bot_url}" target="_blank" '
           f'rel="noopener noreferrer">{svg("send")}<span>Open Bot</span>'
           f'<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>')'''
b3 = '''    cta = cta_html or (f'<a class="btn btn-primary nav-cta" href="{bot_url}" target="_blank" '
                       f'rel="noopener noreferrer">{svg("send")}<span>Open Bot</span>'
                       f'<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>')'''
assert s.count(a3) == 1
s = s.replace(a3, b3, 1)

a4 = """f'<span class="brand-full">Fast Scheduler</span></a>')"""
b4 = """f'<span class="brand-full">Fast Scheduler</span>{brand_extra}</a>')"""
assert s.count(a4) == 1
s = s.replace(a4, b4, 1)

a5 = '''    center = f'<div class="nav-center">{center_extra}</div>' if center_extra else ''
    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{left_extra}{cta}{gear}{brand}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<a class="nav-link" href="{rel}/help.html">{svg("book")}<span>Help Center</span></a>'
            f'{cta}</div></div></header>')'''
b5 = '''    pop = (f'<div class="glass-pop site-menu-pop help-menu nav-menu-pop" id="siteMenu" role="menu" '
           f'aria-label="Help center quick search">'
           f'<form class="help-search" id="helpSearchForm" role="search">'
           f'{svg("search", "sic")}'
           f'<input type="search" id="helpSearchInput" placeholder='
           f'"Search the help center' + chr(8230) + '" '
           f'autocomplete="off" aria-label="Search the help center">'
           f'</form>'
           f'<div class="help-recent">'
           f'<div class="help-recent-title" id="helpRecentTitle">Popular articles</div>'
           f'<div class="help-recent-list" id="helpRecentList"></div>'
           f'</div>'
           f'<a class="gp-row help-menu-open" role="menuitem" href="{rel}/help.html">'
           f'{svg("book")}<span>Open Help Center</span>{svg("chev")}</a>'
           f'</div>')
    center = f'<div class="nav-center">{center_extra}</div>' if center_extra else ''
    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{left_extra}{cta}{gear}{brand}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<span class="site-menu-wrap">'
            f'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" '
            f'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>'
            f'{pop}</span>'
            f'{cta}</div></div></header>')'''
assert s.count(a5) == 1
s = s.replace(a5, b5, 1)

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('s19a done')
