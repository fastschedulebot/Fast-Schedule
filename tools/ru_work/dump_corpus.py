import sys
import importlib
import json
import os

sys.path.insert(0, 'website/_build')
os.makedirs('tools/ru_work', exist_ok=True)
mods = ['blog_articles', 'blog_articles_b', 'blog_articles_c', 'blog_articles_d',
        'blog_articles_e', 'blog_articles_f', 'blog_articles_g', 'blog_articles_h',
        'blog_articles_i', 'blog_articles_j', 'seo_articles', 'seo_articles_b', 'seo_plan_batch5']
corpus = {}
for name in mods:
    m = importlib.import_module(name)
    lists = [(k, v) for k, v in vars(m).items()
             if isinstance(v, list) and v and isinstance(v[0], dict)
             and ('content' in v[0] or 'body' in v[0])]
    for k, L in lists:
        for a in L:
            aid = a.get('id', "%s.%s" % (name, k))
            corpus[aid] = {'mod': name,
                           'title': a.get('title', ''),
                           'desc': a.get('description', ''),
                           'content': a.get('content', a.get('body', '')),
                           'faq': a.get('faq', [])}
import blog_extras as bx
for aid, html in bx.EXTRA_SECTIONS.items():
    corpus['extrasec_' + aid] = {'mod': 'blog_extras_sec', 'title': '',
                                'desc': '', 'content': html, 'faq': []}
co = bx.CONTENT_OVERRIDES
if isinstance(co, dict):
    items = list(co.items())
else:
    items = [('0', co)]
for k, v in items:
    corpus['override_' + str(k)] = {'mod': 'blog_extras_override', 'title': '',
                                    'desc': '',
                                    'content': v if isinstance(v, str) else json.dumps(v, ensure_ascii=False),
                                    'faq': []}
with open('tools/ru_work/corpus.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False)
ids = sorted(corpus.keys())
with open('tools/ru_work/ids.json', 'w', encoding='utf-8') as f:
    json.dump(ids, f, ensure_ascii=False)
total = sum(len(c['content']) + len(c['title']) + len(c['desc'])
            + sum(len(q.get('q', '')) + len(q.get('a', '')) for q in c['faq'])
            for c in corpus.values())
print('entries:', len(corpus))
print('total chars:', total)
