# s14d: remaining s14b replacements. Builder uses REAL curly quotes here.
import io

HELP = 'website/_build/build_help.py'

LQ = '“'
RQ = '”'


def sub_once(old, new):
    s = io.open(HELP, encoding='utf-8').read()
    assert old in s, 'anchor missing: %r' % old[:70]
    assert s.count(old) == 1, 'anchor not unique x%d: %r' % (s.count(old), old[:70])
    io.open(HELP, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
    print('[ok]', old[:60].replace(chr(10), ' '))


old_count = ("    if (searchMeta) searchMeta.textContent = hits.length\n"
             "      ? hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for " + LQ + "' + q + '" + RQ + "'\n"
             "      : '0 results';")
new_count = ("    if (searchMeta) searchMeta.textContent = hits.length\n"
             "      ? (hcRuCount(hits.length, q) || (hits.length + ' result' + (hits.length > 1 ? 's' : '') + ' for " + LQ + "' + q + '" + RQ + "'))\n"
             "      : hcT('0 results');")
sub_once(old_count, new_count)

sub_once('      searchList.innerHTML = html;',
         '      searchList.innerHTML = html;\n      hcTranslateNow(searchList);')
sub_once('    el.innerHTML = html;',
         '    el.innerHTML = html;\n    hcTranslateNow(el);')

sub_once(("    document.addEventListener('viewchange', function () { curKey = null; paint(); });\n"
          "    paint();\n"
          "  })();"),
         ("    document.addEventListener('viewchange', function () { curKey = null; paint(); });\n"
          "    window.__hcReelPaint = function () { curKey = null; paint(); };\n"
          "    window.addEventListener('fs-lang-change', function () { curKey = null; paint(); });\n"
          "    window.addEventListener('fs-lang-applied', function () { curKey = null; paint(); });\n"
          "    paint();\n"
          "  })();"))

print('s14d done')
