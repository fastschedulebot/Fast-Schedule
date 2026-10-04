#!/usr/bin/env python
"""Count structured-data blocks and their byte weight per page."""
from __future__ import annotations

import collections
import json
import os
import re

ROOT = "website"
BLOCK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def _types(d, counter):
    """Count @type, including multi-entity @graph blocks.

    build_site.py emits legal pages as one block holding an @graph of
    WebPage + BreadcrumbList, so a top-level @type lookup reported `None`
    for a page that in fact carried two valid entities.
    """
    if not isinstance(d, dict):
        counter["INVALID"] += 1
        return
    if "@graph" in d:
        for node in d["@graph"]:
            counter[node.get("@type")] += 1
        return
    counter[d.get("@type")] += 1


def scan(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    head_end = s.lower().find("</head>")
    head = s[:head_end] if head_end > 0 else ""
    body = s[head_end:] if head_end > 0 else s
    types_head = collections.Counter()
    types_body = collections.Counter()
    bytes_head = bytes_body = 0
    for blob in BLOCK.findall(head):
        try:
            d = json.loads(blob)
        except Exception:
            types_head["INVALID"] += 1
            continue
        _types(d, types_head)
        bytes_head += len(blob)
    for blob in BLOCK.findall(body):
        try:
            d = json.loads(blob)
        except Exception:
            types_body["INVALID"] += 1
            continue
        _types(d, types_body)
        bytes_body += len(blob)
    return types_head, types_body, bytes_head, bytes_body, len(s)


def main():
    targets = ["index.html", "help.html", "blog/index.html", "help/c/backup.html",
               "help/a/formatting.html", "blog/a/telegram-channel-mistakes.html",
               "legal/privacy.html", "404.html"]
    for t in targets:
        p = os.path.join(ROOT, t)
        if not os.path.exists(p):
            print("%-46s MISSING" % t)
            continue
        th, tb, bh, bb, total = scan(p)
        print("%-46s %7.1f KB | head %s (%d KB) | body %s (%d KB)" % (
            t, total / 1024.0, dict(th), bh // 1024, dict(tb), bb // 1024))

    # how many FAQPage blocks live in body across the site
    agg = collections.Counter()
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in
                   ("_build", "styles", "scripts", "fonts", "img", "images", ".git")]
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = os.path.join(base, f)[len(ROOT) + 1:].replace(os.sep, "/")
            th, tb, bh, bb, total = scan(os.path.join(base, f))
            key = rel.split("/")[0] + ("/" + rel.split("/")[1] if rel.count("/") else "")
            agg[(key, "head")] += sum(th.values())
            agg[(key, "body")] += sum(tb.values())
    print("\n-- JSON-LD block totals by section (head/body) --")
    for k in sorted(set(k[0] for k in agg)):
        print("  %-24s head %5d   body %5d" % (k, agg[(k, "head")], agg[(k, "body")]))


if __name__ == "__main__":
    main()
