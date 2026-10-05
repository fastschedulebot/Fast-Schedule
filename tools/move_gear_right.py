#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move the settings gear to the right of the Open Bot CTA (one-shot).

The unified navbar used to park the gear in .nav-left next to the brand;
the gear now trails the CTA as the last item of .nav-right on every page
(see unified_nav in website/_build/build_help.py). Regenerating all ~670
pages would rewrite a thousand unrelated bytes, so this performs the same
pure move in place: the <span class="settings-wrap">…</span> block (button
+ whole glass-pop menu) is lifted out of .nav-left and re-inserted directly
after the CTA's closing </a>.

    python tools/move_gear_right.py [--check]

--check reports what would change without writing.
"""
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'website')

GEAR_OPEN = '<span class="settings-wrap">'
TAG_RE = re.compile(r'<span[\s>]|</span>')
CTA_RE = re.compile(r'<a\s[^>]*class="[^"]*\bnav-cta\b[^"]*"[^>]*>')


def read(rel):
    with io.open(os.path.join(ROOT, rel), 'r', encoding='utf-8', newline='') as f:
        return f.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    for attempt in range(8):
        try:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            return
        except OSError:
            if attempt == 7:
                raise
            time.sleep(0.2 * (attempt + 1))


def span_end(txt, start):
    """Index just past the </span> balancing the <span> at `start`."""
    depth = 0
    for m in TAG_RE.finditer(txt, start):
        if m.group(0) == '</span>':
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            return m.end()
    return -1


def move(txt):
    """Return (new_txt, status) where status is moved/already/no-nav."""
    # Scope to the page header: in-content CTAs elsewhere must not match.
    i_head = txt.find('<header')
    i_head_end = txt.find('</header>', i_head) if i_head != -1 else -1
    if i_head == -1 or i_head_end == -1:
        return txt, 'no-nav'
    head = txt[i_head:i_head_end]
    i_gear = head.find(GEAR_OPEN)
    m_cta = CTA_RE.search(head)
    if i_gear == -1 or not m_cta:
        return txt, 'no-nav'
    # Work in header-local coordinates, translate back at the end.
    i_gear += i_head
    i_gear_end = span_end(txt, i_gear)
    m_cta = CTA_RE.search(txt, i_head, i_head_end)
    i_cta_close = txt.find('</a>', m_cta.end())
    if i_cta_close == -1 or i_cta_close > i_head_end:
        return txt, 'no-nav'
    i_cta_close += len('</a>')
    if i_gear > i_cta_close:
        return txt, 'already'
    if i_gear_end == -1 or i_gear_end > m_cta.start():
        return txt, 'no-nav'
    gear = txt[i_gear:i_gear_end]
    if gear.count('id="settingsBtn"') != 1 or gear.count('id="settingsMenu"') != 1:
        return txt, 'no-nav'
    txt = txt[:i_gear] + txt[i_gear_end:]
    # indices shifted left by the removal; re-locate the CTA close.
    m_cta = CTA_RE.search(txt)
    i_cta_close = txt.find('</a>', m_cta.end()) + len('</a>')
    txt = txt[:i_cta_close] + gear + txt[i_cta_close:]
    return txt, 'moved'


def main():
    check = '--check' in sys.argv[1:]
    moved = already = nonav = 0
    problems = []
    for dirpath, dirs, files in os.walk(WEB):
        if '_build' in dirpath.split(os.sep) or '__pycache__' in dirs:
            dirs[:] = [d for d in dirs if d != '__pycache__']
        for fn in files:
            if not fn.endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            before = read(rel)
            after, status = move(before)
            if status == 'moved':
                moved += 1
                if not check:
                    write(rel, after)
            elif status == 'already':
                already += 1
            else:
                nonav += 1
                problems.append(rel)
    print('moved=%d already-right=%d no-unified-nav=%d' % (moved, already, nonav))
    for rel in problems[:20]:
        print('  no-nav: %s' % rel)
    return 0


if __name__ == '__main__':
    sys.exit(main())
