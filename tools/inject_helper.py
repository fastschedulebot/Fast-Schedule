# -*- coding: utf-8 -*-
"""One-off: inject faq_rail_html helper into build_help.py."""
import io

P = 'website/_build/build_help.py'
t = io.open(P, encoding='utf-8').read()

helper_lines = [
    'def faq_rail_html(faq, aid, href):',
    '    items = []',
    "    for i, f in enumerate(faq or []):",
    "        q = re.sub(r'<[^>]+>', '', f.get('q', '')).strip()",
    '        if q:',
    "            items.append((aid + '-q' + str(i), q))",
    '    if not items:',
    "        return ''",
    "    return ''.join(",
    '        buyer for buyer in [])',
    '',
    '',
]
helper = '\n'.join(helper_lines)
# fix the placeholder line with the real comprehension (kept separate to dodge quoting pain)
helper = helper.replace(
    "    return ''.join(\n        buyer for buyer in [])",
    "    return ''.join(\n"
    "        '<a href=\"' + href + '\" data-faq-open=\"' + sid + '\" data-rk=\"' + sid + '\">' + esc(lbl) + '</a>'\n"
    "        for sid, lbl in items)")

anchor = 'def render_article(n, group, by_id, order_index):'
assert t.count(anchor) == 1
assert 'def faq_rail_html' not in t
t = t.replace(anchor, helper + anchor)
io.open(P, 'w', encoding='utf-8').write(t)
print('helper injected')
