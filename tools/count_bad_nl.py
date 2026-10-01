# -*- coding: utf-8 -*-
"""Count RU strings containing a literal backslash followed by 'n'."""
import io, json

BS = chr(92)  # backslash

def flat(d, p=''):
    for k, v in d.items():
        kk = p + '.' + k if p else k
        if isinstance(v, dict):
            yield from flat(v, kk)
        else:
            yield kk, v

for path in ('alwaysdata/translations/ru.json', 'local/translations/ru.json'):
    ru = json.load(io.open(path, encoding='utf-8'))
    bad = [k for k, v in flat(ru) if isinstance(v, str) and (BS + 'n') in v]
    print(path, 'literal-backslash-n strings:', len(bad))
    for k in bad[:10]:
        print('  ', k)
