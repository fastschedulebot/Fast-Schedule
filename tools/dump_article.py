#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dump visible text of a help/blog HTML page to stdout-safe file."""
import re
import html as ihtml
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def dump(path):
    t = io.open(path, encoding='utf-8').read()
    m = re.search(r'<main.*?</main>', t, re.S)
    body = m.group(0) if m else t
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    # keep alt text of images out, drop nav chrome: cut everything before first h1
    h1 = re.search(r'<h1[^>]*>', body)
    if h1:
        body = body[h1.start():]
    body = re.sub(r'<[^>]+>', ' ', body)
    body = ihtml.unescape(re.sub(r'[ \t\xa0]+', ' ', body))
    body = re.sub(r'\n\s*\n+', '\n\n', body)
    return body.strip()


if __name__ == '__main__':
    sys.stdout.write(dump(sys.argv[1]))
