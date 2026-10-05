#!/usr/bin/env python3
"""Fix Russian text that does not fit its box.

Russian translations run longer than the English strings they replace, so boxes
sized against the English copy overflow once the site is switched to Russian.

The concrete defect this script repairs: the Help/Blog prev-next pager is a two
column CSS grid declared as `grid-template-columns: 1fr 1fr`. A bare `1fr` track
is `minmax(auto, 1fr)`, so each track refuses to shrink below its own min-content
width -- and the pager titles are `white-space: nowrap` with an ellipsis, so their
min-content width is the *entire* title. In English the two titles happen to add
up to less than the row; in Russian they do not, the tracks get sized to the full
titles, and the row spills past the viewport (measured: 140px of page-level
horizontal scroll at 768px, on every Help article).

The fix is `minmax(0, 1fr)`, which drops the automatic minimum and lets the
ellipsis actually do its job. Both the generated HTML and the build sources that
produce it are patched, so a rebuild does not reintroduce the bug.

    python tools/fix_ru_text_overflow.py           # apply
    python tools/fix_ru_text_overflow.py --check   # report only, non-zero if work remains
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT / "website"
BUILD = WEBSITE / "_build"

OLD_GRID = "grid-template-columns: 1fr 1fr; gap: 12px"
NEW_GRID = "grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 12px"

# Guard against a half-applied edit or an unrelated rule drifting into the match.
OLD_GRID_FQ = ".hc-pager { max-width: 860px; margin: 16px auto 0; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }"
NEW_GRID_FQ = ".hc-pager { max-width: 860px; margin: 16px auto 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 12px; }"

# The single-column fallback inside @media (max-width: 760px) carries the same
# defect: `1fr` is `minmax(auto, 1fr)`, so on a phone the single track was still
# sized to the full nowrap title and the pager spilled sideways instead of
# ellipsizing.
OLD_GRID_1COL = ".hc-pager { grid-template-columns: 1fr; }"
NEW_GRID_1COL = ".hc-pager { grid-template-columns: minmax(0, 1fr); }"


def targets() -> list[Path]:
    """Every file that can emit the pager rule: generated pages and build sources."""
    found: list[Path] = []
    for pattern in ("*.html", "*/*.html", "*/*/*.html", "*/*/*/*.html"):
        found.extend(WEBSITE.glob(pattern))
    if BUILD.is_dir():
        found.extend(sorted(BUILD.glob("*.py")))
        found.extend(sorted(BUILD.glob("*.txt")))
    return sorted({p for p in found if p.is_file()})


def patch_text(text: str) -> tuple[str, int]:
    hits = 0
    if OLD_GRID_FQ in text:
        hits += text.count(OLD_GRID_FQ)
        text = text.replace(OLD_GRID_FQ, NEW_GRID_FQ)
    # Some build sources embed the same declaration with different surrounding
    # text; the bare-token form still identifies the rule unambiguously.
    if OLD_GRID in text:
        hits += text.count(OLD_GRID)
        text = text.replace(OLD_GRID, NEW_GRID)
    if OLD_GRID_1COL in text:
        hits += text.count(OLD_GRID_1COL)
        text = text.replace(OLD_GRID_1COL, NEW_GRID_1COL)
    return text, hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if any file still needs the fix")
    args = ap.parse_args()

    changed: list[tuple[Path, int]] = []
    scanned = 0
    for path in targets():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD_GRID not in text and OLD_GRID_1COL not in text:
            continue
        scanned += 1
        new_text, hits = patch_text(text)
        if hits and not args.check:
            path.write_text(new_text, encoding="utf-8", newline="")
        changed.append((path, hits))

    total = sum(h for _, h in changed)
    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    scope = "would change" if args.check else "changed"
    print(f"{scope} {total} pager grid declaration(s) in {len(changed)} file(s)", file=out)
    if args.check and total:
        for p, h in changed[:10]:
            print(f"  needs fix ({h}x): {p.relative_to(ROOT)}", file=out)
        if len(changed) > 10:
            print(f"  ... and {len(changed) - 10} more", file=out)
    out.flush()
    return 1 if (args.check and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())