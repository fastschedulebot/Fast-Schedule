#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dump EN help article source (title, body HTML, FAQ) for RU translation.

Usage: python tools/dump_en_help.py <aid> [<aid> ...]
Writes tools/ru_work/en_<aid>.txt (UTF-8).
"""
import io
import os
import re
import sys
import html as ihtml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def compact(html):
    html = re.sub(r'\s+', ' ', html)
    html = re.sub(r'>\s+<', '><', html)
    return html.strip()


def dump(aid):
    p = os.path.join(ROOT, 'website', 'help', 'a', aid + '.html')
    t = io.open(p, encoding='utf-8').read()
    out = []
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    title = ihtml.unescape(m.group(1)).strip() if m else aid
    title = re.sub(r'\s*[—–-]\s*Fast Scheduler Help\s*$', '', title)
    out.append('TITLE: ' + title)
    m = re.search(r'<meta name="description" content="(.*?)">', t, re.S)
    if m:
        out.append('DESC: ' + ihtml.unescape(m.group(1)).strip()[:400])
    m = re.search(r'<div class="hc-body">(.*?)</div>\s*(?:<div class="hc-faq"|<div class="hc-cta"|</article>)', t, re.S)
    body = m.group(1).strip() if m else ''
    out.append('BODY-HMTL-LEN: %d' % len(body))
    out.append('BODY:')
    out.append(compact(body))
    faqs = re.findall(r'<details[^>]*><summary>(.*?)</summary>(.*?)</details>', t, re.S)
    out.append('FAQ-COUNT: %d' % len(faqs))
    for q, a in faqs:
        q = ihtml.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', q))).strip()
        links = re.findall(r'href="#/a/([a-z0-9_]+)"', a)
        a = ihtml.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', a))).strip()
        a = re.sub(r'\s*Show more\s*Show less\s*$', '', a).strip()
        out.append('Q: ' + q)
        out.append('A: ' + compact(a)[:2500])
        out.append('LINKS: ' + ' '.join(links))
    # category children chips
    chips = re.findall(r'href="#/a/([a-z0-9_]+)"><span>([^<]+)</span>', t)
    if chips:
        out.append('CHIPS: ' + ' | '.join('%s=%s' % (i, n) for i, n in chips[:14]))
    return '\n'.join(out)


if __name__ == '__main__':
    d = os.path.join(ROOT, 'tools', 'ru_work')
    if not os.path.isdir(d):
        os.makedirs(d)
    for aid in sys.argv[1:]:
        io.open(os.path.join(d, 'en_' + aid + '.txt'), 'w', encoding='utf-8').write(dump(aid))
        print('dumped ' + aid)
