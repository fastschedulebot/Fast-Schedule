# s15d: repaint the floating reel right after reader toggles (no scroll needed).
import io


def sub_once(path, old, new):
    s = io.open(path, encoding='utf-8').read()
    assert old in s, 'anchor missing in %s: %r' % (path, old[:70])
    assert s.count(old) == 1, 'anchor not unique x%d in %s' % (s.count(old), path)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
    print('[ok]', path, old[:50].replace(chr(10), ' '))


sub_once('website/_build/build_blog.py',
         "    q('[data-blog-fonts]', function (box) {",
         "    if (window.__blogReelPaint) { try { window.__blogReelPaint(); } catch (e) {} }\n"
         "    q('[data-blog-fonts]', function (box) {")

# help paintReader tail: aria-checked sync for fs button, then close of paintReader
sub_once('website/_build/build_help.py',
         "      q('[data-fs-btn]', function (b) { b.classList.toggle('on', fs); });\n    }",
         "      q('[data-fs-btn]', function (b) { b.classList.toggle('on', fs); });\n"
         "      if (window.__hcReelPaint) { try { window.__hcReelPaint(); } catch (e) {} }\n    }")

print('s15d done')
