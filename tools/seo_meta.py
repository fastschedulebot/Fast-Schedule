"""Detail view of title/description problems (used to target the fixes)."""
import io
import os
import re
import sys

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'website')
RE_TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.S)
RE_DESC = re.compile(r'<meta name="description" content="(.*?)"', re.S)


def main():
    bad_t, bad_d = [], []
    dup_t, dup_d = {}, {}
    for dp, dirs, fns in os.walk(SITE):
        for fn in fns:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, SITE).replace(os.sep, '/')
            head = io.open(full, encoding='utf-8').read().split('</head>')[0]
            m = RE_TITLE.search(head)
            if m:
                t = m.group(1).strip()
                if not 30 <= len(t) <= 65:
                    bad_t.append((len(t), rel, t))
                dup_t.setdefault(t, []).append(rel)
            m = RE_DESC.search(head)
            if m:
                d = m.group(1).strip()
                if not 70 <= len(d) <= 160:
                    bad_d.append((len(d), rel, d))
                dup_d.setdefault(d, []).append(rel)

    print('TITLE out of 30-65: %d' % len(bad_t))
    for n, p, t in sorted(bad_t):
        print('  %3d  %-34s %s' % (n, p, t))
    print()
    print('DESC out of 70-160: %d' % len(bad_d))
    for n, p, d in sorted(bad_d):
        print('  %3d  %-34s %s' % (n, p, d[:120]))
    print()
    print('DUPLICATE TITLES')
    for t, v in sorted(dup_t.items()):
        if len(v) > 1:
            print('  %r' % t)
            for p in v:
                print('      %s' % p)
    print()
    print('DUPLICATE DESCRIPTIONS: %d groups' % sum(1 for v in dup_d.values() if len(v) > 1))
    for d, v in sorted(dup_d.items()):
        if len(v) > 1:
            print('  %r' % d[:110])
            for p in v:
                print('      %s' % p)
    return 0


if __name__ == '__main__':
    sys.exit(main())