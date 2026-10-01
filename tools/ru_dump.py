#!/usr/bin/env python3
"""Dump untranslated EN leaves for given top-level sections, with dotted paths."""
import json, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def leaves(dotted, value):
    if isinstance(value, dict):
        for k, v in value.items(): yield from leaves(f'{dotted}.{k}' if dotted else k, v)
    elif isinstance(value, list):
        for i, v in enumerate(value): yield from leaves(f'{dotted}.{i}', v)
    else: yield dotted, value
def get_path(tree, dotted):
    cur = tree
    for p in dotted.split('.'):
        if not isinstance(cur, dict) or p not in cur: return None
        cur = cur[p]
    return cur
which = sys.argv[1] if len(sys.argv) > 1 else 'main'
secs = sys.argv[2].split(',') if len(sys.argv) > 2 else None
if which == 'admin':
    en = json.load(open(os.path.join(ROOT,'alwaysdata','translations','admin','en.json'),encoding='utf-8-sig'))
    ru = json.load(open(os.path.join(ROOT,'alwaysdata','translations','admin','ru.json'),encoding='utf-8-sig'))
else:
    en = json.load(open(os.path.join(ROOT,'alwaysdata','translations','en.json'),encoding='utf-8-sig'))
    ru = json.load(open(os.path.join(ROOT,'alwaysdata','translations','ru.json'),encoding='utf-8-sig'))
n=0
for k in (secs or [s for s in en if get_path(ru,s) is None or True]):
    v = en.get(k)
    if v is None: continue
    for dotted, leaf in leaves(k, v):
        cur = get_path(ru, dotted)
        if isinstance(cur, str): continue
        n+=1
        print(f'{dotted}\t{leaf!r}')
print(f'# --- {n} untranslated ---', file=sys.stderr)
