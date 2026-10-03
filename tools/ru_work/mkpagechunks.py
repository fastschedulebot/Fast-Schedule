import html as H
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, 'tools'))

from build_ru_frag import frags  # noqa: E402

real = json.load(open(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'page_missing.json'), encoding='utf-8'))
need = set(real)
byfile = {}
targets = []
for dp, dn, fn in os.walk(os.path.join(REPO_ROOT, 'website', 'blog')):
    for f in fn:
        if f.endswith('.html'):
            targets.append(os.path.join(dp, f))
for dp, dn, fn in os.walk(os.path.join(REPO_ROOT, 'website', 'help')):
    for f in fn:
        if f.endswith('.html'):
            targets.append(os.path.join(dp, f))

for p in sorted(targets):
    try:
        t = open(p, encoding='utf-8').read()
    except Exception:
        continue
    t = re.sub(r'<script.*?</script\s*>', '', t, flags=re.S | re.I)
    t = re.sub(r'<style.*?</style\s*>', '', t, flags=re.S | re.I)
    ordered = []
    for fr in frags(t):
        if fr in need and fr not in ordered:
            ordered.append(fr)
    if ordered:
        rel = os.path.relpath(p, REPO_ROOT)
        byfile[rel] = ordered

# split: big files own chunk, small files grouped
outdir = os.path.join(REPO_ROOT, 'tools', 'ru_work', 'pages')
os.makedirs(outdir, exist_ok=True)
import shutil
for f in os.listdir(outdir):
    os.remove(os.path.join(outdir, f))
n = 0
batch = []
batchchars = 0
manifest = []
for rel in sorted(byfile, key=lambda r: -len(byfile[r])):
    items = byfile[rel]
    chars = sum(len(x) for x in items)
    if len(items) >= 40 or chars >= 12000:
        name = 'pg_%03d.json' % n
        n += 1
        with open(os.path.join(outdir, name), 'w', encoding='utf-8') as f:
            json.dump({'files': {rel: items}}, f, ensure_ascii=False, indent=1)
        manifest.append([name, [rel], len(items), chars])
    else:
        batch.append((rel, items))
        batchchars += chars
        if len(batch) >= 12 or batchchars >= 15000:
            name = 'pg_%03d.json' % n
            n += 1
            with open(os.path.join(outdir, name), 'w', encoding='utf-8') as f:
                json.dump({'files': dict(batch)}, f, ensure_ascii=False, indent=1)
            manifest.append([name, [r for r, _ in batch], sum(len(v) for _, v in batch),
                             sum(sum(len(x) for x in v) for _, v in batch)])
            batch = []
            batchchars = 0
if batch:
    name = 'pg_%03d.json' % n
    n += 1
    with open(os.path.join(outdir, name), 'w', encoding='utf-8') as f:
        json.dump({'files': dict(batch)}, f, ensure_ascii=False, indent=1)
    manifest.append([name, [r for r, _ in batch], sum(len(v) for _, v in batch),
                     sum(sum(len(x) for x in v) for _, v in batch)])
    n += 0
with open(os.path.join(outdir, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
total_items = sum(m[2] for m in manifest)
print('chunks:', len(manifest), 'items:', total_items)
