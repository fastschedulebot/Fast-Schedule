#!/usr/bin/env python3
"""Repoint every social-preview image reference at the regenerated card.

The old og-cover.png was laid out without measuring the text, so the subtitle
and the t.me handle ran off the right edge of the 1200px canvas and every link
preview clipped them mid-word. website/og-cover-v2.png is re-rendered in
headless Chrome with the site's own webfonts and a safe-area + crop-survival
guard (tools/make_og_image.mjs).

The filename changes on purpose. Telegram, Facebook, X and Slack cache preview
images by URL and largely ignore cache-busting headers, so repainting
og-cover.png in place would leave every existing share showing the clipped
card indefinitely. A new URL is the only reliable bust.

Touches the generated pages and the build sources that emit them, so a rebuild
does not reintroduce the old filename.

    python tools/switch_og_image.py           # apply
    python tools/switch_og_image.py --check   # report only, exit 1 if work remains
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT / "website"
BUILD = WEBSITE / "_build"

OLD = "og-cover.png"
NEW = "og-cover-v2.png"


def targets() -> list[Path]:
    out: list[Path] = []
    for pattern in ("*.html", "*/*.html", "*/*/*.html", "*/*/*/*.html"):
        out.extend(WEBSITE.glob(pattern))
    if BUILD.is_dir():
        out.extend(sorted(BUILD.glob("*.py")))
        out.extend(sorted(BUILD.glob("*.txt")))
    return sorted({p for p in out if p.is_file()})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    changed: list[tuple[Path, int]] = []
    for path in targets():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        n = text.count(OLD)
        if not n:
            continue
        # Guard against rewriting a reference that is already the new file.
        n = text.count(OLD) - text.count(NEW)  # NEW contains OLD as a substring
        if n <= 0:
            continue
        if not args.check:
            path.write_text(text.replace(OLD, NEW), encoding="utf-8", newline="")
        changed.append((path, n))

    total = sum(h for _, h in changed)
    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print(f"{'would change' if args.check else 'changed'} {total} reference(s) in {len(changed)} file(s)", file=out)
    if args.check and total:
        for p, h in changed[:8]:
            print(f"  needs update ({h}x): {p.relative_to(ROOT)}", file=out)
        if len(changed) > 8:
            print(f"  ... and {len(changed) - 8} more", file=out)
    out.flush()
    return 1 if (args.check and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())