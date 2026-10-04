#!/usr/bin/env python
"""Measure how much of the static site text the RU translation maps cover.

Reads the browser-side maps the site already ships (ru-content.js long-form
content + ru-chrome.js chrome strings), walks every text node of a page the
same way lang.js does, and reports what fraction would end up translated.

Usage:  python tools/ru_coverage.py [--root website] [--sample N] [--page P]
"""
from __future__ import annotations

import argparse
import collections
import html as html_mod
import json
import os
import re

JS_ASSIGN = re.compile(r"(?:window\.)?(FS_[A-Z_]+)\s*=\s*(\{.*?\})\s*;", re.S)


def load_maps(root: str):
    """Merge every JS translation map the site ships into one dict."""
    merged = {}
    origin = {}
    scripts = os.path.join(root, "scripts")
    for f in sorted(os.listdir(scripts)):
        if not f.endswith(".js"):
            continue
        s = open(os.path.join(scripts, f), encoding="utf-8", errors="replace").read()
        for name, blob in JS_ASSIGN.findall(s):
            try:
                d = json.loads(blob)
            except Exception:
                continue
            if not isinstance(d, dict):
                continue
            for k, v in d.items():
                if isinstance(v, str) and k not in merged:
                    merged[k] = v
                    origin[k] = name
    return merged, origin


def iter_text_nodes(page_html: str):
    """Yield (text, in_script_or_style) for every text node, like lang.js."""
    body = re.sub(r"<script\b.*?</script>", " ", page_html, flags=re.I | re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.I | re.S)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    for m in re.finditer(r">([^<>]+)<", body):
        yield m.group(1)


SKIP = re.compile(r"^[\s\d\W_]*$")


def coverage(page_html: str, maps: dict):
    total = hit = chars = cchars = 0
    misses = []
    for raw in iter_text_nodes(page_html):
        t = raw.strip()
        if not t or SKIP.match(t):
            continue
        total += 1
        chars += len(t)
        if t in maps:
            hit += 1
            cchars += len(t)
        elif len(t) > 40 and len(misses) < 8:
            misses.append(t)
    return total, hit, chars, cchars, misses


def section(rel: str) -> str:
    """Group a repo-relative page path into a reportable section."""
    parts = rel.replace(os.sep, "/").split("/")
    if len(parts) == 1:
        return "root"
    if parts[1] in ("help", "blog") and len(parts) > 2:
        return parts[1] + "/" + parts[2]
    return parts[1]


def by_section(root: str, maps: dict):
    buckets = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in
                   ("_build", "styles", "scripts", "fonts", "img", "images", ".git")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(base, f)
            s = open(p, encoding="utf-8", errors="replace").read()
            t, h, c, cc, _ = coverage(s, maps)
            b = buckets[section(os.path.relpath(p, root))]
            b[0] += t; b[1] += h; b[2] += c; b[3] += cc; b[4] += 1
    print("\n-- by section --")
    print("%-24s %5s %8s %7s %10s %7s" % ("section", "pages", "nodes", "mapped", "chars", "mapped"))
    for k in sorted(buckets):
        t, h, c, cc, n = buckets[k]
        print("%-24s %5d %8d %6.1f%% %10d %6.1f%%" % (
            k, n, t, 100.0 * h / max(1, t), c, 100.0 * cc / max(1, c)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="website")
    ap.add_argument("--sample", type=int, default=40)
    ap.add_argument("--page")
    ap.add_argument("--by-dir", action="store_true",
                    help="coverage per site section over EVERY page")
    a = ap.parse_args()
    maps, origin = load_maps(a.root)
    print("merged map entries: %d from %s" % (
        len(maps), dict(collections.Counter(origin.values()))))
    if a.by_dir:
        by_section(a.root, maps)
        return

    pages = []
    if a.page:
        pages = [a.page]
    else:
        for base, dirs, files in os.walk(a.root):
            dirs[:] = [d for d in dirs if d not in
                       ("_build", "styles", "scripts", "fonts", "img", "images", ".git")]
            for f in files:
                if f.endswith(".html"):
                    pages.append(os.path.join(base, f))
        pages.sort()
        step = max(1, len(pages) // a.sample)
        pages = pages[::step][:a.sample]

    tt = th = tc = cc = 0
    worst = []
    for p in pages:
        s = open(p, encoding="utf-8", errors="replace").read()
        t, h, c, cc2, misses = coverage(s, maps)
        tt += t; th += h; tc += c; cc += cc2
        pct = 100.0 * h / t if t else 0.0
        worst.append((pct, p, misses))
    worst.sort()
    print("\nsampled %d pages" % len(pages))
    print("text nodes: %d, mapped: %d (%.1f%%)" % (tt, th, 100.0 * th / max(1, tt)))
    print("characters: %d, mapped: %d (%.1f%%)" % (tc, cc, 100.0 * cc / max(1, tc)))
    print("\nlowest coverage pages:")
    for pct, p, misses in worst[:6]:
        print("  %5.1f%%  %s" % (pct, p))
        for m in misses[:3]:
            print("        miss: %s" % m[:90])
    for pct, p, misses in worst[-3:]:
        print("  %5.1f%%  %s" % (pct, p))


if __name__ == "__main__":
    main()
