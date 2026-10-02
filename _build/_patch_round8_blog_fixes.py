# One-off patch: blog polish round 8.
# 1. Search view on the blog hub hides the hub topic chips (they used to
#    duplicate the results filter row) and results scroll into view.
# 2. Stray hashes (e.g. stale #q=) no longer leave a half-searched page.
# 3. "Keep reading" chips on article pages link only to other blog posts —
#    no help-center articles in the blog.
# 4. Article-count strings ("67 in-depth guides across 6 topics",
#    "Search all 60 articles", "67 long-form articles") removed.
import glob
import io
import re

ROOT = r"C:\Users\MAX\TG Bots\1Fast Schedule & SetDate\website"


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


changed = []

# ---------- 1+2+4: hub page JS and copy ----------
hub = ROOT + r"\blog\index.html"
s = read(hub)
orig = s

s = s.replace(
    "    chips.forEach(function (c) { c.classList.remove('on'); });\n"
    "    bar.style.display = 'none';\n",
    "    chips.forEach(function (c) { c.classList.remove('on'); });\n"
    "    chips.forEach(function (c) { c.style.display = 'none'; });\n"
    "    bar.style.display = 'none';\n", 1)
s = s.replace(
    "    view.hidden = false;\n    title.textContent = 'Search results';",
    "    view.hidden = false;\n    view.scrollIntoView();\n"
    "    title.textContent = 'Search results';", 1)
s = s.replace(
    "  function showHub() {\n    view.hidden = true;\n    bar.style.display = '';\n    secs.forEach",
    "  function showHub() {\n    view.hidden = true;\n    bar.style.display = '';\n"
    "    chips.forEach(function (c) { c.style.display = ''; });\n    secs.forEach", 1)
s = s.replace(
    "  window.addEventListener('hashchange', function () { applyHash(); });\n  applyHash();",
    "  window.addEventListener('hashchange', function () { applyHash(); });\n"
    "  if (!applyHash()) {\n"
    "    /* a stray hash (or leftover #q= after navigating back) shouldn't leave a\n"
    "       broken half-searched page: restore the plain hub view */\n"
    "    q.value = '';\n    showHub();\n"
    "    chips.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-cat') === 'all'); });\n"
    "  }", 1)
s = s.replace(
    'placeholder="Search all 60 articles — titles, topics, tools…"',
    'placeholder="Search the blog — titles, topics, tools…"')
s = s.replace(
    "67 long-form articles from the Fast Scheduler team.",
    "New guides from the Fast Scheduler team.")

assert s != orig, "hub unchanged"
if s != orig:
    write(hub, s)
    changed.append(hub)

# ---------- 3: article pages — drop help-center chips ----------
n_chips = 0
help_re = re.compile(
    r'<a class="hc-chip" href="\.\./\.\./help/a/[^"]*">.*?</a>', re.S)
for p in glob.glob(ROOT + r"\blog\a\*.html"):
    s = read(p)
    s2, n = help_re.subn("", s)
    if n:
        write(p, s2)
        changed.append(p)
        n_chips += n

# ---------- build script: keep future rebuilds consistent ----------
bb = ROOT + r"\_build\build_blog.py"
s = read(bb)
orig = s

s = s.replace(
    "    chips.forEach(function (c) { c.classList.remove('on'); });\n"
    "    bar.style.display = 'none';\n",
    "    chips.forEach(function (c) { c.classList.remove('on'); });\n"
    "    chips.forEach(function (c) { c.style.display = 'none'; });\n"
    "    bar.style.display = 'none';\n", 1)
s = s.replace(
    "    view.hidden = false;\n    title.textContent = 'Search results';",
    "    view.hidden = false;\n    view.scrollIntoView();\n"
    "    title.textContent = 'Search results';", 1)
s = s.replace(
    "  function showHub() {\n    view.hidden = true;\n    bar.style.display = '';\n    secs.forEach",
    "  function showHub() {\n    view.hidden = true;\n    bar.style.display = '';\n"
    "    chips.forEach(function (c) { c.style.display = ''; });\n    secs.forEach", 1)
s = s.replace(
    "  window.addEventListener('hashchange', function () { applyHash(); });\n  applyHash();",
    "  window.addEventListener('hashchange', function () { applyHash(); });\n"
    "  if (!applyHash()) {\n"
    "    /* a stray hash (or leftover #q= after navigating back) shouldn't leave a\n"
    "       broken half-searched page: restore the plain hub view */\n"
    "    q.value = '';\n    showHub();\n"
    "    chips.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-cat') === 'all'); });\n"
    "  }", 1)
s = s.replace(
    "'<input id=\"blog-q\" type=\"search\" placeholder=\"Search all 60 articles — titles, topics, tools…\" '",
    "'<input id=\"blog-q\" type=\"search\" placeholder=\"Search the blog — titles, topics, tools…\" '")
s = s.replace(
    "    <p class=\"blog-byline\">{n} in-depth guides across {ntopics} topics — new pieces added regularly.</p>",
    "    <p class=\"blog-byline\">New pieces added regularly.</p>")
s = s.replace(
    "f'monetization. {n} long-form articles from the Fast Scheduler team.')",
    "f'monetization. New guides from the Fast Scheduler team.')")

old_rel = (
    "def related_for(art):\n"
    "    \"\"\"Cross-links: same-category siblings + two help-center picks.\"\"\"\n"
    "    rows = [(b['id'], b['title'], 'blog') for b in ARTICLES\n"
    "            if b is not art and b['category'] == art['category']][:4]\n"
    "    rows += [(rid, t, 'help') for rid, t in HELP_PICKS]\n"
    "    chips = ''.join(\n"
    "        f'<a class=\"hc-chip\" href=\"{(\"../../help/a/\" + rid + \".html\") if kind == \"help\" else (rid + \".html\")}\">'\n"
    "        f'<span>{bh.esc(t)}</span>{bh.svg(\"arrow-r\")}</a>'\n"
    "        for rid, t, kind in rows)")
new_rel = (
    "def related_for(art):\n"
    "    \"\"\"Cross-links: same-category siblings (no help-center links here — the\n"
    "    blog is editorial content and shouldn't route readers into support docs).\"\"\"\n"
    "    rows = [(b['id'], b['title'], 'blog') for b in ARTICLES\n"
    "            if b is not art and b['category'] == art['category']][:6]\n"
    "    chips = ''.join(\n"
    "        f'<a class=\"hc-chip\" href=\"{rid + \".html\"}\">'\n"
    "        f'<span>{bh.esc(t)}</span>{bh.svg(\"arrow-r\")}</a>'\n"
    "        for rid, t, kind in rows)")
assert old_rel in s, "related_for block not found in build_blog.py"
s = s.replace(old_rel, new_rel, 1)

assert s != orig, "build_blog.py unchanged"
write(bb, s)
changed.append(bb)

print("files changed:", len(changed))
print("help-center chips removed:", n_chips)
