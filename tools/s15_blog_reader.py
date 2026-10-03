# s15: blog — Reading settings in navbar (article pages), wide/rail/font CSS+JS,
# liquid-glass section reel, normal-case labels.
import io

BLOG = 'website/_build/build_blog.py'


def sub_once(old, new):
    s = io.open(BLOG, encoding='utf-8').read()
    assert old in s, 'anchor missing: %r' % old[:70]
    assert s.count(old) == 1, 'anchor not unique x%d: %r' % (s.count(old), old[:70])
    io.open(BLOG, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
    print('[ok]', old[:60].replace(chr(10), ' '))


# ---- 1. NOFLASH: apply blog reader state before first paint ----
sub_once(
    "if (localStorage.getItem('fs-rail') === 'off') document.documentElement.classList.add('rail-off');",
    "if (localStorage.getItem('fs-rail') === 'off') document.documentElement.classList.add('rail-off');\n"
    "    if (localStorage.getItem('fs-blog-wide') === 'on') document.documentElement.classList.add('blog-wide');\n"
    "    var _bf = localStorage.getItem('fs-blog-font');\n"
    "    if (_bf) document.documentElement.setAttribute('data-blogfont', _bf);")

# ---- 2. normal-case labels ----
sub_once(
    '.blog-toc-t { font-size: .72rem; font-weight: 800; letter-spacing: .06em; text-transform: uppercase;',
    '.blog-toc-t { font-size: .92rem; font-weight: 800; letter-spacing: -.01em;')
sub_once(
    '.blog-toc-navc small { display: block; font-size: .66rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--text-dim); }',
    '.blog-toc-navc small { display: block; font-size: .76rem; font-weight: 700; letter-spacing: 0; color: var(--text-dim); }')
sub_once(
    '.bcard-kicker { display: inline-flex; align-items: center; gap: 6px; font-size: .7rem;',
    '.bcard-kicker { display: inline-flex; align-items: center; gap: 6px; font-size: .78rem;')
sub_once(
    'font-weight: 800; letter-spacing: .07em; text-transform: uppercase;',
    'font-weight: 800; letter-spacing: 0;')
sub_once(
    'letter-spacing: .07em; text-transform: uppercase; color: #b07a1e; margin-left: 10px; }',
    'letter-spacing: 0; color: #b07a1e; margin-left: 10px; }')

# ---- 3. reader + reel CSS before BLOG_CSS close ----
sub_once(
    """    .hc-more[hidden] { display: none; }
    '''""",
    """    .hc-more[hidden] { display: none; }

    /* ---- reader settings (settings menu: Wide / Article navigation / Font) ---- */
    .gp-reading[hidden] { display: none !important; }
    @media (max-width: 1020px) {
      #settingsMenu [data-blog-wide], #settingsMenu [data-blog-rail] { display: none !important; }
    }
    .gp-row.gp-fonts { cursor: default; }
    .hc-fonts { display: inline-flex; align-items: baseline; gap: 2px; margin-left: auto; }
    .hc-fonts button { font: inherit; background: none; border: 0; cursor: pointer; color: var(--text-dim);
      padding: 3px 8px; border-radius: 8px; font-weight: 800; line-height: 1; }
    .hc-fonts button:hover { color: var(--green-strong); }
    .hc-fonts button.on { color: #fff; background: var(--green-strong); }
    .hc-fonts button:nth-child(1) { font-size: .78rem; }
    .hc-fonts button:nth-child(2) { font-size: .95rem; }
    .hc-fonts button:nth-child(3) { font-size: 1.12rem; }
    html[data-blogfont="s"] .blog-doc .hc-body { font-size: .88rem; }
    html[data-blogfont="l"] .blog-doc .hc-body { font-size: 1.12rem; }
    html.blog-wide .blog-cols { grid-template-columns: minmax(0, 1fr); }
    html.blog-wide .blog-toc { display: none; }
    html.blog-wide .blog-doc { max-width: 960px; margin: 0 auto; width: 100%; }
    html.rail-off .blog-cols { grid-template-columns: minmax(0, 1fr); }
    html.rail-off .blog-toc { display: none; }
    /* ---- liquid-glass section reel: floating prev/current/next ---- */
    .blog-reel { position: fixed; left: 50%; bottom: calc(18px + env(safe-area-inset-bottom)); z-index: 90;
      transform: translateX(-50%) translateY(24px); width: min(340px, calc(100vw - 32px));
      border-radius: 18px; padding: 10px 16px 12px; opacity: 0; pointer-events: none;
      transition: opacity .3s, transform .3s cubic-bezier(.22,.61,.36,1);
      background: linear-gradient(135deg, color-mix(in srgb, var(--surface) 62%, transparent), color-mix(in srgb, var(--surface-2) 45%, transparent));
      -webkit-backdrop-filter: blur(18px) saturate(1.4); backdrop-filter: blur(18px) saturate(1.4);
      border: 1px solid color-mix(in srgb, #fff 22%, var(--border));
      box-shadow: 0 12px 40px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.18); overflow: hidden; }
    .blog-reel.show { opacity: 1; pointer-events: auto; transform: translateX(-50%); }
    .blog-reel::after { content: ''; position: absolute; inset: 0; pointer-events: none;
      background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,.14) 45%, transparent 60%);
      transform: translateX(-110%); animation: reelSheen 7s ease-in-out infinite; }
    @keyframes reelSheen { 0%, 72% { transform: translateX(-110%); } 88%, 100% { transform: translateX(110%); } }
    .blog-reel button { display: block; width: 100%; background: none; border: 0; padding: 0; font: inherit;
      color: var(--text-dim); cursor: pointer; text-align: center; }
    .blog-reel button span { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .blog-reel [data-reel-prev] span, .blog-reel [data-reel-next] span { font-size: .74rem; font-weight: 600; opacity: .75; }
    .blog-reel [data-reel-cur] { margin: 2px 0; }
    .blog-reel [data-reel-cur] span { font-size: 1rem; font-weight: 800; letter-spacing: -.01em; color: var(--text); }
    .blog-reel [data-reel-cur]::before { content: ''; display: block; width: 6px; height: 6px; border-radius: 50%;
      background: var(--green); margin: 0 auto 4px; box-shadow: 0 0 8px var(--green); }
    .blog-reel.swap [data-reel-cur] span { animation: reelSwap .32s cubic-bezier(.22,.61,.36,1) both; }
    @keyframes reelSwap { 0% { opacity: 0; transform: translateY(10px) scale(.94); } 60% { opacity: 1; transform: translateY(-1px) scale(1.02); } 100% { opacity: 1; transform: none; } }
    html[data-motion="off"] .blog-reel::after, html[data-motion="off"] .blog-reel.swap [data-reel-cur] span { animation: none; }
    '''""")

# ---- 4. header(): reading flag + rows ----
sub_once(
    '''def header(rel):
    """Same structure as the legal pages' header (build_site._nav): brand,
    nav links, Help quick-search popover, settings menu, Open Bot CTA."""
    return f\\'\\'\\'<header class="site">''',
    '''def header(rel, reading=False):
    """Same structure as the legal pages' header (build_site._nav): brand,
    nav links, Help quick-search popover, settings menu, Open Bot CTA."""
    _reading = ''
    if reading:
        _reading = f\\'\\'\\'<div class="gp-sep gp-reading" data-blog-reading></div>
          <div class="gp-head gp-reading" data-blog-reading>Reading</div>
          <button type="button" class="gp-row gp-reading" data-blog-reading role="menuitemcheckbox" aria-checked="false" data-blog-wide>{bh.svg('expand')}<span>Wide format</span><span class="io-switch" aria-hidden="true"></span></button>
          <button type="button" class="gp-row gp-reading" data-blog-reading role="menuitemcheckbox" aria-checked="true" data-blog-rail>{bh.svg('book')}<span>Article navigation</span><span class="io-switch" aria-hidden="true"></span></button>
          <div class="gp-row gp-reading gp-fonts" data-blog-reading data-blog-fonts>{bh.svg('book')}<span>Font size</span><span class="hc-fonts"><button type="button" data-font="s" aria-label="Small">A</button><button type="button" data-font="m" aria-label="Default">A</button><button type="button" data-font="l" aria-label="Large">A</button></span></div>\\'\\'\\'
    return f\\'\\'\\'<header class="site">''')

sub_once(
    '        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp"',
    '        {_reading}\n        <button type="button" class="gp-row gp-row-sub" id="rowKeysHelp"')

# ---- 5. page_shell(): reading flag passthrough ----
sub_once(
    "def page_shell(title_html, body, rel='..', extra_js='', body_cls='blog'):",
    "def page_shell(title_html, body, rel='..', extra_js='', body_cls='blog', reading=False):")
sub_once(
    '{header(rel)}',
    '{header(rel, reading)}')

# ---- 6. article pages get Reading menu ----
sub_once(
    "html = page_shell(head, body, rel='../..', extra_js=TOC_JS)",
    "html = page_shell(head, body, rel='../..', extra_js=TOC_JS, reading=True)")

# ---- 7. reel container in article body ----
sub_once(
    """  {toc_html(heads)}
</div>'''""",
    """  {toc_html(heads)}
</div>
<div class="blog-reel" data-blog-reel hidden aria-hidden="true"><button type="button" data-reel-prev tabindex="-1"><span></span></button><button type="button" data-reel-cur tabindex="-1"><span></span></button><button type="button" data-reel-next tabindex="-1"><span></span></button></div>'''""")

print('s15 part 1 done')
