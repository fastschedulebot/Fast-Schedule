#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract verifiable claims from help/blog HTML for accuracy audit.

Usage:
  python tools/audit_claims.py commands  -> all unique /command tokens per file
  python tools/audit_claims.py paths     -> all unique A -> B menu paths
  python tools/audit_claims.py numbers   -> all unique money/limit figures
Writes UTF-8 safe output to stdout (wrapped) — caller redirects to file.
"""
import io
import os
import re
import sys
import html as ihtml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pages():
    out = []
    for sub in ('website/help', 'website/ru/help', 'website/blog', 'website/ru/blog'):
        base = os.path.join(ROOT, sub)
        if not os.path.isdir(base):
            continue
        for dp, dn, fn in os.walk(base):
            for f in fn:
                if f.endswith('.html'):
                    out.append(os.path.join(dp, f))
    return sorted(out)


def text_of(path):
    t = io.open(path, encoding='utf-8').read()
    m = re.search(r'<main.*?</main>', t, re.S)
    body = m.group(0) if m else t
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    h1 = re.search(r'<h1[^>]*>', body)
    if h1:
        body = body[h1.start():]
    body = re.sub(r'<[^>]+>', ' ', body)
    body = ihtml.unescape(re.sub(r'[ \t\xa0]+', ' ', body))
    return re.sub(r'\n\s*\n+', '\n', body).strip()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'commands'
    seen = {}
    for p in pages():
        try:
            txt = text_of(p)
        except Exception:
            continue
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        if mode == 'commands':
            toks = set(re.findall(r'(?<!\w)/[a-zA-Z][a-zA-Z0-9_]{1,30}', txt))
        elif mode == 'paths':
            toks = set(re.findall(r'[\w\U0001F300-\U0001FAFF][\w .()\U0001F300-\U0001FAFF-]{1,40}\s*(?:→|->|›)\s*[\w\U0001F300-\U0001FAFF][\w .()\U0001F300-\U0001FAFF-]{1,40}', txt))
        elif mode == 'numbers':
            toks = set(re.findall(r'\$[\d.,]+\b|\b\d+\s?(?:USD|Stars|XTR)\b|\b\d{2,}\s?(?:messages|posts|channels|bots|members|days|months|MB|GB)\b', txt))
        else:
            toks = set()
        for t_ in toks:
            seen.setdefault(t_, []).append(rel)
    for tok in sorted(seen):
        files = seen[tok]
        sys.stdout.write('%s  [%d: %s]\n' % (tok, len(files), ', '.join(files[:6])))


if __name__ == '__main__':
    main()
