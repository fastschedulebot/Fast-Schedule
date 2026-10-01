# -*- coding: utf-8 -*-
"""Regenerates _hc_component_css.txt: the shared .hc-* component CSS that the
STATIC help pages (help/a, help/c) need but main.css doesn't define.

help.html styles its components with an inline <style>; build_static.py emits
static article/hub pages with the same markup but only main.css + hotkeys CSS,
so without this file those pages render with giant unsized SVG icons and
unstyled cards/chips/FAQ/pager.

Run whenever help.html's inline CSS changes, then re-run build_static.py:
    python website/_build/extract_hc_css.py
    python website/_build/build_static.py
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
HELP_HTML = os.path.join(os.path.dirname(HERE), 'help.html')
OUT = os.path.join(HERE, '_hc_component_css.txt')

# Components the static pages actually render.
COMPONENT = re.compile(
    r'\.(hc-crumbs|hc-chips|hc-chiprow|hc-chip|hc-related|hc-pager|hc-faq|hc-fa'
    r'|hc-cta|hc-body|hc-card|hc-try)\b')


def parse_rules(text):
    """Yield (selector, body) for each top-level rule of a CSS fragment."""
    rules = []
    p, n = 0, len(text)
    while p < n:
        m = re.match(r'\s+', text[p:])
        if m:
            p += m.end()
            continue
        m = re.match(r'/\*.*?\*/', text[p:], re.S)
        if m:
            p += m.end()
            continue
        brace = text.find('{', p)
        if brace == -1:
            break
        sel = text[p:brace].strip()
        depth, k = 1, brace + 1
        while k < n and depth:
            if text[k] == '{':
                depth += 1
            elif text[k] == '}':
                depth -= 1
            k += 1
        rules.append((sel, text[brace + 1:k - 1]))
        p = k
    return rules


def main():
    with io.open(HELP_HTML, encoding='utf-8') as f:
        html = f.read()
    css = re.findall(r'<style>(.*?)</style>', html, re.S)[0]

    emitted_rules, emitted_media = [], []
    for sel, body in parse_rules(css):
        if sel.startswith('@media') or sel.startswith('@supports'):
            keep = [(s2, b2.strip()) for s2, b2 in parse_rules(body)
                    if COMPONENT.search(s2)]
            if keep:
                parts = []
                for s2, b2 in keep:
                    b2 = b2.strip()
                    if '\n' in b2:
                        parts.append('  %s {\n    %s\n  }' % (s2, b2.replace('\n   ', '\n  ')))
                    else:
                        parts.append('  %s { %s }' % (s2, b2))
                emitted_media.append('%s {\n%s\n}' % (sel, '\n\n'.join(parts)))
        elif COMPONENT.search(sel):
            b = body.strip()
            if '\n' in b or len(b) >= 700:
                emitted_rules.append('%s {\n  %s\n}' % (sel, b.replace('\n   ', '\n  ')))
            else:
                emitted_rules.append('%s { %s }' % (sel, b))

    css2 = '\n\n'.join(emitted_rules + emitted_media)

    # Drop rules scoped to help.html's interactive shell that static pages lack.
    blocks = re.split(r'\n\n+', css2)
    out = []
    for b in blocks:
        sel = b.split('{')[0].strip()
        if '.hc-content' in sel:                        # help.html shell only
            continue
        if '.hc-try' in sel and '.hc-chip' not in b:    # search-page chips
            continue
        if sel.startswith('header.site, footer.site'):  # print/noscript hide-all
            continue
        out.append(b)
    css2 = '\n\n'.join(out)
    css2 = re.sub(r'^     ', '  ', css2, flags=re.M)

    assert css2.count('{') == css2.count('}'), 'unbalanced braces'
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(css2)
    print('[ok] %s (%d chars)' % (OUT, len(css2)))


if __name__ == '__main__':
    main()
