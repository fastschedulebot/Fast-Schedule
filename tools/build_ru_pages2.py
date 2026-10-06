#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Part 2: RU landing / help-hub / 404 builders. Imported by build_ru_pages."""

import io
import json
import os
import re
import html as H

from build_ru_pages3 import merged_map
from build_ru_pages import (
    ROOT, SITE, BASE, NL, load_map, transform, set_head, fix_asset_paths,
    load_ru_articles, clean_ru, build_help_data_ru,
)

HUB_TITLE_RU = 'Центр помощи — Fast Scheduler для Telegram'
HUB_DESC_RU = ('Справочный центр Fast Scheduler с поиском: '
               '308 ответов о планировании, регулярных постах, '
               'ботах-отправителях, каналах, Premium и оплате.')
IDX_TITLE_RU = 'Fast Scheduler — Планировщик постов для Telegram-каналов'
IDX_DESC_RU = ('Fast Scheduler — бесплатный Telegram-бот: планирование '
               'и публикация постов канала, аналитика. Планируйте неделю '
               'контента в одном чате и публикуйте от своего бота.')
NF_TITLE_RU = 'Страница не найдена — Fast Scheduler'
NF_DESC_RU = ('Такой страницы Fast Scheduler не существует. Поищите '
              'в Центре помощи или откройте блог — руководства '
              'по планированию постов Telegram-канала.')


def _write(path, text, attempts=8, delay=0.25):
    import time
    for i in range(attempts):
        try:
            with io.open(path, 'w', encoding='utf-8', newline=NL) as fh:
                fh.write(text)
            return True
        except OSError:
            if i == attempts - 1:
                raise
            time.sleep(delay * (i + 1))
    return False


def inject_alts(path, url_ru, url_en):
    try:
        s = io.open(path, encoding='utf-8').read()
    except IOError:
        return False
    mark = re.compile('<!--fs:ru-alt-->.*?<!--/fs:ru-alt-->' + NL + '?', re.S)
    s = mark.sub('', s)
    if '</head>' not in s:
        return False
    block = ('<!--fs:ru-alt-->' + NL
             + '<link rel="alternate" hreflang="ru" href="' + url_ru + '">' + NL
             + '<link rel="alternate" hreflang="en" href="' + url_en + '">' + NL
             + '<link rel="alternate" hreflang="x-default" href="' + url_en + '">' + NL
             + '<!--/fs:ru-alt-->')
    s = s.replace('</head>', block + '</head>', 1)
    return _write(path, s)


def swap_hub_titles(html, patch):
    def ru_title(aid, fallback):
        tr = patch.get(aid, {})
        t = clean_ru(tr.get('title', '')) or ''
        return t.strip() or fallback

    def row_sub(m):
        aid = m.group(1)
        return m.group(0)[:m.group(0).find('>', m.group(0).find('hc-row-t')) + 1] \
            + H.escape(ru_title(aid, m.group(2)), quote=False) + '</span>'

    html = re.sub(r'href="#/a/([a-z0-9_]+)">(?:(?!</a>).)*?<span class="hc-row-t">(.*?)</span>',
                  lambda m: m.group(0)[:m.start(2) - m.start(0)]
                  + H.escape(ru_title(m.group(1), m.group(2)), quote=False)
                  + m.group(0)[m.end(2) - m.start(0):],
                  html, flags=re.S)

    def pager_sub(m):
        aid = m.group(2)
        return (m.group(1)
                + H.escape(ru_title(aid, m.group(3)), quote=False) + '</b>')

    html = re.sub(r'(<a class="hc-card (?:next|prev)" href="#/a/([a-z0-9_]+)">(?:(?!</a>).)*?<b>)(.*?)</b>',
                  pager_sub, html, flags=re.S)
    html = re.sub(r'(<a class="hc-toc-navc (?:next|prev)" href="#/a/([a-z0-9_]+)"[^>]*>(?:(?!</a>).)*?<b>)(.*?)</b>',
                  pager_sub, html, flags=re.S)
    return html


def swap_hub_cats(html, patch):
    def cat_sub(m):
        cid = m.group(1)
        inner = m.group(2)
        rec = patch.get(cid, {})
        title = (clean_ru(rec.get('title', '')) or '').strip()
        kids = []
        for k in (rec.get('children') or []):
            t = clean_ru(patch.get(k, {}).get('title', ''))
            if t:
                kids.append((k, t.strip()))
        if title:
            inner = re.sub(r'(<span class="hc-cat-t">).*?(</span>)',
                           lambda mm: mm.group(1) + H.escape(title, quote=False) + mm.group(2),
                           inner, count=1, flags=re.S)
        nm = re.search(r'(<span class="hc-cat-c">)(\d+)( articles</span>)', inner)
        if nm:
            n = int(nm.group(2))
            word = plural_ru(n, 'статья', 'статьи', 'статей')
            inner = (inner[:nm.start()] + nm.group(1) + str(n) + ' ' + word + '</span>'
                     + inner[nm.end():])
        pm = re.search(r'<span class="hc-cat-prev">(.*?)</span>\s*</a?\s*$', inner, re.S)
        if pm and kids:
            prev = ''.join('<span>' + H.escape(t, quote=False) + '</span>' for _, t in kids[:3])
            more_n = max(0, len(kids) - 3)
            if more_n:
                prev += '<span>+' + str(more_n) + ' ещё</span>'
            inner = inner[:pm.start(1)] + prev + inner[pm.end(1):]
        return '<a class="hc-cat hc-card" href="#/c/' + cid + '">' + inner + '</a>'

    html = re.sub(r'<a class="hc-cat hc-card" href="#/c/([a-z0-9_]+)">(.*?)</a>',
                  cat_sub, html, flags=re.S)

    def qna_sub(m):
        n = int(m.group(1))
        return '>' + str(n) + ' ' + plural_ru(n, 'вопрос и ответ', 'вопроса и ответа', 'вопросов и ответов') + '<'

    html = re.sub(r'>(\d+) Q&A<', qna_sub, html)
    return html


def plural_ru(n, one, few, many):
    n = abs(int(n))
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and (n % 100 < 12 or n % 100 > 14):
        return few
    return many


def rebuild_hub_ld(html, patch):
    blocks = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    out = html
    for m in reversed(blocks):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        t = d.get('@type')
        if t == 'BreadcrumbList':
            els = d.get('itemListElement', [])
            if len(els) >= 2:
                els[1]['name'] = 'Центр помощи'
                els[1]['item'] = BASE + '/ru/help.html'
            d['itemListElement'] = els
        elif t == 'CollectionPage':
            d['name'] = 'Центр помощи Fast Scheduler'
            d['url'] = BASE + '/ru/help.html'
            d['description'] = HUB_DESC_RU
            d['inLanguage'] = 'ru'
            main = d.get('mainEntity', {})
            for el in main.get('itemListElement', []):
                url = el.get('url', '')
                mm = re.search(r'/help/a/([a-z0-9_]+)\.html', url)
                if mm and mm.group(1) in patch:
                    tr = patch[mm.group(1)]
                    title = (clean_ru(tr.get('title', '')) or '').strip()
                    if title:
                        el['name'] = title
                    el['url'] = BASE + '/ru/help/a/' + mm.group(1) + '.html'
            d['mainEntity'] = main
        else:
            continue
        new = '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '</script>'
        out = out[:m.start()] + new + out[m.end():]
    return out


def build_help_hub(MAP, patch, audit_only=False):
    src = os.path.join(SITE, 'help.html')
    html = io.open(src, encoding='utf-8').read()
    html = swap_hub_titles(html, patch)
    html = swap_hub_cats(html, patch)
    html = rebuild_hub_ld(html, patch)
    html, unmapped = transform(html, merged_map(MAP))
    m = re.search(r'scripts/help-data\.js\?v=([^"]+)', html)
    ver = m.group(1) if m else '20261005a1'
    html = html.replace('scripts/help-data.js?v=' + ver,
                        'scripts/help-data-ru.js?v=' + ver)
    html = fix_asset_paths(html)
    html = set_head(html, HUB_TITLE_RU, HUB_DESC_RU,
                    BASE + '/ru/help.html', BASE + '/help.html')
    if audit_only:
        return None, unmapped
    out = os.path.join(SITE, 'ru', 'help.html')
    _write(out, html)
    inject_alts(src, BASE + '/ru/help.html', BASE + '/help.html')
    return out, unmapped


def build_index(MAP, audit_only=False):
    src = os.path.join(SITE, 'index.html')
    html = io.open(src, encoding='utf-8').read()
    html, unmapped = transform(html, MAP)
    html = fix_asset_paths(html)
    html = html.replace('<i>your</i>', '<i>ваши</i>')
    html = html.replace('aria-label="Previous plan"', 'aria-label="Предыдущий тариф"')
    html = html.replace('aria-label="Next plan"', 'aria-label="Следующий тариф"')
    html = html.replace('title="Fast Scheduler Blog"', 'title="Блог Fast Scheduler"')
    html = set_head(html, IDX_TITLE_RU, IDX_DESC_RU, BASE + '/ru/', BASE + '/')
    if audit_only:
        return None, unmapped
    out = os.path.join(SITE, 'ru', 'index.html')
    _write(out, html)
    inject_alts(src, BASE + '/ru/', BASE + '/')
    return out, unmapped


def build_404(MAP):
    src = os.path.join(SITE, '404.html')
    html = io.open(src, encoding='utf-8').read()
    html, unmapped = transform(html, merged_map(MAP))
    html = set_head(html, NF_TITLE_RU, NF_DESC_RU, BASE + '/ru/404.html',
                    BASE + '/404.html')
    out = os.path.join(SITE, 'ru', '404.html')
    _write(out, html)
    return out, unmapped


def build_data_file(patch):
    js, _, _ = build_help_data_ru(patch)
    out = os.path.join(SITE, 'scripts', 'help-data-ru.js')
    _write(out, js)
    return out
