import html as H
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, 'website', '_build'))
sys.path.insert(0, os.path.join(REPO_ROOT, 'tools'))

from build_ru_frag import frags  # noqa: E402

try:
    import markdown as _md

    def render(s):
        return _md.markdown(s or '', extensions=['tables', 'fenced_code'])
except Exception:
    def render(s):
        return s or ''

corpus = json.load(open(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'corpus.json'), encoding='utf-8'))
uniq = {}
for aid in sorted(corpus.keys()):
    c = corpus[aid]
    texts = []
    if c['title']:
        texts.append(('title', c['title']))
    if c['desc']:
        texts.append(('desc', c['desc']))
    if c['content']:
        texts.append(('content', c['content']))
    for i, qa in enumerate(c['faq']):
        texts.append(('faq%dq' % i, qa.get('q', '')))
        texts.append(('faq%da' % i, qa.get('a', '')))
    for field, s in texts:
        if not s or not s.strip():
            continue
        for fr in frags(render(s)):
            if len(fr) >= 2:
                uniq.setdefault(fr, []).append(aid + '.' + field)
print('unique fragments:', len(uniq))
with open(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'frags.json'), 'w', encoding='utf-8') as f:
    json.dump(sorted(uniq.keys()), f, ensure_ascii=False)
with open(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'frag_src.json'), 'w', encoding='utf-8') as f:
    json.dump(uniq, f, ensure_ascii=False)
total_chars = sum(len(k) for k in uniq)
print('total frag chars:', total_chars)
