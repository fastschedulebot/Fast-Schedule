# s14: RU EN-flash fix — MAP entries + lang-aware dynamic rendering in help.
import io

HELP = 'website/_build/build_help.py'
CHROME = 'website/scripts/ru-chrome.js'
LANG = 'website/scripts/lang.js'

NEW_MAP_6 = """      'Best result': 'BestRU1',
      'More results': 'BestRU2',
      'All results': 'BestRU3',
      'Up next': 'BestRU4',
      'Now reading': 'BestRU5',
      'No previous article': 'BestRU6',
      'No next article': 'BestRU7',
      'Other categories:': 'BestRU8',
      'Related topics': 'BestRU9',
      'This article has no sections.': 'BestRU10',
      '0 results': 'BestRU11',
      'No exact match for': 'BestRU12',
      'Maybe you meant:': 'BestRU13',
      'Still stuck?': 'BestRU14',
      'Ask in the bot': 'BestRU15',
      'You mean:': 'BestRU16',
"""

RU_PAIRS = [
    ('BestRU1', 'Лучший результат'),
    ('BestRU2', 'Другие результаты'),
    ('BestRU3', 'Все результаты'),
    ('BestRU4', 'Далее'),
    ('BestRU5', 'Читаете сейчас'),
    ('BestRU6', 'Нет предыдущей статьи'),
    ('BestRU7', 'Нет следующей статьи'),
    ('BestRU8', 'Другие категории:'),
    ('BestRU9', 'Похожие темы'),
    ('BestRU10', 'В этой статье нет разделов.'),
    ('BestRU11', 'Ничего не найдено'),
    ('BestRU12', 'Точного совпадения нет:'),
    ('BestRU13', 'Возможно, вы имели в виду:'),
    ('BestRU14', 'Не нашли ответ?'),
    ('BestRU15', 'Спросите в боте'),
    ('BestRU16', 'Вы имеете в виду:'),
]

NEW_MAP_4 = '\n'.join(
    "    '%s': '%s'," % (en, ru) for en, ru in [
        ('Best result', 'BestRU1'),
        ('More results', 'BestRU2'),
        ('All results', 'BestRU3'),
        ('Up next', 'BestRU4'),
        ('Now reading', 'BestRU5'),
        ('No previous article', 'BestRU6'),
        ('No next article', 'BestRU7'),
        ('Other categories:', 'BestRU8'),
        ('Related topics', 'BestRU9'),
        ('This article has no sections.', 'BestRU10'),
        ('0 results', 'BestRU11'),
        ('No exact match for', 'BestRU12'),
        ('Maybe you meant:', 'BestRU13'),
        ('Still stuck?', 'BestRU14'),
        ('Ask in the bot', 'BestRU15'),
        ('You mean:', 'BestRU16'),
    ]) + '\n'


def sub_once(path, old, new):
    s = io.open(path, encoding='utf-8').read()
    assert old in s, 'anchor missing in %s: %r' % (path, old[:70])
    assert s.count(old) == 1, 'anchor not unique in %s: %r x%d' % (path, old[:70], s.count(old))
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
    print('[ok]', path, old[:50].replace(chr(10), ' '))


def sub_all(path, old, new):
    s = io.open(path, encoding='utf-8').read()
    assert old in s, 'anchor missing in %s: %r' % (path, old[:70])
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new))
    print('[ok]', path, old[:50].replace(chr(10), ' '), 'x%d' % s.count(old))


# ---- 1. ru-chrome.js MAP (6-space indent), anchor on 'Reading' ----
s = io.open(CHROME, encoding='utf-8').read()
anchor = "      'Reading':"
assert anchor in s and s.count(anchor) == 1
tmp = NEW_MAP_6
for en, ru in RU_PAIRS:
    tmp = tmp.replace("'%s'" % en, "'%s'" % en)  # noop, keep structure
# swap placeholders for real Russian
real = tmp
for code, ru in RU_PAIRS:
    real = real.replace("'%s'" % code, "'%s'" % ru)
s = s.replace(anchor, real + anchor, 1)
io.open(CHROME, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] ru-chrome MAP')

# ---- 2. lang.js inline fallback (4-space indent), anchor on 'On this page' ----
s = io.open(LANG, encoding='utf-8').read()
anchor2 = "    'On this page':"
assert anchor2 in s and s.count(anchor2) == 1
tmp2 = NEW_MAP_4
for code, ru in RU_PAIRS:
    tmp2 = tmp2.replace("'%s'" % code, "'%s'" % ru)
s = s.replace(anchor2, tmp2 + anchor2, 1)
io.open(LANG, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] lang.js fallback MAP')

print('s14 part 1 done')
