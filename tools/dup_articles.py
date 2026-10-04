"""Compare the help articles whose titles collide (start vs getting_started)."""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'website', '_build'))
os.chdir(ROOT)

import build_static as bs  # noqa: E402


def main():
    for aid in ('start', 'getting_started'):
        p = os.path.join(ROOT, 'website', 'help', 'a', aid + '.html')
        s = io.open(p, encoding='utf-8').read()
        m = re.search(r'<article class="doc">(.*?)</article>', s, re.S)
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip() if m else ''
        h1 = re.search(r'<h1>(.*?)</h1>', s, re.S)
        print('== %s  (%d chars of body)' % (aid, len(text)))
        print('   h1: %s' % (h1.group(1) if h1 else '?'))
        print('   %s' % text[:400])
        links = sorted(set(re.findall(r'href="([^"]+\.html)"', m.group(1) if m else '')))
        print('   links: %s' % links)
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())