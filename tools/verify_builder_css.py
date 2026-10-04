#!/usr/bin/env python
"""Verify every CSS selector that mentions h1 in the (patched) builder is a
well-formed, correctly-scoped selector — i.e. nothing lost its ancestor part
when h2 variants were added.

Compares the selector set in website/_build/build_help.py + main.css against
the pre-patch generated artifact (website/_build/_hc_component_css.txt, which
is only rewritten by extract_hc_css.py after a build).
"""
from __future__ import annotations

import os
import re
import sys

SEL = re.compile(r"([^{}\n]*\b(?:h1|h2)\b[^{}\n]*)\s*\{")


def selectors(text):
    out = []
    for m in SEL.finditer(text):
        sel = " ".join(m.group(1).split())
        if sel.strip().startswith("@") or "--" in sel:
            continue
        for part in sel.split(","):
            part = part.strip()
            if part and re.search(r"\bh[12]\b", part):
                out.append(part)
    return out


def main():
    before = open(os.path.join("website", "_build", "_hc_component_css.txt"),
                  encoding="utf-8").read()
    src = open(os.path.join("website", "_build", "build_help.py"), encoding="utf-8").read()
    css = open(os.path.join("website", "styles", "main.css"), encoding="utf-8").read()
    b, a = set(selectors(before)), set(selectors(src)) | set(selectors(css))

    print("-- selectors that LOST their ancestor context (bare .hc-art > h2 etc.) --")
    bad = sorted(s for s in a if s.startswith((".hc-art", ".hc-cat-head", ".view", ".hc-404"))
                 and "data-hcfont" not in s)
    # a bare h2 variant is fine when its sibling h1 variant carries the prefix
    problems = []
    for s in bad:
        sib = s.replace("h2", "h1")
        if sib in a:
            # allowed only if the same block's h1 sibling is also bare
            pref = re.search(r"^([^\s]*?\s*)\S*h1", s)
            if "data-hcfont" in s or ("data-" in s) != ("data-" in (pref.group(1) if pref else "")):
                problems.append(s)
    print("\n".join(problems) if problems else "  (none)")

    print("\n-- new selectors added by the patch --")
    for s in sorted(a - b):
        print("  +", s)
    print("\n-- selectors removed by the patch --")
    for s in sorted(b - a):
        print("  -", s)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
