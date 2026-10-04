"""Fix tag_ru_chrome.py leaking an orphan </script> on every run.

`broken_re` matched only the OPENING tag:

    <script[^>]*?src="[^"]*?ru-chrome\\.js\\?v=[^"]*"[^>]*?>\\s*

`[^>]*?>` stops at the first '>', i.e. the end of the opening tag, so the
element's closing tag was never consumed. Each run removed the opening tag
and wrote a fresh complete pair, leaving one more closing tag behind -- so
every build grew all 408 pages by 9 bytes and the operation could never be
idempotent.

Measured before the fix: 13-14 stray closing tags on most pages, 64-70 on
the homepage and the archived legal pages, on all 408 pages.

Fix: make the closing tag an optional part of the match, so a run with
nothing to change writes nothing.

Usage:  python tools/fix_ru_chrome_broken_re.py [--check]
"""
import io
import os
import re
import sys

FULL = os.path.join('website', '_build', 'tag_ru_chrome.py')

# Matches the whole assignment line(s) defining broken_re.
LINE = re.compile(r'^broken_re = re\.compile\(.*?\)\n', re.S | re.M)

REPLACEMENT = (
    "# The closing tag must be consumed too. The old pattern stopped at the\n"
    "# first '>' -- the end of the OPENING tag -- so every run orphaned one\n"
    "# more '</script>' in all 408 files (9 bytes each, never idempotent).\n"
    "broken_re = re.compile(\n"
    "    r'<script[^>]*?src=\"[^\"]*?ru-chrome\\.js\\?v=[^\"]*\"[^>]*?>\\s*'\n"
    "    r'(?:</script\\s*>)?', re.I)\n"
)

MARKER = 'r\'(?:</script\\s*>)?\''


def main():
    src = io.open(FULL, encoding='utf-8').read()
    if MARKER in src:
        print('  tag_ru_chrome.py  ok      closing tag consumed')
        return 0
    if '--check' in sys.argv:
        print('  tag_ru_chrome.py  PENDING closing tag consumed')
        return 1
    if not LINE.search(src):
        print('  tag_ru_chrome.py  MISSING broken_re assignment')
        return 1
    src = LINE.sub(lambda _m: REPLACEMENT, src, count=1)
    io.open(FULL, 'w', encoding='utf-8', newline='\n').write(src)
    print('  tag_ru_chrome.py  patched closing tag consumed')
    return 0


if __name__ == '__main__':
    sys.exit(main())