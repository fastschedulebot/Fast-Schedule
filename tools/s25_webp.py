"""Convert blog cover JPGs to WebP (q82) + point builders at .webp.

Kept as-is (with reasons): SVG covers (vector, already optimal),
og-cover-v2.png (social scrapers don't accept webp), apple-touch-icon.png
(Apple requires PNG), videos/* (production sources, not served).
"""
import glob
import io
import os
from PIL import Image

total_old = total_new = n = 0
for d in ('blog/img', 'website/blog/img'):
    for src in sorted(glob.glob(os.path.join(d, '*.jpg'))):
        dst = src[:-4] + '.webp'
        im = Image.open(src).convert('RGB')
        im.save(dst, 'WEBP', quality=82, method=6)
        # verify output decodes
        Image.open(dst).verify()
        o, w = os.path.getsize(src), os.path.getsize(dst)
        total_old += o
        total_new += w
        n += 1
        print('%-60s %7.0fK -> %7.0fK' % (os.path.basename(src), o / 1024, w / 1024))
print('files: %d  total %.1fM -> %.1fM  (saved %.0f%%)' % (
    n, total_old / 2**20, total_new / 2**20,
    100 * (1 - total_new / total_old)))

# ---------- builder refs ----------
p = 'website/_build/build_blog.py'
s = io.open(p, encoding='utf-8', newline='').read()
subs = [
    ('"""<id>.jpg when the photo exists in blog/img, else the generated SVG."""',
     '"""<id>.webp when the photo exists in blog/img, else the generated SVG."""'),
    ("p = os.path.join(BLOG_DIR, 'img', a['id'] + '.jpg')",
     "p = os.path.join(BLOG_DIR, 'img', a['id'] + '.webp')"),
    ("return ('img/%s.jpg' % a['id']) if os.path.isfile(p)",
     "return ('img/%s.webp' % a['id']) if os.path.isfile(p)"),
    ("'image': f'{SITE}/blog/img/{a[\"id\"]}.jpg',",
     "'image': f'{SITE}/blog/img/{a[\"id\"]}.webp',"),
    ("'image': f'{SITE}/blog/img/{art[\"id\"]}.jpg',",
     "'image': f'{SITE}/blog/img/{art[\"id\"]}.webp',"),
    ("<img src=\"../img/{art['id']}.jpg\"",
     "<img src=\"../img/{art['id']}.webp\""),
]
for old, new in subs:
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('[ok] builder refs -> .webp')
