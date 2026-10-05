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

Touches the generated pages, the build sources that emit them, and the
publish/sync tooling, so a rebuild does not reintroduce the old filename.
Both _build trees are covered: _build/ at the repo root is the tracked one,
website/_build/ is the working copy, and they must not drift apart.

tools/sync_root.py and tools/sync_audit.py matter as much as the HTML. They
carry an explicit publish list of the files GitHub Pages serves, and leaving
og-cover.png there meant the new card was never copied to the deploy tree
while the stale clipped one kept being served.

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

OLD = "og-cover.png"
NEW = "og-cover-v2.png"

# This file names OLD on purpose, and make_og_image.mjs explains the old
# generator in prose. Rewriting either would break the tool or falsify a
# comment.
SELF = Path(__file__).resolve()
SKIP = {SELF, ROOT / "tools" / "make_og_image.mjs"}


def targets() -> list[Path]:
    out: list[Path] = []
    for pattern in ("*.html", "*/*.html", "*/*/*.html", "*/*/*/*.html"):
        out.extend(WEBSITE.glob(pattern))
    for build in (ROOT / "_build", WEBSITE / "_build"):
        if build.is_dir():
            out.extend(sorted(build.glob("*.py")))
            out.extend(sorted(build.glob("*.txt")))
    # Tools that write the filename into pages: the RU build, the idempotent
    # patch scripts that seed the build sources, and the publish/audit lists.
    out.extend(sorted((ROOT / "tools").glob("*.py")))
    return sorted({p for p in out if p.is_file() and p.resolve() not in SKIP})


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