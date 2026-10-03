# s16d: leftovers from s16c (failed midway): static versions + index.html.
import io

CSS_V = '20261002c2'
JS_V = '20261002c2'
STATIC = 'website/_build/build_static.py'
INDEX = 'index.html'

KEYS_HELP = '<button type="button" class="gp-row gp-row-sub" id="rowKeysHelp" role="menuitem">'
BOOK_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
            '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>')
FONT_BTNS = ('<span class="hc-fonts">'
             '<button type="button" data-font="s" aria-label="Small">A</button>'
             '<button type="button" data-font="m" aria-label="Default">A</button>'
             '<button type="button" data-font="l" aria-label="Large">A</button>'
             '</span></div>')
FONT_ROW = '<div class="gp-row gp-fonts" data-fonts>' + BOOK_SVG + '<span>Font size</span>' + FONT_BTNS


def patch(path, old, new, count=1):
    s = io.open(path, encoding='utf-8').read()
    assert old in s, 'anchor missing in %s: %r' % (path, old[:80])
    if count == 1:
        assert s.count(old) == 1, 'anchor x%d in %s: %r' % (s.count(old), path, old[:80])
        s = s.replace(old, new, 1)
    else:
        assert s.count(old) == count
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', path.split('/')[-1], old[:56].replace(chr(10), ' '))


patch(STATIC, '/styles/main.css?v=20260930a2', '/styles/main.css?v=' + CSS_V)
patch(STATIC, '/scripts/settings.js"></script>', '/scripts/settings.js?v=' + JS_V + '"></script>', count=2)

patch(INDEX, '          ' + KEYS_HELP, '          ' + FONT_ROW + '\n' + '          ' + KEYS_HELP)
patch(INDEX,
      "      if (localStorage.getItem('fs-rail') === 'off') d.classList.add('rail-off');",
      "      if (localStorage.getItem('fs-rail') === 'off') d.classList.add('rail-off');\n"
      "      var _ffs = localStorage.getItem('fs-font') || localStorage.getItem('fs-help-font') || localStorage.getItem('fs-blog-font');\n"
      "      if (_ffs) d.setAttribute('data-font', _ffs);")
patch(INDEX, 'styles/main.css?v=20260930a2', 'styles/main.css?v=' + CSS_V)
patch(INDEX, 'scripts/settings.js?v=20260930a1', 'scripts/settings.js?v=' + JS_V)

print('s16d done')
