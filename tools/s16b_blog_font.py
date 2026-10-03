# s16b: blog — font row always emitted, unified fs-font key.
import io

BLOG = 'website/_build/build_blog.py'
CSS_V = '20261002c2'
JS_V = '20261002c2'


def patch(old, new, count=1):
    s = io.open(BLOG, encoding='utf-8').read()
    assert old in s, 'anchor missing: %r' % old[:80]
    if count == 1:
        assert s.count(old) == 1, 'anchor x%d: %r' % (s.count(old), old[:80])
        s = s.replace(old, new, 1)
    else:
        assert s.count(old) == count
        s = s.replace(old, new)
    io.open(BLOG, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', old[:60].replace(chr(10), ' '))


FONTS_INNER = ('{bh.svg(\'book\')}<span>Font size</span>'
               '<span class="hc-fonts"><button type="button" data-font="s" aria-label="Small">A</button>'
               '<button type="button" data-font="m" aria-label="Default">A</button>'
               '<button type="button" data-font="l" aria-label="Large">A</button></span></div>')
FONTS_DIV = '<div class="gp-row gp-fonts" data-fonts>' + FONTS_INNER

# 1. fonts div leaves the reading-gated _reading block; becomes always-on _fonts
patch('          <div class="gp-row gp-reading gp-fonts" data-blog-reading data-blog-fonts>' + FONTS_INNER + "'''",
      "          {_fonts}'''")
patch('    _reading = """\n    """\n    if reading:',
      "    _fonts = f'''" + FONTS_DIV + "'''\n"
      '    _reading = """\n    """\n    if reading:')
patch('        {_reading}\n        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp"',
      '        {_fonts}\n        {_reading}\n        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp"')
# 2. NOFLASH unified read
patch("    var _bf = localStorage.getItem('fs-blog-font');\n"
      "    if (_bf) document.documentElement.setAttribute('data-blogfont', _bf);",
      "    var _ffb = localStorage.getItem('fs-font') || localStorage.getItem('fs-blog-font');\n"
      "    if (_ffb) { document.documentElement.setAttribute('data-font', _ffb); "
      "document.documentElement.setAttribute('data-blogfont', _ffb); }")
# 3. inline painter unified
patch("    var font = load('fs-blog-font');",
      "    var font = load('fs-font') || load('fs-blog-font');")
patch("    if (font) root.setAttribute('data-blogfont', font); else root.removeAttribute('data-blogfont');",
      "    if (font) { root.setAttribute('data-font', font); root.setAttribute('data-blogfont', font); } "
      "else { root.removeAttribute('data-font'); root.removeAttribute('data-blogfont'); }")
patch("    q('[data-blog-fonts]', function (box) {",
      "    q('[data-fonts]', function (box) {")
patch("    var f = ev.target.closest('[data-blog-fonts] button');\n"
      "    if (f) { store('fs-blog-font', f.getAttribute('data-font')); paintBlogReader(); return; }",
      "    var f = ev.target.closest('[data-fonts] button');\n"
      "    if (f) { var fv = f.getAttribute('data-font'); store('fs-font', fv); store('fs-blog-font', fv); "
      "try { window.dispatchEvent(new CustomEvent('fs-font-change', { detail: { font: fv } })); } catch (e2) {} "
      "paintBlogReader(); return; }")
patch("  window.__blogPaintReader = paintBlogReader;",
      "  window.addEventListener('fs-font-change', function () { paintBlogReader(); });\n"
      "  window.__blogPaintReader = paintBlogReader;")
# 4. versions (settings.js ref has no version in blog -> add one)
patch('styles/main.css?v=20260930a2', 'styles/main.css?v=' + CSS_V)
patch('<script src="{rel}/scripts/settings.js"></script>',
      '<script src="{rel}/scripts/settings.js?v=' + JS_V + '"></script>')

print('s16b done')
