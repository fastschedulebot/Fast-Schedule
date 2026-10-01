"""Legal version history builder (idempotent, re-runnable).

Reads website/legal/history/<name>-<date>.html snapshots (raw git
extracts), rewrites asset/peer links for the history/ directory, adds
noindex + archive banner + glass version switcher. Also stamps the
switcher and effective-date line into the current website/legal/*.html
pages.

Usage: py -3 tools/build_legal_history.py
"""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGAL = os.path.join(REPO, 'website', 'legal')
HIST = os.path.join(LEGAL, 'history')

PAGES = {
    'privacy': ('Privacy Policy', 'September 26, 2026'),
    'terms': ('Terms of Service', 'September 26, 2026'),
    'refundpolicy': ('Refund Policy', 'September 26, 2026'),
}

VERSIONS = [
    ('2026-09-26', 'September 26, 2026', 'archived'),
    ('2026-10-01', 'October 1, 2026', 'current, effective October 8, 2026'),
]

CHEV_D = ('<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<polyline points="6 9 12 15 18 9"/></svg>')
CHEV_R = ('<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<polyline points="9 18 15 12 9 6"/></svg>')
CHECK = ('<svg class="ver-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<polyline points="20 6 9 17 4 12"/></svg>')


def _opt(v, sub, href, on):
    inner = ('<span class="ver-v">%s</span><span class="ver-s">%s</span>%s'
             % (v, sub, CHECK if on else CHEV_R))
    if on:
        return ('<span class="gp-row ver-opt on" role="menuitem" '
                'aria-current="true">%s</span>' % inner)
    return ('<a class="gp-row ver-opt" role="menuitem" href="%s">%s</a>'
            % (href, inner))


def switcher_html(name, here, in_history):
    """Glass pill + hover menu. in_history=True inside history/."""
    cur_href = ('../%s.html' % name) if in_history else None
    old_href = (('%s-%s.html' % (name, '2026-09-26')) if in_history
                else ('history/%s-2026-09-26.html' % name))
    if here == '2026-10-01':
        pill = '2026-10-01 · current'
        menu = (_opt('2026-10-01', 'current · effective Oct 8, 2026', cur_href, True)
                + _opt('2026-09-26', 'archived', old_href, False))
    else:
        pill = '2026-09-26 · archived'
        menu = (_opt('2026-10-01', 'current · effective Oct 8, 2026', cur_href, False)
                + _opt('2026-09-26', 'this version · archived', old_href, True))
    return ('<div class="ver-dd">'
            '<button type="button" class="ver-pill" aria-haspopup="menu">'
            '<span class="ver-pill-dot" aria-hidden="true"></span>%s%s</button>'
            '<div class="glass-pop ver-menu" role="menu" aria-label="Document versions">'
            '<div class="gp-head">Document versions</div>%s</div></div>'
            % (pill, CHEV_D, menu))


def banner_html(name, title, date_label, current_label):
    peer = '../%s.html' % name
    return ('<div class="ver-banner" role="note"><b>Archived version.</b> '
            'This is the %s as published on %s — it is no longer in effect. '
            '<a href="%s">Read the current version (%s)</a>.</div>'
            % (title, date_label, peer, current_label))


def process_snapshot(name, title, date_label, stamp):
    src = os.path.join(HIST, '%s-%s.html' % (name, stamp))
    html = open(src, encoding='utf-8').read()
    for prefix in ('scripts', 'styles', 'blog', 'help', 'index'):
        html = html.replace('"../%s' % prefix, '"../../%s' % prefix)
    for peer in PAGES:
        html = re.sub(r'"%s\.html((?:#[^"]*)?)"' % peer,
                      r'"%s-%s.html\1"' % (peer, stamp), html)
    html = re.sub(r'lang\.js\?v=[0-9a-z]+', 'lang.js?v=20261002a1', html)
    html = html.replace('<article class="doc">', '<article class="doc archived">', 1)
    html = re.sub(r'<meta name="robots" content="[^"]*">',
                  '<meta name="robots" content="noindex, follow">', html, count=1)
    if '<meta name="robots"' not in html:
        anchor = re.search(r'<meta name="viewport"[^>]*>', html).group(0)
        html = html.replace(anchor, anchor + '\n<meta name="robots" content="noindex, follow">', 1)
    html = re.sub(r'<title>(.*?)</title>',
                  r'<title>\1 (%s)</title>' % stamp, html, count=1)
    anchor = '<p class="updated">Last updated: %s</p>' % date_label
    block = (anchor + '\n    ' +
             banner_html(name, title, date_label, 'October 1, 2026, effective October 8, 2026'))
    assert anchor in html, 'anchor missing in %s' % src
    html = html.replace(anchor, block, 1)
    open(src, 'w', encoding='utf-8').write(html)
    print('history ready:', src)


def stamp_current(name, title):
    path = os.path.join(LEGAL, '%s.html' % name)
    html = open(path, encoding='utf-8').read()
    if 'ver-dd' in html:
        print('already stamped:', path)
        return
    anchor = '<p class="updated">Last updated: October 1, 2026</p>'
    assert anchor in html, 'anchor missing in %s' % path
    block = (anchor +
             '\n    <p class="effective">Effective October 8, 2026. '
             'Continued use of the Services after that date constitutes acceptance.</p>' +
             '\n    ' + switcher_html(name, '2026-10-01', False))
    html = html.replace(anchor, block, 1)
    open(path, 'w', encoding='utf-8').write(html)
    print('stamped:', path)


def main():
    os.makedirs(HIST, exist_ok=True)
    for name, (title, date_label) in PAGES.items():
        process_snapshot(name, title, date_label, '2026-09-26')
    for name, (title, _d) in PAGES.items():
        stamp_current(name, title)


if __name__ == '__main__':
    main()
