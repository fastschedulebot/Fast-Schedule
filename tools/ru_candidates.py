"""Per-page RU coverage, to decide which pages deserve a real /ru/ URL.

ru_coverage.py aggregates by section; this reports per page so a threshold
can be applied. A /ru/ page is only worth publishing if most of its prose is
actually Russian -- a page that is 20% translated is a thin duplicate of the
English original and is worse than no Russian URL at all.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ru_coverage import coverage, load_maps  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'website')


def main():
    thr = float(sys.argv[1]) if len(sys.argv) > 1 else 0.90
    maps, _ = load_maps(SITE)
    rows = []
    for base, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in
                   ('_build', 'styles', 'scripts', 'fonts', 'img', 'images', '.git')]
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(base, f)
            rel = os.path.relpath(p, SITE).replace(os.sep, '/')
            s = open(p, encoding='utf-8', errors='replace').read()
            t, h, c, cc, _ = coverage(s, maps)
            by_char = cc / max(1, c)
            by_node = h / max(1, t)
            rows.append((by_char, by_node, rel, t, h))

    rows.sort(reverse=True)
    qual = [r for r in rows if r[0] >= thr]
    print('threshold: %.0f%% of characters translated\n' % (thr * 100))
    print('pages qualifying: %d of %d' % (len(qual), len(rows)))
    print('%-46s %7s %7s %7s' % ('page', 'chars%', 'nodes%', 'nodes'))
    for by_char, by_node, rel, t, h in qual[:40]:
        print('%-46s %6.1f%% %6.1f%% %7d' % (rel, by_char * 100, by_node * 100, t))

    # what the near-misses look like, so the threshold is an informed choice
    near = [r for r in rows if 0.5 <= r[0] < thr]
    print('\nnear misses (50%%-%.0f%%): %d' % (thr * 100, len(near)))
    for by_char, by_node, rel, t, h in near[:15]:
        print('  %-44s %6.1f%%' % (rel, by_char * 100))
    return 0


if __name__ == '__main__':
    sys.exit(main())