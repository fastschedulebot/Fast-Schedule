"""One-off: find EN frags paired with DIFFERENT RU texts across sections."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_ru_legal import render, frags, sections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seen = {}
for doc in ['terms.md', 'privacy.md', 'refundpolicy.md']:
    en = render(os.path.join(REPO, 'docs', doc))
    ru = render(os.path.join(REPO, 'docs', 'ru', doc))
    for (et, eh), (_rt, rh) in zip(sections(en), sections(ru)):
        for a, b in zip(frags(eh), frags(rh)):
            if a != b and len(a) >= 2:
                seen.setdefault(a, set()).add(b)

OUT = []
n = 0
for a, bs in sorted(seen.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    if len(bs) > 1:
        n += 1
        OUT.append('AMBIG %r -> %d variants:' % (a[:100], len(bs)))
        for b in sorted(bs):
            OUT.append('    :: %r' % b[:100])
open(os.path.join(REPO, 'tools', 'dupes.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
print('ambig keys: %d (list in tools/dupes.txt)' % n)
