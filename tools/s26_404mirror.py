"""build_static: also write a portable root 404.html mirror.

website/404.html uses root-absolute asset paths (correct: a 404 can be
served from any path). The repo-root copy is the portable mirror (like
index.html): same markup with relative paths so it renders styled both
from file:// and when the repo root itself is served.
"""
import io

p = 'website/_build/build_static.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = """    nav404 = bh.unified_nav('', bh.BOT_URL + '?start=start__website_404', _menu404)
    io.open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8', newline='\\n').write(
        f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
{NOFLASH}
{head404}
</head>
<body>
{nav404}
<main class="legal">{body404}</main>
<script src="/scripts/theme.js?v=20260930a1"></script>
<script src="/scripts/settings.js?v=20261002c3"></script>
  <script src="/scripts/lang.js?v=20261001a1"></script>
<script src="/scripts/hotkeys.js?v=20260930a2"></script>
<script src="/scripts/hotkeys-modal.js?v=20260930a2"></script>
</body>
</html>''')"""
assert s.count(old) == 1, s.count(old)
new = """    nav404 = bh.unified_nav('', bh.BOT_URL + '?start=start__website_404', _menu404)
    page404 = (
        f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
{NOFLASH}
{head404}
</head>
<body>
{nav404}
<main class="legal">{body404}</main>
<script src="/scripts/theme.js?v=20260930a1"></script>
<script src="/scripts/settings.js?v=20261002c3"></script>
  <script src="/scripts/lang.js?v=20261001a1"></script>
<script src="/scripts/hotkeys.js?v=20260930a2"></script>
<script src="/scripts/hotkeys-modal.js?v=20260930a2"></script>
</body>
</html>''')
    io.open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8', newline='\\n').write(page404)
    # portable root mirror (like index.html): relative asset paths so the
    # page renders styled from file:// and from a repo-root deploy
    root404 = page404.replace('href="/', 'href="./').replace('src="/', 'src="./')
    io.open(os.path.join(os.path.dirname(OUT), '404.html'), 'w',
            encoding='utf-8', newline='\\n').write(root404)"""
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('[ok]', p)
