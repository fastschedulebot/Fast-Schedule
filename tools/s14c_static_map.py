# s14c: remaining static chrome MAP entries (search empty state + 404 + dropdown tail).
import io

q = "'"
PAIRS = [
    ('\u2014 a human answers every ticket.',
     '\u2014 \u043d\u0430 \u043a\u0430\u0436\u0434\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441 \u043e\u0442\u0432\u0435\u0447\u0430\u0435\u0442 \u0447\u0435\u043b\u043e\u0432\u0435\u043a.'),
    ('No results found for \u201c',
     '\u041d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e: \u00ab'),
    ('Try other words \u2014 for example',
     '\u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0434\u0440\u0443\u0433\u0438\u0435 \u0441\u043b\u043e\u0432\u0430 \u2014 \u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440'),
    ('Back to Help Center',
     '\u041d\u0430\u0437\u0430\u0434 \u0432 \u0446\u0435\u043d\u0442\u0440 \u043f\u043e\u043c\u043e\u0449\u0438'),
    ('That topic doesn\u2019t exist (or moved). Try the search on the home page.',
     '\u0422\u0430\u043a\u043e\u0439 \u0442\u0435\u043c\u044b \u043d\u0435\u0442. \u0412\u043e\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0439\u0442\u0435\u0441\u044c \u043f\u043e\u0438\u0441\u043a\u043e\u043c \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u043e\u0439.'),
]

jobs = [
    ('website/scripts/ru-chrome.js', '      ', "      'Maybe you meant:':"),
    ('website/scripts/lang.js', '    ', "    'Maybe you meant:':"),
]

for path, indent, anchor in jobs:
    s = io.open(path, encoding='utf-8').read()
    assert anchor in s and s.count(anchor) == 1, (path, anchor)
    lines = []
    for en, ru in PAIRS:
        lines.append(indent + q + en + q + ': ' + q + ru + q + ',')
    block = '\n'.join(lines) + '\n'
    s = s.replace(anchor, block + anchor, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', path)

print('s14c done')
