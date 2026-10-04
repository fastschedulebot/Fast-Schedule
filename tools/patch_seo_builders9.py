"""Round-9: one-line guard on the round-8 index label.

A category whose title equals the article title ("Getting Started" inside
Getting Started) made the parenthetical read "Getting Started (Getting
Started)". Skip it when the category adds nothing.

Usage:  python tools/patch_seo_builders9.py [--check]
"""
import io
import os
import sys

FULL = os.path.join('website', '_build', 'build_help.py')
OLD = ("            if _idx_titles.get(k['title'], 0) > 1:\n"
       "                return '%s (%s)' % (k['title'], _ctitle)\n")
NEW = ("            if _idx_titles.get(k['title'], 0) > 1 and \\\n"
       "                    _ctitle.lower() != k['title'].lower():\n"
       "                return '%s (%s)' % (k['title'], _ctitle)\n")


def main():
    src = io.open(FULL, encoding='utf-8').read()
    if NEW in src:
        print('  build_help.py  ok      index label skips a redundant category')
        return 0
    if '--check' in sys.argv:
        print('  build_help.py  PENDING index label skips a redundant category')
        return 1
    if src.count(OLD) != 1:
        print('  build_help.py  MISSING/AMBIGUOUS (%d)' % src.count(OLD))
        return 1
    io.open(FULL, 'w', encoding='utf-8', newline='\n').write(src.replace(OLD, NEW))
    print('  build_help.py  patched index label skips a redundant category')
    return 0


if __name__ == '__main__':
    sys.exit(main())