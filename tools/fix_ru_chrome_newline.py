"""Correct the newline handling introduced by fix_ru_chrome_retry.py.

`fix_ru_chrome_retry.py` wrote with `io.open(path, 'w', encoding='utf-8',
newline='\\n')`. The original used `open(path, 'w', encoding='utf-8')`, whose
default newline translation turns every '\\n' into CRLF on Windows — and the
generated HTML really is CRLF (help.html: 13720 CRLF, 0 bare LF).

Forcing '\\n' would therefore have rewritten all 408 pages with different line
endings: a ~10 MB spurious diff across the site, for no reason. The retry
helper must keep the original translation and only change the error handling.

Usage:  python tools/fix_ru_chrome_newline.py [--check]
"""
import io
import os
import sys

FULL = os.path.join('website', '_build', 'tag_ru_chrome.py')

OLD = "            with io.open(path, 'w', encoding='utf-8', newline='\\n') as fh:\n"
NEW = ("            # No newline= override: the original write used the default\n"
       "            # Windows translation (the generated HTML is CRLF), and forcing\n"
       "            # '\\n' here would reflow all 408 pages for no reason.\n"
       "            with io.open(path, 'w', encoding='utf-8') as fh:\n")


def main():
    src = io.open(FULL, encoding='utf-8').read()
    if NEW in src:
        print('  tag_ru_chrome.py  ok      original newline translation kept')
        return 0
    if '--check' in sys.argv:
        print('  tag_ru_chrome.py  PENDING original newline translation')
        return 1
    if src.count(OLD) != 1:
        print('  tag_ru_chrome.py  MISSING anchor (%d)' % src.count(OLD))
        return 1
    io.open(FULL, 'w', encoding='utf-8', newline='\n').write(src.replace(OLD, NEW))
    print('  tag_ru_chrome.py  patched original newline translation kept')
    return 0


if __name__ == '__main__':
    sys.exit(main())