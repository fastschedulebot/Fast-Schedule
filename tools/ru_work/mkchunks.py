import json

missing = json.load(open('tools/ru_work/frags_missing.json', encoding='utf-8'))
# shorts first (fast), then longs
shorts = [x for x in missing if len(x) < 60]
longs = [x for x in missing if len(x) >= 60]
CH = 400
chunks = []
cur = []
for x in shorts:
    cur.append(x)
    if len(cur) >= 600:
        chunks.append(cur)
        cur = []
if cur:
    chunks.append(cur)
    cur = []
for x in longs:
    cur.append(x)
    if len(cur) >= 250:
        chunks.append(cur)
        cur = []
if cur:
    chunks.append(cur)
for i, ch in enumerate(chunks):
    with open('tools/ru_work/ch_%02d.json' % i, 'w', encoding='utf-8') as f:
        json.dump(ch, f, ensure_ascii=False, indent=1)
print('chunks:', len(chunks), 'sizes:', [len(c) for c in chunks])
