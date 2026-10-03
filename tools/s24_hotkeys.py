"""Main-page hotkeys on small screens.

The navbar section/help links hide on phones, so G/H/1-6 silently did
nothing there. H/G gain footer + mobile-menu fallbacks (resolve() still
picks the first *visible* match, so desktop behavior is unchanged); 1-6
click their anchor directly even inside closed menus (same `always`
treatment the settings rows already have).
"""
import io

def load(p):
    return io.open(p, encoding='utf-8', newline='').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('[ok]', p)

def rep_once(p, old, new):
    s = load(p)
    assert s.count(old) == 1, (p, s.count(old), old[:80])
    save(p, s.replace(old, new, 1))

HJ = 'website/scripts/hotkeys.js'
HM = 'website/scripts/hotkeys-modal.js'

OLD_G = """a.nav-link[href*="blog"], .help-row a[href*="blog"], a[href$="blog/index.html"], a[href$="/blog/"]"""
NEW_G = OLD_G + """, #navMobile a[href*="blog"], footer a[href$="blog/index.html"]"""
OLD_H = """a.nav-link[href*="help"], .site-menu-row, a.gp-row[href*="help"], .help-row a[href*="help"]"""
NEW_H = OLD_H + """, #navMobile a[href*="help"], footer a[href$="help.html"]"""

rep_once(HJ, OLD_G, NEW_G)
rep_once(HJ, OLD_H, NEW_H)
rep_once(HM, OLD_G, NEW_G)
rep_once(HM, OLD_H, NEW_H)

# 1-6: direct click (closed mobile menu no longer blocks them)
for n in '123456':
    rep_once(HJ, "{ key: '%s'," % n, "{ key: '%s', always: true," % n)

print('s24 all done')
