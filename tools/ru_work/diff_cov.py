import json
import re

frags = json.load(open('tools/ru_work/frags.json', encoding='utf-8'))
t = open('website/scripts/ru-content.js', encoding='utf-8').read()
m = re.match(r"window\.FS_RU_CONTENT=(.*);$", t, re.S)
have = set(json.loads(m.group(1)).keys())
extra = json.load(open('tools/ru_blog_extra.json', encoding='utf-8'))
for s in ('titles', 'descs'):
    have.update(extra.get(s, {}).keys())
missing = [f for f in frags if f not in have]
with open('tools/ru_work/frags_missing.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, ensure_ascii=False)
print('total:', len(frags), 'have:', len(frags) - len(missing), 'missing:', len(missing))
print('missing chars:', sum(len(x) for x in missing))
short = [x for x in missing if len(x) < 40]
print('short(<40):', len(short))
long = [x for x in missing if len(x) >= 40]
print('long chars:', sum(len(x) for x in long))
