#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bump the main.css cache-busting version.

Every stylesheet link carries `?v=<stamp>` so a returning visitor gets the
new CSS instead of the copy already in their disk cache. The stamp is
hardcoded in six places - four builders under website/_build/ plus the
hand-maintained homepage - and forgetting one of them is silent: the page
still renders, just with stale CSS, and only on the machines that had
already visited.

Editing styles/main.css without running this is the same trap as editing
lang.js without bump_lang_v.py.

    python tools/bump_css_v.py 20261004a1
    python tools/bump_css_v.py --check          report, change nothing
"""
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGETS = [
    os.path.join('website', '_build', 'build_blog.py'),
    os.path.join('website', '_build', 'build_help.py'),
    os.path.join('website', '_build', 'build_site.py'),
    os.path.join('website', '_build', 'build_static.py'),
    os.path.join('website', 'index.html'),
]

# main.css only. Other stylesheets have their own stamps.
PAT = re.compile(r'(styles/main\.css\?v=)([0-9A-Za-z]+)')


def read(rel):
    with io.open(os.path.join(ROOT, rel), 'r', encoding='utf-8', newline='') as f:
        return f.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    for attempt in range(8):
        try:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            return
        except OSError:
            if attempt == 7:
                raise
            time.sleep(0.2 * (attempt + 1))


def main():
    if '--check' in sys.argv[1:]:
        for rel in TARGETS:
            hits = sorted(set(PAT.findall(read(rel))))
            vers = sorted(set(v for _, v in hits))
            print('%-46s %s' % (rel, ', '.join(vers) or 'NO main.css?v= FOUND'))
        return 0

    if len(sys.argv) < 2:
        sys.stderr.write('usage: bump_css_v.py <new-version>\n')
        return 2
    new = sys.argv[1]
    if not re.match(r'^[0-9A-Za-z]+$', new):
        sys.stderr.write('version must be alphanumeric, got %r\n' % new)
        return 2

    changed = []
    for rel in TARGETS:
        before = read(rel)
        old = sorted(set(v for _, v in PAT.findall(before)))
        if not old:
            sys.stderr.write('WARNING: no main.css?v= in %s - skipped\n' % rel)
            continue
        after = PAT.sub(lambda m: m.group(1) + new, before)
        if after != before:
            write(rel, after)
            changed.append(rel)
        print('%-46s %s -> %s' % (rel, ','.join(old), new))

    if not changed:
        print('nothing changed (already at %s)' % new)
    else:
        print('updated %d file(s); rebuild to push the new stamp to the pages'
              % len(changed))
    return 0


if __name__ == '__main__':
    sys.exit(main())