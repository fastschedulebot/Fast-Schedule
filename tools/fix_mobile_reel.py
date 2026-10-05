#!/usr/bin/env python3
"""Hide the liquid-glass section reel on phones, keeping the Contents pill.

.blog-reel is the frosted prev/current/next card. Under 900px it re-anchors to
the bottom centre at width min(340px, 100vw - 32px) — the same corner the
"Contents" pill (.blog-toc-fab) sits in at left/bottom 14px. The two collided,
and the reel also covered the last lines of the article while it floated there.

The pill already opens the full contents sheet, so the reel was pure overlay on
a phone. It stays exactly as it is from 900px up, where it docks to the right
edge and does not overlap anything.

Patched into the build_blog.py template and the pages it already generated, so
a rebuild reproduces the same output instead of reverting.

    python tools/fix_mobile_reel.py           # apply
    python tools/fix_mobile_reel.py --check   # report only, exit 1 if work remains
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT / "website"

# The mobile half of the reel rule, verbatim. Identical in the generator and in
# every page it emits, so one replacement covers both.
OLD = ".blog-reel { left: 50%; right: auto; top: auto;"
NEW = ".blog-reel { display: none; left: 50%; right: auto; top: auto;"


def targets() -> list[Path]:
    out: list[Path] = [
        ROOT / "_build" / "build_blog.py",
        WEBSITE / "_build" / "build_blog.py",
        WEBSITE / "blog" / "index.html",
    ]
    blog_a = WEBSITE / "blog" / "a"
    if blog_a.is_dir():
        out.extend(sorted(blog_a.glob("*.html")))
    return [p for p in out if p.is_file()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    changed: list[tuple[Path, int]] = []
    for path in targets():
        text = path.read_text(encoding="utf-8")
        n = text.count(OLD)
        if not n:
            continue
        if not args.check:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="")
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        changed.append((rel, n))

    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if not changed:
        print("mobile section reel already hidden.", file=out)
        return 0
    print(f'{"would hide in" if args.check else "hid the reel in"} '
          f"{sum(n for _, n in changed)} rule(s) across {len(changed)} file(s):",
          file=out)
    for rel, n in changed[:6]:
        print(f"  {rel} ({n})", file=out)
    if len(changed) > 6:
        print(f"  ... and {len(changed) - 6} more page(s)", file=out)
    if args.check:
        print("--check: work remains.", file=out)
        return 1
    print("done.", file=out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())