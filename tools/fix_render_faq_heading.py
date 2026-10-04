"""Give render_faq a heading parameter so /ru/ pages are not half-English.

tools/build_ru.py reuses the English page chrome (nav, FAQ accordion, CTA)
so the Russian pages look and behave like the originals. render_faq hardcoded
its heading as `<h2>Common questions</h2>`, which left every Russian article
opening its FAQ block with an English line.

The default keeps the English pages byte-identical; only the Russian callers
pass a translated heading.

Usage:  python tools/fix_render_faq_heading.py [--check]
"""
import io
import os
import sys

FULL = os.path.join('website', '_build', 'build_help.py')

OLD_SIG = "def render_faq(faq, link_href, link_label, aid=None):\n"
NEW_SIG = "def render_faq(faq, link_href, link_label, aid=None, heading='Common questions'):\n"

OLD_OUT = "    out = ['<div class=\"hc-faq\"><h2>Common questions</h2>']\n"
NEW_OUT = "    out = ['<div class=\"hc-faq\"><h2>' + esc(heading) + '</h2>']\n"


def main():
    src = io.open(FULL, encoding='utf-8').read()
    if NEW_SIG in src and NEW_OUT in src:
        print('  build_help.py  ok      render_faq heading parameterised')
        return 0
    if '--check' in sys.argv:
        print('  build_help.py  PENDING render_faq heading parameterised')
        return 1
    if src.count(OLD_SIG) != 1 or src.count(OLD_OUT) != 1:
        print('  build_help.py  MISSING anchor (sig=%d out=%d)'
              % (src.count(OLD_SIG), src.count(OLD_OUT)))
        return 1
    src = src.replace(OLD_SIG, NEW_SIG).replace(OLD_OUT, NEW_OUT)
    io.open(FULL, 'w', encoding='utf-8', newline='\n').write(src)
    print('  build_help.py  patched render_faq heading parameterised')
    return 0


if __name__ == '__main__':
    sys.exit(main())