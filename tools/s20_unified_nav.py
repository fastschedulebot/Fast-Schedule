# s20: unified navbar everywhere except main page + strip Help/Blog/Main-site rows.
import io, os

def load(p):
    return io.open(p, encoding='utf-8', newline='').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('[ok]', p)

def rep_once(p, old, new):
    s = load(p)
    n = s.count(old)
    assert n == 1, 'anchor x%d in %s: %r' % (n, p, old[:100])
    save(p, s.replace(old, new, 1))

def rep_all(p, old, new):
    s = load(p)
    n = s.count(old)
    assert n >= 1, 'anchor missing in %s: %r' % (p, old[:100])
    save(p, s.replace(old, new))
    print('  replaced x%d' % n)

BH = 'website/_build/build_help.py'
BB = 'website/_build/build_blog.py'
BS = 'website/_build/build_static.py'
BL = 'website/_build/build_site.py'

# ============ P1b: right-group Help pill + popover ============
if "nav-menu-pop" not in load(BH):
    p1s = load(BH)
    p1old = """f\'<a class="nav-link" href="{rel}/help.html">{svg("book")}<span>Help Center</span></a>\'"""
    assert p1s.count(p1old) == 1, p1s.count(p1old)
    p1new = """f\'<span class="site-menu-wrap">\'
            f\'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" \'
            f\'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>\'
            f\'{pop}</span>\'"""
    save(BH, p1s.replace(p1old, p1new, 1))
print('P1 done')


# ============ P2: help page header -> unified_nav ============
s = load(BH)
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
assert s.count(anchor) == 1, 'help return anchor x%d' % s.count(anchor)
s = s.replace(anchor, nav_code + anchor, 1)
# swap old header block for {NAV}
start = s.find('<body>\n<header class="site">')
assert start != -1
end = s.find('\n  <div class="hc-progress"', start)
assert end != -1
old_header = s[start + len('<body>\n'):end]
assert 'id="siteMenu"' in old_header and 'hc-brand-help' in old_header, 'unexpected old header'
s = s[:start + len('<body>\n')] + '{NAV}' + s[end:]
save(BH, s)
print('P2 done')

# ============ P3: blog header() -> unified_nav ============
s = load(BB)
start = s.find('def header(rel, reading=False):')
assert start != -1
end = s.find('\n\ndef footer(rel):', start)
assert end != -1
new_header = '''def header(rel, reading=False):
    """Unified navbar (build_help.unified_nav): left group = Open Bot CTA +
    settings gear + brand; right group = Blog + Help Center pills + Open Bot
    CTA. The Help quick-search popover hangs off the Help pill. The settings
    menu holds display/reading controls only (no Help/Blog rows)."""
    _fonts = f\'\'\'<div class="gp-row gp-fonts" data-fonts>{bh.svg(\'book\')}<span>Font size</span><span class="hc-fonts"><button type="button" data-font="s" aria-label="Small">A</button><button type="button" data-font="m" aria-label="Default">A</button><button type="button" data-font="l" aria-label="Large">A</button></span></div>\'\'\'
    _reading = ""
    if reading:
        _reading = f\'\'\'<div class="gp-sep gp-reading" data-blog-reading></div>
          <div class="gp-head gp-reading" data-blog-reading>Reading</div>
          <button type="button" class="gp-row gp-reading" data-blog-reading role="menuitemcheckbox" aria-checked="false" data-blog-wide>{bh.svg(\'expand\')}<span>Wide format</span><span class="io-switch" aria-hidden="true"></span></button>
          <button type="button" class="gp-row gp-reading" data-blog-reading role="menuitemcheckbox" aria-checked="true" data-blog-rail>{bh.svg(\'book\')}<span>Article navigation</span><span class="io-switch" aria-hidden="true"></span></button>
          {_fonts}\'\'\'
    _menu = (f\'\'\'<div class="gp-head">Settings</div>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="false" id="rowDark">{bh.svg(\'moon\')}<span>Dark mode</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowAnim">{bh.svg(\'zap\')}<span>Animations</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowFx">{bh.svg(\'sparkles\')}<span>Effects</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowKeys">{bh.svg(\'keys\')}<span>Hotkeys</span><span class="io-switch" aria-hidden="true"></span></button>
        {_fonts}
        {_reading}
        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp" role="menuitem"><svg viewBox="0 0 24 24" fill="none" stroke="none" aria-hidden="true" style="visibility:hidden;width:18px;height:18px"></svg><span class="gp-sub-label">See hotkeys</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
        <div class="gp-sep" role="separator"></div>
        <a class="gp-row" role="menuitem" href="{SUPPORT_URL}" target="_blank" rel="noopener noreferrer">{bh.svg(\'send\')}<span>Support chat</span>{bh.svg(\'chev\')}</a>\'\'\')
    return bh.unified_nav(rel, BOT_URL, _menu)
'''
s = s[:start] + new_header + s[end:]
save(BB, s)
print('P3 done')

# ============ P4: static page_shell header -> unified_nav ============
s = load(BS)
fn = s.find("def page_shell(title_html, body, rel='../..'):")
assert fn != -1
ret = s.find('    return f\'\'\'<!DOCTYPE html>', fn)
assert ret != -1
menu_code = '''    _menu = (f\'\'\'<div class="gp-head">Settings</div>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="false" id="rowDark">{bh.svg(\'moon\')}<span>Dark mode</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowAnim">{bh.svg(\'zap\')}<span>Animations</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowFx">{bh.svg(\'sparkles\')}<span>Effects</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowKeys">{bh.svg(\'keys\')}<span>Hotkeys</span><span class="io-switch" aria-hidden="true"></span></button>
        <div class="gp-row gp-fonts" data-fonts>{bh.svg(\'book\')}<span>Font size</span><span class="hc-fonts"><button type="button" data-font="s" aria-label="Small">A</button><button type="button" data-font="m" aria-label="Default">A</button><button type="button" data-font="l" aria-label="Large">A</button></span></div>
        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp" role="menuitem"><svg viewBox="0 0 24 24" fill="none" stroke="none" aria-hidden="true" style="visibility:hidden;width:18px;height:18px"></svg><span class="gp-sub-label">See hotkeys</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
        <div class="gp-sep" role="separator"></div>
        <a class="gp-row" role="menuitem" href="https://t.me/FastSchedulerSupport_bot" target="_blank" rel="noopener noreferrer">{bh.svg(\'send\')}<span>Support chat</span>{bh.svg(\'chev\')}</a>\'\'\')
    NAV = bh.unified_nav(rel, bh.BOT_URL, _menu)
'''
s = s[:ret] + menu_code + s[ret:]
# now swap the header block inside page_shell for {NAV}
hstart = s.find('<header class="site">\n  <div class="wrap nav">\n    <a class="brand" href="{rel}/index.html"')
assert hstart != -1
hend = s.find('</header>', hstart)
assert hend != -1
s = s[:hstart] + '{NAV}' + s[hend + len('</header>'):]
save(BS, s)
print('P4 done')

# ============ P5: static nav404 -> unified_nav ============
s = load(BS)
start = s.find('    nav404 = (f"""<header class="site">')
assert start != -1
end = s.find('</header>""")', start)
assert end != -1
new404 = '''    _menu404 = (f\'\'\'<div class="gp-head">Settings</div>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="false" id="rowDark">{bh.svg(\'moon\')}<span>Dark mode</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowAnim">{bh.svg(\'zap\')}<span>Animations</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowFx">{bh.svg(\'sparkles\')}<span>Effects</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowKeys">{bh.svg(\'keys\')}<span>Hotkeys</span><span class="io-switch" aria-hidden="true"></span></button>
        <div class="gp-row gp-fonts" data-fonts>{bh.svg(\'book\')}<span>Font size</span><span class="hc-fonts"><button type="button" data-font="s" aria-label="Small">A</button><button type="button" data-font="m" aria-label="Default">A</button><button type="button" data-font="l" aria-label="Large">A</button></span></div>
        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp" role="menuitem"><svg viewBox="0 0 24 24" fill="none" stroke="none" aria-hidden="true" style="visibility:hidden;width:18px;height:18px"></svg><span class="gp-sub-label">See hotkeys</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
        <div class="gp-sep" role="separator"></div>
        <a class="gp-row" role="menuitem" href="https://t.me/FastSchedulerSupport_bot" target="_blank" rel="noopener noreferrer">{bh.svg(\'send\')}<span>Support chat</span>{bh.svg(\'chev\')}</a>\'\'\')
    nav404 = bh.unified_nav('', bh.BOT_URL + '?start=start__website_404', _menu404)'''
s = s[:start] + new404 + s[end + len('</header>""")'):]
save(BS, s)
print('P5 done')

# ============ P6: legal _nav() -> unified_nav ============
s = load(BL)
start = s.find('def _nav(current):')
assert start != -1
end = s.find('\nFOOTER = ', start)
assert end != -1
new_nav = '''def _nav(current):
    """Unified navbar (build_help.unified_nav): left group = Open Bot CTA +
    settings gear + brand; right group = Blog + Help Center pills + Open Bot
    CTA; the legal doc tabs ride in the center slot. The settings menu holds
    display controls only (no Help row). ``current`` marks the active tab."""
    _build_dir = os.path.join(WEBSITE_DIR, '_build')
    if _build_dir not in sys.path:
        sys.path.insert(0, _build_dir)
    import build_help as _bh  # noqa: E402
    def tab(href, label, doc):
        cls = 'doc-tab active' if doc == current else 'doc-tab'
        return f'<a class="{cls}" href="{href}">{label}</a>'
    _tabs = (f'<nav class="doc-tabs" aria-label="Legal documents">'
             f'{tab("privacy.html", "Privacy", "privacy")}'
             f'{tab("terms.html", "Terms", "terms")}'
             f'{tab("refundpolicy.html", "Refunds", "refund")}</nav>')
    _cta = (f'<a class="btn btn-primary nav-cta has-tip" '
            f'data-tip="Opens the bot in Telegram. The page you came from is recorded for first-time users." '
            f'href="{BOT_DEEP_LINK}?start=start__legal" target="_blank" '
            f'rel="noopener noreferrer">{svg(\'send\')}<span>Open Bot</span>'
            f'<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>')
    _menu = (f\'\'\'<div class="gp-head">Settings</div>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="false" id="rowDark">{svg(\'moon\')}<span>Dark mode</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowAnim">{svg(\'bolt\')}<span>Animations</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowFx">{svg(\'sparkles\')}<span>Effects</span><span class="io-switch" aria-hidden="true"></span></button>
        <button type="button" class="gp-row" role="menuitemcheckbox" aria-checked="true" id="rowKeys">{svg(\'keys\')}<span>Hotkeys</span><span class="io-switch" aria-hidden="true"></span></button>
        <div class="gp-row gp-fonts" data-fonts>{svg(\'book\')}<span>Font size</span><span class="hc-fonts"><button type="button" data-font="s" aria-label="Small">A</button><button type="button" data-font="m" aria-label="Default">A</button><button type="button" data-font="l" aria-label="Large">A</button></span></div>
        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp" role="menuitem"><svg viewBox="0 0 24 24" fill="none" stroke="none" aria-hidden="true" style="visibility:hidden;width:18px;height:18px"></svg><span class="gp-sub-label">See hotkeys</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
        <div class="gp-sep" role="separator"></div>
        <a class="gp-row" role="menuitem" href="https://t.me/FastSchedulerSupport_bot" target="_blank" rel="noopener noreferrer">{svg(\'send\')}<span>Support chat</span>{svg(\'chev\', cls=\'chev\')}</a>\'\'\')
    return _bh.unified_nav('..', f'{BOT_DEEP_LINK}?start=start__legal', _menu,
                           center_extra=_tabs, cta_html=_cta)
'''
s = s[:start] + new_nav + s[end:]
save(BL, s)
print('P6 done')

# ============ P7: settings.js selector (popover now hangs off navbar Help pill) ============
SJ = 'website/scripts/settings.js'
rep_once(SJ,
    "var siteWrap = document.querySelector('.settings-wrap .site-menu-wrap');",
    "var siteWrap = document.querySelector('.site-menu-wrap');")
rep_once(SJ,
    '/* ---------- "Main site" hover submenu (site sections) ---------- */',
    '/* ---------- Help quick-search popover (hangs off the navbar Help pill) ---------- */')
rep_once(SJ,
    "    /* Hover opens this popover ONLY when the wrap is the Help row's (the row\n"
    "       links to the help center and the popover is the quick-search). On the\n"
    "       help center page the same markup is the \"Main site\" row \u2014 hovering it\n"
    "       must never open the help search; it is a plain navigation link there. */",
    "    /* Hovering the Help Center pill opens the quick-search popover (desktop\n"
    "       fine pointers only). The pill itself stays a plain navigation link. */")
print('P7 done')

# ============ P8: liquid-nav.js fallbacks for .nav-group wrappers ============
LN = 'website/scripts/liquid-nav.js'
rep_once(LN,
    '    var brand = nav.querySelector(\':scope > .brand\');',
    '    var brand = nav.querySelector(\':scope > .brand\') || nav.querySelector(\'.brand\');')
rep_once(LN,
    "    var settings = (linksBox && linksBox.querySelector(':scope > .settings-wrap')) || nav.querySelector(':scope > .settings-wrap');",
    "    var settings = (linksBox && linksBox.querySelector(':scope > .settings-wrap')) || nav.querySelector(':scope > .settings-wrap') || nav.querySelector('.settings-wrap');")
print('P8 done')

# ============ P9: navbar popover + mobile CSS (both main.css copies) ============
CSS_ANCHOR = '.nav-unified .nav-cta kbd { margin-left: 2px; }'
CSS_ADD = ('.nav-unified .nav-cta kbd { margin-left: 2px; }\n'
 '/* Help quick-search popover hanging off the navbar Help pill (not the settings menu) */\n'
 '.nav-unified .site-menu-wrap { position: relative; display: inline-flex; }\n'
 '.nav-menu-pop { position: absolute; top: calc(100% + 10px); right: 0; left: auto;\n'
 '  min-width: min(300px, calc(100vw - 32px)); margin: 0; z-index: 60;\n'
 '  opacity: 0; visibility: hidden; transform: translateY(-6px);\n'
 '  transition: opacity .2s var(--ease-apple), transform .25s var(--ease-apple), visibility 0s .25s; }\n'
 '.nav-menu-pop.open { opacity: 1; visibility: visible; transform: translateY(0); transition-delay: 0s; }\n'
 '@media (max-width: 640px) { .nav-unified .nav-left .nav-cta { display: none; } }')
for _css in ('website/styles/main.css', 'styles/main.css'):
    rep_once(_css, CSS_ANCHOR, CSS_ADD)
print('P9 done')

# ============ P10: asset version bumps ============
for _f in (BH, BB, BS, BL):
    rep_all(_f, 'main.css?v=20261002c3', 'main.css?v=20261002c4')
for _f in (BH, BB, BS, BL):
    rep_all(_f, 'settings.js?v=20261002c2', 'settings.js?v=20261002c3')
for _f in (BH, BS):
    s = load(_f)
    n = s.count('liquid-nav.js?v=20260930a1')
    if n:
        save(_f, s.replace('liquid-nav.js?v=20260930a1', 'liquid-nav.js?v=20260930a2'))
        print('  liquid-nav bump x%d in %s' % (n, _f))
for _f in ('website/index.html', 'index.html'):
    s = load(_f)
    for _old, _new in (('main.css?v=20261002c3', 'main.css?v=20261002c4'),
                       ('settings.js?v=20261002c2', 'settings.js?v=20261002c3'),
                       ('liquid-nav.js?v=20260930a1', 'liquid-nav.js?v=20260930a2')):
        if _old in s:
            s = s.replace(_old, _new)
            print('  bump %s in %s' % (_old, _f))
    save(_f, s)
print('P10 done')
print('s20 all done')
