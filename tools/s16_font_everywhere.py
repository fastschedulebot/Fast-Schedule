# s16: Font size button + function everywhere. Unified key fs-font / attr
# data-font, owned by website/scripts/settings.js (FS_FONT). Builders add row
# HTML + NOFLASH reads; help/blog inline painters use the unified key.
import io

CSS_V = '20261002c2'
JS_V = '20261002c2'

HELP = 'website/_build/build_help.py'
BLOG = 'website/_build/build_blog.py'
SITE = 'website/_build/build_site.py'
STATIC = 'website/_build/build_static.py'
INDEX = 'index.html'

BOOK = ('<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>')


def font_row(svg_book):
    return ('<div class="gp-row gp-fonts" data-fonts>' + svg_book + '<span>Font size</span>'
            '<span class="hc-fonts">'
            '<button type="button" data-font="s" aria-label="Small">A</button>'
            '<button type="button" data-font="m" aria-label="Default">A</button>'
            '<button type="button" data-font="l" aria-label="Large">A</button>'
            '</span></div>')


def patch(path, old, new, count=1):
    s = io.open(path, encoding='utf-8').read()
    assert old in s, 'anchor missing in %s: %r' % (path, old[:80])
    if count == 1:
        assert s.count(old) == 1, 'anchor x%d in %s: %r' % (s.count(old), path, old[:80])
        s = s.replace(old, new, 1)
    else:
        assert s.count(old) == count, 'anchor x%d!=%d in %s' % (s.count(old), count, path)
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', path.split('/')[-1], old[:60].replace(chr(10), ' '))


# ================= help =================
patch(HELP,
      '<div class="gp-row gp-reading gp-fonts" data-reading data-fonts hidden>',
      '<div class="gp-row gp-fonts" data-fonts>')
patch(HELP,
      "var _hcf = localStorage.getItem('fs-help-font');\n"
      "      if (_hcf) document.documentElement.setAttribute('data-hcfont', _hcf);",
      "var _ff = localStorage.getItem('fs-font') || localStorage.getItem('fs-help-font');\n"
      "      if (_ff) { document.documentElement.setAttribute('data-font', _ff); "
      "document.documentElement.setAttribute('data-hcfont', _ff); }",
      count=2)
patch(HELP,
      "var font = load('fs-help-font');",
      "var font = load('fs-font') || load('fs-help-font');")
patch(HELP,
      "if (font) root.setAttribute('data-hcfont', font); else root.removeAttribute('data-hcfont');",
      "if (font) { root.setAttribute('data-font', font); root.setAttribute('data-hcfont', font); } "
      "else { root.removeAttribute('data-font'); root.removeAttribute('data-hcfont'); }")
patch(HELP,
      "if (f) { store('fs-help-font', f.getAttribute('data-font')); paintReader(); return; }",
      "if (f) { var fv = f.getAttribute('data-font'); store('fs-font', fv); store('fs-help-font', fv); "
      "try { window.dispatchEvent(new CustomEvent('fs-font-change', { detail: { font: fv } })); } catch (e2) {} "
      "paintReader(); return; }")
patch(HELP,
      "window.__hcPaintReader = paintReader;",
      "window.addEventListener('fs-font-change', function () { paintReader(); });\n"
      "    window.__hcPaintReader = paintReader;")
patch(HELP, 'styles/main.css?v=20260930a2', 'styles/main.css?v=' + CSS_V)
patch(HELP, 'scripts/settings.js?v=20260930a1', 'scripts/settings.js?v=' + JS_V)

print('s16 help done')
