"""Repair mangled script tags + wire ru-chrome.js correctly site-wide."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_V = '20261002b1'

broken_re = re.compile(r'<script[^>]*?src="[^"]*?ru-chrome\.js\?v=[^"]*"[^>]*?>\s*')
lang_re = re.compile(r'<script([^>]*?)src="([^"]*?)(?:scripts/)?s?lang\.js\?v=[^"]*"([^>]*?)>')
files = 0
tags = 0

for dirpath, _dirs, filenames in os.walk(ROOT):
    if '_build' in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dirpath, fn)
        s = open(p, encoding='utf-8').read()
        orig = s
        s = broken_re.sub('', s)

        def repl(m):
            global tags
            pre, src, post = m.group(1), m.group(2), m.group(3)
            # src is the path before 'scripts/lang.js' with 'scripts/' possibly
            # mangled to a bare 's' (or fully present). Normalize to '...scripts/'.
            if src.endswith('scripts/'):
                prefix = src
            else:
                prefix = re.sub(r's$', 'scripts/', src)
                if not prefix.endswith('scripts/'):
                    prefix = src + 'scripts/'
            tags += 1
            return ('<script' + pre + 'src="' + prefix + 'ru-chrome.js?v=' + LANG_V + '"' + post + '>'
                    '<script' + pre + 'src="' + prefix + 'lang.js?v=' + LANG_V + '"' + post + '>')

        s = lang_re.sub(repl, s)
        if s != orig:
            open(p, 'w', encoding='utf-8').write(s)
            files += 1

print('files updated:', files, '| lang tags wired:', tags)
