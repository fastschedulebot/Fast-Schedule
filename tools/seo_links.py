#!/usr/bin/env python
"""Internal link graph + article-level structured data inspection."""
from __future__ import annotations

import collections
import json
import os
import re

ROOT = "website"


def pages():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in
                   ("_build", "styles", "scripts", "fonts", "img", "images", ".git")]
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.join(base, f).replace(os.sep, "/")[len(ROOT) + 1:])
    return sorted(out)


def main():
    pg = pages()
    pset = set(pg)
    inbound = collections.Counter()
    out_links = collections.Counter()
    from_help = collections.Counter()
    from_blog = collections.Counter()
    for p in pg:
        s = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
        body = re.sub(r"<script\b.*?</script>", " ", s, flags=re.I | re.S)
        body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.I | re.S)
        hrefs = re.findall(r'<a\b[^>]*href="([^"]+)"', body, re.I)
        d = os.path.dirname(p)
        seen = set()
        for h in hrefs:
            if h.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
                continue
            h = h.split("#")[0].split("?")[0]
            if not h:
                continue
            tgt = os.path.normpath(os.path.join(d, h)).replace(os.sep, "/")
            if tgt in ("", "."):
                tgt = "index.html"
            if tgt not in pset:
                continue
            seen.add(tgt)
            out_links[p] += 1
        for t in seen:
            inbound[t] += 1
            if p.startswith("help"):
                from_help[t] += 1
            if p.startswith("blog"):
                from_blog[t] += 1

    orphans = [p for p in pg if inbound[p] == 0 and p != "index.html"]
    print("pages: %d   orphans (0 inbound internal links): %d" % (len(pg), len(orphans)))
    for p in orphans[:25]:
        print("   ", p)
    weak = [(p, inbound[p]) for p in pg if 0 < inbound[p] <= 1]
    print("pages with exactly 1 inbound link: %d" % len(weak))
    for p, n in weak[:10]:
        print("   %d  %s" % (n, p))
    print("\nhelp pages linked from help pages: %d" % len([k for k in from_help if k]))
    print("blog/help articles linked from blog pages: %d" % len([k for k in from_blog if k.startswith(('help/', 'blog/a/'))]))
    print("avg out-links per page: %.1f" % (sum(out_links.values()) / max(1, len(pg))))

    # structured data on a blog article and a help article
    for p in ["blog/a/telegram-channel-mistakes.html", "help/a/formatting.html", "help/c/backup.html"]:
        s = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
        head = s[:s.lower().find("</head>")]
        print("\n== %s ==" % p)
        print("bytes: %d  og:type: %s" % (len(s), (re.search(r'property="og:type"\s+content="([^"]+)"', head) or [None, "-"])[1]))
        print("article:* meta:", re.findall(r'<meta property="(article:[^"]+)" content="([^"]+)"', head))
        print("published/modified:", re.findall(r'"date(Published|Modified)"\s*:\s*"([^"]+)"', head))
        for blob in re.findall(r"<script type=\"application/ld\+json\">(.*?)</script>", head, re.S):
            try:
                d = json.loads(blob)
            except Exception as e:
                print("   BAD JSON-LD:", e, blob[:120])
                continue
            t = d.get("@type")
            print("   JSON-LD @type:", t, "| keys:", sorted(d.keys()))
            if t == "BlogPosting":
                print("      author:", d.get("author"), "| publisher:", (d.get("publisher") or {}).get("name"))
        print("   FAQPage?", "FAQPage" in head, " BreadcrumbList?", "BreadcrumbList" in head)
        print("   h1 count:", len(re.findall(r"<h1\b", s, re.I)), " word count(body):", len(re.findall(r"\b\w+\b", re.sub(r"<[^>]+>", " ", body if False else s))))

    # category hub weight
    for p in ["help/c/backup.html", "help/a/formatting.html"]:
        print("\n%s size: %d bytes" % (p, os.path.getsize(os.path.join(ROOT, p))))


if __name__ == "__main__":
    main()
