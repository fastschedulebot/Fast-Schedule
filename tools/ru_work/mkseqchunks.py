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
targets = []
for dp, dn, fn in os.walk(os.path.join(REPO_ROOT, 'website', 'blog')):
    for f in fn:
        if f.endswith('.html'):
            targets.append(os.path.join(dp, f))
for dp, dn, fn in os.walk(os.path.join(REPO_ROOT, 'website', 'help')):
    for f in fn:
        if f.endswith('.html'):
            targets.append(os.path.join(dp, f))

# blog articles first (biggest value), then hub, then help
def sortkey(p):
    rel = os.path.relpath(p, REPO_ROOT)
    if 'blog' in rel and '/a/' in rel.replace('\\', '/'):
        return (0, rel)
    if 'blog' in rel:
        return (1, rel)
    return (2, rel)

seq = []
seen = set()
bounds = []
for p in sorted(targets, key=sortkey):
    try:
        t = open(p, encoding='utf-8').read()
    except Exception:
        continue
    t = re.sub(r'<script.*?</script\s*>', '', t, flags=re.S | re.I)
    t = re.sub(r'<style.*?</style\s*>', '', t, flags=re.S | re.I)
    start = len(seq)
    for fr in frags(t):
        if fr in need and fr not in seen:
            seen.add(fr)
            seq.append(fr)
    if len(seq) > start:
        rel = os.path.relpath(p, REPO_ROOT)
        bounds.append([rel, start, len(seq)])
print('unique ordered:', len(seq), 'unplaced:', len(need - seen))

outdir = os.path.join(REPO_ROOT, 'tools', 'ru_work', 'seq')
os.makedirs(outdir, exist_ok=True)
import shutil
for f in os.listdir(outdir):
    os.remove(os.path.join(outdir, f))
CH = 450
n = 0
manifest = []
for i in range(0, len(seq), CH):
    part = seq[i:i + CH]
    # find which files this range covers
    files = sorted(set(b[0] for b in bounds if b[1] < i + CH and b[2] > i))
    name = 'sq_%02d.json' % n
    n += 1
    with open(os.path.join(outdir, name), 'w', encoding='utf-8') as f:
        json.dump({'covers': files, 'items': part}, f, ensure_ascii=False, indent=1)
    manifest.append([name, len(part), sum(len(x) for x in part), files[:6]])
with open(os.path.join(outdir, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
print('chunks:', len(manifest))
