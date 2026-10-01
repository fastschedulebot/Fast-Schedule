import io

# ---- build_static.py: dedupe sitemap + fresh lastmod --------------------
p = '_build/build_static.py'
s = open(p, encoding='utf-8').read()

# 1. BUILD_DATE = today, not a stale constant (keeps sitemap/JSON-LD fresh each build)
old = "BUILD_DATE = '2026-09-20'"
assert s.count(old) == 1
s = s.replace(old, "import datetime as _dt\nBUILD_DATE = _dt.date.today().isoformat()")

# 2. dedupe the article URL list (misc-group kids were added twice -> duplicate sitemap URLs)
old = "    urls += [(f'{SITE}/help/a/{n[\"id\"]}.html', '0.8') for n in article_order]"
assert s.count(old) == 1
new = ("    seen_ids = set()\n"
       "    uniq_articles = [n for n in article_order if not (n['id'] in seen_ids or seen_ids.add(n['id']))]\n"
       "    urls += [(f'{SITE}/help/a/{n[\"id\"]}.html', '0.8') for n in uniq_articles]")
s = s.replace(old, new)

# 3. dedupe the static article page writing too, so both stay consistent
old = "    for n in article_order:\n"
if s.count(old) >= 1:
    # only replace the occurrence right after art_ids/order_index setup that writes pages
    idx = s.find(old, s.find('order_index'))
    if idx != -1:
        s = s[:idx] + "    for n in uniq_articles:\n" + s[idx+len(old):]

open(p, 'w', encoding='utf-8', newline='').write(s)
print('build_static.py: BUILD_DATE fresh + sitemap dedupe')

# ---- llms.txt: support bot + faster discovery lines ----------------------
# (generated in build_static.py; patch the generator lines)
old = "    lines = ['# Fast Scheduler',"
i = s.find(old)
assert i != -1
j = s.find("'Bot: https://t.me/FastSchedulerBot',", i) if False else s.find("t.me/FastSchedulerBot", i)
print('bot url line found:', j != -1)
