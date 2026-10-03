# s19: unified navbar everywhere (except main page) + strip Help/Blog rows from settings.
import io

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', p)

def rep_once(p, old, new):
    s = load(p)
    assert s.count(old) == 1, 'anchor x%d in %s: %r' % (s.count(old), p, old[:90])
    save(p, s.replace(old, new, 1))

BH = 'website/_build/build_help.py'

# ============ 1. unified_nav: Help-pill popover + brand_extra + cta_html ============
old_nav = '''def unified_nav(rel, bot_url, menu_inner, left_extra='', center_extra=''):
    """Single shared navbar for every non-main page (help, blog, legal, 404).

    Left group: Open Bot CTA + settings gear + brand. Right group: Blog and
    Help Center pills + Open Bot CTA. Page-specific extras slot into
    left_extra (help sidebar burger) and center_extra (help search, legal
    doc tabs). The main page (index) keeps its own navbar.
    """
    cta = (f'<a class="btn btn-primary nav-cta" href="{bot_url}" target="_blank" '
           f'rel="noopener noreferrer">{svg("send")}<span>Open Bot</span>'
           f'<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>')
    gear = ('<span class="settings-wrap">'
            '<button type="button" class="icon-btn" id="settingsBtn" aria-haspopup="menu" '
            'aria-expanded="false" aria-label="Settings" data-hk="settings dark anim fx keys">'
            f'{svg("gear")}</button>'
            '<div class="glass-pop" id="settingsMenu" role="menu" aria-label="Settings">'
            f'{menu_inner}</div></span>')
    brand = (f'<a class="brand" href="{rel}/index.html" aria-label="Fast Scheduler \\\u2014 home">'
             f'<span class="brand-mark">{svg("calendar")}</span>'
             f'<span class="brand-full">Fast Scheduler</span></a>')
    center = f'<div class="nav-center">{center_extra}</div>' if center_extra else ''
    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{left_extra}{cta}{gear}{brand}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<a class="nav-link" href="{rel}/help.html">{svg("book")}<span>Help Center</span></a>'
            f'{cta}</div></div></header>')'''

new_nav = '''def unified_nav(rel, bot_url, menu_inner, left_extra='', center_extra='',
                brand_extra='', cta_html=None):
    """Single shared navbar for every non-main page (help, blog, legal, 404).

    Left group: Open Bot CTA + settings gear + brand. Right group: Blog and
    Help Center pills + Open Bot CTA. Page-specific extras slot into
    left_extra (help sidebar burger) and center_extra (help search, legal
    doc tabs); brand_extra appends to the brand (help "Help Center" suffix);
    cta_html overrides the default CTA (legal tooltip CTA). The Help
    quick-search popover (#siteMenu, owned by help-search.js) hangs off the
    Help Center pill — NOT inside the settings menu. The main page (index)
    keeps its own navbar.
    """
    cta = cta_html or (f'<a class="btn btn-primary nav-cta" href="{bot_url}" target="_blank" '
                       f'rel="noopener noreferrer">{svg("send")}<span>Open Bot</span>'
                       f'<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>')
    gear = ('<span class="settings-wrap">'
            '<button type="button" class="icon-btn" id="settingsBtn" aria-haspopup="menu" '
            'aria-expanded="false" aria-label="Settings" data-hk="settings dark anim fx keys">'
            f'{svg("gear")}</button>'
            '<div class="glass-pop" id="settingsMenu" role="menu" aria-label="Settings">'
            f'{menu_inner}</div></span>')
    brand = (f'<a class="brand" href="{rel}/index.html" aria-label="Fast Scheduler \\\u2014 home">'
             f'<span class="brand-mark">{svg("calendar")}</span>'
             f'<span class="brand-full">Fast Scheduler</span>{brand_extra}</a>')
    pop = (f'<div class="glass-pop site-menu-pop help-menu nav-menu-pop" id="siteMenu" role="menu" '
           f'aria-label="Help center quick search">'
           f'<form class="help-search" id="helpSearchForm" role="search">'
           f'{svg("search", "sic")}'
           f'<input type="search" id="helpSearchInput" placeholder="Search the help center\\u2026" '
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

rep_once(BH, old_nav, new_nav)

# ============ 2. help page: build NAV from parts, replace old header ============
s = load(BH)
old_header_start = '<body>\n<header class="site">'
assert s.count(old_header_start) == 1
hi = s.find(old_header_start)
he = s.find('\n  <div class="hc-progress"', hi)
assert he > hi
old_header = s[hi + len('<body>\n'):he]
assert '<div class="hc-progress"' not in old_header and 'id="siteMenu"' in old_header

nav_code = '''    BURGER = ('<button class="icon-btn hc-menu-btn" id="hcMenuBtn" aria-label="Open navigation" '
              'aria-controls="hcSideNav">%s</button>' % svg('menu'))
    HSEARCH = ('<div class="hc-hsearch">%s'
               '<input id="hcSearchH" type="search" placeholder="Search articles" '
               'aria-label="Search help articles" autocomplete="off" aria-expanded="false" '
               'aria-controls="hcResultsH" enterkeyhint="search">'
               '<kbd>S</kbd>'
               '<div class="hc-results" id="hcResultsH" role="listbox" '
               'aria-label="Search results" hidden></div></div>' % svg('search', 'sic'))
    MENU_INNER = (
      '<div class="gp-head">Settings</div>'
      '<button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="false" '
      'id="rowDark">%s<span>Dark mode</span><span class="io-switch" aria-hidden="true"></span></button>'
      '<button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" '
      'id="rowAnim">%s<span>Animations</span><span class="io-switch" aria-hidden="true"></span></button>'
      '<button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" '
      'id="rowFx">%s<span>Effects</span><span class="io-switch" aria-hidden="true"></span></button>'
      '<button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" '
      'id="rowKeys">%s<span>Hotkeys</span><span class="io-switch" aria-hidden="true"></span></button>'
      '<div class="gp-sep gp-reading" data-reading hidden></div>'
      '<div class="gp-head gp-reading" data-reading hidden>Reading</div>'
      '<button type="button" class="gp-row gp-reading" data-reading role="menuitemcheckbox" '
      'aria-checked="false" data-wide-toggle hidden>%s<span>Wide format</span>'
      '<span class="io-switch" aria-hidden="true"></span></button>'
      '<button type="button" class="gp-row gp-reading" data-reading role="menuitemcheckbox" '
      'aria-checked="true" data-rail-toggle hidden>%s<span>Article navigation</span>'
      '<span class="io-switch" aria-hidden="true"></span></button>'
      '<div class="gp-row gp-fonts" data-fonts>%s<span>Font size</span><span class="hc-fonts">'
      '<button type="button" data-font="s" aria-label="Small">A</button>'
      '<button type="button" data-font="m" aria-label="Default">A</button>'
      '<button type="button" data-font="l" aria-label="Large">A</button></span></div>'
      '<button type="button" class="gp-row gp-row-sub" id="rowKeysHelp" role="menuitem">'
      '<svg viewBox="0 0 24 24" fill="none" stroke="none" aria-hidden="true" '
      'style="visibility:hidden;width:18px;height:18px"></svg><span class="gp-sub-label">See hotkeys</span>'
      '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
      '<polyline points="9 18 15 12 9 6"/></svg></button>'
      '<div class="gp-sep" role="separator"></div>'
      '<a class="gp-row" role="menuitem" href="%s" target="_blank" rel="noopener noreferrer">'
      '%s<span>Support chat</span>%s</a>'
      % (svg('moon'), svg('zap'), svg('sparkles'), svg('keys'), svg('expand'), svg('book'),
         svg('book'), SUPPORT_URL, svg('send'), svg('chev')))
    NAV = unified_nav('.', BOT_URL, MENU_INNER, left_extra=BURGER, center_extra=HSEARCH,
                      brand_extra='<span class="hc-brand-help">Help Center</span>')
'''

anchor = "    return f'''<!doctype html>"
assert s.count(anchor) == 1
s = s.replace(anchor, nav_code + '    page = f\'\'\'<!doctype html>', 1)
assert old_header in s
s = s.replace(old_header, '@@HDR@@', 1)
tail = "</html>'''\n\n\ndef main():"
assert s.count(tail) == 1
s = s.replace(tail, "</html>'''\n    return page.replace('@@HDR@@', NAV)\n\n\ndef main():", 1)
save(BH, s)
print('help header switched')
print('s19 part 1 done')
