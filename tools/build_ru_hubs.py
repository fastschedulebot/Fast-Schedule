#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build server-rendered Russian landing / help-hub / 404 + RU search data.

Usage:
  python tools/build_ru_hubs.py            build everything
  python tools/build_ru_hubs.py --audit    report unmapped text nodes only

Idempotent: outputs are fully regenerated each run.
"""

import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT + os.sep + 'tools')
sys.path.insert(0, ROOT)

from build_ru_pages import load_map, load_ru_articles, filter_unmapped  # noqa: E402
from build_ru_pages2 import (  # noqa: E402
    build_index, build_404, build_data_file,
)
from build_ru_pages4 import build_help_hub_full  # noqa: E402


def _report(name, unmapped, fh):
    items = sorted(unmapped.items(), key=lambda kv: (-kv[1], kv[0]))
    fh.write('=== %s: %d unmapped ===%s' % (name, len(items), chr(10)))
    for k, c in items[:120]:
        fh.write('[x%d] %s%s' % (c, k[:220], chr(10)))


def main():
    audit = '--audit' in sys.argv
    MAP = load_map()
    print('MAP keys: %d' % len(MAP))
    patch = load_ru_articles()
    print('RU records: %d' % len(patch))

    rep = []
    if audit:
        _, u1 = build_index(MAP, audit_only=True)
        _, u2, _st = build_help_hub_full(MAP, patch, {}, audit_only=True)
        u1 = filter_unmapped(u1, patch)
        u2 = filter_unmapped(u2, patch)
        buf = io.StringIO()
        _report('index', u1, buf)
        _report('help-hub', u2, buf)
        io.open(os.path.join(ROOT, 'tools', 'tmpwork', 'hub_audit.txt'),
                'w', encoding='utf-8').write(buf.getvalue())
        print('audit written to tools/tmpwork/hub_audit.txt')
        return 0

    data_path = build_data_file(patch)
    print('wrote %s' % data_path)
    p1, u1 = build_index(MAP)
    print('wrote %s (%d unmapped)' % (p1, len(u1)))
    p2, u2, st = build_help_hub_full(MAP, patch, {})
    print('wrote %s (%d unmapped) art=%d cat=%d' % (p2, len(u2), st.get('art'), st.get('cat')))
    p3, u3 = build_404(MAP)
    u1 = filter_unmapped(u1, patch)
    u2 = filter_unmapped(u2, patch)
    u3 = filter_unmapped(u3, patch)
    print('wrote %s (%d unmapped)' % (p3, len(u3)))
    buf = io.StringIO()
    _report('index', u1, buf)
    _report('help-hub', u2, buf)
    _report('404', u3, buf)
    io.open(os.path.join(ROOT, 'tools', 'tmpwork', 'hub_audit.txt'),
            'w', encoding='utf-8').write(buf.getvalue())
    left = {k for k in list(u1) + list(u2) + list(u3)}
    print('total distinct unmapped: %d (see tools/tmpwork/hub_audit.txt)' % len(left))
    return 0


if __name__ == '__main__':
    sys.exit(main())
