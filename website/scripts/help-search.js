/* Help quick-search inside Settings > Help (all pages).
   Hover (or click) the "Help" row in the settings menu and a popover opens
   with the search field + recent/popular searches. Submit routes to
   help.html#/s/<query>, which renders the results page directly on load. */
(function () {
  'use strict';
  var pop = document.getElementById('siteMenu');
  var form = document.getElementById('helpSearchForm');
  var input = document.getElementById('helpSearchInput');
  var list = document.getElementById('helpRecentList');
  var title = document.getElementById('helpRecentTitle');
  if (!pop || !form || !input || !list) return;
  var KEY = 'fs-help-recents';
  var HELP_URL = (function () {
    var open = pop.querySelector('a.help-menu-open');
    return open ? open.getAttribute('href') : 'help.html';
  })();
  var SUGGESTED = [
    { t: 'Getting Started', q: 'getting started' },
    { t: 'Connecting a Channel', q: 'connecting a channel' },
    { t: 'Recurring Messages', q: 'recurring messages' },
    { t: 'Premium & Billing', q: 'premium billing' },
    { t: 'Media & Photo Posts', q: 'photo video posts' },
    { t: 'Fix: Post Not Sent', q: 'post not sent' },
    { t: 'Edit or Delete a Post', q: 'edit delete scheduled' }
  ];

  function readRecents() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }
  /* pick n random items (Fisher-Yates on a copy) — the list rotates on
     every open instead of always showing the same seven entries */
  function pickRandom(arr, n) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a.slice(0, n);
  }
  function render() {
    var rec = readRecents().slice(0, 5);
    list.textContent = '';
    if (rec.length) {
      title.textContent = 'Recent searches';
      rec.forEach(function (q) {
        var a = document.createElement('a');
        a.href = HELP_URL + '#/s/' + encodeURIComponent(q);
        a.textContent = q;
        list.appendChild(a);
      });
    } else {
      title.textContent = 'Popular articles';
      pickRandom(SUGGESTED, 3).forEach(function (s) {
        var a = document.createElement('a');
        a.href = HELP_URL + '#/s/' + encodeURIComponent(s.q);
        a.textContent = s.t;
        list.appendChild(a);
      });
    }
  }

  /* prefill as soon as the submenu opens (settings.js toggles .open) */
  var obs = new MutationObserver(function () {
    if (pop.classList.contains('open')) render();
  });
  obs.observe(pop, { attributes: true, attributeFilter: ['class'] });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q) return;
    try {
      var rec = readRecents().filter(function (x) { return x !== q; });
      rec.unshift(q);
      localStorage.setItem(KEY, JSON.stringify(rec.slice(0, 6)));
    } catch (err) {}
    window.open(HELP_URL + '#/s/' + encodeURIComponent(q), '_blank', 'noopener');
  });
})();
