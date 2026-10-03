"""Merge tools/ru_work/tr/tr_*.json (EN->RU fragment pairs) into
website/scripts/ru-content.js (client-side RU dictionary) and
tools/ru_blog_extra.json (titles/descs, picked up by build_ru_frag.py
and the coverage checkers).

Additive only: existing entries are never overwritten or removed.
Run from the repo root:  python tools/merge_ru_tr.py
"""
import glob
import io
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE_RE = re.compile(r'\s\u2014\sFast Scheduler (Help|Blog)\s*$')


def load_json(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    tr_dir = os.path.join(REPO_ROOT, 'tools', 'ru_work', 'tr')
    tr = {}
    for fp in sorted(glob.glob(os.path.join(tr_dir, 'tr_*.json'))):
        tr.update(load_json(fp))
    print('tr pairs:', len(tr))

    # 1. ru-content.js
    js_path = os.path.join(REPO_ROOT, 'website', 'scripts', 'ru-content.js')
    with io.open(js_path, encoding='utf-8') as f:
        t = f.read()
    m = re.match(r'window\.FS_RU_CONTENT=(.*);\s*$', t, re.S)
    d = json.loads(m.group(1))
    n0 = len(d)
    added = 0
    for k, v in tr.items():
        # self-pairs (k == v) are intentional: brands, commands, placeholders
        # stay English; presence in the dict marks the fragment as covered.
        if k and v and k not in d:
            d[k] = v
            added += 1
    js = 'window.FS_RU_CONTENT=' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';'
    with io.open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print('ru-content: had %d, added %d, now %d' % (n0, added, len(d)))

    # 2. ru_blog_extra.json (titles/descs mirror for rebuilds + coverage)
    extra_path = os.path.join(REPO_ROOT, 'tools', 'ru_blog_extra.json')
    extra = load_json(extra_path)
    extra.setdefault('titles', {})
    extra.setdefault('descs', {})
    corpus = load_json(os.path.join(REPO_ROOT, 'tools', 'ru_work', 'corpus.json'))
    cdesc = set(c['desc'] for c in corpus.values() if c.get('desc'))
    at = ad = 0
    for k, v in tr.items():
        if not (k and v):
            continue
        if TITLE_RE.search(k):
            if k not in extra['titles']:
                extra['titles'][k] = v
                at += 1
        elif k in cdesc:
            if k not in extra['descs']:
                extra['descs'][k] = v
                ad += 1
    with io.open(extra_path, 'w', encoding='utf-8') as f:
        json.dump(extra, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('extra: titles +%d = %d, descs +%d = %d' % (at, len(extra['titles']), ad, len(extra['descs'])))


if __name__ == '__main__':
    main()
