# -*- coding: utf-8 -*-
"""Dump help.* leaves as dotted paths for translation batches.
Usage: python tools/dump_help.py a-g   (letter range) -> stdout
"""
import io, json, sys

en = json.load(io.open('alwaysdata/translations/en.json', encoding='utf-8'))
h = en['help']

rng = sys.argv[1] if len(sys.argv) > 1 else 'a-z'
lo, hi = rng.split('-')

def emit(path, v):
    if isinstance(v, dict):
        for k, vv in v.items():
            emit(f'{path}.{k}', vv)
    elif isinstance(v, list):
        # identifier lists (children/links) - print as one unit
        print(f'{path} = [IDENTS] {json.dumps(v, ensure_ascii=False)}')
    else:
        print(f'{path} = {json.dumps(v, ensure_ascii=False)}')

keys = sorted(k for k in h if lo <= k[:1] <= hi)
for k in keys:
    print(f'##### {k}')
    emit(f'help.{k}', h[k])
