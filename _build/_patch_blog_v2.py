# -*- coding: utf-8 -*-
"""One-shot patch (2026-09-26, session 2): real-photo covers + full-page
bento layout + Premium & Safety category (blog_articles_d.py).

Run:  python _patch_blog_v2.py
"""
import io

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()
n0 = s

# 1) new article source (blog_articles_d.py) -------------------------------
s = s.replace(
    "from blog_articles_c import BLOG_ARTICLES_C  # noqa: E402\n",
    "from blog_articles_c import BLOG_ARTICLES_C  # noqa: E402\n"
    "from blog_articles_d import BLOG_ARTICLES_D  # noqa: E402\n", 1)
s = s.replace(
    "ARTICLES = BLOG_ARTICLES + BLOG_ARTICLES_B + BLOG_ARTICLES_C\n",
    "ARTICLES = BLOG_ARTICLES + BLOG_ARTICLES_B + BLOG_ARTICLES_C + BLOG_ARTICLES_D\n", 1)

# 2) Premium & Safety category --------------------------------------------
s = s.replace(
    "    'money':    {'title': 'Monetization',",
    "    'premium':  {'title': 'Premium & Safety', 'desc': 'Verification, Premium perks, Mini Apps — the platform layer behind channels.'},\n"
    "    'money':    {'title': 'Monetization',", 1)
s = s.replace(
    "CAT_ICON = {'growth': 'gauge', 'content': 'book',\n"
    "            'tools': 'bot',\n"
    "            'platform': 'globe', 'money': 'crown'}",
    "CAT_ICON = {'growth': 'gauge', 'content': 'book',\n"
    "            'tools': 'bot',\n"
    "            'premium': 'shield', 'platform': 'globe', 'money': 'crown'}", 1)
s = s.replace(
    "    'platform': ('#4aa9c9', '#275a6e'),",
    "    'premium':  ('#9b6ef3', '#5a3b96'),\n"
    "    'platform': ('#4aa9c9', '#275a6e'),", 1)

# 3) real-photo covers (jpg with svg fallback) ------------------------------
s = s.replace(
    "def cover_svg(art):",
    "# Real photo covers, downloaded from Unsplash (royalty-free) into blog/img/\n"
    "# at build time. Fallback: the generated SVG gradient, so builds never break\n"
    "# when a photo is missing.\n"
    "\n"
    "def cover_url(a):\n"
    "    \"\"\"<id>.jpg when the photo exists in blog/img, else the generated SVG.\"\"\"\n"
    "    p = os.path.join(BLOG_DIR, 'img', a['id'] + '.jpg')\n"
    "    return ('img/%s.jpg' % a['id']) if os.path.isfile(p) \\\n"
    "        else ('img/%s.svg' % a['id'])\n"
    "\n"
    "\n"
    "def cover_svg(art):", 1)
s = s.replace(
    "f'<span class=\"bcard-cover\"><img src=\"img/{bh.esc(a[\"id\"])}.svg\" alt=\"\" '\n"
    "            f'width=\"800\" height=\"450\" loading=\"lazy\"></span>'",
    "f'<span class=\"bcard-cover\"><img src=\"{bh.esc(cover_url(a))}\" alt=\"\" '\n"
    "            f'width=\"900\" height=\"506\" loading=\"lazy\"></span>'", 1)
s = s.replace("'image': f'{SITE}/blog/img/{a[\"id\"]}.svg',",
              "'image': f'{SITE}/blog/img/{a[\"id\"]}.jpg',", 1)
s = s.replace("'image': f'{SITE}/blog/img/{art[\"id\"]}.svg',",
              "'image': f'{SITE}/blog/img/{art[\"id\"]}.jpg',", 1)

# 4) full-page width layout -------------------------------------------------
s = s.replace(".blog-wrap { max-width: 860px; margin: 0 auto; padding: 26px 20px 40px; }",
              ".blog-wrap { max-width: 1240px; margin: 0 auto; padding: 26px 28px 40px; }", 1)
s = s.replace(".bcard-cover img { display: block; width: 100%; height: 100%; object-fit: cover; }",
              ".bcard-cover img { display: block; width: 100%; height: 100%; object-fit: cover;\n"
              "      transition: transform .35s ease; }\n"
              "    .bcard:hover .bcard-cover img { transform: scale(1.04); }", 1)
s = s.replace("@media (max-width: 1100px) { .bento { grid-template-columns: repeat(2, 1fr); } }",
              "@media (max-width: 1100px) { .bento { grid-template-columns: repeat(3, 1fr); } }\n"
              "    @media (max-width: 940px) { .bento { grid-template-columns: repeat(2, 1fr); } }", 1)

# 5) hero image --------------------------------------------------------------
s = s.replace(
    "  <div class=\"blog-chips\">{chips}</div>\n  {''.join(secs)}",
    "  <div class=\"blog-chips\">{chips}</div>\n"
    "  <figure class=\"blog-hero-img\"><img src=\"img/hero.jpg\" "
    "alt=\"Workspace with a phone showing a Telegram channel\" width=\"1600\" height=\"600\" "
    "loading=\"eager\"></figure>\n  {''.join(secs)}", 1)
s = s.replace(
    "    .blog-hero h1 { font-size: clamp(1.8rem, 4.5vw, 2.6rem); margin: 0 0 10px; letter-spacing: -.03em; color: var(--text); }",
    "    .blog-hero h1 { font-size: clamp(1.8rem, 4.5vw, 2.6rem); margin: 0 0 10px; letter-spacing: -.03em; color: var(--text); }\n"
    "    .blog-hero-img { margin: 18px 0 4px; border-radius: 18px; overflow: hidden;\n"
    "      border: 1px solid var(--border); box-shadow: var(--shadow-sm); }\n"
    "    .blog-hero-img img { display: block; width: 100%; height: clamp(180px, 26vw, 300px);\n"
    "      object-fit: cover; }", 1)

# 6) hub topic order ----------------------------------------------------------
s = s.replace("order = ('growth', 'content', 'tools', 'platform', 'money')",
              "order = ('growth', 'content', 'tools', 'premium', 'platform', 'money')", 1)

assert s != n0, 'nothing replaced'
changed = sum(1 for a, b in zip(n0.split('\n'), s.split('\n')) if a != b)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print(f'[ok] patched build_blog.py ({changed} lines changed)')
