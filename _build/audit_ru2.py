"""Post-fix audit: landing EN nodes vs RU coverage (chrome MAP + content dict)."""
import os
import re
import html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_SUB = ('@fastschedule', 't.me/', 'FastSchedulerBot', 'Fast Schedule',
            '21.09.2026', '22.09.2026', '11:42', '18:15', '09:12', '14:05',
            '1 284 subscribers', 'fastschedule_test3', '1 148', 'Sunday,',
            'Message', 'Downloads', 'Telegram', 'Instagram', 'Calendar',
            'Music', 'Photos', 'Files', 'Settings', 'Things', 'Open',
            'Cancel', 'now', 'posted from the queue',
            'one batch,', 'schedule multiple', 'see everything',
            'use stats for', 'only admins can post',
            '~2.5 h', '$', '%', '/start', 'vs $',
            'Milena', 'Artem', 'Sofia')

src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
src2 = re.sub(r'<script.*?</script\s*>', '', src, flags=re.S | re.I)
src2 = re.sub(r'<style.*?</style\s*>', '', src2, flags=re.S | re.I)
parts = re.split(r'<[^>]+>', src2)
texts = []
for p in parts:
    t = H.unescape(p)
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) >= 3 and re.search(r'[A-Za-z]', t):
        texts.append(t)
seen = list(dict.fromkeys(texts))

chrome = open(os.path.join(ROOT, 'scripts', 'ru-chrome.js'), encoding='utf-8').read()
lang = open(os.path.join(ROOT, 'scripts', 'lang.js'), encoding='utf-8').read()
rc = open(os.path.join(ROOT, 'scripts', 'ru-content.js'), encoding='utf-8').read()
pool = (chrome + lang + rc).replace("\\'", "'").replace('\\"', '"')

missing = []
for t in seen:
    if t in pool:
        continue
    if any(s in t for s in SKIP_SUB):
        continue
    missing.append(t)

print('TOTAL_NODES: %d' % len(seen))
print('STILL MISSING: %d' % len(missing))
for t in missing:
    print('- ' + t)
