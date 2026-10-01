# -*- coding: utf-8 -*-
"""Correct coverage: dotted-path lookup against nested ru, with flat-key fallback."""
import io, json, sys

def load(p):
    return json.load(io.open(p, encoding='utf-8'))

def flat(d, p=''):
    for k, v in d.items():
        kk = p + '.' + k if p else k
        if isinstance(v, dict):
            yield from flat(v, kk)
        else:
            yield kk, v

def resolve(root, path):
    """Resolve a dotted path in a nested dict; fall back to flat key."""
    cur = root
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return root.get(path)  # flat fallback
    return cur

en_path = sys.argv[1] if len(sys.argv) > 1 else 'alwaysdata/translations/en.json'
ru_path = sys.argv[2] if len(sys.argv) > 2 else 'alwaysdata/translations/ru.json'
en, ru = load(en_path), load(ru_path)

en_leaves = list(flat(en))
missing = [p for p, _ in en_leaves if resolve(ru, p) is None]
empty = [p for p, _ in en_leaves if isinstance(resolve(ru, p), str) and not resolve(ru, p).strip()]
print('en leaves: %d | missing in ru: %d | empty: %d' % (len(en_leaves), len(missing), len(empty)))
secs = {}
for p in missing:
    secs[p.split('.')[0]] = secs.get(p.split('.')[0], 0) + 1
for s in sorted(secs, key=lambda x: -secs[x]):
    print('%5d  %s' % (secs[s], s))
