"""Round-6 SEO patch (idempotent).

The crawlable index in build_help.py listed articles by their raw title, so
the category landing article ("Getting Started", id `start`) rendered
identically to the real guide ("Getting Started", id `getting_started`) --
two identical rows in the same list, linking to two different pages. Their
own page titles already say "Overview", so the index now matches.

Usage:  python tools/patch_seo_builders6.py [--check]
"""
import io
import os
import sys

BUILD = os.path.join('website', '_build')
EDITS = [
    ('build_help.py',
     "        _items = ''.join(\n"
     "            '<li><a href=\"help/a/%s.html\">%s</a></li>' % (esc(k['id']), esc(k['title']))\n"
     "            for k in _entries)\n",
     "        _items = ''.join(\n"
     "            '<li><a href=\"help/a/%s.html\">%s</a></li>'\n"
     "            % (esc(k['id']),\n"
     "               esc(k['title'] + (' Overview' if k['id'] == _cid else '')))\n"
     "            for k in _entries)\n",
     'index labels the category landing article "Overview"'),
]


def main():
    check_only = '--check' in sys.argv
    ok = True
    for path, old, new, tag in EDITS:
        full = os.path.join(BUILD, path)
        src = io.open(full, encoding='utf-8').read()
        if new in src:
            status = 'ok     '
        elif old in src:
            if check_only:
                print('  %-14s PENDING %s' % (path, tag))
                ok = False
                continue
            if src.count(old) != 1:
                print('  %-14s AMBIGUOUS (%d) %s' % (path, src.count(old), tag))
                ok = False
                continue
            src = src.replace(old, new)
            io.open(full, 'w', encoding='utf-8', newline='\n').write(src)
            status = 'patched '
        else:
            print('  %-14s MISSING  %s' % (path, tag))
            ok = False
            continue
        print('  %-14s %s %s' % (path, status, tag))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())