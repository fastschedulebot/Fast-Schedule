#!/usr/bin/env python
"""One-off repair: a count=0 replace of `.hc-art > h1 {` also matched inside
`html[data-hcfont="l"] .hc-art > h1 {`, so the large-font rule came out as
`html[data-hcfont="l"] .hc-art > h1, .hc-art > h2` — the h2 half lost its
prefix and would apply at every font size.

Restores the scoped selector. Idempotent.
"""
import os
import sys

P = os.path.join("website", "_build", "build_help.py")
BAD = 'html[data-hcfont="l"] .hc-art > h1, .hc-art > h2 {'
GOOD = 'html[data-hcfont="l"] .hc-art > h1, html[data-hcfont="l"] .hc-art > h2 {'


def main():
    s = open(P, encoding="utf-8").read()
    if GOOD in s:
        print("already correct")
        return 0
    if BAD not in s:
        print("ANCHOR MISSING: neither spelling found — inspect line ~1635 by hand")
        return 1
    open(P, "w", encoding="utf-8", newline="\n").write(s.replace(BAD, GOOD, 1))
    print("repaired large-font article-title selector")
    return 0


if __name__ == "__main__":
    sys.exit(main())
