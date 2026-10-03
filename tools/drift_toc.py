"""One-off: compare TOC labels/anchors vs h2s in built legal pages."""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
for page in ['terms.html', 'privacy.html', 'refundpolicy.html']:
    html = open(os.path.join(REPO, 'website', 'legal', page), encoding='utf-8').read()
    h2s = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html)
    OUT.append('=' * 20 + ' ' + page + ' h2s: %d' % len(h2s))
    h2set = {}
    for hid, label in h2s:
        h2set[hid] = re.sub(r'<[^>]+>', '', label).strip()
    for m in re.finditer(r'<li><a href="((?:[^"]*?\.html)?#[^"]+)" title="([^"]*)">([^<]*)</a></li>', html):
        href, title, text = m.groups()
        anchor = href.split('#', 1)[1]
        if '#' not in href.split('#', 1)[0] and '.html' not in href:
            # same-page link: anchor must exist as h2 id
            if anchor not in h2set:
                OUT.append('DEAD anchor %s (label %r)' % (href, text))
            elif h2set[anchor] != text:
                OUT.append('LABEL drift anchor=%s toc=%r h2=%r' % (anchor, text, h2set[anchor]))
    OUT.append('cross-page toc refs checked visually only')
open(os.path.join(REPO, 'tools', 'drift_toc.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
