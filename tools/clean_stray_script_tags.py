"""Remove orphaned </script> tags left by the tag_ru_chrome.py bug.

tag_ru_chrome.py used to strip only the opening <script ...> of a ru-chrome
tag and leave its </script> behind, adding one orphan per build. Every page
the builders regenerate is now clean, but four files are NOT produced by the
build chain and kept the accumulated garbage:

  index.html                    (hand-maintained, no builder writes it)
  legal/history/*.html x3       (archived revisions, not in build_site's output)

index.html had 92 </script> against 22 <script; each archived legal page had
64 against 22.

A </script> with no open script before it is, by definition, orphaned: in
well-formed HTML a closing script tag always follows its own opening tag. This
counts depth and deletes only the ones that arrive at depth 0, so it cannot
touch a legitimate pair.

Usage:  python tools/clean_stray_script_tags.py [--check]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'website')

TARGETS = [
    'index.html',
    'legal/history/privacy-2026-09-26.html',
    'legal/history/terms-2026-09-26.html',
    'legal/history/refundpolicy-2026-09-26.html',
]

TOKEN = re.compile(r'<script\b|</script\s*>', re.I)


def stray_count(text):
    depth = stray = 0
    for m in TOKEN.finditer(text):
        if m.group(0).lower().startswith('</'):
            if depth:
                depth -= 1
            else:
                stray += 1
        else:
            depth += 1
    return stray, depth


def strip_stray(text):
    out = []
    last = 0
    depth = 0
    for m in TOKEN.finditer(text):
        if m.group(0).lower().startswith('</'):
            if depth:
                depth -= 1
            else:
                out.append(text[last:m.start()])
                last = m.end()
        else:
            depth += 1
    out.append(text[last:])
    return ''.join(out)


def main():
    check = '--check' in sys.argv
    ok = True
    for rel in TARGETS:
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            print('  %-42s MISSING' % rel)
            ok = False
            continue
        raw = io.open(p, encoding='utf-8', newline='').read()
        stray, depth = stray_count(raw)
        if stray == 0:
            print('  %-42s clean (%d unclosed)' % (rel, depth))
            continue
        if check:
            print('  %-42s PENDING %d stray' % (rel, stray))
            ok = False
            continue
        fixed = strip_stray(raw)
        after, depth2 = stray_count(fixed)
        if after:
            print('  %-42s FAILED (%d left)' % (rel, after))
            ok = False
            continue
        io.open(p, 'w', encoding='utf-8', newline='').write(fixed)
        print('  %-42s removed %d stray </script>' % (rel, stray))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())