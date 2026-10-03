# s14b: help builder — lang-aware dynamic rendering (no EN flash in RU).
import io

HELP = 'website/_build/build_help.py'

HELPERS = """  /* lang-aware chrome labels: write the final language synchronously so
     freshly injected nodes never flash EN before the RU observer runs. */
  function hcT(en) {
    try {
      if (window.FS_LANG && FS_LANG.get() === 'ru') {
        var m = (FS_LANG.RU_MAP || {})[en];
        if (m) return m;
        if (window.FS_RU_CHROME && FS_RU_CHROME.MAP && FS_RU_CHROME.MAP[en]) return FS_RU_CHROME.MAP[en];
      }
    } catch (e) {}
    return en;
  }
  function hcRuCount(n, q) {
    try {
      if (window.FS_LANG && FS_LANG.get() === 'ru') {
        var w = 'результатов';
        var m10 = n % 10, h10 = n % 100;
        if (m10 === 1 && h10 !== 11) w = 'результат';
        else if (m10 >= 2 && m10 <= 4 && (h10 < 12 || h10 > 14)) w = 'результата';
        return n + ' ' + w + ' по запросу \\u201c' + q + '\\u201d';
      }
    } catch (e) {}
    return null;
  }
  window.__hcDyn = window.__hcDyn || [];
  function hcTrack(n, en) {
    try {
      var arr = window.__hcDyn;
      for (var i = 0; i < arr.length; i++) { if (arr[i].n === n) { arr[i].en = en; return; } }
      arr.push({ n: n, en: en });
    } catch (e) {}
  }
  function hcTranslateNow(root) {
    try {
      if (!(window.FS_LANG && FS_LANG.get() === 'ru')) return;
      var map = FS_LANG.RU_MAP || {};
      var dict = (window.FS_RU_CHROME && FS_RU_CHROME.MAP) || {};
      var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
      var batch = [], tn;
      while ((tn = w.nextNode())) batch.push(tn);
      batch.forEach(function (n) {
        try {
          var p = n.parentNode;
          if (!p || (p.closest && p.closest('.fs-lang-seg'))) return;
          var tag = (p.tagName || '').toLowerCase();
          if (tag === 'script' || tag === 'style' || tag === 'code' || tag === 'pre' || tag === 'textarea') return;
          var t = n.nodeValue.trim();
          if (!t) return;
          var m = map[t] || dict[t];
          if (m && n.nodeValue.indexOf(m) === -1) {
            hcTrack(n, n.nodeValue);
            var lead = (n.nodeValue.match(/^\\s*/) || [''])[0];
            var trail = (n.nodeValue.match(/\\s*$/) || [''])[0];
            n.nodeValue = lead + m + trail;
          }
        } catch (e2) {}
      });
    } catch (e) {}
  }
  window.addEventListener('fs-lang-change', function (e) {
    /* RU->EN: restore synchronously translated dynamic nodes; EN->RU: the
       debounced observer plus hcTranslateNow on next render covers it. */
    try {
      var lang = (e && e.detail && e.detail.lang) || (window.FS_LANG && FS_LANG.get());
      if (lang === 'ru') return;
      var arr = window.__hcDyn || [];
      window.__hcDyn = [];
      arr.forEach(function (rec) { try { rec.n.nodeValue = rec.en; } catch (x) {} });
      /* re-render visible search UI so composite strings (counts) flip now */
      ['hcSearch', 'hcSearchH'].forEach(function (id) {
        var inp = document.getElementById(id);
        if (inp && inp.value && inp.offsetParent !== null) {
          try { inp.dispatchEvent(new Event('input', { bubbles: true })); } catch (x) {}
        }
      });
      if (window.__hcReelPaint) { try { window.__hcReelPaint(); } catch (x) {} }
    } catch (x) {}
  });
  /* floating liquid-glass section reel: prev / current / next */"""


def sub_once(old, new):
    s = io.open(HELP, encoding='utf-8').read()
    assert old in s, 'anchor missing: %r' % old[:70]
    assert s.count(old) == 1, 'anchor not unique x%d: %r' % (s.count(old), old[:70])
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
    print('[ok]', old[:60].replace(chr(10), ' '))


def sub_all(old, new):
    s = io.open(HELP, encoding='utf-8').read()
    assert old in s, 'anchor missing: %r' % old[:70]
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new))
    print('[ok] x%d' % s.count(old), old[:60].replace(chr(10), ' '))


# 1. helpers before reel IIFE
sub_once('  /* floating liquid-glass section reel: prev / current / next */', HELPERS)

# 2. dropdown labels
sub_once("html += '<div class=\"hc-res-sec\">Best result</div>';",
         "html += '<div class=\"hc-res-sec\">' + hcT('Best result') + '</div>';")
sub_once("html += '<div class=\"hc-res-sec\">More results</div>';",
         "html += '<div class=\"hc-res-sec\">' + hcT('More results') + '</div>';")
sub_all("html += '<div class=\"hc-sug-h\">Maybe you meant:</div>';",
        "html += '<div class=\"hc-sug-h\">' + hcT('Maybe you meant:') + '</div>';")
sub_once("var html = '<div class=\"hc-empty\">No exact match for \\u201c' + escapeHtml(q) + '\\u201d.</div>';",
         "var html = '<div class=\"hc-empty\">' + hcT('No exact match for') + ' \\u201c' + escapeHtml(q) + '\\u201d.</div>';")
sub_once("var aiHtml = ai ? '<div class=\"hc-ai-line\"><span class=\"hc-ai-dot\"></span>You mean: <b>' + escapeHtml(ai) + '</b></div>' : '';",
         "var aiHtml = ai ? '<div class=\"hc-ai-line\"><span class=\"hc-ai-dot\"></span>' + hcT('You mean:') + ' <b>' + escapeHtml(ai) + '</b></div>' : '';")
sub_once("html += '<div class=\"hc-sug-h\">Still stuck? <a href=\"__BOTURL__\" target=\"_blank\" rel=\"noopener noreferrer\">Ask in the bot</a> \\u2014 a human answers every ticket.</div>';",
         "html += '<div class=\"hc-sug-h\">' + hcT('Still stuck?') + ' <a href=\"__BOTURL__\" target=\"_blank\" rel=\"noopener noreferrer\">' + hcT('Ask in the bot') + '</a> ' + hcT('\\u2014 a human answers every ticket.') + '</div>';")

# 3. dropdown innerHTML -> sync translate (both occurrences)
sub_all('      results.innerHTML = html;',
        '      results.innerHTML = html;\n      hcTranslateNow(results);')

# 4. search page labels + count + sync translate
sub_once("'<span class=\"hc-best-label\">Best result</span>' +",
         "'<span class=\"hc-best-label\">' + hcT('Best result') + '</span>' +")
sub_once('>All results</div>',
         '>\' + hcT(\'All results\') + \'</div>')
sub_once("""    if (searchMeta) searchMeta.textContent = hits.length
      ? hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for \\u201c' + q + '\\u201d'
      : '0 results';""",
         """    if (searchMeta) searchMeta.textContent = hits.length
      ? (hcRuCount(hits.length, q) || (hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for \\u201c' + q + '\\u201d'))
      : hcT('0 results');""")
sub_once('      searchList.innerHTML = html;',
         '      searchList.innerHTML = html;\n      hcTranslateNow(searchList);')
sub_once('    el.innerHTML = html;',
         '    el.innerHTML = html;\n    hcTranslateNow(el);')

# 5. reel: expose repaint + lang listeners
sub_once("""    document.addEventListener('viewchange', function () { curKey = null; paint(); });
    paint();
  })();""",
         """    document.addEventListener('viewchange', function () { curKey = null; paint(); });
    window.__hcReelPaint = function () { curKey = null; paint(); };
    window.addEventListener('fs-lang-change', function () { curKey = null; paint(); });
    window.addEventListener('fs-lang-applied', function () { curKey = null; paint(); });
    paint();
  })();""")

print('s14b done')
