/* Article navigation hotkeys (blog + help articles, desktop).
   J / ArrowRight → next article, K / ArrowLeft → previous article.
   Targets the prev/next cards that already exist on the page:
   blog articles use .blog-toc-navc.prev/.next, help articles use
   .hc-pager a.prev/.next (or the sheet equivalents). Respects the site's
   Hotkeys switch and stands down while typing. */
(function () {
  'use strict';
  if (window.matchMedia && !matchMedia('(min-width: 861px)').matches) return;

  function findLink(dirs) {
    for (var i = 0; i < dirs.length; i++) {
      var el = document.querySelector(dirs[i]);
      if (el && el.tagName === 'A' && el.getAttribute('href')) return el;
    }
    return null;
  }
  function nextLink() {
    return findLink([
      'a.hc-pager.next[href]:not([href="../index.html"])',
      'a.blog-toc-navc.next[href]',
      '.blog-toc-sheet a.blog-toc-navc.next[href]',
      '.hc-toc-sheet a.hc-toc-navc.next[href]'
    ]);
  }
  function prevLink() {
    return findLink([
      'a.hc-pager.prev[href]',
      'a.blog-toc-navc.prev[href]',
      '.blog-toc-sheet a.blog-toc-navc.prev[href]',
      '.hc-toc-sheet a.hc-toc-navc.prev[href]'
    ]);
  }

  document.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.repeat) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (document.documentElement.getAttribute('data-keys') === 'off') return;
    var el = document.activeElement, tag = (el && el.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (el && el.isContentEditable)) return;
    /* never fight the hotkeys editor while it records a chord */
    if (window.FS_HK_RECORDING) return;

    var go = null;
    if (e.key === 'ArrowRight' || e.key === 'j' || e.key === 'J') go = nextLink();
    else if (e.key === 'ArrowLeft' || e.key === 'k' || e.key === 'K') go = prevLink();
    if (go) {
      /* arrow keys must still work for horizontal scrollers */
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        var sc = document.querySelector('.table-scroll:hover, .hc-body .table-scroll:hover');
        if (sc) return;
      }
      e.preventDefault();
      window.location.href = go.getAttribute('href');
    }
  });
})();
