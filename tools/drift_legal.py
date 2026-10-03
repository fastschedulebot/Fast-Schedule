"""One-off: diff fresh docs render vs built legal HTML bodies (UTF-8 safe)."""
import sys
import os
import re
import difflib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from build_ru_legal import render

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []


def log(s):
    OUT.append(s)


def blocks(h):
    h = re.sub(r' id="[^"]*"', '', h)
    h = re.sub(r'<div class="table-scroll"><table>', '<table>', h)
    h = re.sub(r'</table></div>', '</table>', h)
    parts = re.split(r'(?=<h2[ >]|<h3[ >]|<p>|<ul>|<ol>|<table>|<hr />|<blockquote>)', h)
    return [re.sub(r'\s+', ' ', p).strip() for p in parts if re.sub(r'<[^>]+>', '', p).strip()]


for doc, page in [('terms.md', 'terms.html'), ('privacy.md', 'privacy.html'),
                  ('refundpolicy.md', 'refundpolicy.html')]:
    fresh = render(os.path.join(REPO, 'docs', doc))
    built = open(os.path.join(REPO, 'website', 'legal', page), encoding='utf-8').read()
    a = re.search(r'<article class="doc">(.*?)</article>', built, re.S).group(1)
    body_built = a[a.find('<h2'):]
    fb, bb = blocks(fresh), blocks(body_built)
    log('=' * 30 + ' ' + page)
    sm = difflib.SequenceMatcher(None, fb, bb, autojunk=False)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        n += 1
        log('--- %s fresh[%d:%d] built[%d:%d]' % (tag, i1, i2, j1, j2))
        for x in fb[i1:i2][:3]:
            log('  FRESH: ' + x[:300])
        for x in bb[j1:j2][:3]:
            log('  BUILT: ' + x[:300])
    log('drift blocks: %d | fresh: %d built: %d' % (n, len(fb), len(bb)))

open(os.path.join(REPO, 'tools', 'drift_out.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
print('\n'.join(OUT[:60]))
print('... full in tools/drift_out.txt')
