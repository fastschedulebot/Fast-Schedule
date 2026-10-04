"""Bump the cache-busting version for lang.js / ru-chrome.js.

tag_ru_chrome.py hardcodes LANG_V and stamps it onto both script URLs. It was
left at 20261003d1 while lang.js itself changed, so browsers kept serving the
old body from cache under an unchanged cache key -- which is how a /ru/ page
still flipped back to English after lang.js was taught to honour the served
`<html lang>`.

Any edit to lang.js or ru-chrome.js must bump this constant, otherwise the
change never reaches a returning visitor.

Usage:  python tools/bump_lang_v.py [new-version]
"""
import io
import os
import re
import sys

FULL = os.path.join('website', '_build', 'tag_ru_chrome.py')
LINE = re.compile(r"^LANG_V = '(\d{8}[a-z]?\d*?)'\n", re.M)


def main():
    src = io.open(FULL, encoding='utf-8').read()
    m = LINE.search(src)
    if not m:
        print('  tag_ru_chrome.py  MISSING LANG_V')
        return 1
    cur = m.group(1)
    new = sys.argv[1] if len(sys.argv) > 1 else '20261004a1'
    if new == cur:
        print('  LANG_V already %s' % new)
        return 0
    src = LINE.sub("LANG_V = '%s'\n" % new, src, count=1)
    io.open(FULL, 'w', encoding='utf-8', newline='\n').write(src)
    print('  LANG_V %s -> %s' % (cur, new))
    return 0


if __name__ == '__main__':
    sys.exit(main())