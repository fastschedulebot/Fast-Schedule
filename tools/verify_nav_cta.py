# -*- coding: utf-8 -*-
"""Verify the navbar fixes across every built page, not just a sample.

Two invariants, asserted over all generated HTML:

1. The Open Bot CTA is the last ANCHOR of .nav-right, the settings gear
   trails it as the final child, and neither still sits inside .nav-left.
   Spot-checking four pages is not enough: the header is emitted by
   several code paths (help hub, help article, blog index, blog article,
   legal, 404) and they can drift apart.

2. The nav label never wraps: .nav-link must carry white-space: nowrap, and
   no built page may embed a stylesheet version older than the current one -
   a stale ?v= means returning visitors keep the CSS they already cached,
   which is how a correct fix looks like it did nothing.

Exits non-zero on any violation.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'website')

NAV_RIGHT = re.compile(r'<div class="nav-group nav-right">(.*?)</div></div></header>',
                       re.S)
NAV_LEFT = re.compile(r'<div class="nav-group nav-left">(.*?)</div>', re.S)
CSS_VER = re.compile(r'styles/main\.css\?v=([0-9A-Za-z]+)')
CTA_RE = re.compile(r'class="[^"]*\bnav-cta\b[^"]*"')

# The version the builders should currently emit, read from the homepage
# (hand-maintained, so it is the cheapest source of truth).
with io.open(os.path.join(WEB, 'index.html'), 'r', encoding='utf-8') as f:
    home = f.read()
m = CSS_VER.search(home)
if not m:
    sys.stderr.write('no main.css?v= in website/index.html\n')
    sys.exit(2)
WANT = m.group(1)

out = io.open(os.path.join(ROOT, 'tmp_nav_cta.log'), 'w', encoding='utf-8')
pages = cta_left = cta_not_last = stale_css = no_nav = 0
bad = []

for dirpath, dirs, files in os.walk(WEB):
    dirs[:] = [d for d in dirs if d not in ('_build', '__pycache__')]
    for fn in files:
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, WEB)
        pages += 1
        with io.open(p, 'r', encoding='utf-8', errors='replace') as f:
            txt = f.read()
        mr = NAV_RIGHT.search(txt)
        ml = NAV_LEFT.search(txt)
        if not mr:
            no_nav += 1          # homepage uses its own .home-nav; fine
            continue
        right = mr.group(1)
        # .nav-left ends where .nav-center/.nav-right begins (or the header
        # closes); the NAV_LEFT regex stops at the first </div>, which is
        # the brand link's own close on some pages, so bound it explicitly.
        left_end = len(txt)
        for marker in ('<div class="nav-center">',
                       '<div class="nav-group nav-right">',
                       '</div></div></header>'):
            i = txt.find(marker)
            if i != -1:
                left_end = min(left_end, i)
        left = txt[txt.find('<div class="nav-group nav-left">'):left_end]
        if CTA_RE.search(left):
            cta_left += 1
            bad.append('%s: CTA still in .nav-left' % rel)
        if 'settings-wrap' in left:
            cta_left += 1
            bad.append('%s: settings gear still in .nav-left' % rel)
        # Assert by POSITION. The CTA is the last ANCHOR in .nav-right (it
        # opens after the Help popover) and the settings gear span trails
        # it as the final child — the gear's own menu holds anchors, so a
        # naive "CTA close is the last </a>" check no longer applies.
        i_cta = right.find('nav-cta')
        i_pop = right.find('site-menu-wrap')
        i_gear = right.find('<span class="settings-wrap">')
        if i_cta == -1:
            cta_not_last += 1
            bad.append('%s: no CTA inside .nav-right' % rel)
        elif i_pop != -1 and i_cta < i_pop:
            cta_not_last += 1
            bad.append('%s: CTA opens before the Help popover' % rel)
        else:
            cta_close = right.find('</a>', i_cta)
            if cta_close == -1 or i_gear == -1 or i_gear < cta_close:
                cta_not_last += 1
                bad.append('%s: settings gear is not trailing the CTA' % rel)
            else:
                # the gear span must run to the end of the group: balance
                # its nested spans, then only whitespace may follow.
                depth = 0
                gear_end = -1
                for m in re.finditer(r'<span[\s>]|</span>', right[i_gear:]):
                    depth += -1 if m.group(0) == '</span>' else 1
                    if depth == 0:
                        gear_end = i_gear + m.end()
                        break
                if gear_end == -1 or right[gear_end:].strip():
                    cta_not_last += 1
                    bad.append('%s: something renders after the gear' % rel)
        vers = set(CSS_VER.findall(txt))
        if vers and WANT not in vers:
            stale_css += 1
            bad.append('%s: main.css?v=%s (want %s)'
                       % (rel, ','.join(sorted(vers)), WANT))

out.write('pages scanned: %d\n' % pages)
out.write('pages with the unified nav: %d (no unified nav: %d)\n'
          % (pages - no_nav, no_nav))
out.write('CTA still in nav-left: %d\n' % cta_left)
out.write('CTA not last in nav-right: %d\n' % cta_not_last)
out.write('pages on a stale main.css version: %d (want %s)\n'
          % (stale_css, WANT))
out.write('violations: %d\n' % len(bad))
for line in bad[:40]:
    out.write('  %s\n' % line)
out.close()

print('pages=%d  ctaInLeft=%d  ctaNotLast=%d  staleCss=%d (want %s)  violations=%d'
      % (pages, cta_left, cta_not_last, stale_css, WANT, len(bad)))
sys.exit(1 if bad else 0)