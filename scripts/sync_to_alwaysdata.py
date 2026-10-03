#!/usr/bin/env python3
"""Synchronize the current runtime into the uploadable ``alwaysdata`` bundle.

This never copies .env or runtime data. It is intentionally limited to files
needed by the production launcher; tests, website sources, local databases,
virtual environments, caches, and development tooling stay out of the bundle.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DST = ROOT / "alwaysdata"

SYNC_DIRS = ["src", "translations", "SetDate", "Support Bot"]
SYNC_FILES = ["requirements.txt"]
EXCLUDE_DIR_NAMES = {
    ".git", ".pytest_cache", "__pycache__", "venv", ".venv", "data",
    ".idea", ".vscode", "tests", "test", "website", "docs",
}
EXCLUDE_FILE_NAMES = {
    "token_manager.json", "token_manager.json.migrated", "missing_setdate.txt",
    "bot_database.json", "user_languages.json", "saved_times.json",
    "missing_admin.txt", "admin_texts.json.deprecated",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".log", ".db", ".sqlite", ".sqlite3"}


def should_exclude(path: pathlib.Path) -> bool:
    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return True
    if path.name in EXCLUDE_FILE_NAMES:
        return True
    return path.suffix.lower() in EXCLUDE_SUFFIXES


def collect_sources() -> list[pathlib.Path]:
    items: list[pathlib.Path] = []
    for directory in SYNC_DIRS:
        source = ROOT / directory
        if not source.is_dir():
            continue
        for path in source.rglob("*"):
            if path.is_file() and not should_exclude(path.relative_to(ROOT)):
                items.append(path.relative_to(ROOT))
    for filename in SYNC_FILES:
        path = ROOT / filename
        if path.is_file():
            items.append(path.relative_to(ROOT))
    return sorted(set(items))


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync runtime sources into alwaysdata/")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    DST.mkdir(parents=True, exist_ok=True)

    items = collect_sources()
    mismatches: list[str] = []
    for relative in items:
        source = ROOT / relative
        target = DST / relative
        if args.check:
            if not target.is_file():
                mismatches.append(f"MISSING {relative}")
            elif digest(source) != digest(target):
                mismatches.append(f"DIFF {relative}")
        elif args.dry_run:
            print(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            print(f"copied {relative}")

    if args.check:
        if mismatches:
            print("Bundle is out of sync:", file=sys.stderr)
            print("\n".join(mismatches), file=sys.stderr)
            return 2
        print(f"OK — {len(items)} runtime files are synchronized.")
    elif not args.dry_run:
        print(f"Done — {len(items)} runtime files synchronized into {DST}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
