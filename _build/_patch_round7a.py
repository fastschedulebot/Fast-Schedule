# -*- coding: utf-8 -*-
"""Patch round 7a (blog builder):

  design
    - uniform card grid: no lg/md spans -> no half-empty rows anywhere
  monetization order (matches the screenshot request)
    Monetize + Crypto | Paid subs + Affiliate | Stars + Sell + Sponsorships
  articles
    - "Try it in Telegram" block deleted (markup + CSS)
    - "More on this topic" -> ../index.html#cat=<id> (hub pre-filters)
  search
    - blog exports its full-text search index for the help center
"""
import io

P = 'build_blog.py'
s = io.open(P, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, n)

# 1) uniform cards -----------------------------------------------------------
rep("""def size_for(art, i):
    # Deterministic per-slug size mix: stable builds, varied bento layouts.
    pool = ('lg', 'sm', 'sm', 'md', 'sm', 'sm')
    return pool[(i + _hash(art['id'])) % len(pool)]""",
    """def size_for(art, i):
    # Uniform grid: every card the same size -> no half-empty rows anywhere.
    return 'sm'""")

rep("""    .s-lg, .s-md { grid-column: span 2; }
    .s-lg .bcard-body b { font-size: 1.18rem; }
    .s-lg .bcard-desc, .s-md .bcard-desc {
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }""",
    """    .bcard-desc {
      display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }""")

rep("    .bcard-desc { display: none; color: var(--text-dim); font-size: .88rem; line-height: 1.5; }",
    "    .bcard-desc { color: var(--text-dim); font-size: .88rem; line-height: 1.5; }")

# 2) monetization display order ---------------------------------------------
rep("""    secs = []
    for cid in order:""",
    """    secs = []
    # Monetization reading order: overview first, then rails, then selling.
    MONET_ORDER = ['monetize-telegram-channel', 'telegram-crypto-payments',
                   'telegram-paid-subscriptions', 'telegram-affiliate-marketing',
                   'telegram-stars-for-channel-owners', 'sell-products-in-telegram',
                   'telegram-sponsorships', 'telegram-channel-for-crypto-signals']
    mo = groups.get('money')
    if mo:
        mo.sort(key=lambda a: MONET_ORDER.index(a['id']) if a['id'] in MONET_ORDER else 99)
    for cid in order:""")

# 3) remove the "Try it in Telegram" block ----------------------------------
rep("""      <div class="blog-moreq"><a href="../index.html#q={bh.esc(art['category'])}">More on this topic{bh.svg('arrow-r')}</a></div>
      <div class="blog-bot-links">
        <b>Try it in Telegram</b>
        <p>Fast Scheduler is free to start: open <a href="{BOT_URL}" target="_blank" rel="noopener noreferrer">@FastSchedulerBot</a>, send your posts with dates, and it publishes them on schedule. Questions or setup help — the support chat is one tap away: <a href="{SUPPORT_URL}" target="_blank" rel="noopener noreferrer">@FastSchedulerSupport_bot</a>.</p>
      </div>
      {related_for(art)}""",
    """      <div class="blog-moreq"><a href="../index.html#cat={bh.esc(art['category'])}">More on this topic{bh.svg('arrow-r')}</a></div>
      {related_for(art)}""")

rep("""    .blog-bot-links { margin: 22px 0 4px; padding: 14px 18px; border-radius: 14px;
      background: color-mix(in srgb, var(--green) 7%, var(--surface));
      border: 1px solid color-mix(in srgb, var(--green) 25%, var(--border)); }
    .blog-bot-links b { font-size: .82rem; letter-spacing: .05em; text-transform: uppercase;
      color: var(--green-strong); }
    .blog-bot-links p { margin: 6px 0 0; font-size: .92rem; line-height: 1.6; color: var(--text); }
    .blog-bot-links a { color: var(--green-strong); font-weight: 650; }
""", "")

# 4) search index export -----------------------------------------------------
rep("""def cover_url(a):""",
    """def _search_docs():
    \"\"\"Full-text search index for the blog (used by the hub's results view
    and exported for the help center's unified search).\"\"\"
    docs = []
    for a in ARTICLES:
        body = re.sub(r'\\s+', ' ', re.sub(r'<[^>]+>', ' ', a['content'])).strip()
        faq = ' '.join((f['q'] + ' ' + re.sub(r'<[^>]+>', ' ', f['a']))
                       for f in a.get('faq') or []).strip()
        docs.append({'id': a['id'], 'c': a['category'], 't': a['title'],
                     'd': a['description'], 'b': body, 'f': faq})
    return json.dumps(docs, ensure_ascii=False)


def cover_url(a):""")

rep("    print(f'[ok] blog: {len(ARTICLES)} article pages + hub at blog/index.html')",
    "    # export the blog search index for the help center's unified search\n"
    "    io.open(os.path.join(HERE, '_blog_search_data.json'), 'w', encoding='utf-8').write(_search_docs())\n"
    "    print(f'[ok] blog: {len(ARTICLES)} article pages + hub at blog/index.html')")

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('[ok] build_blog.py design/order/blocks')
