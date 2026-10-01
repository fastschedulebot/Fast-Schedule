"""Legal version history builder (idempotent, re-runnable).

Reads website/legal/history/<name>-<date>.html snapshots (raw git
extracts), rewrites asset/peer links for the history/ directory, adds
noindex + archive banner + version switcher. Also stamps the switcher
and effective-date line into the current website/legal/*.html pages.

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

CSS = ('<link rel="stylesheet" href="../../styles/mobile-fix.css?v=20261001b1">'
       if False else '')


def switcher_html(name, title, here, in_history):
    """Version switcher block. in_history=True when rendered inside history/."""
    items = []
    for v, label, note in VERSIONS:
        if v == here:
            items.append('<span aria-current="true">%s (%s)</span>' % (v, 'current' if v == '2026-10-01' else 'this version'))
        elif v == '2026-10-01':
            items.append('<a href="%s%s.html">%s (current)</a>' % ('../' if in_history else '', name, v))
        else:
            items.append('<a href="%s%s-%s.html">%s</a>' % ('history/' if not in_history else '', name, v, v))
    return ('<div class="ver-switch" role="navigation" aria-label="Document versions">'
            'Version: ' + ' · '.join(items) + '</div>')


def banner_html(name, title, date_label, current_label):
    peer = '../%s.html' % name
    return ('<div class="ver-banner" role="note"><b>Archived version.</b> '
            'This is the %s as published on %s — it is no longer in effect. '
            '<a href="%s">Read the current version (%s)</a>.</div>'
            % (title, date_label, peer, current_label))


def process_snapshot(name, title, date_label, stamp):
    src = os.path.join(HIST, '%s-%s.html' % (name, stamp))
    html = open(src, encoding='utf-8').read()
    # 1. asset paths for history/ depth
    for prefix in ('scripts', 'styles', 'blog', 'help', 'index'):
        html = html.replace('"../%s' % prefix, '"../../%s' % prefix)
    # 2. peer legal links -> same-date history peers
    for peer in PAGES:
        html = re.sub(r'"%s\.html((?:#[^"]*)?)"' % peer,
                      r'"%s-%s.html\1"' % (peer, stamp), html)
    # 2b. pin the current lang.js (archives must use the engine with the
    # .archived opt-out, not whatever version was current at snapshot time)
    html = re.sub(r'lang\.js\?v=[0-9a-z]+', 'lang.js?v=20261002a1', html)
    # 3. archived marker (opts out of RU body translation)
    html = html.replace('<article class="doc">', '<article class="doc archived">', 1)
    # 4. noindex (archived legal versions must not compete in search)
    html = re.sub(r'<meta name="robots" content="[^"]*">',
                  '<meta name="robots" content="noindex, follow">', html, count=1)
    # 5. title stamp
    html = re.sub(r'<title>(.*?)</title>',
                  r'<title>\1 (%s)</title>' % stamp, html, count=1)
    # 6. banner + switcher after the updated line
    anchor = '<p class="updated">Last updated: %s</p>' % date_label
    block = (anchor + '\n    ' +
             banner_html(name, title, date_label, 'October 1, 2026, effective October 8, 2026') +
             '\n    ' + switcher_html(name, title, stamp, True))
    assert anchor in html, 'anchor missing in %s' % src
    html = html.replace(anchor, block, 1)
    open(src, 'w', encoding='utf-8').write(html)
    print('history ready:', src)


def stamp_current(name, title):
    path = os.path.join(LEGAL, '%s.html' % name)
    html = open(path, encoding='utf-8').read()
    if 'ver-switch' in html:
        print('already stamped:', path)
        return
    anchor = '<p class="updated">Last updated: October 1, 2026</p>'
    assert anchor in html, 'anchor missing in %s' % path
    block = (anchor +
             '\n    <p class="effective">Effective October 8, 2026. '
             'Continued use of the Services after that date constitutes acceptance.</p>' +
             '\n    ' + switcher_html(name, title, '2026-10-01', False))
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
