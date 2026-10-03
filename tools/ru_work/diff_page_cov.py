import json
import re

frags = json.load(open('tools/ru_work/page_frags.json', encoding='utf-8'))
src = json.load(open('tools/ru_work/page_frag_src.json', encoding='utf-8'))
t = open('website/scripts/ru-content.js', encoding='utf-8').read()
m = re.match(r"window\.FS_RU_CONTENT=(.*);$", t, re.S)
have = set(json.loads(m.group(1)).keys())
extra = json.load(open('tools/ru_blog_extra.json', encoding='utf-8'))
for s in ('titles', 'descs'):
    have.update(extra.get(s, {}).keys())
# ru-chrome MAP covers site chrome; load it too
try:
    tc = open('website/scripts/ru-chrome.js', encoding='utf-8').read()
    for mm in re.finditer(r'"((?:[^"\\]|\\.)*)"\s*:\s*"', tc):
        try:
            have.add(json.loads('"' + mm.group(1) + '"'))
        except Exception:
            pass
except Exception as e:
    print('chrome load note:', e)

missing = [f for f in frags if f not in have]
# skip pure code/numbers/urls/handles
SKIP_RE = re.compile(r'^(@[\w_]+|/[\w]+|https?://\S+|[\d\s\.,%$€×→—\-–:;()#]+|[\w-]+\.(html|json|js|css|png|jpg))$', re.I)
real = []
skipped = 0
for f in missing:
    if SKIP_RE.match(f) or len(f) < 2:
        skipped += 1
        continue
    # mostly non-cyrillic and no latin words >=3 chars -> skip (code/symbols)
    if not re.search(r'[A-Za-z]{3,}', f):
        skipped += 1
        continue
    real.append(f)
with open('tools/ru_work/page_missing.json', 'w', encoding='utf-8') as f:
    json.dump(real, f, ensure_ascii=False)
print('page frags:', len(frags), 'missing:', len(missing), 'real:', len(real), 'skipped:', skipped)
print('real chars:', sum(len(x) for x in real))
from collections import Counter
c = Counter()
for f in real:
    for p in src.get(f, ['?']):
        c[p.split('/')[1] if '/' in p else p] += 1
print('top files:', c.most_common(12))
