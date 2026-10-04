#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move the Open Bot CTA to the right of the navbar, and stop the Help
pill's label from wrapping.

Two defects, one script, because both live in the same header.

1. "Help Center" renders huge and on two lines
---------------------------------------------
`.nav-link` has a FIXED height of 42px but no `white-space: nowrap`, and a
flex item shrinks by default. Once the header runs out of room the label
wraps to a second line inside the fixed box and spills out of it. Measured
at a 960px viewport with the help search box visible (it disappears on the
help home view, so this only shows on an article):

    pill 137px wide -> forced to 109px, label 46px tall inside a 42px pill

The stylesheet already hides nav labels at <=900px, but the pill is still
absorbing that squeeze at 960px, so between ~900px and ~1000px there is a
window where the label wraps instead of being dropped.

2. Open Bot sits in the middle
------------------------------
`unified_nav()` put the CTA in `.nav-left`, between the brand and the gear,
with Blog and Help Center in `.nav-right`. It reads as a dead control in the
middle of the header. Both builders - build_help.py and build_site.py - go
through this one function, so the fix is one edit and one rebuild.

Usage:  python tools/fix_nav_wrap_and_cta.py          apply
        python tools/fix_nav_wrap_and_cta.py --check  verify only
"""
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUILD_HELP = os.path.join('website', '_build', 'build_help.py')
CSS = os.path.join('website', 'styles', 'main.css')

# --- builder: move the CTA from .nav-left to the end of .nav-right --------
OLD_NAV = (
    """    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{brand}{cta}{gear}{left_extra}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<span class="site-menu-wrap">'
            f'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" '
            f'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>'
            f'{pop}</span>'
            f'</div></div></header>')""")

NEW_NAV = (
    """    return (f'<header class="site"><div class="wrap nav nav-unified">'
            f'<div class="nav-group nav-left">{brand}{gear}{left_extra}</div>'
            f'{center}'
            f'<div class="nav-group nav-right">'
            f'<a class="nav-link" href="{rel}/blog/index.html">{svg("megaphone")}<span>Blog</span></a>'
            f'<span class="site-menu-wrap">'
            f'<a class="nav-link site-menu-row" role="menuitem" href="{rel}/help.html" '
            f'aria-haspopup="menu" aria-expanded="false">{svg("book")}<span>Help Center</span></a>'
            f'{pop}</span>'
            f'{cta}'
            f'</div></div></header>')""")

# The compact-CTA media query targeted the old position.
OLD_CTA_CSS = """      .nav-unified .nav-left .nav-cta span { display: none; }
      .nav-unified .nav-left .nav-cta { padding: 0 12px; }"""
NEW_CTA_CSS = """      .nav-unified .nav-right .nav-cta span { display: none; }
      .nav-unified .nav-right .nav-cta { padding: 0 12px; }"""

# --- CSS: a pill label must never wrap ----------------------------------
OLD_LINK = """  font-weight: 600; font-size: .9rem; cursor: pointer; text-decoration: none;
  transition: transform .2s, border-color .2s, background .2s;
}"""
NEW_LINK = """  font-weight: 600; font-size: .9rem; cursor: pointer; text-decoration: none;
  /* A fixed-height pill whose label is allowed to wrap spills the label out
     of the pill. Shrinking is the flex item's job, not the label's: the
     label stays on one line and the item gives up width instead. */
  white-space: nowrap; flex: 0 0 auto;
  transition: transform .2s, border-color .2s, background .2s;
}"""

# --- CSS: drop labels before they can squeeze ---------------------------
OLD_900 = """@media (max-width: 900px) {
  .nav-unified .nav-link span { display: none; }
  .nav-unified .nav-link { padding: 0 11px; height: 40px; }
  .nav-unified .nav-group { gap: 8px; }
}"""
NEW_900 = """@media (max-width: 1080px) {
  .nav-unified .nav-link span { display: none; }
  .nav-unified .nav-link { padding: 0 11px; height: 40px; }
  .nav-unified .nav-group { gap: 8px; }
}"""

EDITS = {
    BUILD_HELP: [(OLD_NAV, NEW_NAV, 'nav'),
                 (OLD_CTA_CSS, NEW_CTA_CSS, 'cta-css')],
    CSS: [(OLD_LINK, NEW_LINK, 'nowrap'),
          (OLD_900, NEW_900, 'breakpoint')],
}

# (file, marker) that must be present afterwards.
REQUIRED = [
    (BUILD_HELP, "f'<div class=\"nav-group nav-left\">{brand}{gear}{left_extra}</div>'"),
    (BUILD_HELP, "f'{pop}</span>'\n            f'{cta}'"),
    (BUILD_HELP, '.nav-unified .nav-right .nav-cta span { display: none; }'),
    (CSS, 'white-space: nowrap; flex: 0 0 auto;'),
    (CSS, '@media (max-width: 1080px) {'),
]
# (file, marker) that must be gone afterwards.
LEFTOVER = [
    (BUILD_HELP, '{brand}{cta}{gear}{left_extra}'),
    (BUILD_HELP, '.nav-unified .nav-left .nav-cta'),
    (CSS, '@media (max-width: 900px) {\n  .nav-unified .nav-link span'),
]


def read(rel):
    with io.open(os.path.join(ROOT, rel), 'r', encoding='utf-8', newline='') as f:
        return f.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    for attempt in range(8):
        try:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            return
        except OSError:
            if attempt == 7:
                raise
            time.sleep(0.2 * (attempt + 1))


def nl_of(text):
    return '\r\n' if '\r\n' in text else '\n'


def adapt(s, nl):
    return s if nl == '\n' else s.replace('\n', nl)


def main():
    check = '--check' in sys.argv[1:]
    staged, changed = {}, []

    # Phase 1: compute everything in memory; write only once it all checks.
    for rel, edits in EDITS.items():
        before = read(rel)
        nl = nl_of(before)
        after = before
        for old, new, tag in edits:
            o, n = adapt(old, nl), adapt(new, nl)
            if o in after:
                after = after.replace(o, n, 1)
                changed.append('%s (%s)' % (rel, tag))
        staged[rel] = after

    missing = ['%s: %s' % (rel, m) for rel, m in REQUIRED
               if adapt(m, nl_of(staged.get(rel, read(rel)))) not in
               staged.get(rel, read(rel))]
    left = ['%s: %s' % (rel, m) for rel, m in LEFTOVER
            if adapt(m, nl_of(staged.get(rel, read(rel)))) in
            staged.get(rel, read(rel))]
    if missing or left:
        for line in missing:
            sys.stderr.write('REQUIRED missing -> %s\n' % line)
        for line in left:
            sys.stderr.write('LEFTOVER still present -> %s\n' % line)
        sys.stderr.write('nothing written\n')
        return 2

    if not check:
        for rel in EDITS:
            if staged[rel] != read(rel):
                write(rel, staged[rel])

    sys.stdout.write('edits applied: %s\n' % (', '.join(changed) or 'none '
                                               '(already applied)'))
    if check and not changed:
        sys.stdout.write('state: already applied\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())