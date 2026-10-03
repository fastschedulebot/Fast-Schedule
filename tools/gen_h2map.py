"""One-off: emit ru-chrome MAP lines for legal h2 headings (EN -> RU)."""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = []
for doc in ['terms.md', 'privacy.md', 'refundpolicy.md']:
    en = open(os.path.join(REPO, 'docs', doc), encoding='utf-8-sig').read()
    ru = open(os.path.join(REPO, 'docs', 'ru', doc), encoding='utf-8-sig').read()
    enh = re.findall(r'^## (.+)$', en, re.M)
    ruh = re.findall(r'^## (.+)$', ru, re.M)
    assert len(enh) == len(ruh), doc
    OUT.append('      // %s headings' % doc)
    for a, b in zip(enh, ruh):
        OUT.append("      '%s': '%s'," % (a.replace("'", "\\'"), b.replace("'", "\\'")))
open(os.path.join(REPO, 'tools', 'h2map.txt'), 'w', encoding='utf-8').write('\n'.join(OUT))
