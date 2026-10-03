# s18a: shared unified navbar builder in build_help.py.
import io

p = 'website/_build/build_help.py'
s = io.open(p, encoding='utf-8').read()

anchor = "def esc(text):"
assert s.count(anchor) == 1

func = '''def unified_nav(rel, bot_url, menu_inner, left_extra='', center_extra=''):
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
    brand = (f'<a class="brand" href="{rel}/index.html" aria-label="Fast Scheduler \\u2014 home">'
             f'<span class="brand-mark">{svg("calendar")}</span>'
             f'<span class="brand-full">Fast Scheduler</span></a>')
    center = f'<div class="nav-center">{center_extra}</div>' if center_extra else ''
    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{left_extra}{cta}{gear}{brand}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<a class="nav-link" href="{rel}/help.html">{svg("book")}<span>Help Center</span></a>'
            f'{cta}</div></div></header>')


'''
io.open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(anchor, func + anchor, 1))
print('unified_nav added')
