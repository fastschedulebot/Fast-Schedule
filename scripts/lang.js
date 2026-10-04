// Website language: EN/RU switcher, persisted in localStorage (fs-lang).
// Liquid-glass EN/RU segmented control in #settingsMenu.
// Full-site RU: chrome (settings/nav/footer/search) + index sections
// (hero/features/how/pricing/FAQ/CTA) + legal/blog/help chrome
// via exact-text map with safe revert (dataset.fsEn). Bodies of help/blog
// articles stay EN (phase 2) — chrome and landing are fully RU.
(function () {
  'use strict';
  var STR = {
    en: {
      settings: 'Settings', dark: 'Dark mode', anim: 'Animations', fx: 'Effects',
      keys: 'Hotkeys', seeKeys: 'See hotkeys', help: 'Help', support: 'Support chat',
      openBot: 'Open Bot', langLabel: 'Language', openHelp: 'Open Help Center',
      recent: 'Recent searches', searchPh: 'Search the help center…',
      openMenu: 'Open menu', closeMenu: 'Close menu'
    },
    ru: {
      settings: 'Настройки', dark: 'Тёмная тема', anim: 'Анимации', fx: 'Эффекты',
      keys: 'Горячие клавиши', seeKeys: 'Показать клавиши', help: 'Помощь', support: 'Чат поддержки',
      openBot: 'Открыть бота', langLabel: 'Язык', openHelp: 'Открыть центр помощи',
      recent: 'Недавние запросы', searchPh: 'Поиск по центру помощи…',
      openMenu: 'Открыть меню', closeMenu: 'Закрыть меню'
    }
  };

  // Exact English visible strings -> Russian. Landing-first, then shared chrome.
  // Keep brand names, commands, URLs untouched.
  var RU_MAP = {
    // nav
    'Time saved': 'Экономия времени',
    'Features': 'Возможности',
    'How it works': 'Как это работает',
    'Pricing': 'Тарифы',
    'FAQ': 'Вопросы и ответы',
    'Blog': 'Блог',
    'Help': 'Помощь',
    'Open Bot': 'Открыть бота',
    // hero
    'Your channel posts itself.You just write.': 'Ваш канал публикуется сам. Вы просто пишете.',
    'Scheduled in one chat. Posted forever.': 'Запланировали в одном чате. Публикуется всегда.',
    // sections
    'How much time you get back': 'Сколько времени вы вернёте',
    'Everything a channel needs, in one chat': 'Всё для канала — в одном чате',
    'Three steps. Sixty seconds.': 'Три шага. Шестьдесят секунд.',
    'Start free. Upgrade when it pays for itself.': 'Начните бесплатно. Переходите на Premium, когда окупится.',
    'Questions, answered': 'Вопросы и ответы',
    'Your next post is already scheduled.': 'Ваш следующий пост уже запланирован.',
    // features
    'Batch scheduling': 'Пакетное планирование',
    'Recurring posts': 'Регулярные посты',
    'Rich media posts': 'Посты с медиа',
    'Stats & leaderboards': 'Статистика и рейтинги',
    'Post from your own bot': 'Публикация от вашего бота',
    'Your timezone, your rules': 'Ваш часовой пояс, ваши правила',
    'Auto reports': 'Автоматические отчёты',
    'Multi-channel + team admins': 'Мультиканальность и команда',
    'Encrypted backups': 'Зашифрованные бэкапы',
    // how
    'Open the bot & connect a channel': 'Откройте бота и подключите канал',
    'Schedule one post or fifty': 'Запланируйте один пост или пятьдесят',
    'Live your life': 'Живите своей жизнью',
    // faq / pricing chrome
    'Full plan comparison': 'Полное сравнение тарифов',
    'Is Fast Scheduler really free?': 'Fast Scheduler действительно бесплатный?',
    'How does it save me time?': 'Как он экономит моё время?',
    'Do posts come from my own bot?': 'Посты выходят от моего бота?',
    'Will posts go out if I\'m offline or asleep?': 'Выйдут ли посты, если я офлайн или сплю?',
    'Can I see who comments on my posts?': 'Видно ли, кто комментирует мои посты?',
    'Is my data safe?': 'Мои данные в безопасности?',
    'Free': 'Бесплатно',
    'Premium': 'Premium',
    'per month': 'в месяц',
    'Get started': 'Начать',
    'Try the bot': 'Попробовать бота',
    'Open Help Center': 'Открыть центр помощи',
    'Recent searches': 'Недавние запросы',
    'Search the help center…': 'Поиск по центру помощи…',
    'Search docs…': 'Поиск по документам…',
    'All articles': 'Все статьи',
    'Was this helpful?': 'Было ли это полезно?',
    'Yes': 'Да',
    'No': 'Нет',
    'Previous': 'Назад',
    'Next': 'Далее',
    'Table of contents': 'Содержание',
    'Best result': 'Лучший результат',
    'More results': 'Другие результаты',
    'All results': 'Все результаты',
    'Up next': 'Далее',
    'Now reading': 'Читаете сейчас',
    'No previous article': 'Нет предыдущей статьи',
    'No next article': 'Нет следующей статьи',
    'Other categories:': 'Другие категории:',
    'Related topics': 'Похожие темы',
    'This article has no sections.': 'В этой статье нет разделов.',
    '0 results': 'Ничего не найдено',
    'No exact match for': 'Точного совпадения нет:',
    '— a human answers every ticket.': '— на каждый вопрос отвечает человек.',
    'No results found for “': 'Ничего не найдено: «',
    'Try other words — for example': 'Попробуйте другие слова — например',
    'Back to Help Center': 'Назад в центр помощи',
    'That topic doesn’t exist (or moved). Try the search on the home page.': 'Такой темы нет. Воспользуйтесь поиском на главной.',
    'Maybe you meant:': 'Возможно, вы имели в виду:',
    'Still stuck?': 'Не нашли ответ?',
    'Ask in the bot': 'Спросите в боте',
    'You mean:': 'Вы имеете в виду:',
    'On this page': 'На этой странице',
    // NOTE: 'Privacy Policy' / 'Refund Policy' intentionally absent here —
    // those titles need per-context Russian cases, handled by scoped FIXUPs
    // in ru-chrome.js plus multi-node window keys in ru-content.js. A
    // whole-node MAP entry would mistranslate them inside sentences.
    'Terms of Service': 'Условия использования',
    'Settings': 'Настройки',
    'Dark mode': 'Тёмная тема',
    'Animations': 'Анимации',
    'Effects': 'Эффекты',
    'Hotkeys': 'Горячие клавиши',
    'See hotkeys': 'Показать клавиши',
    'Support chat': 'Чат поддержки',
    'Language': 'Язык',
    'Back to top': 'Наверх',
    'Back to blog': 'Назад в блог',
    'Back to help': 'Назад в помощь',
    'Related articles': 'Похожие статьи',
    'Read more': 'Читать далее',
    'min read': 'мин чтения',
    'Last updated': 'Обновлено',
    'Page not found': 'Страница не найдена',
    'Go home': 'На главную',
    'All topics': 'Все темы',
    'Growth': 'Рост',
    'Content': 'Контент',
    'Bots & Tools': 'Боты и инструменты',
    'Premium & Safety': 'Premium и безопасность',
    'Platform': 'Платформа',
    'Monetization': 'Монетизация',
    'Subscribers, swaps, discoverability and retention — the playbooks that compound.': 'Подписчики, свапы, поиск и удержание — стратегии, которые работают на перспективу.',
    'Formatting, calendars and content systems that keep a channel alive.': 'Оформление, календари и контент-системы, которые держат канал на плаву.',
    'The bot stack behind successful channels — scheduling, analytics, moderation.': 'Стек ботов успешных каналов — планирование, аналитика, модерация.',
    'Verification, Premium perks, Mini Apps — the platform layer behind channels.': 'Верификация, преимущества Premium, Mini Apps — платформа за кулисами каналов.',
    'How Telegram itself works: channels vs groups, bot safety, algorithms.': 'Как устроен сам Telegram: каналы и группы, безопасность ботов, алгоритмы.',
    'Ads, Stars, subscriptions and products — what pays, and when.': 'Реклама, Stars, подписки и товары — что приносит деньги и когда.'
  };

  var META = {
    title: {
      en: 'Fast Scheduler — Telegram Channel Post Scheduler',
      ru: 'Fast Scheduler — Планировщик постов для Telegram-каналов'
    },
    desc: {
      en: 'Fast Scheduler is a free Telegram bot that schedules, publishes and tracks your channel posts. Batch-schedule a week in one chat, post from your own bot.',
      ru: 'Fast Scheduler — бесплатный Telegram-бот: планирование и публикация постов канала, аналитика. Планируйте неделю контента в одном чате и публикуйте от своего бота.'
    }
  };

  function get() {
    try {
      var saved = localStorage.getItem('fs-lang');
      if (saved === 'ru' || saved === 'en') return saved;
    } catch (e) {}
    // No stored preference: follow the language the server actually served.
    // /ru/ pages are built with <html lang="ru">; without this a first-time
    // visitor to /ru/... would be flipped back to English by this script.
    try {
      return document.documentElement.getAttribute('lang') === 'ru' ? 'ru' : 'en';
    } catch (e) { return 'en'; }
  }
  function set(lang) {
    lang = lang === 'ru' ? 'ru' : 'en';
    try { localStorage.setItem('fs-lang', lang); } catch (e) {}
    document.documentElement.setAttribute('lang', lang);
    apply(lang);
    try { window.dispatchEvent(new CustomEvent('fs-lang-change', { detail: { lang: lang } })); } catch (e) {}
  }
  function t(key) { return (STR[get()] || STR.en)[key] || STR.en[key] || key; }

  // Extended RU dictionary lives in ru-chrome.js (separate file, loaded with
  // `defer` BEFORE this file, so it is always available synchronously —
  // switching languages translates the whole page instantly, no refresh.
  // Merged over the inline core above, which stays as an offline fallback.
  var FIXUPS = [];
  try {
    if (window.FS_RU_CHROME) {
      if (window.FS_RU_CHROME.STR) STR.ru = window.FS_RU_CHROME.STR;
      // ru-chrome.js ships META as a flat {title, desc} pair of RU strings,
      // while lang.js keeps the nested {en, ru} shape and reads META.title.en
      // on the home page. Assigning the flat object straight over META left
      // META.title.en undefined, so every load stamped document.title and
      // the meta description with the literal text "undefined" - which is
      // also what a crawler rendering the page saw.
      if (window.FS_RU_CHROME.META) {
        var rm = window.FS_RU_CHROME.META;
        if (rm.title) META.title.ru = typeof rm.title === 'string' ? rm.title : rm.title.ru;
        if (rm.desc) META.desc.ru = typeof rm.desc === 'string' ? rm.desc : rm.desc.ru;
      }
      if (window.FS_RU_CHROME.MAP) {
        for (var _ck in window.FS_RU_CHROME.MAP) RU_MAP[_ck] = window.FS_RU_CHROME.MAP[_ck];
      }
      if (window.FS_RU_CHROME.FIXUPS) FIXUPS = window.FS_RU_CHROME.FIXUPS;
    }
  } catch (e) {}

  // Elements that must NEVER be translated: product-demo mockups (phone
  // cinema, mock chats/channels, iOS home screen, review stats), code and
  // form fields. Marketing copy around them still translates node by node.
  var SKIP_SEL = '[data-no-ru],code,pre,script,style,textarea,.phone-stage,.demo,' +
    '.ios-app,.chan-msg,.sl-head,.sl-foot,.tg-header,.tg-input,.tg-explorer,.rl-notif,.fx-bar';
  function skipTextNode(n) {
    try {
      var p = n.parentNode;
      if (!p || p.nodeType !== 1) return true;
      if (p.closest('.fs-lang-seg')) return true;
      if (p.closest(SKIP_SEL)) return true;
      var tag = (p.tagName || '').toLowerCase();
      if (tag === 'script' || tag === 'style' || tag === 'code' || tag === 'pre' || tag === 'textarea') return true;
    } catch (e) { return true; }
    return false;
  }
  // Revert-safe store: text nodes cannot carry dataset, so keep originals here.
  var chromeOrig = (typeof Map !== 'undefined') ? new Map() : null;
  var chromeList = [];
  function chromeRemember(n) {
    if (chromeOrig) { if (!chromeOrig.has(n)) chromeOrig.set(n, n.nodeValue); }
    else {
      for (var i = 0; i < chromeList.length; i++) { if (chromeList[i].n === n) return; }
      chromeList.push({ n: n, t: n.nodeValue });
    }
  }
  function chromeRestore(n) {
    if (chromeOrig) {
      if (chromeOrig.has(n)) { try { n.nodeValue = chromeOrig.get(n); } catch (e) {} chromeOrig.delete(n); }
    } else {
      for (var i = 0; i < chromeList.length; i++) {
        if (chromeList[i].n === n) { try { n.nodeValue = chromeList[i].t; } catch (e) {} chromeList.splice(i, 1); break; }
      }
    }
  }
  function translateTextNode(n, ru) {
    if (!n || !n.nodeValue) return;
    if (skipTextNode(n)) return;
    // Only whole-node matches: short keys can never corrupt longer sentences,
    // and inline <svg>/<b>/<span> elements are never touched (no icon loss,
    // no broken centering — layout and formatting survive translation).
    var trimmed = n.nodeValue.trim();
    if (!trimmed || !/[A-Za-z\u00C0-\u024F\u0400-\u04FF]/.test(trimmed)) return;
    if (ru) {
      var mapped = RU_MAP[trimmed];
      if (mapped && n.nodeValue.indexOf(mapped) === -1) {
        chromeRemember(n);
        var lead = (n.nodeValue.match(/^\s*/) || [''])[0];
        var trail = (n.nodeValue.match(/\s*$/) || [''])[0];
        n.nodeValue = lead + mapped + trail;
      }
    } else {
      chromeRestore(n);
    }
  }
  function applyTree(root, ru) {
    try {
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
      var batch = [];
      var tn;
      while ((tn = walker.nextNode())) batch.push(tn);
      for (var i = 0; i < batch.length; i++) translateTextNode(batch[i], ru);
    } catch (e) {}
  }
  function applyFixups(ru) {
    if (!FIXUPS || !FIXUPS.length) return;
    FIXUPS.forEach(function (fx) {
      var sel = fx[0], attr = fx[1], en = fx[2], ruStr = fx[3];
      document.querySelectorAll(sel).forEach(function (el) {
        try {
          if (attr) {
            if (ru) {
              if (!el.dataset.fsAttrEn) el.dataset.fsAttrEn = el.getAttribute(attr) || '';
              if ((el.getAttribute(attr) || '') === en || (el.dataset.fsAttrEn || '') === en) el.setAttribute(attr, ruStr);
            } else if (el.dataset.fsAttrEn) {
              el.setAttribute(attr, el.dataset.fsAttrEn);
              delete el.dataset.fsAttrEn;
            }
          } else if ((el.textContent || '').trim() === en) {
            if (ru) {
              if (!el.dataset.fsEn) el.dataset.fsEn = en;
              el.textContent = ruStr;
            }
          } else if (ru && el.dataset.fsEn === en) {
            el.textContent = ruStr;
          } else if (!ru && el.dataset.fsEn === en) {
            el.textContent = el.dataset.fsEn;
            delete el.dataset.fsEn;
          }
        } catch (e) {}
      });
    });
  }

  // NOTE: the old element-level translateNode() was removed. It replaced
  // el.textContent on elements holding an <svg>, which destroyed icons, and
  // it skipped every element with inline tags (<b>/<span>/<br>), which left
  // split headings half-English. translateTextNode() above replaces only
  // text nodes, so markup, icons and layout always survive.

  function apply(lang) {
    var ru = lang === 'ru';
    var d = STR[lang] || STR.en;
    document.documentElement.setAttribute('lang', lang);
    // settings head
    /* the main "Settings" head only — "Reading" heads keep their own label
       and translate through the exact-text map (no EN flash, no overwrite) */
    document.querySelectorAll('#settingsMenu .gp-head:not([data-reading]):not([data-blog-reading])').forEach(function (el) {
      if (!el.dataset.fsEn) el.dataset.fsEn = el.textContent.trim();
      el.textContent = ru ? d.settings : el.dataset.fsEn;
    });
    var map = [['rowDark', d.dark], ['rowAnim', d.anim], ['rowFx', d.fx], ['rowKeys', d.keys], ['rowKeysHelp', d.seeKeys]];
    map.forEach(function (pair) {
      var row = document.getElementById(pair[0]);
      if (row) { var s = row.querySelector('span'); if (s) s.textContent = pair[1]; }
    });
    // nav CTA (svg + text)
    document.querySelectorAll('.nav-cta-sm, .nav-cta-m').forEach(function (a) {
      var txt = d.openBot;
      a.childNodes.forEach(function (n) {
        if (n.nodeType === 3 && n.textContent.trim().length > 2) n.textContent = ' ' + txt + ' ';
      });
    });
    // help menu chrome
    document.querySelectorAll('#siteMenu .help-menu-open span').forEach(function (s) { s.textContent = d.openHelp; });
    var rt = document.getElementById('helpRecentTitle');
    if (rt) rt.textContent = d.recent;
    document.querySelectorAll('#helpSearchInput').forEach(function (inp) {
      inp.setAttribute('placeholder', d.searchPh);
      inp.setAttribute('aria-label', d.searchPh);
    });
    var burger = document.getElementById('navBurger');
    if (burger) burger.setAttribute('aria-label', ru ? d.openMenu : STR.en.openMenu);
    // data-i18n elements (templates that opt in)
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      var dict = I18N[key];
      if (dict) {
        var v = ru ? (dict.ru || dict.en) : dict.en;
        if (v) el.textContent = v;
      }
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-ph');
      var dict = I18N[key];
      if (dict) el.setAttribute('placeholder', ru ? (dict.ru || dict.en) : dict.en);
    });
    // generic exact-text map across body (landing + shared chrome).
    // Text-node level: SVG icons, <b>/<span> formatting and alignment survive.
    applyTree(document.body, ru);
    applyFixups(ru);
    // full article bodies (help center + blog titles/descs), lazy + revert-safe
    try { translateContent(ru); } catch (e) {}
    // segmented control state + label
    document.querySelectorAll('.fs-lang-label').forEach(function (el) { el.textContent = d.langLabel; });
    document.querySelectorAll('.fs-lang-seg button').forEach(function (b) {
      var on = b.getAttribute('data-lang') === lang;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.classList.toggle('on', on);
    });
    // title + meta description (home only; articles keep their own)
    try {
      if (document.body && document.body.classList.contains('home')) {
        document.title = ru ? META.title.ru : META.title.en;
        var md = document.querySelector('meta[name="description"]');
        if (md) md.setAttribute('content', ru ? META.desc.ru : META.desc.en);
      }
    } catch (e) {}
    try {
      var ev = new CustomEvent('fs-lang-applied', { detail: { lang: lang } });
      window.dispatchEvent(ev);
    } catch (e) {}
  }

  // ---- Article-body RU translation (help center + blog titles/descs) ----
  // EN sentences come from the bot's own RU translations (ru-content.js,
  // lazy-loaded via this file's own <script> path, so it works at any page
  // depth). Matching works across inline tags: exact text nodes, 2-3 node
  // windows inside one block, and sentence substrings. Revert-safe: every
  // touched text node is restored verbatim, so no listeners ever break.
  var contentOrig = null;
  var contentDone = false;
  var contentStarted = false;
  var contentLoading = false;
  var origTitle = null;

  function normContent(s) {
    return s.replace(/\s+/g, ' ')
      .replace(/^\s+|\s+$/g, '')
      .replace(/([A-Za-z\u00c0-\u024f\u0400-\u04ff])(\d+\.)/g, '$1 $2')
      .replace(/([.!?])([A-Z\u0410-\u042f\u0401])/g, '$1 $2');
  }
  function keepWS(orig, val) {
    var lead = (orig.match(/^\s*/) || [''])[0];
    var trail = (orig.match(/\s*$/) || [''])[0];
    return lead + val + trail;
  }
  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function ensureContent(cb) {
    if (window.FS_RU_CONTENT) { cb(); return; }
    if (contentLoading) { setTimeout(function () { ensureContent(cb); }, 300); return; }
    contentLoading = true;
    var src = 'scripts/ru-content.js?v=20261004b2';
    try {
      var self = document.querySelector('script[src*="lang.js"]');
      if (self) src = self.getAttribute('src').replace(/lang\.js.*$/, 'ru-content.js?v=20261004b2');
    } catch (e) {}
    var el = document.createElement('script');
    el.src = src;
    el.onload = function () { cb(); };
    el.onerror = function () { contentLoading = false; contentStarted = false; };
    document.head.appendChild(el);
  }
  function contentTouch(n) {
    for (var i = 0; i < contentOrig.length; i++) {
      if (contentOrig[i].n === n) return;
    }
    contentOrig.push({ n: n, t: n.nodeValue });
  }
  function contentSet(n, val) {
    if (n.nodeValue === val) return;
    contentTouch(n);
    n.nodeValue = val;
  }
  function skipContentNode(n) {
    var p = n.parentNode;
    while (p && p.nodeType === 1) {
      var t = (p.tagName || '').toLowerCase();
      if (t === 'code' || t === 'pre' || t === 'script' || t === 'style' || t === 'textarea') return true;
      p = p.parentNode;
    }
    return false;
  }
  function blockOf(n, scope) {
    var p = n.parentNode;
    while (p && p !== scope) {
      var t = (p.tagName || '').toLowerCase();
      if (/^(p|li|h1|h2|h3|h4|h5|h6|td|th|div|section|article|ul|ol|blockquote|summary)$/.test(t)) return p;
      p = p.parentNode;
    }
    return scope;
  }
  function applyContent() {
    var dict = window.FS_RU_CONTENT || {};
    var keys = [];
    for (var k in dict) {
      if (Object.prototype.hasOwnProperty.call(dict, k) && !RU_MAP[k]) keys.push(k);
    }
    if (!keys.length) return;
    keys.sort(function (a, b) { return b.length - a.length; });
    var lookup = {};
    var anchor = {};
    keys.forEach(function (kk) {
      lookup[kk] = dict[kk];
      var m = kk.toLowerCase().match(/[a-z\u00c0-\u024f\u0400-\u04ff]{4,}/);
      if (m) { var ak = m[0]; if (!Object.prototype.hasOwnProperty.call(anchor, ak)) anchor[ak] = []; anchor[ak].push(kk); }
    });
    var scopes = document.querySelectorAll('.doc, .blog-doc, .bento, .blog-chips');
    if (!scopes.length) return;
    Array.prototype.forEach.call(scopes, function (scope) {
      // archived legal versions stay in their original language
      try { if (scope.closest('.archived')) return; } catch (e) {}
      var nodes = [];
      var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, null, false);
      var tn;
      while ((tn = walker.nextNode())) {
        if (!tn.nodeValue || !/[^\s]/.test(tn.nodeValue)) continue;
        if (skipContentNode(tn)) continue;
        nodes.push(tn);
      }
      if (!nodes.length) return;
      var done = nodes.map(function () { return false; });
      var i, norm;
      // pass 1: exact full-node matches (plus truncated-card … fallback)
      nodes.forEach(function (n, idx) {
        norm = normContent(n.nodeValue);
        var hit = lookup[norm];
        if (!hit && /[….]{1,3}\s*$/.test(norm)) {
          var short = norm.replace(/[…\s.]+$/, '');
          hit = lookup[short];
        }
        if (hit) { contentSet(n, keepWS(n.nodeValue, hit)); done[idx] = true; }
      });
      // pass 2: 3- and 2-node windows inside one block (inline-tag splits)
      [3, 2].forEach(function (w) {
        for (i = 0; i + w <= nodes.length; i++) {
          var free = true;
          for (var j = 0; j < w; j++) { if (done[i + j]) { free = false; break; } }
          if (!free) continue;
          var blk = blockOf(nodes[i], scope);
          var same = true;
          for (j = 1; j < w; j++) { if (blockOf(nodes[i + j], scope) !== blk) { same = false; break; } }
          if (!same) continue;
          var joined = '';
          for (j = 0; j < w; j++) joined += nodes[i + j].nodeValue;
          norm = normContent(joined);
          if (lookup[norm]) {
            var lead = (nodes[i].nodeValue.match(/^\s*/) || [''])[0];
            var trail = (nodes[i + w - 1].nodeValue.match(/\s*$/) || [''])[0];
            contentSet(nodes[i], lead + lookup[norm] + (w === 1 ? trail : ''));
            for (j = 1; j < w; j++) contentSet(nodes[i + j], j === w - 1 ? trail : '');
            for (j = 0; j < w; j++) done[i + j] = true;
          }
        }
      });
      // pass 3: sentence substrings inside long untouched nodes (anchored)
      nodes.forEach(function (n, idx) {
        if (done[idx] || n.nodeValue.length < 40) return;
        var words = n.nodeValue.toLowerCase().match(/[a-z\u00c0-\u024f\u0400-\u04ff]{4,}/g) || [];
        var seen = {};
        words.forEach(function (wd) {
          if (seen[wd]) return;
          seen[wd] = true;
          var cands = Object.prototype.hasOwnProperty.call(anchor, wd) ? anchor[wd] : null;
          if (!cands) return;
          cands.forEach(function (kk) {
            if (kk.length < 12 || kk.length > n.nodeValue.length + 20) return;
            var re = new RegExp('(^|[^A-Za-z\\u00c0-\\u024f\\u0400-\\u04ff])(' +
              escRe(kk).replace(/\s+/g, '\\s+') + ')(?![A-Za-z\\u00c0-\\u024f\\u0400-\\u04ff])');
            var m = re.exec(n.nodeValue);
            if (m) contentSet(n, n.nodeValue.replace(re, '$1' + lookup[kk]));
          });
        });
      });
    });
  }
  function translateContent(ru) {
    if (!ru) {
      if (contentOrig) {
        contentOrig.forEach(function (rec) { try { rec.n.nodeValue = rec.t; } catch (e) {} });
        contentOrig = null;
      }
      contentDone = false;
      contentStarted = false;
      if (origTitle !== null) { try { document.title = origTitle; } catch (e) {} origTitle = null; }
      return;
    }
    if (contentDone || contentStarted) return;
    contentStarted = true;
    ensureContent(function () {
      if (contentDone) return;
      contentOrig = [];
      try { applyContent(); } catch (e) {}
      try {
        var h1 = document.querySelector('.doc h1, .blog-doc h1');
        if (h1 && h1.textContent.trim().length > 3) {
          if (origTitle === null) origTitle = document.title;
          // The suffix must match what the page actually is. Legal pages share
          // the same .doc scope as help articles, so the old two-way branch
          // stamped every legal document with "\u041f\u043e\u043c\u043e\u0449\u044c"
          // (Help) and produced titles like "\u0423\u0441\u043b\u043e\u0432\u0438\u044f \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u2014 \u041f\u043e\u043c\u043e\u0449\u044c"
          // for a page that is not help at all.
          var suffix;
          if (document.querySelector('.blog-doc')) {
            suffix = ' \u2014 \u0411\u043b\u043e\u0433 Fast Scheduler';
          } else if (document.body && document.body.classList.contains('legal')) {
            suffix = ' \u2014 Fast Scheduler';
          } else {
            suffix = ' \u2014 \u041f\u043e\u043c\u043e\u0449\u044c Fast Scheduler';
          }
          document.title = h1.textContent.trim() + suffix;
        }
      } catch (e2) {}
      contentDone = true;
    });
  }

  // data-i18n registry for templates (extend without touching HTML widely)
  var I18N = {};

  function inject() {
    var menu = document.getElementById('settingsMenu');
    if (!menu || menu.querySelector('.fs-lang-seg')) return;
    var wrap = document.createElement('div');
    wrap.className = 'fs-lang-row';
    wrap.innerHTML = '<span class="fs-lang-label">Language</span>' +
      '<div class="fs-lang-seg" role="group" aria-label="Language">' +
      '<button type="button" data-lang="en" aria-pressed="true"><span class="fs-flag">🇬🇧</span>EN</button>' +
      '<button type="button" data-lang="ru" aria-pressed="false"><span class="fs-flag">🇷🇺</span>RU</button>' +
      '</div>';
    var head = menu.querySelector('.gp-head');
    if (head && head.nextSibling) menu.insertBefore(wrap, head.nextSibling);
    else menu.insertBefore(wrap, menu.firstChild);
    wrap.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) { e.stopPropagation(); set(b.getAttribute('data-lang')); });
    });
  }
  window.FS_LANG = { get: get, set: set, t: t, apply: apply, RU_MAP: RU_MAP, I18N: I18N };
  function boot() {
    inject();
    var lang = get();
    document.documentElement.setAttribute('lang', lang);
    apply(lang);
    observeLate();
    // idle preload: RU dict arrives before the user ever clicks RU,
    // so the first switch is instant even on slow networks
    try {
      var idle = window.requestIdleCallback || function (cb) { return setTimeout(cb, 1500); };
      idle(function () { if (get() === 'ru') ensureContent(function () {}); });
    } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  window.addEventListener('storage', function (e) {
    if (e.key === 'fs-lang' && e.newValue) apply(e.newValue === 'ru' ? 'ru' : 'en');
  });
  // Instant switching for late/dynamic content: the plan-comparison table
  // (main.js), help-search results and RU-dict bodies render AFTER this
  // file, so watch for added nodes and translate them in the current
  // language immediately — no refresh needed.
  var obsTimer = null;
  function observeLate() {
    try {
      if (!('MutationObserver' in window) || !document.body) return;
      var obs = new MutationObserver(function (muts) {
        if (get() !== 'ru') return;
        if (obsTimer) return;
        obsTimer = setTimeout(function () {
          obsTimer = null;
          try {
            muts.forEach(function () {});
            applyTree(document.body, true);
            applyFixups(true);
            // article-body dict covers new nodes too (guarded: store exists)
            try { if (window.FS_RU_CONTENT && contentOrig) applyContent(); } catch (e) {}
          } catch (e3) {}
        }, 60);
      });
      obs.observe(document.body, { childList: true, subtree: true });
    } catch (e) {}
  }
  window.addEventListener('fs-lang-change', function () {});
  // safety net for very late widgets; the observer above does the real work
  setTimeout(function () { try { apply(get()); } catch (e) {} }, 1500);
})();
