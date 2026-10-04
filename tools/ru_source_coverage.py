"""How much of the site does the Russian source corpus actually cover?

tools/ru_batches/help_*.py hold full Russian articles (title, content, FAQ)
and docs/ru/*.md hold the legal policies. This counts how many of the built
help articles have a Russian counterpart, so /ru/ pages are only generated
where real translated text exists -- never as a thin duplicate of English.
"""
import importlib.util
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.path.join(ROOT, 'tools', 'ru_batches')
SITE = os.path.join(ROOT, 'website')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PATCH


def main():
    patch = {}
    for f in sorted(os.listdir(BATCH)):
        if not (f.startswith('help_') and f.endswith('.py')):
            continue
        patch.update(load(os.path.join(BATCH, f), 'b_' + f[:-3]))

    built = [f[:-5] for f in os.listdir(os.path.join(SITE, 'help', 'a'))
             if f.endswith('.html')]
    have = [a for a in built if a in patch]
    missing = [a for a in built if a not in patch]
    full = [a for a in have
            if patch[a].get('content') and patch[a].get('faq')]

    print('RU help articles available : %d' % len(patch))
    print('built help articles        : %d' % len(built))
    print('covered by RU source       : %d (%.1f%%)' % (
        len(have), 100.0 * len(have) / max(1, len(built))))
    print('  with title+content+faq   : %d' % len(full))
    print('missing translation        : %d' % len(missing))
    print('\nmissing (first 25): %s' % ', '.join(missing[:25]))

    # sample one article end-to-end to confirm the shape is usable
    a = have[0]
    print('\n-- sample: %s --' % a)
    print('title  : %s' % patch[a].get('title'))
    print('content: %s...' % str(patch[a].get('content'))[:150])
    print('faq[0] : %s' % patch[a]['faq'][0]['q'][:100] if patch[a].get('faq') else 'none')

    legal = sorted(os.listdir(os.path.join(ROOT, 'docs', 'ru')))
    print('\nRU legal docs: %s' % ', '.join(legal))
    return 0


if __name__ == '__main__':
    sys.exit(main())