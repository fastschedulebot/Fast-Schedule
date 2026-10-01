// Website language: EN/RU switcher, persisted in localStorage (fs-lang).
// Liquid-glass EN/RU segmented control in #settingsMenu.
// Full-site RU: chrome (settings/nav/footer/search) + index sections
// (hero/features/how/reviews/pricing/FAQ/CTA) + legal/blog/help chrome
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
    'Reviews': 'Отзывы',
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
    'Channels that stopped posting by hand': 'Каналы, которые перестали публиковать вручную',
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
    'On this page': 'На этой странице',
    'Privacy Policy': 'Политика конфиденциальности',
    'Terms of Service': 'Условия использования',
    'Refund Policy': 'Политика возвратов',
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
    'Go home': 'На главную'
  };

  var META = {
    title: {
      en: 'Fast Scheduler — Schedule Telegram Channel Posts on Autopilot',
      ru: 'Fast Scheduler — автопланирование постов Telegram-канала'
    },
    desc: {
      en: 'Fast Scheduler is a free Telegram bot that schedules, publishes and tracks your channel posts on autopilot. Batch-schedule weeks of content in one chat, post from your own bot, and see what performs. Set it once — save hours every week.',
      ru: 'Fast Scheduler — бесплатный Telegram-бот для автопланирования, публикации и аналитики постов канала. Планируйте недели контента в одном чате, публикуйте от своего бота и смотрите, что заходит. Настройте один раз — экономьте часы каждую неделю.'
    }
  };

  function get() {
    try { return localStorage.getItem('fs-lang') === 'ru' ? 'ru' : 'en'; }
    catch (e) { return 'en'; }
  }
  function set(lang) {
    lang = lang === 'ru' ? 'ru' : 'en';
    try { localStorage.setItem('fs-lang', lang); } catch (e) {}
    document.documentElement.setAttribute('lang', lang);
    apply(lang);
    try { window.dispatchEvent(new CustomEvent('fs-lang-change', { detail: { lang: lang } })); } catch (e) {}
  }
  function t(key) { return (STR[get()] || STR.en)[key] || STR.en[key] || key; }

  function translateNode(el, ru) {
    if (!el || el.querySelector('.fs-lang-seg')) return;
    // skip code, pre, script, style, svg paths
    var tag = (el.tagName || '').toLowerCase();
    if (tag === 'script' || tag === 'style' || tag === 'code' || tag === 'pre') return;
    // only leaf-ish elements: no element children, or single svg + text (nav cta)
    var hasElChild = false;
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i];
      if (n.nodeType === 1 && (n.tagName || '').toLowerCase() !== 'svg') { hasElChild = true; break; }
    }
    if (hasElChild) return;
    var cur = el.textContent;
    var trimmed = cur.trim();
    if (!trimmed) return;
    if (ru) {
      var mapped = RU_MAP[trimmed];
      if (mapped) {
        if (!el.dataset.fsEn) el.dataset.fsEn = trimmed;
        // preserve surrounding whitespace
        var lead = cur.match(/^\s*/)[0], trail = cur.match(/\s*$/)[0];
        el.textContent = lead + mapped + trail;
      }
    } else if (el.dataset.fsEn) {
      var lead2 = cur.match(/^\s*/)[0], trail2 = cur.match(/\s*$/)[0];
      el.textContent = lead2 + el.dataset.fsEn + trail2;
      delete el.dataset.fsEn;
    }
  }

  function apply(lang) {
    var ru = lang === 'ru';
    var d = STR[lang] || STR.en;
    document.documentElement.setAttribute('lang', lang);
    // settings head
    document.querySelectorAll('#settingsMenu .gp-head').forEach(function (el) {
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
    // generic exact-text map across body (landing + shared chrome)
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT, null);
    var batch = [];
    while (walker.nextNode()) batch.push(walker.currentNode);
    batch.forEach(function (el) { translateNode(el, ru); });
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
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  window.addEventListener('storage', function (e) {
    if (e.key === 'fs-lang' && e.newValue) apply(e.newValue === 'ru' ? 'ru' : 'en');
  });
  // re-apply after late widgets (help-ai, hero-demo) render
  window.addEventListener('fs-lang-change', function () {});
  setTimeout(function () { try { apply(get()); } catch (e) {} }, 1200);
})();
