# s15c: TOC_JS += reader JS + liquid-glass reel JS + lang repaint.
import io

BLOG = 'website/_build/build_blog.py'
Q3 = chr(39) * 3

JS = """/* Reader settings: Wide / Article navigation / Font size (article pages). */
(function () {
  'use strict';
  var root = document.documentElement;
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function paintBlogReader() {
    var wide = load('fs-blog-wide') === 'on';
    var railOff = load('fs-rail') === 'off';
    var font = load('fs-blog-font');
    root.classList.toggle('blog-wide', wide);
    root.classList.toggle('rail-off', railOff);
    if (font) root.setAttribute('data-blogfont', font); else root.removeAttribute('data-blogfont');
    var q = function (sel, fn) { Array.prototype.forEach.call(document.querySelectorAll(sel), fn); };
    q('[data-blog-wide]', function (b) { b.setAttribute('aria-checked', wide ? 'true' : 'false'); });
    q('[data-blog-rail]', function (b) { b.setAttribute('aria-checked', railOff ? 'false' : 'true'); });
    q('[data-blog-fonts]', function (box) {
      Array.prototype.forEach.call(box.querySelectorAll('button'), function (b) {
        b.classList.toggle('on', (font || 'm') === b.getAttribute('data-font'));
      });
    });
  }
  document.addEventListener('click', function (ev) {
    if (!ev.target.closest) return;
    var w = ev.target.closest('[data-blog-wide]');
    if (w) { store('fs-blog-wide', w.getAttribute('aria-checked') !== 'true' ? 'on' : 'off'); paintBlogReader(); return; }
    var r = ev.target.closest('[data-blog-rail]');
    if (r) { store('fs-rail', r.getAttribute('aria-checked') === 'true' ? 'off' : 'on'); paintBlogReader(); return; }
    var f = ev.target.closest('[data-blog-fonts] button');
    if (f) { store('fs-blog-font', f.getAttribute('data-font')); paintBlogReader(); return; }
  });
  window.__blogPaintReader = paintBlogReader;
  paintBlogReader();
})();
/* Floating liquid-glass section reel: prev / current / next section. */
(function () {
  'use strict';
  var reel = document.querySelector('[data-blog-reel]');
  if (!reel) return;
  var bPrev = reel.querySelector('[data-reel-prev]');
  var bCur = reel.querySelector('[data-reel-cur]');
  var bNext = reel.querySelector('[data-reel-next]');
  var curKey = null, ticking = false;
  function tocLinks() {
    var nav = document.querySelector('.blog-cols .blog-toc');
    return nav ? Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]')) : [];
  }
  function railGone() {
    if (document.documentElement.classList.contains('blog-wide')) return true;
    try { return window.matchMedia('(max-width: 1140px)').matches; } catch (e) { return true; }
  }
  function setLabel(btn, link) {
    btn.querySelector('span').textContent = link ? link.textContent.trim() : '';
    btn._to = link ? link.getAttribute('href') : null;
  }
  function jump(btn) {
    if (!btn._to) return;
    var el = document.getElementById(btn._to.slice(1));
    if (!el) return;
    var off = el.getBoundingClientRect().top + window.pageYOffset - 76;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
                 document.documentElement.getAttribute('data-motion') === 'off';
    window.scrollTo({ top: off, behavior: reduce ? 'auto' : 'smooth' });
  }
  function paint() {
    var links = tocLinks();
    var idx = -1;
    links.forEach(function (a, i) { if (a.classList.contains('on')) idx = i; });
    var sc = window.scrollY || document.documentElement.scrollTop || 0;
    var show = links.length >= 2 && sc > 480 && railGone();
    reel.hidden = !show;
    reel.setAttribute('aria-hidden', show ? 'false' : 'true');
    if (reel.classList.contains('show') !== show) reel.classList.toggle('show', show);
    if (!show) { curKey = null; return; }
    if (idx === -1) idx = 0;
    var key = links[idx].getAttribute('href');
    if (key === curKey) return;
    curKey = key;
    setLabel(bPrev, links[idx - 1]);
    setLabel(bCur, links[idx]);
    setLabel(bNext, links[idx + 1]);
    bPrev.style.visibility = links[idx - 1] ? 'visible' : 'hidden';
    bNext.style.visibility = links[idx + 1] ? 'visible' : 'hidden';
    reel.classList.remove('swap');
    void reel.offsetWidth;
    reel.classList.add('swap');
  }
  bPrev.addEventListener('click', function () { jump(bPrev); });
  bCur.addEventListener('click', function () { jump(bCur); });
  bNext.addEventListener('click', function () { jump(bNext); });
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    var raf = window.requestAnimationFrame || function (cb) { setTimeout(cb, 100); };
    raf(function () { ticking = false; paint(); });
  }, { passive: true });
  window.__blogReelPaint = function () { curKey = null; paint(); };
  window.addEventListener('fs-lang-change', function () { curKey = null; paint(); });
  window.addEventListener('fs-lang-applied', function () { curKey = null; paint(); });
  paint();
})();
</script>"""

s = io.open(BLOG, encoding='utf-8').read()
old = ("      var m = document.querySelector('.blog-toc-m');\n"
       "      if (m && m.open) m.open = false;\n"
       '    });\n  });\n})();\n</script>' + Q3)
assert s.count(old) == 1, 'toc tail count=%d' % s.count(old)
new = ("      var m = document.querySelector('.blog-toc-m');\n"
       "      if (m && m.open) m.open = false;\n"
       '    });\n  });\n})();\n' + JS + Q3)
s = s.replace(old, new, 1)
io.open(BLOG, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] TOC_JS extended')
print('s15c done')
