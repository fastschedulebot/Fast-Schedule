"""October 2026 help refresh: Storage Premium features + legal update.

- Expands ms_premium / ms_manage with Move All, Copy All, Download Box.
- Adds ms_bulk (bulk organize & box download guide) and legal_update
  (October 2026 policy refresh) topics in EN + RU, wired into the
  bot children trees. ES falls back to EN (i18n has en fallback).
- Aligns premium_refund + legal with the October 2026 policy documents.

Run from repo root:  python tools/update_help_oct2026.py
"""
import io
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(l):
    with io.open(os.path.join(REPO_ROOT, 'translations', l + '.json'), encoding='utf-8-sig') as f:
        return json.load(f)


def save(l, d):
    p = os.path.join(REPO_ROOT, 'translations', l + '.json')
    with io.open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')


en = load('en')
ru = load('ru')
log = []

# ---- 1. ms_premium: document the Premium storage toolkit ----
en['help']['ms_premium']['content'] = (
    "Premium storage benefits:\n"
    "• {storage_count_prem} boxes instead of {storage_count_free}, "
    "with up to {storage_items_prem} items each.\n"
    "• Videos allowed in storage ({storage_video_prem}).\n"
    "• Larger uploads ({max_media_prem}).\n"
    "• <b>Move All / Copy All</b> — reorganize a whole box in one tap, "
    "optionally filtered by type (images, videos, files).\n"
    "• <b>Download Box</b> — save an entire box as a single archive.\n"
    "\n"
    "On Free you can still move, copy, and download items one at a time.\n"
    "\n"
    "Upgrade via <code>/premium</code> to unlock them."
)
ru['help']['ms_premium']['content'] = (
    "Преимущества хранилища на Premium:\n"
    "• {storage_count_prem} боксов вместо {storage_count_free}, "
    "до {storage_items_prem} элементов в каждом.\n"
    "• Видео разрешены в хранилище ({storage_video_prem}).\n"
    "• Большие загрузки ({max_media_prem}).\n"
    "• <b>Переместить всё / Копировать всё</b> — перестройка целого бокса в один тап, "
    "при желании с фильтром по типу (изображения, видео, файлы).\n"
    "• <b>Скачать бокс</b> — сохранение целого бокса одним архивом.\n"
    "\n"
    "На бесплатном тарифе элементы можно перемещать, копировать и скачивать по одному.\n"
    "\n"
    "Откройте через <code>/premium</code>, чтобы разблокировать."
)
log.append('ms_premium rewritten (en+ru)')

# ---- 2. ms_manage: point at the bulk tools ----
en['help']['ms_manage']['content'] = (
    "All storage actions are available from <b>Storage</b> in the main menu:\n"
    "• Create/rename/delete boxes.\n"
    "• Upload, preview, copy, move, replace, and delete items.\n"
    "• Premium bulk tools inside an open box: <b>Move All</b>, <b>Copy All</b> "
    "(optionally filtered by type) and <b>Download Box</b> for the whole box as an archive.\n"
    "\n"
    "Items are kept until you delete them. If Premium lapses, the expiry cleanup may remove excess media."
)
ru['help']['ms_manage']['content'] = (
    "Все действия с хранилищем доступны из <b>Хранилища</b> в главном меню:\n"
    "• Создание, переименование и удаление боксов.\n"
    "• Загрузка, предпросмотр, копирование, перемещение, замена и удаление элементов.\n"
    "• Массовые инструменты Premium внутри открытого бокса: <b>Переместить всё</b>, "
    "<b>Копировать всё</b> (при желании с фильтром по типу) и <b>Скачать бокс</b> — весь бокс одним архивом.\n"
    "\n"
    "Элементы хранятся, пока не удалите их. Если Premium кончится, чистка при истечении может убрать лишнее медиа."
)
log.append('ms_manage rewritten (en+ru)')

# ---- 3. New topic: ms_bulk ----
en['help']['ms_bulk'] = {
    'title': '@@STORAGE@@Bulk Move, Copy & Box Download',
    'content': (
        "Reorganizing a box item by item is slow. Premium adds three bulk tools inside any open box:\n"
        "\n"
        "<b>Move All</b>\n"
        "• Moves every item (or only one type: images, videos, files) into a box you pick.\n"
        "• Use it to split a mixed box by type or to retire a finished campaign in one tap.\n"
        "\n"
        "<b>Copy All</b>\n"
        "• Same flow, but the source box keeps its items — handy for seeding a new campaign "
        "box from an archive without touching the original.\n"
        "\n"
        "<b>Download Box</b>\n"
        "• Saves the whole box as a single archive, so you can keep an offline copy or hand "
        "assets to a teammate.\n"
        "\n"
        "On Free, open any item and use <b>Move</b>, <b>Copy</b>, or <b>Download</b> for one file at a time."
    ),
    'faq': [
        {'q': '@@STORAGE@@Is bulk move/copy a Premium feature?',
         'a': 'Yes — <b>Move All</b>, <b>Copy All</b>, and <b>Download Box</b> need Premium. '
              'On Free you can move, copy, or download one file at a time instead.'},
        {'q': '@@STORAGE@@Can I move only videos or only photos?',
         'a': 'Yes. <b>Move All</b> and <b>Copy All</b> offer an optional type filter '
              '(images, videos, files), so one tap can split a mixed box by type.'},
        {'q': '@@STORAGE@@What do I get when I download a box?',
         'a': 'One archive with the box files, for offline backup or sharing with a teammate. '
              'On Free, open items one by one and tap <b>Download</b> instead.'},
    ],
}
ru['help']['ms_bulk'] = {
    'title': '@@STORAGE@@Массовые перенос, копирование и скачивание бокса',
    'content': (
        "Перестраивать бокс по одному элементу долго. Premium добавляет три массовых инструмента "
        "внутри любого открытого бокса:\n"
        "\n"
        "<b>Переместить всё</b>\n"
        "• Переносит каждый элемент (или только один тип: изображения, видео, файлы) в выбранный бокс.\n"
        "• Так удобно делить смешанный бокс по типам или закрывать завершённую кампанию в один тап.\n"
        "\n"
        "<b>Копировать всё</b>\n"
        "• Тот же сценарий, но исходный бокс сохраняет элементы — удобно засеять новый бокс кампании "
        "из архива, не трогая оригинал.\n"
        "\n"
        "<b>Скачать бокс</b>\n"
        "• Сохраняет целый бокс одним архивом — для офлайн-копии или передачи ресурсов коллеге.\n"
        "\n"
        "На бесплатном тарифе откройте любой элемент и используйте <b>Переместить</b>, "
        "<b>Копировать</b> или <b>Скачать</b> для одного файла за раз."
    ),
    'faq': [
        {'q': '@@STORAGE@@Массовые перенос и копирование — функция Premium?',
         'a': 'Да — <b>Переместить всё</b>, <b>Копировать всё</b> и <b>Скачать бокс</b> требуют Premium. '
              'На бесплатном тарифе вместо этого перемещайте, копируйте или скачивайте по одному файлу.'},
        {'q': '@@STORAGE@@Можно ли перенести только видео или только фото?',
         'a': 'Да. <b>Переместить всё</b> и <b>Копировать всё</b> предлагают необязательный фильтр по типу '
              '(изображения, видео, файлы): один тап делит смешанный бокс по типам.'},
        {'q': '@@STORAGE@@Что я получаю при скачивании бокса?',
         'a': 'Один архив с файлами бокса — для офлайн-копии или передачи коллеге. '
              'На бесплатном тарифе открывайте элементы по одному и нажимайте <b>Скачать</b>.'},
    ],
}
en['help']['media_storage']['children'].append('ms_bulk')
ru['help']['media_storage']['children'].append('ms_bulk')
log.append('ms_bulk added (en+ru) + wired into media_storage children')

# ---- 4. legal: point at the October 2026 refresh + version history ----
en['help']['legal']['content'] = (
    "The service runs under three documents, all on the website:\n"
    "\n"
    "• <b>Terms of Service</b> — the rules for using Fast Scheduler, plan limits, and fair use.\n"
    "• <b>Privacy Policy</b> — what data is stored and how it is protected.\n"
    "• <b>Refund Policy</b> — when and how Premium payments are refunded.\n"
    "\n"
    "The documents were last refreshed in October 2026 (each shows its effective date). "
    "Previous versions are kept in the version history on the website, so you can always "
    "see what changed.\n"
    "\n"
    "Short version: schedule only content you have the right to publish, keep your channel "
    "compliant with Telegram's own rules, and refunds follow the published policy. "
    "The full texts are linked from the website footer."
)
ru['help']['legal']['content'] = (
    "Сервис работает по трём документам, все на сайте:\n"
    "\n"
    "• <b>Условия использования</b> — правила Fast Scheduler, лимиты тарифов и добросовестное использование.\n"
    "• <b>Политика конфиденциальности</b> — какие данные хранятся и как защищены.\n"
    "• <b>Политика возвратов</b> — когда и как возвращаются платежи Premium.\n"
    "\n"
    "Документы последний раз обновлялись в октябре 2026 (у каждого указана дата вступления в силу). "
    "Предыдущие версии хранятся в истории версий на сайте — всегда видно, что изменилось.\n"
    "\n"
    "Коротко: планируйте только контент, на который есть права, держите канал в рамках собственных "
    "правил Telegram, а возвраты идут по опубликованной политике. Полные тексты приведены в подвале сайта."
)
log.append('legal refreshed (en+ru)')

# ---- 5. New topic: legal_update ----
en['help']['legal_update'] = {
    'title': 'October 2026 Policy Refresh',
    'content': (
        "In October 2026 the three legal documents were rewritten for clarity — "
        "no new data collection, no new fees, no change to what the bot does:\n"
        "\n"
        "• <b>Privacy Policy</b> — now names every service explicitly (Fast Scheduler, SetDate, "
        "Support bot, website) and lists exactly what is stored and why. Your rights are unchanged: "
        "export a copy anytime (<code>/export</code>, full backup with <code>/backup</code> on Premium) "
        "and delete everything on request.\n"
        "• <b>Terms of Service</b> — clearer plan and fair-use rules, plus how material changes "
        "are announced (in-app notice; continued use after the effective date means acceptance).\n"
        "• <b>Refund Policy</b> — spelled out for Telegram Stars: Stars purchases are final under "
        "Telegram's own rules, with discretionary refunds for genuine failures (double charge, "
        "technical fault). Request via fastschedulebot@gmail.com; we acknowledge within 7 business days.\n"
        "\n"
        "Each document shows its effective date, and previous versions stay available in the "
        "version history on the website."
    ),
    'faq': [
        {'q': 'Do I need to accept the updated policies?',
         'a': 'No extra tap is needed. Per the Terms, material changes are announced in-app, and '
              'continued use after the effective date means acceptance. If you disagree, stop using '
              'the service and export or delete your data first.'},
        {'q': 'Where can I read the previous versions?',
         'a': 'On the website under Legal → version history. Every past version stays published '
              'with its effective date, so changes are auditable.'},
        {'q': 'Did the refund rules change?',
         'a': 'The October 2026 text states the standing practice plainly: Telegram Stars purchases '
              'are final, with case-by-case discretionary refunds for genuine failures. The request '
              'address is fastschedulebot@gmail.com and we acknowledge within 7 business days.'},
    ],
}
ru['help']['legal_update'] = {
    'title': 'Обновление политик в октябре 2026',
    'content': (
        "В октябре 2026 три юридических документа переписаны для ясности — "
        "без нового сбора данных, без новых комиссий, без изменений в работе бота:\n"
        "\n"
        "• <b>Политика конфиденциальности</b> — теперь явно называет каждый сервис (Fast Scheduler, "
        "SetDate, бот поддержки, сайт) и перечисляет, что хранится и зачем. Ваши права прежние: "
        "копия в любой момент (<code>/export</code>, полная копия через <code>/backup</code> на Premium) "
        "и удаление всего по запросу.\n"
        "• <b>Условия использования</b> — более ясные правила тарифов и добросовестного использования плюс порядок анонса "
        "существенных изменений (уведомление в приложении; продолжение использования после даты "
        "вступления означает согласие).\n"
        "• <b>Политика возвратов</b> — расписана для Stars Telegram: покупки за Stars окончательны по собственным "
        "правилам Telegram, с возвратами на усмотрение при настоящих сбоях (двойное списание, "
        "технический сбой). Запрос на fastschedulebot@gmail.com; подтверждаем в течение 7 рабочих дней.\n"
        "\n"
        "У каждого документа указана дата вступления в силу, а предыдущие версии остаются доступными "
        "в истории версий на сайте."
    ),
    'faq': [
        {'q': 'Нужно ли принимать обновлённые политики?',
         'a': 'Лишний тап не нужен. По Условиям существенные изменения анонсируются в приложении, '
              'а продолжение использования после даты вступления означает согласие. Если не согласны — '
              'перестаньте пользоваться сервисом, сначала экспортировав или удалив данные.'},
        {'q': 'Где читать предыдущие версии?',
         'a': 'На сайте в разделе правовых документов → история версий. Каждая прошлая версия остаётся '
              'опубликованной со своей датой вступления — изменения проверяемы.'},
        {'q': 'Правила возвратов изменились?',
         'a': 'Текст октября 2026 прямо фиксирует сложившуюся практику: покупки за Stars Telegram final, '
              'с возвратами в индивидуальном порядке при настоящих сбоях. Адрес запроса — '
              'fastschedulebot@gmail.com, подтверждаем в течение 7 рабочих дней.'},
    ],
}
en['help']['legal']['children'].append('legal_update')
ru['help']['legal']['children'].append('legal_update')
log.append('legal_update added (en+ru) + wired into legal children')

# ---- 6. premium_refund: align with the October 2026 refund policy ----
en['help']['premium_refund']['content'] = (
    "Premium is paid in Telegram Stars, and Stars purchases are final under Telegram's own rules. "
    "Outside mandatory consumer rights, refunds are discretionary and granted case by case — "
    "typically for a double charge or a technical fault on our side.\n"
    "\n"
    "To request a refund, email <b>fastschedulebot@gmail.com</b> with:\n"
    "• The transaction ID (in the Stars payment confirmation or Settings → Payments).\n"
    "• Your Telegram username.\n"
    "• The purchase date and a short reason.\n"
    "\n"
    "We acknowledge requests within <b>7 business days</b>. Approved refunds return through Telegram "
    "only; referral days and promo free periods have no monetary value and are never refundable.\n"
    "\n"
    "To stop future billing on a monthly plan, cancel via <code>/premium</code> — the paid period "
    "stays active until its end date."
)
ru['help']['premium_refund']['content'] = (
    "Premium оплачивается в Stars Telegram, а покупки за Stars окончательны по собственным правилам Telegram. "
    "Вне обязательных прав потребителей возвраты — на усмотрение и выдаются в индивидуальном порядке: "
    "обычно при двойном списании или техническом сбое на нашей стороне.\n"
    "\n"
    "Чтобы запросить возврат, напишите на <b>fastschedulebot@gmail.com</b>:\n"
    "• ID транзакции (в подтверждении оплаты Stars или Настройки → Платежи).\n"
    "• Ваше имя пользователя Telegram.\n"
    "• Дату покупки и короткую причину.\n"
    "\n"
    "Подтверждаем запросы в течение <b>7 рабочих дней</b>. Одобренные возвраты идут только через Telegram; "
    "реферальные дни и бесплатные периоды по промокодам денежной ценности не имеют и не возвращаются.\n"
    "\n"
    "Чтобы остановить будущие списания месячного плана, отмените через <code>/premium</code> — оплаченный "
    "период остаётся активным до даты окончания."
)
log.append('premium_refund aligned with policy (en+ru)')

save('en', en)
save('ru', ru)
with io.open(os.path.join(REPO_ROOT, 'TRANSLATION_EDIT_LOG.txt'), 'a', encoding='utf-8') as f:
    f.write('\n' + '\n'.join(log) + '\n')
print('\n'.join(log))
