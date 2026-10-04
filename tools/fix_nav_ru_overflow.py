#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Stop the Russian homepage navbar from pushing the controls off-screen.

Symptom
-------
On the homepage in Russian, the settings gear (and behind it the
"Открыть бота" CTA) was not visible: the nav was wider than the viewport
and the overflow ran off the right edge, where the header clipped it. In
English the same bar fits.

Measured at a 1280px viewport
----------------------------
    English nav, natural width ......... 891px   (998px available)  fits
    Russian nav, natural width ......... 1187px  (998px available)  overflows by 189px

"Экономия времени" is 168px against "Time saved" at 109px; "Вопросы и
ответы" is 159px against "FAQ" at 55px. Russian is simply wider, and the
only collapse rule in the stylesheet fired at 860px - far too late.

Why this is scoped to html[lang="ru"]
-------------------------------------
The two languages have different natural widths, so a breakpoint tuned for
English is wrong for Russian and a breakpoint tuned for Russian would hide
nav links from English users who did not need them to go. lang.js already
sets <html lang>, so the rule can simply address the wider case. Blog and
Help do not disappear from the site - they are in the mobile menu and in
the footer - only from the top bar.

Breakpoints, and why they are where they are
---------------------------------------------
Measured in the rendered page, not estimated. The chrome (brand + both
gutters) is a fixed 362px, so the viewport must be at least
`nav width + 362`:

    Russian bar with the Blog/Help pills .... 1097px  ->  1459px
    Russian bar without them ................  938px  ->  1300px

The first guess of 1400/1180 was wrong - at 1440px the gear was still 9px
off the right edge - which is why these are measured numbers. 1500 and
1320 are used rather than 1459 and 1300 so neither breakpoint sits exactly
on its limit.

    >= 1501px  full bar, both languages
    1321-1500  Russian bar without the Blog/Help pills, tighter padding
    <= 1320    Russian bar keeps only the gear, the CTA and the burger

Usage:  python tools/fix_nav_ru_overflow.py          apply
        python tools/fix_nav_ru_overflow.py --check  verify only
"""
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = 'website/index.html'

ANCHOR = ('    @media (max-width: 860px) { .home-nav nav > a:not(.nav-cta-sm) '
          '{ display: none; } .home-nav .help-row, .home-nav .support-ib '
          '{ display: none; } }\n')

PATCH_BODY = """    /* Russian labels are about a third wider than the English ones, so the
       bar that fits in English overflowed in Russian and pushed the settings
       gear and the Open Bot CTA past the right edge, where the header
       clipped them. The two controls must never be what gets clipped, so
       Russian sheds the optional items at the width Russian actually needs
       (see tools/fix_nav_ru_overflow.py for the measurements). */
    @media (max-width: 1500px) {
      html[lang="ru"] .home-nav .help-row { display: none; }
      html[lang="ru"] .home-nav nav a:not(.nav-cta-sm) { padding: 9px 9px; }
    }
    @media (max-width: 1320px) {
      html[lang="ru"] .home-nav nav > a:not(.nav-cta-sm) { display: none; }
    }"""

REQUIRED = [
    '@media (max-width: 1500px) {\n      html[lang="ru"] .home-nav .help-row',
    '@media (max-width: 1320px) {\n      html[lang="ru"] .home-nav '
    'nav > a:not(.nav-cta-sm)',
]

# The rule must appear exactly once. Two copies are a real defect: they
# duplicate the rule and make the stylesheet lie about its own breakpoints.
EXPECT_ONCE = ('@media (max-width: 1500px) {\n      html[lang="ru"] '
               '.home-nav .help-row')

# Any media block that targets the Russian homepage nav, whatever its
# breakpoints. Used to purge stale copies before inserting the current one.
RULE_RE = re.compile(
    r'[ \t]*@media \(max-width: \d+px\) \{\r?\n'
    r'(?:[ \t]*html\[lang="ru"\][^\n]*\r?\n)+[ \t]*\}\r?\n',
    re.M)

# The explanatory comment is purged SEPARATELY, not folded into RULE_RE.
# Two reasons: it has to be removed even when it is left orphaned with no
# media block after it (which is exactly what accumulated), and a combined
# pattern cannot match a comment that is not followed by a block.
#
# Stripping only the media blocks left the comment behind, so every run
# appended another one - the file grew to four copies of the same paragraph
# while the guard still reported "rule present exactly once", because it
# only counted the blocks.
COMMENT_RE = re.compile(
    r'[ \t]*/\* Russian labels are about a third[^*]*\*/\r?\n')

# Everything between the <=860px collapse rule and the rule that follows it
# is ours to rewrite. Splicing a fixed body into this range makes the script
# idempotent no matter what a previous version left behind.
GAP_RE = re.compile(
    r'(?P<anchor>[ \t]*@media \(max-width: 860px\) \{ \.home-nav nav[^\n]*'
    r'[^\n]*\}\r?\n)'
    r'(?P<gap>.*?)'
    r'(?P<next>[ \t]*/\* burger \+ mobile menu \*/)',
    re.S)


def read():
    with io.open(os.path.join(ROOT, REL), 'r', encoding='utf-8', newline='') as f:
        return f.read()


def write(text):
    path = os.path.join(ROOT, REL)
    for attempt in range(8):
        try:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            return
        except OSError:
            if attempt == 7:
                raise
            time.sleep(0.2 * (attempt + 1))


def main():
    check = '--check' in sys.argv[1:]
    before = read()
    nl = '\r\n' if '\r\n' in before else '\n'
    anchor = ANCHOR.replace('\n', nl)
    patch = PATCH_BODY.replace('\n', nl)

    # Rewrite the gap between the 860px rule and the next rule wholesale
    # rather than purging-and-appending. Purge-then-append leaves whatever
    # blank lines surrounded the old copy behind, so each run added one and
    # the script never reached a true no-op. Splicing a fixed block into a
    # fixed range is idempotent by construction, whatever is in the range.
    m = GAP_RE.search(before)
    if m:
        body = PATCH_BODY.replace('\n', nl)
        gap = nl + body + nl
        after = before[:m.start('gap')] + gap + before[m.end('gap'):]
    else:
        after = before          # anchor moved; guard below will complain
    changed = after != before

    missing = [m for m in REQUIRED if m.replace('\n', nl) not in after]
    once = after.count(EXPECT_ONCE.replace('\n', nl))
    # One installation = TWO media blocks (1500 and 1320), so counting
    # RULE_RE hits would say "2" for a perfectly correct file. Count the
    # installation anchor instead, and separately reject the stale
    # breakpoints that a previous run left behind.
    stale = [bp for bp in ('1400px', '1180px')
             if re.search(r'@media \(max-width: %s\) \{\s*html\[lang="ru"\]'
                          % bp, after)]
    comments = after.count('Russian labels are about a third')
    if comments != 1:
        stale.append('comment copies: %d' % comments)
    if missing or once != 1 or stale:
        for m in missing:
            sys.stderr.write('REQUIRED marker missing -> %r\n' % m)
        sys.stderr.write('rule installations: %d (expected 1)\n' % once)
        if stale:
            sys.stderr.write('stale RU breakpoint(s) still present: %s\n'
                             % ', '.join(stale))
        sys.stderr.write('nothing written\n')
        return 2
    if not check and changed:
        write(after)

    sys.stdout.write('%s   rule present exactly once\n'
                     % ('files updated: 1' if (changed and not check)
                        else 'files updated: 0'))
    return 1 if (changed and check) else 0


if __name__ == '__main__':
    sys.exit(main())