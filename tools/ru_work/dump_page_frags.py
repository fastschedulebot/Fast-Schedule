import html as H
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, 'tools'))

from build_ru_frag import frags  # noqa: E402

page_frags = {}
targets = []
for dp, dn, fn in os.walk(os.path.join(REPO_ROOT, 'website', 'blog')):
    for f in fn:
        if f.endswith('.html'):
            targets.append(os.path.join(dp, f))
for dp, dn, fn in os.walk(os.path.join(REPO_ROOT, 'website', 'help')):
    for f in fn:
        if f.endswith('.html'):
            targets.append(os.path.join(dp, f))

allf = {}
for p in sorted(targets):
    try:
        t = open(p, encoding='utf-8').read()
    except Exception:
        continue
    # drop scripts/styles/json-ld
    t = re.sub(r'<script.*?</script\s*>', '', t, flags=re.S | re.I)
    t = re.sub(r'<style.*?</style\s*>', '', t, flags=re.S | re.I)
    for fr in frags(t):
        if len(fr) >= 2:
            allf.setdefault(fr, []).append(os.path.relpath(p, REPO_ROOT))
print('pages:', len(targets), 'unique frags:', len(allf))
with open(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'page_frags.json'), 'w', encoding='utf-8') as f:
    json.dump(sorted(allf.keys()), f, ensure_ascii=False)
with open(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'page_frag_src.json'), 'w', encoding='utf-8') as f:
    json.dump(allf, f, ensure_ascii=False)
