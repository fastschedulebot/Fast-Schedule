import io
P = 'website/_build/build_help.py'
s = io.open(P, encoding='utf-8').read()
old = "  window.addEventListener('hashchange', navigate);"
assert old in s
js = """  /* floating liquid-glass section reel: prev / current / next */
  (function () {
    var reel = document.querySelector('[data-reel]');
    if (!reel) return;
    var bPrev = reel.querySelector('[data-reel-prev]');
    var bCur = reel.querySelector('[data-reel-cur]');
    var bNext = reel.querySelector('[data-reel-next]');
    var curKey = null, ticking = false;
    function railLinks() {
      var v = document.querySelector('section.view:not([hidden])');
      var nav = v && v.querySelector('[data-rail]');
      return nav ? Array.prototype.slice.call(nav.querySelectorAll('a')) : [];
    }
    function railGone() {
      if (document.documentElement.classList.contains('hc-fs')) return true;
      try { return window.matchMedia('(max-width: 1279px)').matches; } catch (e) { return true; }
    }
    function setLabel(btn, link) {
      btn.querySelector('span').textContent = link ? link.textContent.trim() : '';
      btn._rk = link ? link.getAttribute('data-rk') : null;
    }
    function jump(btn) {
      var el = btn._rk && document.getElementById(btn._rk);
      if (!el) return;
      if (el.tagName === 'DETAILS') el.open = true;
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    function paint() {
      var links = railLinks();
      var idx = -1;
      links.forEach(function (a, i) { if (a.classList.contains('on')) idx = i; });
      var sc = window.scrollY || document.documentElement.scrollTop || 0;
      var show = links.length >= 2 && sc > 480 && railGone();
      reel.hidden = !show;
      reel.setAttribute('aria-hidden', show ? 'false' : 'true');
      if (!show) { curKey = null; return; }
      if (idx === -1) idx = 0;
      var key = links[idx].getAttribute('data-rk');
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
    document.addEventListener('viewchange', function () { curKey = null; paint(); });
    paint();
  })();
  window.addEventListener('hashchange', navigate);"""
s = s.replace(old, js, 1)
io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] s13')
