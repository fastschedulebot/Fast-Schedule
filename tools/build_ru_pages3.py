#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Part 3: per-section surgery for the RU help hub (full article/category swap)."""

import re
import html as H

from build_ru_pages import clean_ru, plural, strip_ru

RU_EXT2 = {
    'Ask in Telegram': 'Спросить в Telegram',
    'The in-bot assistant answers the same questions':
        'Встроенный помощник отвечает на те же вопросы',
    'and a human reads every ticket.': 'а каждый тикет читает человек.',
    'Common questions': 'Частые вопросы',
    'More topics': 'Другие темы',
    'Start here': 'Начните отсюда',
    'Show more': 'Показать больше',
    'Show less': 'Показать меньше',
    'No previous article': 'Нет предыдущей статьи',
    'Now reading': 'Сейчас читаете',
    'Contents': 'Содержание',
    'Open contents': 'Открыть содержание',
    'Close contents': 'Закрыть содержание',
    'Jump to a section': 'Перейти к разделу',
    'Sections': 'Разделы',
    'Guide': 'Гайд',
    'Other categories:': 'Другие категории:',
    'Encrypted backup': 'Зашифрованная копия',
    'Open the bot': 'Открыть бота',
    'Privacy Policy': 'Политика конфиденциальности',
    'Unlimited sends': 'Безлимитные отправки',
    'Popular articles': 'Популярные статьи',
    'Topics': 'Темы',
    'Chat with us': 'Написать нам',
    'The in-bot assistant answers the same questions — and a human reads every ticket.': 'Встроенный помощник отвечает на те же вопросы — а каждый тикет читает человек.',
    # --- help-center greeting hero (TRY_ASKING + render_home chrome) ---
    'Try asking': 'Попробуйте спросить',
    "What's the difference between .fsback and .fspback?": 'Чем отличаются файлы .fsback и .fspback?',
    'Why are my scheduled posts not publishing?': 'Почему отложенные посты не публикуются?',
    'How do I connect my own sender bot?': 'Как подключить своего бота-отправителя?',
    'How do I repeat a post every week?': 'Как повторять пост каждую неделю?',
    'What are the free plan limits?': 'Какие лимиты на бесплатном тарифе?',
    'How do I get a refund?': 'Как получить возврат?',
    'Ask in Telegram — a human answers every ticket.': 'Спросите в Telegram — на каждый запрос отвечает человек.',
    'Help Center — Fast Scheduler for Telegram': 'Центр помощи — Fast Scheduler для Telegram',
    # --- category card descriptions (CAT_DESC) + featured fallback ---
    'Guides and answers': 'Гайды и ответы',
    'Connect a channel and send your first post': 'Подключите канал и отправьте первый пост',
    'One-time and recurring posts': 'Разовые и регулярные посты',
    'Connect and manage channels': 'Подключение и управление каналами',
    'Use your own sender bot': 'Используйте своего бота-отправителя',
    'Team access and shared limits': 'Доступ команды и общие лимиты',
    'Plans, Stars and payments': 'Тарифы, Stars и оплата',
    'Invite owners, earn Premium days': 'Приглашайте владельцев, получайте дни Premium',
    'Free and Premium quotas': 'Лимиты бесплатного и Premium тарифов',
    'Post at the right hour': 'Публикуйте в нужный час',
    'Interface languages': 'Языки интерфейса',
    'Take your data with you': 'Заберите свои данные',
    'Bring chats and files in': 'Перенос чатов и файлов',
    'Backups, restore and safety': 'Копии, восстановление и безопасность',
    'Store photos, video and files': 'Хранение фото, видео и файлов',
    'Search, stats and calendar': 'Поиск, статистика и календарь',
    'Pro workflows that save hours': 'Про-приёмы, экономящие часы',
    'Report bugs, request features': 'Баги и предложения',
    'Short answers, fast': 'Короткие ответы',
    'Bot commands cheat sheet': 'Шпаргалка по командам бота',
    'Fix what went wrong': 'Что пошло не так',
    'Your data and safety': 'Ваши данные и безопасность',
    'About this help center': 'Об этом центре помощи',
    'Signatures and fine-tuning': 'Подписи и тонкая настройка',
    'Talk to a human': 'Свяжитесь с человеком',
    'Everything else': 'Всё остальное',
}

MAYBE_RU = {
    'Related topics': 'Похожие темы',
    'Search articles': 'Поиск статей',
    'Search help articles': 'Поиск по справке',
    'Search results': 'Результаты поиска',
}


def merged_map(MAP):
    m = dict(MAP)
    m.update(RU_EXT2)
    for k, v in MAYBE_RU.items():
        m.setdefault(k, v)
    return m


def ru_title(patch, aid, fallback=''):
    tr = patch.get(aid, {})
    t = (clean_ru(tr.get('title', '')) or '').strip()
    return t or fallback


def _div_span(html, open_start):
    depth = 0
    i = open_start
    n = len(html)
    while i < n:
        if html.startswith('<div', i):
            j = html.find('>', i)
            if j < 0:
                return None
            if html[j - 1] == '/':
                i = j + 1
                continue
            depth += 1
            i = j + 1
        elif html.startswith('</div>', i):
            depth -= 1
            i += 6
            if depth == 0:
                return i
        else:
            i += 1
    return None


def _replace_div_block(sec, cls, new_inner_or_none):
    key = '<div class="' + cls + '">'
    i = sec.find(key)
    if i < 0:
        return sec, False
    end = _div_span(sec, i)
    if end is None:
        return sec, False
    if new_inner_or_none is None:
        return sec[:i] + sec[end:], True
    return sec[:i] + key + new_inner_or_none + '</div>' + sec[end:], True


def _paras(raw_html):
    parts = [p.strip() for p in raw_html.split(chr(10) + chr(10))]
    parts = [p for p in parts if p]
    return ''.join('<p>' + p + '</p>' for p in parts)


def faq_html_ru(tr):
    items = []
    for f in (tr.get('faq') or []):
        if not isinstance(f, dict) or not f.get('q'):
            continue
        q = H.escape(strip_ru(clean_ru(f.get('q', '')) or ''), quote=False)
        a = _paras(clean_ru(f.get('a', '')) or '')
        items.append('<details><summary>' + q + '</summary><div class="hc-fa">' + a + '</div></details>')
    if not items:
        return None
    return '<h2>Частые вопросы</h2>' + ''.join(items)


def split_sections(html):
    pat = re.compile(r'<section class="view" data-view="(article|category|home)" data-(?:art|cat)="([a-z0-9_]+)"[^>]*>')
    spans = []
    for m in pat.finditer(html):
        depth = 0
        i = m.start()
        n = len(html)
        end = None
        while i < n:
            if html.startswith('<section', i):
                j = html.find('>', i)
                if j < 0:
                    break
                if html[j - 1] == '/':
                    i = j + 1
                    continue
                depth += 1
                i = j + 1
            elif html.startswith('</section>', i):
                depth -= 1
                i += 10
                if depth == 0:
                    end = i
                    break
            else:
                i += 1
        if end is not None:
            spans.append((m.group(1), m.group(2), m.start(), end))
    home = [(k, v, a, b) for k, v, a, b in spans if k == 'home']
    return spans, home


def surgery_article(sec, aid, patch, en_cat):
    tr = patch.get(aid)
    if tr is None:
        return sec
    title = (clean_ru(tr.get('title', '')) or '').strip()
    if not title:
        return sec
    t_esc = H.escape(title, quote=False)
    sec = re.sub(r'(<article class="hc-art hc-card">\s*<h2>).*?(</h2>)',
                 lambda m: m.group(1) + t_esc + m.group(2), sec, count=1, flags=re.S)
    sec = re.sub(r'(aria-current="page">).*?(</span>)',
                 lambda m: m.group(1) + t_esc + m.group(2), sec, count=1, flags=re.S)
    sec = re.sub(r'(<div class="hc-toc-navc cur">(?:(?!</div>).)*?<b>)(.*?)(</b>)',
                 lambda m: m.group(1) + t_esc + m.group(3), sec, count=1, flags=re.S)

    def meta_sub(m):
        cid = m.group(1)
        ct = ru_title(patch, cid, m.group(2))
        if cid == 'misc':
            ct = 'Другие темы'
        return '<a href="#/c/' + cid + '">' + H.escape(ct, quote=False) + '</a>'

    sec = re.sub(r'<a href="#/c/([a-z0-9_]+)">(.*?)</a>', meta_sub, sec, count=1, flags=re.S)
    body = clean_ru(tr.get('content') or '')
    sec, _ = _replace_div_block(sec, 'hc-body', body)
    sec, _ = _replace_div_block(sec, 'hc-faq', faq_html_ru(tr))
    return sec


def surgery_category(sec, cid, patch):
    if cid == 'misc':
        title = 'Другие темы'
        rec = {}
    else:
        rec = patch.get(cid, {})
        title = (clean_ru(rec.get('title', '')) or '').strip() or cid
    t_esc = H.escape(title, quote=False)
    sec = re.sub(r'(aria-current="page">).*?(</span>)',
                 lambda m: m.group(1) + t_esc + m.group(2), sec, count=1, flags=re.S)
    sec = re.sub(r'(<header class="hc-cat-head">(?:(?!</header>).)*?<h2>).*?(</h2>)',
                 lambda m: m.group(1) + t_esc + m.group(2), sec, count=1, flags=re.S)

    def count_sub(m):
        n = int(m.group(2))
        return m.group(1) + str(n) + ' ' + plural(n, 'статья', 'статьи', 'статей') + '</p>'

    sec = re.sub(r'(<p>)(\d+)( articles</p>)', count_sub, sec, count=1)
    sec = re.sub(r'(<h2>All articles</h2><span>)(\d+)( articles</span>)',
                 lambda m: m.group(1) + m.group(2) + ' ' + plural(int(m.group(2)), 'статья', 'статьи', 'статей') + '</span>',
                 sec, count=1)
    content = (clean_ru(rec.get('content') or '') or '').strip()
    if content:
        sec, _ = _replace_div_block(sec, 'hc-intro', _paras(content))
    sec, _ = _replace_div_block(sec, 'hc-faq', faq_html_ru(rec))

    def lead_sub(m):
        aid = m.group(1)
        t = ru_title(patch, aid, m.group(2).replace('Overview: ', '', 1))
        meta = m.group(3)
        if 'Start here' in meta:
            meta = meta.replace('Start here', 'Начните отсюда')
        return ('<a class="hc-row hc-row-lead" href="#/a/' + aid + '">'
                '<span class="hc-row-t">Обзор: ' + H.escape(t, quote=False) + '</span>' + meta)

    sec = re.sub(r'<a class="hc-row hc-row-lead" href="#/a/([a-z0-9_]+)">'
                 r'<span class="hc-row-t">Overview: (.*?)</span>(<span class="hc-row-m">.*?</span>)',
                 lead_sub, sec, flags=re.S)
    return sec


def _swap_home_chrome(html, patch):
    html = html.replace(
        '<h1>Hi, how can we <span class="grad">help</span>?</h1>',
        '<h1>Привет! Чем мы можем <span class="grad">помочь</span>?</h1>')
    html = html.replace(
        'Everything about Fast Scheduler &mdash; scheduling, recurring posts, '
        'sender bots, channels, statistics and payments. '
        'Search it or browse by topic.',
        'Всё о Fast Scheduler — планирование, регулярные посты, '
        'боты-отправители, каналы, статистика и оплата. '
        'Ищите или выбирайте тему ниже.')
    html = re.sub(
        r'Scheduling, delivery, bots, payments and tools (?:&mdash;|—|–|-) '
        r'pick a section to dive in\.',
        'Планирование, доставка, боты, оплата и инструменты — '
        'выберите раздел.', html)
    html = re.sub(
        r'(<span>)(\d+)( articles &middot; )(\d+)( categories</span>)',
        lambda m: (m.group(1) + m.group(2) + ' '
                   + plural(int(m.group(2)), 'статья', 'статьи', 'статей')
                   + ' · ' + m.group(4) + ' '
                   + plural(int(m.group(4)), 'категория', 'категории', 'категорий')
                   + '</span>'), html)
    html = html.replace('Can&rsquo;t find an answer?', 'Не нашли ответ?')
    html = html.replace('<i>recurring posts</i>', '<i>регулярные посты</i>')
    html = html.replace('<i>sender bot</i>', '<i>бот-отправитель</i>')
    html = html.replace('<i>refund</i>', '<i>возврат</i>')
    html = html.replace('placeholder="Search the help center…"',
                        'placeholder="Поиск по центру помощи…"')
    html = html.replace('aria-label="Search the help center"',
                        'aria-label="Поиск по центру помощи"')
    html = html.replace('placeholder="Search articles"',
                        'placeholder="Поиск статей"')
    html = html.replace('aria-label="Search help articles"',
                        'aria-label="Поиск по справке"')
    html = html.replace('aria-label="Search results"',
                        'aria-label="Результаты поиска"')
    html = html.replace('aria-label="Help center quick search"',
                        'aria-label="Быстрый поиск по справке"')
    html = html.replace('aria-label="Help topics"',
                        'aria-label="Темы помощи"')
    html = html.replace('aria-label="Breadcrumb"',
                        'aria-label="Хлебные крошки"')
    html = html.replace('aria-label="Open navigation"',
                        'aria-label="Открыть навигацию"')
    html = html.replace('aria-label="Chat with support"',
                        'aria-label="Чат поддержки"')
    html = html.replace('aria-label="Settings"', 'aria-label="Настройки"')
    html = html.replace('aria-label="Close contents"',
                        'aria-label="Закрыть содержание"')
    html = html.replace('aria-label="Open contents"',
                        'aria-label="Открыть содержание"')
    html = html.replace('aria-label="Hide contents"',
                        'aria-label="Скрыть содержание"')

    def band_sub(m):
        cid = m.group(1)
        if cid == 'misc':
            t = 'Другие темы'
        else:
            t = ru_title(patch, cid, m.group(2))
        n = int(m.group(3))
        return ('<a href="#/c/' + cid + '"><b>'
                + H.escape(t, quote=False) + '</b><span>' + str(n) + ' '
                + plural(n, 'статья', 'статьи', 'статей') + '</span>')

    html = re.sub(r'<a href="#/c/([a-z0-9_]+)"><b>(.*?)</b><span>([0-9]+) articles</span></a>',
                  band_sub, html, flags=re.S)

    def band2_sub(m):
        cid = m.group(1)
        if cid == 'misc':
            t = 'Другие темы'
        else:
            t = ru_title(patch, cid, m.group(3))
        return m.group(0)[:m.start(3) - m.start(0)] + H.escape(t, quote=False) + '</b>'

    html = re.sub(r'<a href="#/c/([a-z0-9_]+)">((?:(?!</a>).)*?)<b>(.*?)</b>',
                  band2_sub, html, flags=re.S)
    return html


def global_swaps(html, patch):
    html = _swap_home_chrome(html, patch)
    def row_sub(m):
        aid = m.group(1)
        t = ru_title(patch, aid, m.group(2))
        meta = m.group(3)
        qm = re.match(r'(\d+) Q&amp;A', meta)
        if qm:
            n = int(qm.group(1))
            meta = str(n) + ' ' + plural(n, 'вопрос и ответ', 'вопроса и ответа', 'вопросов и ответов')
        elif meta == 'Guide':
            meta = 'Гайд'
        elif meta == 'Start here':
            meta = 'Начните отсюда'
        return ('<a class="hc-row" href="#/a/' + aid + '">'
                '<span class="hc-row-t">' + H.escape(t, quote=False) + '</span>'
                '<span class="hc-row-m">' + meta + '</span>')

    html = re.sub(r'<a class="hc-row" href="#/a/([a-z0-9_]+)">'
                  r'<span class="hc-row-t">(.*?)</span>'
                  r'<span class="hc-row-m">(.*?)</span>',
                  row_sub, html, flags=re.S)

    def pager_sub(m):
        aid = m.group(2)
        return m.group(1) + H.escape(ru_title(patch, aid, m.group(3)), quote=False) + '</b>'

    html = re.sub(r'(<a class="hc-card (?:next|prev)" href="#/a/([a-z0-9_]+)">(?:(?!</a>).)*?<b>)(.*?)</b>',
                  pager_sub, html, flags=re.S)
    html = re.sub(r'(<a class="hc-toc-navc (?:next|prev)" href="#/a/([a-z0-9_]+)"[^>]*>(?:(?!</a>).)*?<b>)(.*?)</b>',
                  pager_sub, html, flags=re.S)

    def chip_sub(m):
        aid = m.group(1)
        return (m.group(1) and '<a class="hc-chip" href="#/a/' + aid + '"><span>'
                + H.escape(ru_title(patch, aid, m.group(2)), quote=False) + '</span>')

    html = re.sub(r'<a class="hc-chip" href="#/a/([a-z0-9_]+)"><span>(.*?)</span>',
                  lambda m: '<a class="hc-chip" href="#/a/' + m.group(1) + '"><span>'
                  + H.escape(ru_title(patch, m.group(1), m.group(2)), quote=False) + '</span>',
                  html, flags=re.S)

    def rail_sub(m):
        aid = m.group(1)
        return ('<a href="#/a/' + aid + '"' + m.group(2) + '>'
                + H.escape(ru_title(patch, aid, m.group(3)), quote=False) + '</a>')

    html = re.sub(r'<a href="#/a/([a-z0-9_]+)"([^>]*?)>([^<>]+?)</a>', rail_sub, html, flags=re.S)

    def others_sub(m):
        cid = m.group(1)
        if '<' in m.group(2):
            return m.group(0)
        if cid == 'misc':
            t = 'Другие темы'
        else:
            t = ru_title(patch, cid, m.group(2))
        return '<a href="#/c/' + cid + '">' + H.escape(t, quote=False) + '</a>'

    html = re.sub(r'<a href="#/c/([a-z0-9_]+)">(.*?)</a>', others_sub, html, flags=re.S)
    html = re.sub(r'<span class="dot">([0-9]+) Q&amp;A</span>',
                  lambda m: '<span class="dot">' + m.group(1) + ' '
                  + plural(int(m.group(1)), 'вопрос и ответ', 'вопроса и ответа', 'вопросов и ответов') + '</span>',
                  html, flags=re.S)
    html = _swap_idx(html, patch)
    html = _swap_misc_prev(html, patch)
    def _span_end(html, open_start):
        depth = 0
        i = open_start
        n = len(html)
        while i < n:
            if html.startswith('<span', i):
                j = html.find('>', i)
                if j < 0:
                    return None
                if html[j - 1] == '/':
                    i = j + 1
                    continue
                depth += 1
                i = j + 1
            elif html.startswith('</span>', i):
                depth -= 1
                i += 7
                if depth == 0:
                    return i
            else:
                i += 1
        return None

    def cat_sub(m):
        cid = m.group(1)
        inner = m.group(2)
        if cid == 'misc':
            title = 'Другие темы'
            kids = []
        else:
            rec = patch.get(cid, {})
            title = (clean_ru(rec.get('title', '')) or '').strip() or cid
            kids = []
            for k in (rec.get('children') or []):
                t = (clean_ru(patch.get(k, {}).get('title', '')) or '').strip()
                if t:
                    kids.append(t)
        inner = re.sub(r'(<span class="hc-cat-t">).*?(</span>)',
                       lambda mm: mm.group(1) + H.escape(title, quote=False) + mm.group(2),
                       inner, count=1, flags=re.S)
        nm = re.search(r'(<span class="hc-cat-c">)([0-9]+)( articles</span>)', inner)
        if nm:
            n = int(nm.group(2))
            inner = (inner[:nm.start()] + nm.group(1) + str(n) + ' '
                     + plural(n, 'статья', 'статьи', 'статей') + '</span>' + inner[nm.end():])
        ps = inner.find('<span class="hc-cat-prev">')
        if ps >= 0 and kids:
            pe = _span_end(inner, ps)
            if pe is not None:
                prev = ''.join('<span>' + H.escape(t, quote=False) + '</span>' for t in kids[:3])
                more_n = max(0, len(kids) - 3)
                if more_n:
                    prev += '<span>+' + str(more_n) + ' ещё</span>'
                inner = inner[:ps] + '<span class="hc-cat-prev">' + prev + '</span>' + inner[pe:]
        return '<a class="hc-cat hc-card" href="#/c/' + cid + '">' + inner + '</a>'

    html = re.sub(r'<a class="hc-cat hc-card" href="#/c/([a-z0-9_]+)">(.*?)</a>',
                  cat_sub, html, flags=re.S)
    return html


def apply_surgery(html, patch, en_data):
    spans, _ = split_sections(html)
    out = []
    pos = 0
    stats = {'art': 0, 'cat': 0}
    for kind, ident, a, b in spans:
        out.append(html[pos:a])
        sec = html[a:b]
        if kind == 'article':
            sec = surgery_article(sec, ident, patch, en_data)
            stats['art'] += 1
        elif kind == 'category':
            sec = surgery_category(sec, ident, patch)
            stats['cat'] += 1
        out.append(sec)
        pos = b
    out.append(html[pos:])
    html = ''.join(out)
    html = global_swaps(html, patch)
    return html, stats

_EN_TITLES = None


def _en_titles():
    global _EN_TITLES
    if _EN_TITLES is None:
        import json
        from build_ru_pages import SITE as _SITE
        src = io_open(_SITE + '/scripts/help-data.js')
        import re as _re
        arr = json.loads(_re.search(r'__HELP_DATA=(\[.*\])', src, _re.S).group(1))
        _EN_TITLES = {x['id']: x.get('t', '') for x in arr}
    return _EN_TITLES


def io_open(path):
    import io as _io
    return _io.open(path, encoding='utf-8').read()


def _swap_idx(html, patch):
    def h3_sub(m):
        cid = m.group(1)
        if cid == 'misc':
            t = 'Другие темы'
        else:
            t = ru_title(patch, cid, m.group(2))
        n = int(m.group(3))
        return ('<h3><a href="#/c/' + cid + '">' + H.escape(t, quote=False) + '</a><span>'
                + str(n) + ' ' + plural(n, 'гайд', 'гайда', 'гайдов') + '</span></h3>')
    html = re.sub(r'<h3><a href="help/c/([a-z0-9_]+)\.html">(.*?)</a><span>([0-9]+) guides</span></h3>',
                  h3_sub, html, flags=re.S)
    html = re.sub(r'<li><a href="help/a/([a-z0-9_]+)\.html">(.*?)</a></li>',
                  lambda m: '<li><a href="#/a/' + m.group(1) + '">'
                  + H.escape(ru_title(patch, m.group(1), m.group(2)), quote=False) + '</a></li>',
                  html, flags=re.S)
    html = html.replace('<h2 id="hcIndexH">Every help article, by topic</h2>',
                        '<h2 id="hcIndexH">Все статьи помощи по темам</h2>')
    html = html.replace('Each guide below also has its own page, so you can link to it, bookmark it or search for it directly.',
                        'У каждого гайда ниже есть своя страница — можно делиться ссылкой, добавлять в закладки и искать напрямую.')
    return html


def _swap_misc_prev(html, patch):
    ent = _en_titles()
    rev = {}
    for aid, et in ent.items():
        t = ru_title(patch, aid, '')
        if et and t:
            rev[et] = t
    def prev_sub(m):
        inner = m.group(1)
        def sp(mm):
            return '<span>' + H.escape(rev.get(mm.group(1), mm.group(1)), quote=False) + '</span>'
        inner = re.sub(r'<span>(.*?)</span>', sp, inner, flags=re.S)
        inner = re.sub(r'<span>\+([0-9]+) more</span>',
                       lambda mm: '<span>+' + mm.group(1) + ' ещё</span>', inner, flags=re.S)
        return '<span class="hc-cat-prev">' + inner + '</span>'
    return re.sub(r'<span class="hc-cat-prev">((?:(?!</a>).)*)</span>', prev_sub, html, flags=re.S)
