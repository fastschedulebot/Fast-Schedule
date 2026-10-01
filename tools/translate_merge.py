#!/usr/bin/env python3
"""Merge translator batches into translations/ru.json (bot + admin).

A batch file is a Python module defining PATCH = { 'dotted.key': 'русский текст' }.
Rules:
  - only leaf keys that are MISSING in ru.json are filled; existing translations
    are never overwritten (use --force to change that)
  - '{placeholders}' in the English text must survive: a patch whose braces do
    not match the English source is rejected loudly
  - '@@STORAGE@@' content markers and leading/trailing whitespace are preserved
  - the merge is idempotent: applying the same batch twice changes nothing
"""
import json, sys, os, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCHES_DIR = os.path.join(ROOT, 'tools', 'ru_batches')

def load(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

def set_path(tree, dotted, value, flat_in_source=False):
    # Some keys are LITERAL flat strings containing dots (e.g. 'tips.cmd.addbot').
    # i18n._resolve checks direct lookup first, so we mirror the source shape.
    if flat_in_source:
        tree[dotted] = value
        return
    parts = dotted.split('.')
    cur = tree
    for p in parts[:-1]:
        if not isinstance(cur.get(p), dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = value

def get_path(tree, dotted):
    # direct flat key wins (keys like 'tips.cmd.addbot' exist literally)
    if isinstance(tree, dict) and dotted in tree:
        return tree[dotted]
    cur = tree
    for p in dotted.split('.'):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur

def leaves(dotted, value):
    """Yield (dotted_path, leaf) pairs for a subtree."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(f'{dotted}.{k}' if dotted else k, v)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from leaves(f'{dotted}.{i}', v)
    else:
        yield dotted, value

def braces(s):
    import re
    return sorted(re.findall(r'\{[^{}]*\}', s or ''))

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'main'   # main | admin
    force = '--force' in sys.argv
    if which == 'admin':
        en_path = os.path.join(ROOT, 'alwaysdata', 'translations', 'admin', 'en.json')
        ru_path = os.path.join(ROOT, 'alwaysdata', 'translations', 'admin', 'ru.json')
    else:
        en_path = os.path.join(ROOT, 'alwaysdata', 'translations', 'en.json')
        ru_path = os.path.join(ROOT, 'alwaysdata', 'translations', 'ru.json')
    en, ru = load(en_path), load(ru_path)

    # also mirror into local/ when the file exists there
    mirror = ru_path.replace(os.sep + 'alwaysdata' + os.sep, os.sep + 'local' + os.sep)
    has_mirror = os.path.exists(os.path.dirname(mirror)) or 'local' in mirror

    applied, skipped_present, bad_braces, no_source = 0, 0, [], []
    for name in sorted(os.listdir(BATCHES_DIR)):
        if not name.startswith(which + '_') or not name.endswith('.py'):
            continue
        spec = importlib.util.spec_from_file_location(name[:-3], os.path.join(BATCHES_DIR, name))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for dotted, ru_text in getattr(mod, 'PATCH', {}).items():
            src = get_path(en, dotted)
            if src is None:
                no_source.append(f'{name}:{dotted}')
                continue
            cur = get_path(ru, dotted)
            if cur is not None and not force:
                skipped_present += 1
                continue
            if braces(src) != braces(ru_text):
                bad_braces.append(f'{dotted}: src={braces(src)} patch={braces(ru_text)}')
                continue
            if isinstance(src, str) and src.startswith('@@STORAGE@@') and not ru_text.startswith('@@STORAGE@@'):
                ru_text = '@@STORAGE@@' + ru_text
            set_path(ru, dotted, ru_text, flat_in_source=(dotted in en))
            applied += 1

    save(ru_path, ru)
    if has_mirror:
        os.makedirs(os.path.dirname(mirror), exist_ok=True)
        save(mirror, ru)
    print(f'[{which}] applied={applied} skipped_present={skipped_present} '
          f'bad_braces={len(bad_braces)} no_source={len(no_source)}')
    for b in bad_braces[:10]: print('  BRACES', b)
    for b in no_source[:10]: print('  NOSRC', b)

    # coverage report
    def count_missing(en_t, ru_t, prefix=''):
        miss = []
        def walk(e, r, p):
            if isinstance(e, dict):
                if not isinstance(r, dict): r = {}
                for k, v in e.items(): walk(v, r.get(k), f'{p}.{k}' if p else k)
            elif isinstance(e, list):
                if not isinstance(r, list): r = []
                for i, v in enumerate(e): walk(v, r[i] if i < len(r) else None, f'{p}.{i}')
            elif r is None or not isinstance(r, str):
                miss.append(p)
        walk(en_t, ru_t, prefix)
        return miss
    missing = count_missing(en, ru)
    print(f'[{which}] still missing {len(missing)} of {sum(1 for _ in leaves("en", en))} leaves')

if __name__ == '__main__':
    main()
