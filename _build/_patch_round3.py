# -*- coding: utf-8 -*-
"""Patch round 3 (2026-09-26):

  hotkeys.js      - H and G stop answering .help-row (home page only);
                    H = Help on all pages, G = Blog on all pages
  hotkeys-modal.js- registry entries for the same two keys
  build_blog.py   - cover image inside article pages; tighter card meta;
                    "Try Fast Scheduler" links block inside every article
  build_help.py   - "Hide sidebar" keycap hint T -> O (matches the O action)
"""
import io

def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, (path, old[:70])
        s = s.replace(old, new, 1)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('[ok]', path)

# ---------------------------------------------------------------- hotkeys.js
patch('../scripts/hotkeys.js', [
    ("""    { key: 'm', sel: '#navBurger', name: 'Menu', hint: false },
    { key: ',', sel: '#settingsBtn', name: 'Settings', hint: 'rail', tip: true },
    { key: 'h', sel: '.help-row a, .site-menu-row, a.gp-row[href*="help"]', name: 'Help', hint: 'rail' },""",
     """    { key: 'm', sel: '#navBurger', name: 'Menu', hint: false },
    { key: ',', sel: '#settingsBtn', name: 'Settings', hint: 'rail', tip: true },
    /* H = Help on every page (on the home page the old H entry answered the
       help-row, which holds BOTH the Blog and the Help link and picked the
       first visible one — so H went to the Blog). G = Blog on every page.
       On the home page G used to toggle the jump menu (scroll-jump.js); the
       hotkeys editor's 'jumpFab' entry keeps that remappable there. */"""),
    ("""    /* pricing: billing period, then act on whichever plan is centred */""",
     """    { key: 'g', sel: 'a.nav-link[href*="blog"], .help-row a[href*="blog"], a[href$="blog/index.html"], a[href$="/blog/"]',
      name: 'Blog', hint: 'rail' },
    { key: 'h', sel: 'a.nav-link[href*="help"], .site-menu-row, a.gp-row[href*="help"], .help-row a[href*="help"]',
      name: 'Help', hint: 'rail' },

    /* pricing: billing period, then act on whichever plan is centred */"""),
])

# ----------------------------------------------------------- hotkeys-modal.js
patch('../scripts/hotkeys-modal.js', [
    ("""    { id: 'help',     key: 'H',            page: 'all',  name: 'Help',                      sel: '.help-row a, .site-menu-row, a.gp-row[href*="help"]' },""",
     """    { id: 'blog',     key: 'G',            page: 'all',  name: 'Blog',                      sel: 'a.nav-link[href*="blog"], .help-row a[href*="blog"], a[href$="blog/index.html"], a[href$="/blog/"]' },
    { id: 'help',     key: 'H',            page: 'all',  name: 'Help',                      sel: 'a.nav-link[href*="help"], .site-menu-row, a.gp-row[href*="help"], .help-row a[href*="help"]' },"""),
])

# -------------------------------------------------------------- build_blog.py
patch('build_blog.py', [
    # 1) cover image inside the article page
    ("""      <div class="hc-body">{content}</div>""",
     """      <figure class="blog-doc-cover"><img src="../img/{art['id']}.jpg" alt="" width="1200" height="675" loading="eager" onerror="this.parentNode.style.display='none'"></figure>
      <div class="hc-body">{content}</div>"""),
    # 2) tighter gap between caption and read-time/date
    ("""    .bcard-meta { margin-top: auto; padding-top: 4px; font-size: .78rem; color: var(--text-dim); }""",
     """    .bcard-meta { margin-top: 0; padding-top: 2px; font-size: .78rem; color: var(--text-dim); }"""),
    ("""    .blog-doc .hc-body { margin-top: 22px; }""",
     """    .blog-doc-cover { margin: 16px 0 4px; border-radius: 14px; overflow: hidden;
      border: 1px solid var(--border); }
    .blog-doc-cover img { display: block; width: 100%; height: auto; }
    .blog-doc .hc-body { margin-top: 16px; }"""),
    # 3) bot links block inside every article
    ("""      {related_for(art)}""",
     """      <div class="blog-bot-links">
        <b>Try it in Telegram</b>
        <p>Fast Scheduler is free to start: open <a href="{BOT_URL}" target="_blank" rel="noopener noreferrer">@FastSchedulerBot</a>, send your posts with dates, and it publishes them on schedule. Questions or setup help — the support chat is one tap away: <a href="{SUPPORT_URL}" target="_blank" rel="noopener noreferrer">@FastSchedulerSupport_bot</a>.</p>
      </div>
      {related_for(art)}"""),
    # CSS for both new blocks
    ("""    .blog-doc h1 { font-size: 2.05rem; margin: 0; letter-spacing: -.02em; line-height: 1.2; }""",
     """    .blog-doc h1 { font-size: 2.05rem; margin: 0; letter-spacing: -.02em; line-height: 1.2; }
    .blog-bot-links { margin: 22px 0 4px; padding: 14px 18px; border-radius: 14px;
      background: color-mix(in srgb, var(--green) 7%, var(--surface));
      border: 1px solid color-mix(in srgb, var(--green) 25%, var(--border)); }
    .blog-bot-links b { font-size: .82rem; letter-spacing: .05em; text-transform: uppercase;
      color: var(--green-strong); }
    .blog-bot-links p { margin: 6px 0 0; font-size: .92rem; line-height: 1.6; color: var(--text); }
    .blog-bot-links a { color: var(--green-strong); font-weight: 650; }"""),
])

# -------------------------------------------------------------- build_help.py
patch('build_help.py', [
    ("""<button type="button" class="hc-side-x" id="hcSideToggle" aria-label="Hide sidebar" title="Hide sidebar (O)">{svg('chev')}<kbd class="tab-kbd" aria-hidden="true">T</kbd></button>""",
     """<button type="button" class="hc-side-x" id="hcSideToggle" aria-label="Hide sidebar" title="Hide sidebar (O)">{svg('chev')}<kbd class="tab-kbd" aria-hidden="true">O</kbd></button>"""),
])

print('[done] round 3')
