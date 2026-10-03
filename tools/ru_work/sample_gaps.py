import json

real = json.load(open('tools/ru_work/page_missing.json', encoding='utf-8'))
src = json.load(open('tools/ru_work/page_frag_src.json', encoding='utf-8'))
want = ['premium.html', 'config.html', 'index.html', 'qa_what_is_fast_scheduler.html',
        'commands_list.html', 'connect_channel.html', 'schedule-posts-with-photos-and-video.html']
out = []
for f in real:
    files = [p.split('\\')[-1] if '\\' in p else p.split('/')[-1] for p in src.get(f, [])]
    if any(w in files for w in want):
        out.append(files[0] + ' :: ' + f)
        if len(out) >= 90:
            break
with open('tools/ru_work/gap_sample.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print('wrote', len(out))
