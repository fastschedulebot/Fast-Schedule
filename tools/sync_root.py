"""Sync the repo-root deploy tree (what GitHub Pages serves) from website/.

Copies every differing + website-only file for the published paths.
Keeps root-only files (dev .py in scripts/, etc.). Removes the stale
pruned article root/help/a/channel_default.html.
"""
import os
import shutil

PUB = ['index.html', 'help.html', '404.html', 'robots.txt', 'sitemap.xml',
       'llms.txt', 'llms-full.txt', 'blog', 'help', 'legal', 'scripts',
       'styles', 'fonts', 'apple-touch-icon.png', 'og-cover.png',
       'storage_state.json', '_headers', 'google7ebfb86d3a3c2fa9.html']
SKIP_DIRS = {'_build', '__pycache__'}
PRUNE = [os.path.join('help', 'a', 'channel_default.html')]

copied = removed = 0


def sync_file(src, dst):
    global copied
    with open(src, 'rb') as f:
        data = f.read()
    if os.path.isfile(dst):
        with open(dst, 'rb') as f:
            if f.read() == data:
                return
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    with open(dst, 'wb') as f:
        f.write(data)
    copied += 1


for top in PUB:
    src = os.path.join('website', top)
    if os.path.isfile(src):
        sync_file(src, top)
    elif os.path.isdir(src):
        for dp, dn, fn in os.walk(src):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in fn:
                s = os.path.join(dp, f)
                d = os.path.relpath(s, 'website')
                sync_file(s, d)

for p in PRUNE:
    if os.path.isfile(p):
        os.remove(p)
        removed += 1
        print('pruned', p)

print('copied/updated: %d  removed: %d' % (copied, removed))
