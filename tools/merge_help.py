#!/usr/bin/env python3
"""Merge help-tree translation batches into translations/ru.json.

A batch module defines PATCH = { '<topic>': <translated topic> , ... } where a
topic is either a plain string (btn, text, ...) or the full dict
{title, content, faq?, children?}. Only topics MISSING in ru['help'] are
filled (use --force to overwrite). Validation per topic:
  - dict topics must have exactly the same key set as English
  - 'children' lists must be identical to English (identifier lists)
  - faq item count must match; 'links' inside items must be identical;
    '{placeholders}' in q/a/content must match the English source
Mirrors into local/translations/ru.json like translate_merge.py.
"""
import json, sys, os, importlib.util, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCHES_DIR = os.path.join(ROOT, 'tools', 'ru_batches')

def load(p):
    with open(p, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save(p, d):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

def braces(s):
    return sorted(re.findall(r'\{[^{}]*\}', s or ''))

def check_text(en_s, ru_s, where, errors):
    if not isinstance(ru_s, str):
        errors.append(f'{where}: not a string'); return
    if braces(en_s) != braces(ru_s):
        errors.append(f'{where}: braces src={braces(en_s)} ru={braces(ru_s)}')
    if en_s.startswith('@@STORAGE@@') and not ru_s.startswith('@@STORAGE@@'):
        errors.append(f'{where}: missing @@STORAGE@@ marker')

def check_topic(en_t, ru_t, where, errors):
    if isinstance(en_t, str):
        check_text(en_t, ru_t, where, errors); return
    if not isinstance(ru_t, dict):
        errors.append(f'{where}: not a dict'); return
    if set(en_t.keys()) != set(ru_t.keys()):
        errors.append(f'{where}: keys {sorted(en_t)} != {sorted(ru_t)}'); return
    for k in ('title', 'content'):
        if k in en_t:
            check_text(en_t[k], ru_t[k], f'{where}.{k}', errors)
    if 'children' in en_t and en_t['children'] != ru_t.get('children'):
        errors.append(f'{where}.children: must be identical to English')
    if 'faq' in en_t:
        ef, rf = en_t['faq'], ru_t.get('faq')
        if not isinstance(rf, list) or len(ef) != len(rf):
            errors.append(f'{where}.faq: must be a list of {len(ef)} items'); return
        for i, (ei, ri) in enumerate(zip(ef, rf)):
            if set(ei.keys()) != set(ri.keys()):
                errors.append(f'{where}.faq.{i}: keys differ'); continue
            for fld in ('q', 'a'):
                if fld in ei:
                    check_text(ei[fld], ri[fld], f'{where}.faq.{i}.{fld}', errors)
            if 'links' in ei and ei['links'] != ri.get('links'):
                errors.append(f'{where}.faq.{i}.links: must be identical')

def main():
    force = '--force' in sys.argv
    en = load(os.path.join(ROOT, 'alwaysdata', 'translations', 'en.json'))
    ru_path = os.path.join(ROOT, 'alwaysdata', 'translations', 'ru.json')
    ru = load(ru_path)
    mirror = ru_path.replace(os.sep + 'alwaysdata' + os.sep, os.sep + 'local' + os.sep)

    applied, skipped, done = 0, 0, []
    errors = []
    for name in sorted(os.listdir(BATCHES_DIR)):
        if not name.startswith('help_') or not name.endswith('.py'):
            continue
        spec = importlib.util.spec_from_file_location(name[:-3], os.path.join(BATCHES_DIR, name))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for topic, tr in getattr(mod, 'PATCH', {}).items():
            if topic not in en.get('help', {}):
                errors.append(f'{name}: no English topic {topic}'); continue
            if topic in ru.get('help', {}) and not force:
                skipped += 1; continue
            errs0 = []
            check_topic(en['help'][topic], tr, f'help.{topic}', errs0)
            errors.extend(errs0)
            if not errs0:
                ru.setdefault('help', {})[topic] = tr
                applied += 1; done.append(topic)

    save(ru_path, ru)
    if os.path.exists(os.path.dirname(mirror)) or 'local' in mirror:
        os.makedirs(os.path.dirname(mirror), exist_ok=True)
        save(mirror, ru)

    print(f'[help] applied={applied} skipped_present={skipped} errors={len(errors)}')
    for e in errors[:20]:
        print('  ERR', e)
    # coverage
    en_h, ru_h = en.get('help', {}), ru.get('help', {})
    missing = [k for k in en_h if k not in ru_h]
    print(f'[help] still missing {len(missing)} of {len(en_h)} topics: {missing[:20]}')

if __name__ == '__main__':
    main()
