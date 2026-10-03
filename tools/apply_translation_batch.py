import json

def load(l):
    return json.load(open(f'translations/{l}.json', encoding='utf-8'))

def save(l, d):
    with open(f'translations/{l}.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

en, ru, es = load('en'), load('ru'), load('es')
log = []

# ══ 1. RU default-channel purge (match en/es) ══
assert 'default' in ru
ru.pop('default', None); log.append('ru: deleted top-level default')
ru.get('help', {}).pop('channel_default', None); log.append('ru: deleted help.channel_default')
ch = (ru.get('help', {}).get('channels', {}) or {}).get('children', [])
assert 'channel_default' in ch
ch.remove('channel_default'); log.append('ru: removed channel_default from children')
assert 'channel_default_hint' in ru.get('select', {})
ru['select'].pop('channel_default_hint'); log.append('ru: deleted select.channel_default_hint')

# ══ 2. RU channel_manage — drop star/default bullets (mirror EN) ══
ru['help']['channel_manage']['content'] = (
    "Всё об одном канале живёт в двух местах: списке <b>Подключённый канал</b> "
    "и собственном <b>экране информации</b> канала.\n\n"
    "<b>Подключённый канал</b> (главное меню) перечисляет все подключённые каналы. "
    "Для каждого канала доступны:\n"
    "• Название канала.\n"
    "• <b>Изменить часовой пояс</b> — посты этого канала отправляются в его собственном "
    "часовом поясе, вручную пересчитывать смещения UTC не нужно.\n"
    "• <b>Сменить канал</b> — заменить этот канал другим; его отложенные сообщения "
    "переедут вместе с вами.\n"
    "• <b>Отключить канал</b> — отвязать канал (см. «Удаление канала»).\n\n"
    "Нажмите кнопку информации у канала, чтобы открыть подробности: роль подключения, "
    "бот-отправитель, часовой пояс и сколько отложенных и повторяющихся сообщений хранит канал.\n\n"
    "Каждый канал настраивается независимо — удобно для многоканальных схем."
)
log.append('ru: channel_manage rewritten')

# ══ 3. RU config content — default block -> Channels block ══
old_block = ("<b>Канал по умолчанию</b>\n"
             "• Задайте канал по умолчанию в настройках канала, чтобы пропускать выбор канала\n"
             "• У каждого канала может быть свой часовой пояс\n"
             "• Управляйте подключёнными каналами через <code>/channel</code>")
new_block = ("<b>Каналы</b>\n"
             "• У каждого канала может быть свой часовой пояс\n"
             "• Управляйте подключёнными каналами через <code>/channel</code>")
cfg = ru['help']['config']['content']
assert old_block in cfg, 'config old block not found'
ru['help']['config']['content'] = cfg.replace(old_block, new_block)
log.append('ru: config content fixed')

# ══ 4. RU config faq ══
faq = ru['help']['config']['faq']
assert faq[0]['q'] == "Где настройки?"
old_a = faq[0]['a']
assert "управление каналами и каналом по умолчанию" in old_a
faq[0]['a'] = old_a.replace(" — управление каналами и каналом по умолчанию",
                            " — управление каналами")
before = len(faq)
faq[:] = [x for x in faq if x.get('q') != "Как задать канал по умолчанию?"]
assert len(faq) == before - 1
log.append('ru: config faq fixed')

# ══ 5. RU connect_channel content ══
conn = ru['help']['connect_channel']['content']
old_line = "• Задайте <b>Канал по умолчанию</b> (Premium), чтобы пропускать выбор канала\n"
assert old_line in conn, 'connect old line not found'
ru['help']['connect_channel']['content'] = conn.replace(old_line, "")
log.append('ru: connect_channel content fixed')

# ══ 6. RU connect_channel faq — drop default-channel item ══
cfaq = ru['help']['connect_channel']['faq']
before = len(cfaq)
cfaq[:] = [x for x in cfaq if x.get('q') != "Как задать канал по умолчанию?"]
assert len(cfaq) == before - 1
log.append('ru: connect_channel faq fixed')

# ══ 7. RU multichannel (mirror EN) ══
ru['help']['multichannel']['content'] = (
    "Premium открывает до {channels_prem} каналов, у каждого свой бот-отправитель, "
    "расписание и идентичность.\n\n"
    "<b>Как это работает</b>\n"
    "• Каждому каналу соответствует свой бот-отправитель — посты всегда выходят от его имени.\n"
    "• При планировании вы выбираете целевой канал.\n"
    "• У каждого канала свои часовой пояс, подпись и настройки.\n\n"
    "<b>Повседневный процесс</b>\n"
    "• Используйте Список сообщений с фильтром по каналу, чтобы ревизовать один канал за раз.\n"
    "• Кросспост одного сообщения? Запланируйте его отдельно для каждого канала.\n\n"
    "Free покрывает {channels_free} канал и {bots_free} бота; Premium поднимает оба до {channels_prem}."
)
log.append('ru: multichannel rewritten')

# ══ 8. Bulk Premium-only help: move-FAQ answers (en/ru/es) ══
EN_MOVE_A = (
    "Yes — bulk move and copy is a <b>Premium</b> feature. Step by step:\n"
    "@@STORAGE@@1. Click <b>Media Storage</b> → open the source box\n"
    "2. Use <b>Move All</b> or <b>Copy All</b> (optionally filtered by type: images, videos, files)\n"
    "3. Choose the destination box from the list\n"
    "4. The items are moved/copied — no need to re-upload\n\n"
    "On the Free plan you can move or copy one file at a time instead — "
    "open the item and use <b>Move</b> / <b>Copy</b>.\n\n"
    "This helps you reorganize your media collection without re-uploading anything."
)
RU_MOVE_A = (
    "Да — массовое перемещение и копирование — функция <b>Premium</b>. Пошагово:\n"
    "@@STORAGE@@1. Нажмите <b>Хранилище медиа</b> → откройте исходный бокс\n"
    "2. Используйте <b>Переместить всё</b> или <b>Копировать всё</b> "
    "(можно с фильтром по типу: изображения, видео, файлы)\n"
    "3. Выберите бокс-приёмник из списка\n"
    "4. Элементы перемещены/скопированы — перезагружать ничего не нужно\n\n"
    "На тарифе Free перемещайте или копируйте по одному файлу — откройте элемент "
    "и используйте <b>Переместить</b> / <b>Копировать</b>.\n\n"
    "Это помогает реорганизовать медиатеку без повторных загрузок."
)

def patch_move(d, text):
    faq = d['help']['media_storage']['faq']
    for item in faq:
        q = item.get('q', '')
        if 'move items between storage boxes' in q or 'перемещать элементы между боксами' in q:
            item['a'] = text
            return item['q']
    raise AssertionError('move faq not found')

patch_move(en, EN_MOVE_A); log.append('en: move faq premium-only')
patch_move(ru, RU_MOVE_A); log.append('ru: move faq premium-only')
patch_move(es, EN_MOVE_A); log.append('es: move faq premium-only')

# ══ 9. New box-download FAQ (en/ru/es) ══
EN_BOX = {
    "q": "@@STORAGE@@Can I download a whole storage box?",
    "a": ("@@STORAGE@@Yes — box download is a <b>Premium</b> feature: open the box and tap "
          "<b>Download Box</b> to get its files as an archive.\n\n"
          "On the Free plan open any item and tap <b>Download</b> to save files one at a time, "
          "without compression."),
}
RU_BOX = {
    "q": "@@STORAGE@@Можно ли скачать целый бокс хранилища?",
    "a": ("@@STORAGE@@Да — скачивание бокса целиком — функция <b>Premium</b>: откройте бокс "
          "и нажмите <b>Скачать хранилище</b>, чтобы получить файлы архивом.\n\n"
          "На тарифе Free открывайте элементы по одному и нажимайте <b>Скачать</b> — "
          "файлы сохраняются без сжатия."),
}

def insert_box(d, entry):
    faq = d['help']['media_storage']['faq']
    for i, item in enumerate(faq):
        q = item.get('q', '')
        if 'move items between storage boxes' in q or 'перемещать элементы между боксами' in q:
            faq.insert(i + 1, dict(entry))
            return
    raise AssertionError('move faq anchor not found')

insert_box(en, EN_BOX); log.append('en: box-download faq added')
insert_box(ru, RU_BOX); log.append('ru: box-download faq added')
insert_box(es, dict(EN_BOX)); log.append('es: box-download faq added')

save('en', en); save('ru', ru); save('es', es)

# ══ verify ══
en2, ru2, es2 = load('en'), load('ru'), load('es')
checks = []
checks.append('default' not in ru2)
checks.append('channel_default' not in ru2.get('help', {}))
checks.append('channel_default' not in ((ru2.get('help', {}).get('channels', {}) or {}).get('children', [])))
checks.append('channel_default_hint' not in ru2.get('select', {}))
import re
pat = re.compile(r'канал по умолчанию|сделать по умолчанию|убрать по умолчанию', re.I)
for k in ['channel_manage', 'config', 'connect_channel', 'multichannel']:
    s = json.dumps(ru2['help'][k], ensure_ascii=False)
    checks.append(not pat.search(s))
for lang, d, move_txt in [('en', en2, 'Premium'), ('ru', ru2, 'Premium'), ('es', es2, 'Premium')]:
    s = json.dumps(d['help']['media_storage'], ensure_ascii=False)
    checks.append(move_txt in s and 'Free plan' in s or 'Free' in s)
assert all(checks), checks
log.append('verify: ALL OK')

open('TRANSLATION_EDIT_LOG.txt', 'w', encoding='utf-8').write('\n'.join(log))
