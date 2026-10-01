# -*- coding: utf-8 -*-
"""One-shot hook installer: blog_extras.py deep-dives merge at load time
into build_blog.py's ARTICLES (before reading time / search index / pages)."""
import io

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()
old = ("# Combined article list (source order = display order on the hub).\n"
       "ARTICLES = BLOG_ARTICLES + BLOG_ARTICLES_B + BLOG_ARTICLES_C + BLOG_ARTICLES_D\n")
new = old + """
# Optional per-article deep-dive sections (blog_extras.py). Merging happens
# HERE, at load time, so reading time, search indexing, JSON-LD articleBody,
# the TOC and the rendered page all automatically see the expanded content.
try:
    from blog_extras import EXTRA_SECTIONS, CONTENT_OVERRIDES
except ImportError:  # extras are optional
    EXTRA_SECTIONS, CONTENT_OVERRIDES = {}, {}
for _art in ARTICLES:
    if _art['id'] in CONTENT_OVERRIDES:
        _art['content'] = CONTENT_OVERRIDES[_art['id']]
    _x = EXTRA_SECTIONS.get(_art['id'])
    if _x:
        _art['content'] = _art['content'] + _x
"""
assert old in s and 'blog_extras' not in s
s = s.replace(old, new, 1)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] blog_extras hook installed')
