# -*- coding: utf-8 -*-
"""Blog articles, part 3 — NEW topics (polls, media, stars, bots-from-scratch,
fonts, migration, privacy, comments, mistakes, niches deep-dives…).
Same editorial rules: real tools named as plain text, no links, no sugar."""

BLOG_ARTICLES_C = []

def _c(i, **kw):
    kw['id'] = i
    BLOG_ARTICLES_C.append(kw)

# ---------------------------------------------------------------- CONTENT --
_c('telegram-polls-guide',
   category='content',
   title='How to Use Polls in a Telegram Channel (They’re Underrated)',
   description='Polls are Telegram’s cheapest engagement engine: anonymous vs public votes, quiz mode, un/quizzes in channels vs groups, 12 question-type tricks, and how polls feed the algorithm.',
   date='2026-09-26',
   content=(
       "<p>Polls are the most underused feature in Telegram channels. They cost nothing, take "
       "the reader three seconds, and generate the engagement signals that feed Telegram’s "
       "recommendation surfaces. Here’s how the format actually works and where it shines.</p>"

       "<h3>The poll types (and the one nobody uses right)</h3>"
       "<ul>"
       "<li><b>Regular poll</b> — voters pick, results visible. The workhorse.</li>"
       "<li><b>Anonymous vs public</b> — in channels, votes are always anonymous to readers "
       "(only totals show); in groups you can expose who voted. Public votes in groups create "
       "gentle peer pressure — use for “who’s coming Friday”.</li>"
       "<li><b>Quiz mode</b> — one correct answer, revealed after voting. This is the "
       "engagement cheat code: quizzes get 2–3× the participation of plain polls because "
       "people can’t resist testing themselves.</li>"
       "<li><b>Multiple answers</b> — up to 10 options; essential for “which topics do you "
       "want next?” surveys.</li>"
       "</ul>"

       "<h3>Channels vs groups: the mechanics differ</h3>"
       "<p>In a <b>channel</b>, a poll is a broadcast: subscribers vote where they see it, "
       "results update live, nobody sees who voted. In a <b>discussion group</b>, polls become "
       "social — vote visibility, debate in threads, quote-replies. The pro move is posting "
       "the poll in the channel and letting the comment thread argue about it. That single "
       "habit puts engagement signals in two surfaces at once.</p>"

       "<h3>Little-known tricks</h3>"
       "<ul>"
       "<li><b>The “wrong answers only” poll</b> — quiz mode with deliberately silly options; "
       "the comment thread does the rest.</li>"
       "<li><b>The two-poll sequence</b> — Monday: “what should I cover?” (multiple answers). "
       "Friday: the winning topic. Readers see their vote mattered; that’s retention "
       "engineering.</li>"
       "<li><b>Binary choice beats open questions</b> — A/B polls (“Version 1 or 2?”) get "
       "more votes than “what do you think?” ever gets answers.</li>"
       "<li><b>Revoting</b> — polls can allow vote changes; for live decisions (naming "
       "something, choosing a date), enable it and watch options swing in real time.</li>"
       "</ul>"

       "<h3>Scheduling polls (yes, you can)</h3>"
       "<p>The native composer doesn’t schedule polls — a poll sent through a scheduling bot "
       "preserves its type and options. Most scheduling bots handle them: ControllerBot posts "
       "polls with full options, Fast Scheduler supports polls in batches and recurring slots "
       "(“Friday poll” as a recurring rule is a one-command setup). If your scheduler drops "
       "poll options, that’s a real limitation — test before committing your content plan.</p>"

       "<h3>What polls actually do for growth</h3>"
       "<p>Reactions and views feed aggregate engagement; votes are the lowest-friction "
       "reaction there is. Channels that poll weekly show steadier view curves — the "
       "subscribers who voted once come back to see results. Polls also mine content ideas: "
       "the losing options are next month’s posts.</p>"),

   faq=[
       {'q': 'Can you schedule a poll in Telegram?',
        'a': 'Not with the native scheduler, but scheduling bots support polls — ControllerBot and Fast Scheduler both publish polls with their options intact, including in recurring slots.',},
       {'q': 'Are Telegram channel polls anonymous?',
        'a': 'Yes — channel polls show only totals. In groups, admins can allow public votes where participant names are visible.',},
       {'q': 'What is quiz mode in Telegram polls?',
        'a': 'A poll with one predefined correct answer; the explanation appears after voting. Quizzes consistently out-poll regular polls for participation.',},
       {'q': 'How many options can a Telegram poll have?',
        'a': 'Up to 10 answers, with optional multiple choice and revoting. Keep 3–5 options for the cleanest results.',},
   ])

# ---------------------------------------------------------------- CONTENT --
_c('schedule-posts-with-photos-and-video',
   category='content',
   title='Scheduling Media Posts in Telegram: Photos, Albums, Video and the Limits',
   description='Media-grouping rules, the 10MB/50MB/2GB video ceilings, albums vs single photos, media storage for reused assets, and how scheduling bots handle albums, GIFs and captions.',
   date='2026-09-26',
   content=(
       "<p>Media posts are where scheduling gets technical. Albums break, captions detach, "
       "videos get compressed, and a bot that handled your text posts fine can mangle a photo "
       "dump. Here’s the full map of what works and what the limits actually are.</p>"

       "<h3>The limits that matter (2026)</h3>"
       "<ul>"
       "<li><b>Photos:</b> up to 10 photos per album, each compressed to Telegram’s photo "
       "format (~200–300KB effective). Send as file/document to keep full quality, but "
       "documents don’t preview as images in the feed.</li>"
       "<li><b>Video:</b> bots and clients send files up to 2GB, but most <i>publishing bots</i> "
       "cap uploads far lower (10–50MB) because media is stored server-side. Check your bot’s "
       "ceiling before planning video-heavy content.</li>"
       "<li><b>Album captions:</b> one caption per album (shown under the first item), 1024 "
       "characters. The caption travels with the whole album — front-load it.</li>"
       "<li><b>GIFs:</b> Telegram converts MP4s ≤ certain sizes into looping GIFs; true GIF "
       "files become MP4s. Either way they count as video for bots.</li>"
       "</ul>"

       "<h3>Albums: the grouping rules that trip everyone</h3>"
       "<ul>"
       "<li>Telegram groups photos sent in one burst (up to 10) into an album — with 1–2 "
       "second gaps between sends they arrive as separate messages. When a bot “rebuilt” your "
       "album as ten separate posts, that’s almost always why.</li>"
       "<li>Mixed albums (photos + videos) are allowed and usually preserved by bots — but "
       "test your exact mix before scheduling a month of them.</li>"
       "</ul>"

       "<h3>Media storage: the underrated feature</h3>"
       "<p>Reposting the same cover image, logo card or product shot every week is a queue "
       "killer. Some schedulers include a media-storage layer: upload reusable assets once, "
       "reference them in future posts. ControllerBot keeps recent media for reuse, and Fast "
       "Scheduler organizes reusable assets into named “storage boxes”; ManyBot-style simple "
       "bots make you re-send files every time. If your content system recycles visuals (and "
       "it should), storage pays for itself in a week.</p>"

       "<h3>Compression: when to fight it, when to accept it</h3>"
       "<ul>"
       "<li><b>Accept compression</b> for feed photos — Telegram’s format loads instantly, "
       "and readers on mobile data thank you.</li>"
       "<li><b>Send as document</b> for infographics, text-heavy cards and anything with "
       "small type — compression destroys readable text. Trade-off: documents preview as a "
       "file card, not an image.</li>"
       "<li><b>Video</b> gets recompressed for streaming; text in videos should be large and "
       "high-contrast.</li>"
       "</ul>"

       "<h3>A media-post checklist before scheduling</h3>"
       "<ul>"
       "<li>Album arrives as one album (not ten posts) in a test send?</li>"
       "<li>Caption under the right item, first 60 characters a hook?</li>"
       "<li>Video within the bot’s size ceiling, tested end-to-end once?</li>"
       "<li>Reused assets in storage instead of re-uploaded?</li>"
       "</ul>"),

   faq=[
       {'q': 'Can scheduling bots post albums?',
        'a': 'Yes — ControllerBot and Fast Scheduler both send photo groups as albums, preserving the caption. Always test-send once before queueing a batch, since grouping depends on send timing.',},
       {'q': 'What is the video size limit for scheduled Telegram posts?',
        'a': 'Telegram itself allows up to 2GB, but publishing bots store media server-side and cap uploads lower — commonly 10–50MB depending on plan. Check the bot’s limits page before planning video content.',},
       {'q': 'How do I keep image quality in Telegram?',
        'a': 'Send the image as a file/document to skip compression — it previews as a card. For feed photos, accept Telegram’s compression; it loads fast and looks fine at feed sizes.',},
       {'q': 'Can I reuse the same image in multiple scheduled posts?',
        'a': 'Yes, via media storage features — ControllerBot keeps recent media for reuse, and Fast Scheduler organizes reusable assets into named boxes. Without storage you re-upload files for every post.',},
   ])

# ---------------------------------------------------------------- TOOLS ----
_c('how-to-create-a-telegram-bot',
   category='tools',
   title='How to Create Your Own Telegram Bot with BotFather (Step by Step)',
   description='BotFather from zero: /newbot, tokens, descriptions and avatars, commands, privacy mode, inline mode — and what you can realistically build without writing code.',
   date='2026-09-26',
   content=(
       "<p>Every tool ecosystem in Telegram starts in the same place: <b>@BotFather</b>, the "
       "official bot that creates bots. Creating one takes two minutes and unlocks the whole "
       "platform — sender bots for your channel, custom assistants, even your own published "
       "bot. Here’s the full walkthrough.</p>"

       "<h3>Creating the bot (the 2-minute version)</h3>"
       "<ul>"
       "<li>1. Open <b>@BotFather</b> → send <code>/newbot</code>.</li>"
       "<li>2. Choose a <b>display name</b> (anything, changeable later).</li>"
       "<li>3. Choose a <b>username</b> — must end in <code>bot</code> (e.g. "
       "<code>MyChannelHelperBot</code>), globally unique, permanent.</li>"
       "<li>4. BotFather replies with your <b>API token</b> — a long string like "
       "<code>123456789:AAE…</code>. That token <i>is</i> the bot. Copy it somewhere safe and "
       "never share it.</li>"
       "</ul>"

       "<h3>Dressing the bot up (the part everyone skips)</h3>"
       "<ul>"
       "<li><code>/setuserpic</code> — an avatar; a bot without a face looks like spam.</li>"
       "<li><code>/setdescription</code> — the “What can this bot do?” text shown before "
       "start.</li>"
       "<li><code>/setabouttext</code> — the profile bio line.</li>"
       "<li><code>/setcommands</code> — the command menu (a list like "
       "<code>start – begin</code>, <code>help – how to use</code>) that appears in the input "
       "field. Sets expectations instantly.</li>"
       "</ul>"

       "<h3>The two switches that change behavior</h3>"
       "<ul>"
       "<li><b>Privacy mode</b> (<code>/setprivacy</code>) — in groups, a privacy-enabled bot "
       "only sees messages that mention it; disabled, it sees everything. Moderation bots "
       "like Rose and Combot need it off; a channel-posting bot doesn’t care.</li>"
       "<li><b>Inline mode</b> (<code>/setinline</code>) — lets users type <code>@yourbot "
       "query</code> in any chat. Only relevant if you build something with inline search.</li>"
       "</ul>"

       "<h3>Using the bot without writing code</h3>"
       "<p>The token’s main use for channel owners: <b>sender bots</b>. Add your new bot as an "
       "admin to your channel and connect the token to a publishing service — ControllerBot "
       "and Fast Scheduler both support it — and your posts publish under your brand instead "
       "of a third-party bot name. Beyond that, no-code bot builders exist for menus and "
       "auto-replies, and the Bot API is famously simple if you ever want to script "
       "something (a weekend of Python gets you surprisingly far).</p>"

       "<h3>Token hygiene (the security part)</h3>"
       "<ul>"
       "<li>Treat the token like a password: anyone holding it controls the bot.</li>"
       "<li>Leaked or compromised? <code>/revoke</code> in BotFather — instant, free, "
       "painless.</li>"
       "<li>Rotate tokens you haven’t touched in a year.</li>"
       "<li>Never paste tokens into unverified websites “analytics tools” — the official "
       "chat with BotFather or a reputable service is the only place they belong.</li>"
       "</ul>"),

   faq=[
       {'q': 'Is creating a Telegram bot free?',
        'a': 'Yes — BotFather is free and unlimited for personal use. Costs appear only if you host your own bot logic on a server or pay third-party services built on top.',},
       {'q': 'Can I rename a Telegram bot or change its username?',
        'a': 'Display name and avatar anytime via BotFather. The @username is permanent — choose it carefully, it ends in “bot” and must be unique.',},
       {'q': 'What can I do with a bot token?',
        'a': 'Control the bot via the Bot API: send messages it’s admin of, build menus and automations, or connect it to services as a “sender bot” so channel posts publish under your brand (ControllerBot and Fast Scheduler both support this).',},
       {'q': 'Someone got my bot token — what now?',
        'a': 'Revoke it immediately in BotFather (/mybots → API Token → Revoke), get a new one, and update it wherever the bot was connected. Old token dies instantly.',},
   ])

# ---------------------------------------------------------------- TOOLS ----
_c('telegram-stars-for-channel-owners',
   category='money',
   title='Telegram Stars Explained: What Channel Owners Can Actually Do With Them',
   description='Stars from the owner side: paid posts, channel subscriptions, gifts, withdrawal realities, pricing psychology, and how Stars compare to CryptoBot and classic ad money.',
   date='2026-09-26',
   content=(
       "<p>Telegram Stars are the platform’s in-app currency, and for channel owners they’ve "
       "quietly become a real monetization rail. Here’s the owner-side picture: what Stars "
       "unlock, what they pay, and where they beat (and lose to) other money paths.</p>"

       "<h3>What Stars buy in your channel</h3>"
       "<ul>"
       "<li><b>Paid photos/videos</b> — you mark media as paid; subscribers pay Stars to "
       "unlock. Works for exclusive shots, templates, preset packs.</li>"
       "<li><b>Channel subscriptions</b> — recurring Stars payments for a private channel "
       "tier. Telegram handles the paywall and renewal natively; you just set the price.</li>"
       "<li><b>Gifts</b> — subscribers send Stars gifts to the channel; a light monetization "
       "and engagement signal at once.</li>"
       "<li><b>Reactions with Stars</b> — paid reactions on posts. Mostly a Telegram "
       "Premium-user behavior, but it adds up on large channels.</li>"
       "</ul>"

       "<h3>The economics (the honest part)</h3>"
       "<ul>"
       "<li>Stars convert to rewards at Telegram’s published rate; app-store purchases (via "
       "Apple/Google) carry their usual cuts, so effective rates vary by purchase path. "
       "Check the current rates in Telegram’s own documentation before pricing — they shift.</li>"
       "<li>Withdrawal for channel owners runs through Telegram’s fragment/rewards flow "
       "rather than instant cash-out — plan for it as a slow drip, not payroll.</li>"
       "<li>Pricing psychology: Stars bundles make small prices feel trivial (199 Stars reads "
       "cheaper than $2.49), which favors impulse unlocks — exclusive content, not "
       "subscriptions.</li>"
       "</ul>"

       "<h3>Stars vs the alternatives</h3>"
       "<ul>"
       "<li><b>vs paid ad posts:</b> ad money (booked through Telega.in or direct) pays more "
       "per subscriber but taxes your content feed. Stars monetize the audience directly "
       "without renting their attention to anyone.</li>"
       "<li><b>vs CryptoBot:</b> CryptoBot is the peer-to-peer wallet bot — better for tips, "
       "invoices and paying contractors inside Telegram. Stars are better for in-feed "
       "monetization because the payment UI is native and frictionless.</li>"
       "<li><b>vs private-channel sales:</b> Stars subscriptions remove all payment plumbing "
       "(no manual invites, no external billing) at the cost of Telegram’s cut. For small "
       "tiers, the plumbing you don’t maintain is usually worth it.</li>"
       "</ul>"

       "<h3>A realistic starter setup</h3>"
       "<ul>"
       "<li>Free channel keeps its rhythm (scheduler-run, as always).</li>"
       "<li>One paid-media post per week — genuinely exclusive, advertised in the free feed "
       "with a teaser.</li>"
       "<li>Stars subscription tier for the archive + answers crowd, priced at impulse level.</li>"
       "<li>CryptoBot for tips and one-off purchases; Telega.in for ad inventory once the "
       "ratio is above 20%.</li>"
       "</ul>"),

   faq=[
       {'q': 'What are Telegram Stars?',
        'a': 'Telegram’s in-app currency. Users buy Stars and spend them on digital goods — including paid media, channel subscriptions and gifts in your channel. Owners convert collected Stars to rewards through Telegram’s payout system.',},
       {'q': 'Do I need Stars to run a paid private channel?',
        'a': 'No — classic invite-link sales (via CryptoBot or external payments) still work. Stars subscriptions just remove all the plumbing: Telegram handles billing, renewal and access automatically.',},
       {'q': 'How much does Telegram take from Stars?',
        'a': 'The effective cut depends on how the Stars were purchased (in-app purchases carry platform fees). Check Telegram’s current payout documentation — rates have shifted more than once.',},
       {'q': 'Are Stars worth it for a small channel?',
        'a': 'From ~1K engaged subscribers, one paid exclusive per week converts measurably. Below that, focus on growth first — Stars monetize attention that already exists.',},
   ])

# ---------------------------------------------------------------- GROWTH ---
_c('telegram-channel-mistakes',
   category='growth',
   title='15 Telegram Channel Mistakes That Quietly Kill Growth',
   description='The mistakes that don’t announce themselves: stacking posts, dead-hour publishing, caption walls, fake-subscriber temptations, ignoring the ratio — with the fix for each.',
   date='2026-09-26',
   content=(
       "<p>Channels rarely die from one big mistake. They bleed from small ones that never "
       "announce themselves. Fifteen of them, each with the fix — collected from watching "
       "hundreds of channels stall.</p>"

       "<h3>Publishing mistakes</h3>"
       "<ul>"
       "<li><b>1. Stacking posts.</b> Five posts in ten minutes = one muted channel. Space "
       "them hours apart — schedule the spacing, not just the sending.</li>"
       "<li><b>2. Dead-hour publishing.</b> Posting at 3 AM because that’s when you finished "
       "writing. Schedule for the audience’s prime time, not your free time.</li>"
       "<li><b>3. Caption walls.</b> 1,000-character captions on photos get truncated in "
       "previews. Hook in 60 characters, details in a text post.</li>"
       "<li><b>4. No signature.</b> Forwards without the channel name are free advertising "
       "you never receive. Toggle “sign messages” on.</li>"
       "<li><b>5. The midnight queue dump.</b> Batch-writing is good; releasing it all at "
       "once isn’t. Any scheduler (ControllerBot, Fast Scheduler, ManyBot) fixes this "
       "permanently.</li>"
       "</ul>"

       "<h3>Content mistakes</h3>"
       "<ul>"
       "<li><b>6. Topic drift.</b> Subscribers came for a promise. Every off-topic post "
       "mutes a few of them.</li>"
       "<li><b>7. The feed dump.</b> Unfiltered RSS/news reposts make you replaceable. "
       "Curation is the product.</li>"
       "<li><b>8. “Part 2” bait.</b> Splitting value across posts to inflate views teaches "
       "readers not to open part 1.</li>"
       "<li><b>9. Never asking.</b> No polls, no questions, no comment replies — a channel "
       "without interaction signals decays in the recommendation surfaces.</li>"
       "</ul>"

       "<h3>Growth mistakes</h3>"
       "<ul>"
       "<li><b>10. Buying subscribers.</b> Bot followers never read, and TGStat displays the "
       "damage permanently — swaps and advertisers check it before you get a reply.</li>"
       "<li><b>11. Swapping with zombies.</b> A 10K channel with a 8% view ratio delivers "
       "nothing. Vet on TGStat/Telemetr first.</li>"
       "<li><b>12. Ignoring the ratio.</b> Views ÷ subscribers is your currency everywhere; "
       "not knowing your number is sailing blind.</li>"
       "<li><b>13. Growing before retaining.</b> Buying ads into a leaky channel. Retention "
       "data first, ads second.</li>"
       "</ul>"

       "<h3>Operations mistakes</h3>"
       "<ul>"
       "<li><b>14. Manual-everything.</b> Posting by hand daily collapses around week six. "
       "Batch + schedule is the fix — this is the mistake behind most dead channels.</li>"
       "<li><b>15. No backup.</b> A channel’s asset is its content pipeline. Export it "
       "periodically (every major scheduler has an export) — “it won’t happen to me” is not "
       "a plan.</li>"
       "</ul>"

       "<p>None of these fixes cost money. That’s the point: Telegram punishes sloppiness, "
       "not poverty.</p>"),

   faq=[
       {'q': 'What is the most common Telegram channel mistake?',
        'a': 'Inconsistent publishing — usually manual posting that collapses under real life. It compounds into every other metric: view ratios, recommendation eligibility, swap credibility.',},
       {'q': 'Are bought Telegram subscribers really that bad?',
        'a': 'Yes — they never view posts, so they permanently depress your view-to-subscriber ratio, which TGStat displays publicly. Swap partners and advertisers see it before you can explain it.',},
       {'q': 'How do I know if my channel is dying?',
        'a': 'Falling first-hour views with stable subscriber count, rising mute indicators (fewer poll votes), and churn after every post burst. All three are visible in your scheduler’s per-post stats.',},
       {'q': 'How often should I back up my channel content?',
        'a': 'Monthly, and before any big change. Scheduler exports capture scheduled and recurring posts — rebuilding months of queue from memory is worse.',},
   ])

# ---------------------------------------------------------------- GROWTH ---
_c('telegram-niche-research',
   category='growth',
   title='How to Research a Telegram Niche Before You Start a Channel',
   description='A data-first niche validation routine: TGStat/Telemetr catalogs, engagement-rate math, gap analysis, and the 10-question checklist that predicts whether a channel will keep subscribers.',
   date='2026-09-26',
   content=(
       "<p>Most channels fail in week one — before the first post — by picking a niche from "
       "vibes. A single evening of research with the right tools predicts most of what six "
       "months of trial would teach. Here’s the routine.</p>"

       "<h3>Step 1: map the niche on TGStat / Telemetr</h3>"
       "<ul>"
       "<li>Search your topic in <b>TGStat’s</b> and <b>Telemetr’s</b> catalogs — these are "
       "the two standard analytics services, and their listings rank in Google too.</li>"
       "<li>Sort by <b>engagement rate (ERR)</b>, not subscriber count. A 3K channel with 35% "
       "ERR is a healthier niche signal than a 200K channel at 6%.</li>"
       "<li>Open the top five channels. Note: posting frequency, formats (text/photos/"
       "polls), time of day, and comment activity.</li>"
       "</ul>"

       "<h3>Step 2: the math that matters</h3>"
       "<ul>"
       "<li><b>Total niche reach:</b> sum the top 10 channels’ average views. Small total = "
       "small ceiling (maybe fine — local niches monetize oddly well).</li>"
       "<li><b>Engagement spread:</b> if everyone in the niche sits below 15% ERR, the "
       "audience is stale — a sign of bot-polluted history, not a bad topic.</li>"
       "<li><b>Churn shape:</b> TGStat’s subscriber graphs show whether channels grow in "
       "steps (swap-driven) or smoothly (content-driven). Smooth growers have the model you "
       "want.</li>"
       "</ul>"

       "<h3>Step 3: find the gap</h3>"
       "<p>Read the top channels’ last 30 posts each and score what’s missing:</p>"
       "<ul>"
       "<li>Nobody formats well? (Most don’t.) Better typography is an instant edge.</li>"
       "<li>Nobody posts consistently? Rhythm is a moat — see the view curves of channels "
       "that do.</li>"
       "<li>Nobody serves a sub-audience? “Python jobs” inside “programming jobs” is a "
       "classic wedge.</li>"
       "<li>Nobody uses comments? An active discussion group is retention other channels "
       "literally don’t have.</li>"
       "</ul>"

       "<h3>Step 4: the sustainability test</h3>"
       "<p>Answer honestly:</p>"
       "<ul>"
       "<li>Can I name 30 post ideas right now without research?</li>"
       "<li>Do I consume this topic’s material anyway?</li>"
       "<li>Would I still post weekly if nobody said anything for two months?</li>"
       "<li>Is there a monetization path I actually understand (ads via Telega.in, product, "
       "affiliate)?</li>"
       "</ul>"
       "<p>Four yeses = start tonight. Two or fewer = the niche is a costume; keep looking.</p>"

       "<h3>Step 5: set up the rhythm before announcing</h3>"
       "<p>Whatever the niche, the launch playbook is identical: 10–15 posts banked, fixed "
       "daily slot on a scheduler (ManyBot for simplicity, ControllerBot for reports, Fast "
       "Scheduler for batch queues on a free tier), signature on, discussion group attached. "
       "Research told you what to post; the pipeline makes sure you keep posting it.</p>"),

   faq=[
       {'q': 'How do I find Telegram channels in a niche?',
        'a': 'TGStat and Telemetr catalogs are the standard — both are searchable, filterable channel directories with engagement data. Telegram’s in-app search and Google (“site:t.me” searches) fill the gaps.',},
       {'q': 'What engagement rate is good for a Telegram channel?',
        'a': '20–40% view-to-subscriber is healthy; ERR above 30% marks a strong channel in most niches. Compare within your niche — rates vary by topic and region.',},
       {'q': 'Is a small niche worth a channel?',
        'a': 'Often yes: small niches monetize through products and premium communities rather than ad volume, and competition for attention is thin. Check whether the top channels earn somehow — if they do, you can too.',},
       {'q': 'How many channels are too many in one niche?',
        'a': 'Matters less than the quality gap. Ten mediocre channels with one obvious gap (consistency, formatting, comments) is a better market than two strong ones with no gap.',},
   ])

# ---------------------------------------------------------------- PLATFORM -
_c('telegram-privacy-for-channel-owners',
   category='platform',
   title='Telegram Privacy Settings Every Channel Owner Should Know',
   description='What subscribers can see about you: phone number, last seen, profile photos, forwards and your personal account — the settings that separate a channel persona from a private life.',
   date='2026-09-26',
   content=(
       "<p>Running a channel means strangers click your name. Telegram gives you precise "
       "control over what they find — but the defaults leak more than most owners realize. "
       "Here’s the tour that matters.</p>"

       "<h3>What subscribers can see by default</h3>"
       "<ul>"
       "<li>Your <b>profile photo</b> (all of them, in the photo tab).</li>"
       "<li>Your <b>bio</b> and (if set) username.</li>"
       "<li><b>Last seen & online status</b> — “last seen recently” by default, which is "
       "vague enough for most; check Settings → Privacy and Security.</li>"
       "<li>Your <b>phone number</b> — default is “Everybody” for contacts but hidden from "
       "the public; verify it’s “My Contacts” or “Nobody”.</li>"
       "</ul>"

       "<h3>The settings worth five minutes</h3>"
       "<ul>"
       "<li><b>Settings → Privacy and Security → Phone Number → Nobody.</b> Non-negotiable "
       "for channel owners with public personas.</li>"
       "<li><b>Last seen → Everybody / Contacts.</b> “Nobody” looks suspicious; “Everybody” "
       "with granular exceptions is the sweet spot.</li>"
       "<li><b>Profile photos → Everybody</b> but curate <i>which</i> photos; the public "
       "photo tab shows everything not marked private.</li>"
       "<li><b>Forwarded messages</b> — your name shows on anything you forward from private "
       "chats. If the channel persona and private life differ, never forward personal chats "
       "into channel-adjacent spaces.</li>"
       "</ul>"

       "<h3>Channels, comments and your personal account</h3>"
       "<p>Channel posts are anonymous by design — the channel signs them, not you. But the "
       "linked <b>discussion group</b> is a different surface: replies you write there come "
       "from your personal account unless you post as the channel (the composer lets you "
       "switch identity in groups where you’re admin). Decide once: owners who answer "
       "comments as the channel keep the persona clean and get better engagement — readers "
       "trust the brand, not the human behind it.</p>"

       "<h3>Bots and privacy (the part people fear needlessly)</h3>"
       "<ul>"
       "<li>A publishing bot sees only what it’s granted: post rights in the channel, "
       "nothing about you personally.</li>"
       "<li>Moderation bots (Combot, Rose, Shieldy) see group messages — that’s their job "
       "and it stops there.</li>"
       "<li>No bot needs your phone number, login code or 2FA password — ever. Those asks "
       "are always attacks.</li>"
       "<li>Token hygiene is privacy hygiene: a leaked sender-bot token lets strangers speak "
       "as your brand. BotFather → revoke, 30 seconds.</li>"
       "</ul>"

       "<h3>The two-account pattern (if you need it)</h3>"
       "<p>Telegram allows multiple accounts on one device. Owners who mix business with "
       "personal chats often run the channel from a dedicated account — clean history, "
       "clean persona, zero risk of cross-forwarding. It’s overkill for most, but it "
       "completely solves the “my private life is one tap from my subscribers” problem.</p>"),

   faq=[
       {'q': 'Can Telegram channel subscribers see my phone number?',
        'a': 'Not unless you set phone number visibility to Everybody. Check Settings → Privacy and Security → Phone Number and keep it on “My Contacts” or “Nobody”.',},
       {'q': 'Can I reply to channel comments without showing my personal account?',
        'a': 'Yes — in the linked discussion group, admin accounts can post as the channel itself via the identity switch in the composer. Replies signed as the channel also build brand trust.',},
       {'q': 'Do bots that post to my channel see my private data?',
        'a': 'No. A scheduler or moderation bot acts within the rights you granted — channel posting rights or group message access. Nothing touches your personal profile, and no legitimate bot ever asks for your login code or 2FA.',},
       {'q': 'Should I run my channel from a second Telegram account?',
        'a': 'If your channel persona and personal life must stay separate, yes — Telegram supports multiple accounts on one device. For most owners, tightened privacy settings plus posting-as-channel in comments are enough.',},
   ])

# ---------------------------------------------------------------- PLATFORM -
_c('telegram-comments-and-discussion-groups',
   category='platform',
   title='How Telegram Comments Work (and How to Make Discussion Groups Thrive)',
   description='Linked groups explained: posting as the channel, moderation stacks with Combot/Rose/Shieldy, slow mode, comment etiquette, and the formats that make readers actually reply.',
   date='2026-09-26',
   content=(
       "<p>A channel without comments is a billboard. The linked discussion group turns it "
       "into a place — but only if you run the group half as seriously as the channel. "
       "Here’s how comments really work and how owners get them alive.</p>"

       "<h3>The mechanics (30 seconds)</h3>"
       "<ul>"
       "<li>Settings → Discussion → add a group. Every channel post then appears in the "
       "group as a message with a “comments” thread.</li>"
       "<li>Replies in the group never appear in the channel — the channel stays clean; the "
       "group holds the noise and the conversation.</li>"
       "<li>As a channel admin you post in the group <b>as the channel</b> (identity switch "
       "in the composer) or as yourself. Channel-identity replies read as official; "
       "personal replies read as human. Pick per channel — consistency wins either way.</li>"
       "</ul>"

       "<h3>Getting comments to exist (the hard part)</h3>"
       "<ul>"
       "<li><b>End posts with a question that has a low answer cost.</b> “Which of these "
       "are you guilty of?” outperforms “What do you think?” ten to one.</li>"
       "<li><b>Polls in the channel, arguments in the group.</b> The poll collects votes; "
       "the comment thread collects opinions about the poll.</li>"
       "<li><b>Reply within the hour.</b> Early replies breed threads; unanswered questions "
       "breed silence.</li>"
       "<li><b>Feature commenters.</b> “Best reply this week” in a Friday post makes being "
       "interesting in your group socially rewarded.</li>"
       "</ul>"

       "<h3>Moderation: the minimum viable stack</h3>"
       "<ul>"
       "<li><b>Shieldy</b> — the anti-spam gate: captcha for newcomers, flood and link "
       "protection. Free, set-and-forget.</li>"
       "<li><b>Combot</b> — the standard: activity analytics, reputation, moderation logs, "
       "warnings. Its leaderboard quietly gamifies participation.</li>"
       "<li><b>Rose</b> — deep configuration: locks, blacklists, approval modes, admin "
       "permissions. The choice when Shieldy+Combot aren’t enough.</li>"
       "<li><b>Slow mode</b> — built into Telegram: 1 message per N seconds for members. "
       "Turn it on before your first spam wave, not after.</li>"
       "</ul>"

       "<h3>Etiquette rules that keep groups alive</h3>"
       "<ul>"
       "<li>Delete spam fast, argue never. A visible mod presence (Combot logs help) is "
       "cheaper than a dead group.</li>"
       "<li>Pin the group rules; three lines is enough.</li>"
       "<li>Never let the group’s rhythm replace the channel’s — the channel keeps "
       "publishing on schedule regardless of how chatty the group is. (This is why the "
       "scheduler and the moderation stack are separate tools: ControllerBot or Fast "
       "Scheduler runs the channel; Combot/Rose/Shieldy run the room.)</li>"
       "</ul>"),

   faq=[
       {'q': 'How do I enable comments on a Telegram channel?',
        'a': 'Channel Settings → Discussion → attach a group. Every post gets a comment thread; group members see channel posts and can reply.',},
       {'q': 'Can I post in the discussion group as my channel instead of myself?',
        'a': 'Yes — admins see an identity switch in the composer. Posting as the channel reads official; posting as yourself reads human. Both work; consistency matters more than the choice.',},
       {'q': 'Which bots do I need for a Telegram discussion group?',
        'a': 'The common stack: Shieldy for anti-spam captcha, Combot for analytics and reputation, Rose for deep moderation config. A new group needs Shieldy at minimum before you promote anywhere.',},
       {'q': 'Do comments show up in the channel feed?',
        'a': 'No — channel stays clean; replies live only in the linked group. Subscribers jump to them from the “comments” button under each post.',},
   ])

# ---------------------------------------------------------------- CONTENT --
_c('telegram-fonts-and-rich-text',
   category='content',
   title='Telegram Formatting Secrets: Bold, Monospace, Spoilers and Custom Emoji',
   description='Every text entity Telegram supports — including the ones the mobile composer hides — plus markdown shortcuts, custom emoji packs for channels, and where formatting gets lost.',
   date='2026-09-26',
   content=(
       "<p>Telegram’s text engine supports more formatting than any mainstream social "
       "platform — and half of it is hidden behind menus you’ve never opened. The full map, "
       "plus where formatting silently breaks.</p>"

       "<h3>The complete entity list</h3>"
       "<ul>"
       "<li><b>Bold, italic, underline, strikethrough</b> — the basics; mobile composer "
       "hides underline behind the biu menu, desktop uses Ctrl+U.</li>"
       "<li><b>Monospace</b> — <code>fixed-width</code> for dates, prices, code. Instantly "
       "signals “this is data”.</li>"
       "<li><b>Spoilers</b> — tap-to-reveal black bars. Use as a curiosity device: "
       "predictions, answers, punchlines.</li>"
       "<li><b>Block quotes</b> — the expandable quote block (desktop composer, and bots "
       "via the API). Underused and beautiful for citations.</li>"
       "<li><b>Nested lists?</b> — no. Telegram has no native lists; people fake them with "
       "emoji bullets. That’s why “1️⃣ 2️⃣ 3️⃣” headers look native here.</li>"
       "</ul>"

       "<h3>Markdown shortcuts power users actually use</h3>"
       "<p>In the message field: <code>**bold**</code>, <code>__italic__</code>, "
       "<code>`monospace`</code>, <code>||spoiler||</code> work in most clients (and in the "
       "bots that accept markdown). Faster than any menu once it’s in your fingers.</p>"

       "<h3>Custom emoji for channels</h3>"
       "<p>Channels can use <b>custom emoji packs</b> — Telegram Premium users create them, "
       "but everyone sees them in your posts. A branded pack (your mascot reacting, your "
       "niche’s in-jokes) is a subtle status marker; packs are made in the @stickers bot. "
       "Custom emoji count against your formatting, not your character budget.</p>"

       "<h3>Where formatting gets lost (and how bots fix it)</h3>"
       "<ul>"
       "<li>Copy-pasting from Word/Google Docs brings invisible characters that break "
       "formatting — paste into a plain editor first when it matters.</li>"
       "<li>Editing a published post on a different device can drop entities the second "
       "client doesn’t render.</li>"
       "<li>The native scheduler preserves formatting but shows no preview; scheduling bots "
       "compete on this — ControllerBot and Fast Scheduler both render a preview of the "
       "final message before it queues, which catches broken markdown before your "
       "subscribers do.</li>"
       "</ul>"

       "<h3>A formatting kit that survives scrolling</h3>"
       "<ul>"
       "<li>One bolded takeaway per paragraph (the scanning layer).</li>"
       "<li>One emoji per section header, never mid-sentence.</li>"
       "<li>Monospace for anything a reader might copy: dates, prices, links.</li>"
       "<li>Spoilers for genuine reveals — never for load-bearing information.</li>"
       "</ul>"),

   faq=[
       {'q': 'How do I underline text in Telegram?',
        'a': 'Mobile: select text → BIU menu → underline. Desktop: Ctrl+U (Cmd+U). Bots and scheduling tools accept underline entities too — it survives scheduling if the bot supports rich formatting.',},
       {'q': 'What are Telegram spoilers?',
        'a': 'Tap-to-reveal regions (||double pipes|| in markdown-style input). Great for answers and reveals; annoying if overused for basic information.',},
       {'q': 'What is monospace used for in Telegram posts?',
        'a': 'Anything data-like: dates, prices, commands, code. Fixed-width makes it visually distinct and copy-paste safe.',},
       {'q': 'Does scheduling a post keep its formatting?',
        'a': 'Yes with bots that support rich entities — ControllerBot and Fast Scheduler preview and preserve bold, spoilers, monospace and custom emoji through editing and scheduling.',},
   ])

# ---------------------------------------------------------------- TOOLS ----
_c('telegram-analytics-tools-compared',
   category='tools',
   title='Telegram Analytics Compared: TGStat vs Telemetr vs Your Scheduler’s Stats',
   description='What each analytics layer actually measures — TGStat’s ERR and citation index, Telemetr’s ad analytics, Combot for groups, and built-in scheduler stats — and which to use for which decision.',
   date='2026-09-26',
   content=(
       "<p>“Check your analytics” is useless advice until you know which tool answers which "
       "question. Telegram has three analytics layers, and confusing them wastes money and "
       "weeks. Here’s the comparison by use case.</p>"

       "<h3>Layer 1: TGStat — the public record</h3>"
       "<ul>"
       "<li><b>What it is:</b> the reference analytics + catalog service for public "
       "channels. Anyone can look up any channel.</li>"
       "<li><b>Key numbers:</b> average post reach, <b>ERR</b> (engagement rate per reach — "
       "views vs subscribers), subscriber dynamics, <b>citation index</b> (how often other "
       "channels link you).</li>"
       "<li><b>Use it for:</b> vetting swap partners, benchmarking your niche, being "
       "vetted by advertisers. Your TGStat page is your public credit report.</li>"
       "<li><b>Limitation:</b> public aggregates only — no per-hour view curves for your "
       "own decision-making.</li>"
       "</ul>"

       "<h3>Layer 2: Telemetr — the advertiser’s microscope</h3>"
       "<ul>"
       "<li><b>What it is:</b> the second major analytics/catalog platform, strongest on "
       "<b>ad analytics</b>: which channels run whose ads, price estimates, audience "
       "overlap.</li>"
       "<li><b>Use it for:</b> pricing your ad inventory, checking a channel’s ad history "
       "before buying, competitive recon in your niche.</li>"
       "<li><b>Limitation:</b> same as TGStat’s — public-facing, aggregate.</li>"
       "</ul>"

       "<h3>Layer 3: your scheduler’s stats — the decision layer</h3>"
       "<ul>"
       "<li><b>What it is:</b> per-post analytics from the tool that actually publishes for "
       "you. ControllerBot reports views and engagement per post; Fast Scheduler charts "
       "view dynamics per post plus sends and channel history.</li>"
       "<li><b>Use it for:</b> the questions that matter weekly — which slot performs, "
       "which content shape gets first-hour views, what to make more of.</li>"
       "<li><b>Limitation:</b> your channel only; no market context.</li>"
       "</ul>"

       "<h3>(Bonus) Combot — the group layer</h3>"
       "<p>For the discussion group: member activity, reputation, top commenters, moderation "
       "history. Group health predicts channel retention — a thriving comment section shows "
       "up in Combot before it shows anywhere else.</p>"

       "<h3>The decision matrix</h3>"
       "<ul>"
       "<li>“Should I swap with this channel?” → TGStat/Telemetr.</li>"
       "<li>“What should I post Tuesday?” → scheduler stats.</li>"
       "<li>“What do I charge for an ad?” → Telemetr comps + your TGStat ERR.</li>"
       "<li>“Is my community healthy?” → Combot.</li>"
       "<li>“When should I post?” → your scheduler’s first-hour curves (native stats are "
       "too coarse).</li>"
       "</ul>"),

   faq=[
       {'q': 'What is ERR in TGStat?',
        'a': 'Engagement Rate per Reach — average post views relative to subscriber count. It normalizes channel size so a 3K channel can be compared honestly with a 300K one. Above 30% is strong in most niches.',},
       {'q': 'Do I need paid analytics for a small channel?',
        'a': 'No — TGStat’s free lookups cover vetting and benchmarking, and your scheduler’s built-in stats cover daily decisions. Paid tiers matter once you trade ad inventory seriously.',},
       {'q': 'Why do TGStat numbers differ from my channel’s stats?',
        'a': 'They sample and average differently (time windows, post selection). Both are honest; use TGStat for public comparison and your scheduler’s numbers for operational decisions.',},
       {'q': 'Which Telegram analytics shows who viewed my post?',
        'a': 'None — Telegram doesn’t expose individual viewers. Views are anonymous counts; the deepest public signal is the view curve over time, which scheduling bots chart per post.',},
   ])

# ---------------------------------------------------------------- MONEY ----
_c('sell-products-in-telegram',
   category='money',
   title='Selling in Telegram: From Tip Jar to Full Shop (Without a Website)',
   description='The no-website sales stack: CryptoBot invoices, Stars paid content, order-taking bots, catalog bots, payment flow patterns that work in channels, and trust signals buyers check.',
   date='2026-09-26',
   content=(
       "<p>Telegram is quietly one of the easiest places to sell without a website: payments, "
       "delivery and even storefronts live inside the app. Here’s the stack, from “take tips” "
       "to “run orders”, with the trust mechanics that make people actually pay.</p>"

       "<h3>Level 1: tips and donations</h3>"
       "<ul>"
       "<li><b>CryptoBot</b> — the established wallet bot: generate payment links/invoices "
       "in a few taps, keep balance in-app. The default tip jar for channels.</li>"
       "<li><b>Telegram Stars gifts</b> — zero-setup; readers gifted your channel already "
       "have a way to say thanks.</li>"
       "<li>Pin a small “support” card with your CryptoBot link; repeat it quarterly, not "
       "weekly — begging frequency taxes goodwill.</li>"
       "</ul>"

       "<h3>Level 2: selling digital goods</h3>"
       "<ul>"
       "<li><b>Paid media with Stars</b> — mark a photo/video as paid; Telegram handles "
       "unlocking natively. Perfect for single-file products (presets, checklists, "
       "templates).</li>"
       "<li><b>Manual delivery with CryptoBot invoices</b> — buyer pays the invoice, you "
       "send the file. Fine to start; automation comes later.</li>"
       "<li><b>Order bots</b> — shop-builder bots (several established ones) give you a "
       "catalog, cart and payment in a bot you link from the channel. Best for >5 products "
       "or physical goods with variations.</li>"
       "</ul>"

       "<h3>Level 3: the shop pattern that converts</h3>"
       "<ul>"
       "<li>Channel = audience and trust; <b>bot = store</b>; the link between them is "
       "pinned and repeated in relevant posts.</li>"
       "<li>Every product post: what it is, who it’s for, price in both currency and Stars, "
       "one proof (screenshot/result), payment link. No life stories.</li>"
       "<li>Deliver instantly where possible — file bots and paid media deliver in seconds, "
       "and instant delivery is the trust multiplier nobody talks about.</li>"
       "<li>Public “delivery confirmed” replies (with permission) compound faster than any "
       "discount.</li>"
       "</ul>"

       "<h3>Trust signals buyers check before paying you</h3>"
       "<ul>"
       "<li><b>Consistent publishing history</b> — a channel that posts on schedule for "
       "months (visible in the feed) reads as a real operation. This is the quiet reason "
       "scheduler-run channels outsell manual ones.</li>"
       "<li><b>Real engagement</b> — comments, poll votes, view ratios. Buyers check "
       "TGStat’s numbers on bigger channels before trusting a shop.</li>"
       "<li><b>Refund policy stated in one line</b> — even “no refunds after delivery” "
       "beats silence.</li>"
       "</ul>"

       "<h3>What not to do</h3>"
       "<ul>"
       "<li>Don’t move sales into DMs without a bot or invoice trail — disputes become "
       "unwinnable.</li>"
       "<li>Don’t spam the channel with product posts; the 1-in-5 content-to-ad ratio "
       "applies to your own products too.</li>"
       "<li>Don’t promise Telegram-Star refunds you can’t process — understand the "
       "payout/refund flow before launch day.</li>"
       "</ul>"),

   faq=[
       {'q': 'Can I sell products directly inside Telegram?',
        'a': 'Yes — paid media via Stars, CryptoBot invoices, and shop-builder bots all work without a website. The channel drives demand; a bot or native paid content handles payment and delivery.',},
       {'q': 'What is CryptoBot used for?',
        'a': 'It’s Telegram’s established wallet bot: balance, transfers, payment links and invoices. Channel owners use it for tips, product payments and paying contractors without leaving Telegram.',},
       {'q': 'Do I need a bot to take payments?',
        'a': 'For Stars paid content, no — Telegram handles it natively. For everything else (crypto invoices, order forms, catalogs), a bot is the standard mechanism.',},
       {'q': 'How do buyers trust a Telegram shop?',
        'a': 'Publishing consistency, visible engagement, public delivery confirmations and a stated refund line. A scheduled, active channel is itself the strongest trust signal.',},
   ])

# ---------------------------------------------------------------- GROWTH ---
_c('telegram-for-local-business',
   category='growth',
   title='Telegram for Local Businesses: A Channel That Customers Actually Read',
   description='Why local channels outperform local social pages: geo search, neighborhood mechanics, what to post between promos, and the booking/notification stack (bots, reminders) for small businesses.',
   date='2026-09-26',
   content=(
       "<p>Local businesses were Telegram’s quiet early adopters — bakeries, gyms, repair "
       "shops — because a channel beats every local social page on one metric: <b>posts "
       "actually reach customers</b>. No algorithm, no page suppression, just your subscriber "
       "list. Here’s the local playbook.</p>"

       "<h3>Setup: be findable in your city</h3>"
       "<ul>"
       "<li>Name = searchable words + city: “S inconspicuous — Barbershop Lisbon” beats "
       "“SharpCuts official”. In-app search ranks name matches; locals search “[service] + "
       "[city]”.</li>"
       "<li>Description = address line, hours, booking link. It indexes in Google too.</li>"
       "<li>Invite QR code at the physical counter — the offline→online funnel is the whole "
       "local game. Every receipt, every window sticker.</li>"
       "</ul>"

       "<h3>What to post (the 80/20 for local)</h3>"
       "<ul>"
       "<li><b>80% useful-local:</b> today’s menu, open slots, weather-dependent changes, "
       "new arrivals, staff introductions, neighborhood news you’d tell a regular anyway.</li>"
       "<li><b>20% promo:</b> offers with deadlines. Locals tolerate promos well because "
       "they’re neighbors, not an anonymous audience.</li>"
       "<li><b>Photos of real things:</b> today’s actual bread, this morning’s queue — "
       "authenticity beats production values locally.</li>"
       "</ul>"

       "<h3>The booking and notification stack</h3>"
       "<ul>"
       "<li><b>Reminder bots</b> — send scheduled appointment reminders to clients (many "
       "booking integrations and simple reminder bots exist; pick by reliability, not "
       "features).</li>"
       "<li><b>A scheduling bot for the channel itself</b> — “today’s specials” at 9:00 "
       "daily, recurring; weekly menu Friday evenings. This is the same pipeline every "
       "serious channel runs (ManyBot/ControllerBot/Fast Scheduler class tools), and it’s "
       "why the bakery’s channel posts at 8:59 whether the owner is proofing dough or "
       "asleep.</li>"
       "<li><b>Discussion group for regulars</b> — comments on posts, “does anyone want the "
       "last two slots” energy. Moderate lightly with Shieldy-class anti-spam; locals are "
       "not a spam target, mostly.</li>"
       "</ul>"

       "<h3>Why locals read channels but abandon pages</h3>"
       "<ul>"
       "<li>Notifications are opt-in and honored — every post lands.</li>"
       "<li>The channel doubles as an archive: “what was Monday’s menu?” is scrollable "
       "history.</li>"
       "<li>One-tap share: customers forward your post to the building chat — the "
       "neighborhood’s real network.</li>"
       "</ul>"

       "<h3>The one metric that matters locally</h3>"
       "<p>Not subscribers — <b>redemption</b>. Show-post → show-up conversion. Track it "
       "with simple codes (“mention this post”), and you’ll know your channel’s actual "
       "business value within a month.</p>"),

   faq=[
       {'q': 'Is Telegram good for a small local business?',
        'a': 'Yes — channel posts reach every subscriber (no algorithm), the channel is a searchable local archive, and forwarding into neighborhood chats is native. It outperforms local social pages on reach per post.',},
       {'q': 'How do local customers find my Telegram channel?',
        'a': 'In-app search (put service + city in the name), QR codes at the physical location, links on receipts and Google Maps profile, and word-of-mouth forwards.',},
       {'q': 'What should a local business post besides promotions?',
        'a': 'Daily useful updates: open slots, arrivals, changes, staff, local news. The 80/20 rule — 80% useful, 20% promotional — keeps subscribers from muting.',},
       {'q': 'Do I need bots as a local business?',
        'a': 'Two are enough: a scheduling bot for the channel’s daily rhythm, and a reminder bot for appointments. Add anti-spam (Shieldy-class) only if you open a discussion group.',},
   ])

# ---------------------------------------------------------------- CONTENT --
_c('telegram-video-content-guide',
   category='content',
   title='Video in Telegram Channels: Formats, Sizes, Views and What Actually Gets Watched',
   description='Video mechanics for channels: autoplay and compression, size ceilings for bots, circles vs regular video, length sweet spots by niche, and scheduling video without breaking albums.',
   date='2026-09-26',
   content=(
       "<p>Video works differently in Telegram than everywhere else: no autoplay feed "
       "farming, no watch-time algorithm — just files your subscribers chose to receive. "
       "That changes what “good video” means here. The practical guide.</p>"

       "<h3>The format map</h3>"
       "<ul>"
       "<li><b>Regular video</b> — compressed for streaming, scrubbable, up to 2GB "
       "client-side (bots typically cap 10–50MB server-side — check your publishing bot’s "
       "ceiling before planning).</li>"
       "<li><b>Video notes (circles)</b> — round messages recorded in-chat. Casual, "
       "personal, high-trust. Owners’ faces outperform studio production in channels "
       "consistently.</li>"
       "<li><b>GIF-style loops</b> — short MP4s looping inline; great for demos under 10 "
       "seconds.</li>"
       "<li><b>Video documents</b> — uncompressed, no streaming preview; only for assets "
       "readers download (templates, footage).</li>"
       "</ul>"

       "<h3>What gets watched in channels (vs feeds)</h3>"
       "<ul>"
       "<li><b>Under 90 seconds</b> for near-full view rates; Telegram viewers scrub more, "
       "abandon less — there’s no next-video trap pulling them away.</li>"
       "<li><b>Text-first framing:</b> a strong caption decides the watch. The caption is "
       "the thumbnail here — first 60 characters are your title.</li>"
       "<li><b>Circles beat production:</b> a 30-second circle from the founder gets more "
       "replies than an edited promo. Telegram culture rewards presence over polish.</li>"
       "<li><b>Subtitles win:</b> much of your audience reads in quiet places; burned-in "
       "subs lift completion rates visibly.</li>"
       "</ul>"

       "<h3>The technical traps (and the fixes)</h3>"
       "<ul>"
       "<li><b>Compression:</b> Telegram recompresses for streaming; text overlays must be "
       "large and high-contrast to survive.</li>"
       "<li><b>Album mixing:</b> video + photos group into albums, but caption behavior "
       "differs — test your exact mix once before queueing a batch.</li>"
       "<li><b>Scheduling:</b> the native composer barely schedules video beyond short "
       "horizons; publishing bots do it properly — ControllerBot and Fast Scheduler both "
       "queue video with captions intact, and Fast Scheduler’s media storage holds reusable "
       "clips so weekly formats don’t require re-uploads.</li>"
       "<li><b>Thumbnails:</b> Telegram picks a frame; use a bright first second if the "
       "frame matters.</li>"
       "</ul>"

       "<h3>A weekly video rhythm that works</h3>"
       "<ul>"
       "<li>One <b>circle</b> mid-week: face, one idea, 45 seconds.</li>"
       "<li>One <b>produced short</b> on the weekend slot: the niche’s shareable piece.</li>"
       "<li><b>Repost winners</b> as evergreen Saturdays — new subscribers haven’t seen "
       "them, and Telegram doesn’t punish reposts.</li>"
       "</ul>"),

   faq=[
       {'q': 'What video size can I schedule in Telegram?',
        'a': 'Telegram allows up to 2GB via clients, but publishing bots store media server-side and cap lower — commonly 10–50MB. Verify your bot’s limit before planning video content.',},
       {'q': 'What are Telegram video circles?',
        'a': 'Round video notes recorded in-app. Casual and personal, they consistently outperform polished promos for engagement in channels — presence beats production on Telegram.',},
       {'q': 'Can I schedule a video with a caption?',
        'a': 'Yes with publishing bots — ControllerBot and Fast Scheduler queue video with captions and preview the result. Test once before batching, since caption attachment differs for single video vs albums.',},
       {'q': 'How long should Telegram channel videos be?',
        'a': 'Under 90 seconds for near-full completion; circles 30–60 seconds. There’s no watch-time algorithm rewarding length — clarity beats duration.',},
   ])

# ---------------------------------------------------------------- GROWTH ---
_c('telegram-channel-migration',
   category='growth',
   title='How to Move a Telegram Channel: Merging, Renaming and Migrating Audiences',
   description='Changing a channel’s identity the safe way: renames that keep subscribers, the merge problem (Telegram has no merge), redirect channels, content-pipeline migration and the 30-day transition plan.',
   date='2026-09-26',
   content=(
       "<p>At some point every owner faces it: the niche drifted, the name no longer fits, or "
       "two channels should be one. Telegram handles some of this gracefully and none of it "
       "automatically. Here’s what moves and what doesn’t.</p>"

       "<h3>Renaming: safe, with one caveat</h3>"
       "<ul>"
       "<li><b>Name and description:</b> change freely — they’re metadata.</li>"
       "<li><b>The @link:</b> changeable but breaks old t.me links. If the old link is "
       "printed anywhere (business cards, other channels’ swap posts), announce the change "
       "a week ahead and keep a redirect: the old link stops working the moment you change "
       "it, so time the swap with a pinned post.</li>"
       "<li>Renaming keeps <b>all subscribers, history and stats</b>. TGStat history follows "
       "the channel ID, not the name — your public record survives.</li>"
       "</ul>"

       "<h3>Merging: the thing Telegram can’t do</h3>"
       "<p>There is <b>no native merge</b> — two channels are two channels forever. The "
       "working patterns:</p>"
       "<ul>"
       "<li><b>Announce-and-archive (the standard):</b> pin a goodbye post on the smaller "
       "channel with the big channel’s link; keep the small channel alive for a month "
       "cross-posting the highlights, then mute it. Expect 15–40% of subscribers to make "
       "the jump — people who never open the channel won’t see even the pinned post.</li>"
       "<li><b>Convert-to-redirect:</b> rename the small channel to mirror the big one’s "
       "brand (“OldName moved → @NewName”) and leave one pinned post. Cost: the dead "
       "channel still shows in search results, now pointing the right way.</li>"
       "<li><b>The event migration:</b> time the move to a content event (season restart, "
       "rebrand launch) — a reason to move converts better than a request to move.</li>"
       "</ul>"

       "<h3>Migrating the content pipeline (the part owners forget)</h3>"
       "<ul>"
       "<li><b>Scheduled and recurring posts:</b> these live in your scheduling bot’s "
       "account, not the channel. If the new channel replaces the old, reconnect the bot’s "
       "channel binding — with export/import tools this is minutes: ControllerBot and Fast "
       "Scheduler both export the full queue and restore it elsewhere. Rebuilding a month of "
       "queue by hand is the alternative.</li>"
       "<li><b>Media storage:</b> reusable assets move with the bot account too — one more "
       "reason to keep media in storage rather than re-uploaded per post.</li>"
       "<li><b>Discussion group:</b> a linked group can re-link to the new channel. "
       "Existing comment history stays in the group — a quiet win for continuity.</li>"
       "</ul>"

       "<h3>The 30-day transition plan</h3>"
       "<ul>"
       "<li><b>Week 1:</b> announce on both channels; pin the move; link in both bios.</li>"
       "<li><b>Week 2–3:</b> cross-post the best content; run the subscriber push with an "
       "incentive (a guide, an archive) on the destination channel.</li>"
       "<li><b>Week 4:</b> new channel fully on schedule (visible rhythm is what retains "
       "the arrivals); old channel muted to a redirect card.</li>"
       "</ul>"),

   faq=[
       {'q': 'Can I merge two Telegram channels?',
        'a': 'No native merge exists. The standard pattern is announce-and-archive: pin a redirect post on the smaller channel, cross-post for a month, expect 15–40% of subscribers to move.',},
       {'q': 'Will renaming my channel lose subscribers or history?',
        'a': 'No — rename keeps subscribers, posts and stats. Only the @link change breaks old t.me URLs, so announce it ahead and update printed materials.',},
       {'q': 'How do I move my scheduled posts to a new channel?',
        'a': 'They live in your scheduling bot, not the channel. Reconnect the bot to the new channel, or use its export/import to move the pipeline between accounts.',},
       {'q': 'Can a discussion group be linked to a different channel later?',
        'a': 'Yes — unlink and re-link in channel settings. Comment history stays with the group, which preserves community continuity across the move.',},
   ])

# ---------------------------------------------------------------- TOOLS ----
_c('telegram-bot-commands-cheatsheet',
   category='tools',
   title='The Channel Owner’s Bot Cheatsheet: Commands Worth Memorizing',
   description='The commands that actually matter across the tools you already use: BotFather essentials, scheduling basics, TGStat lookups, moderation staples — a one-page reference.',
   date='2026-09-26',
   content=(
       "<p>Nobody needs 500 commands. A channel owner needs about thirty, spread across the "
       "five tools that run everything. The cheatsheet.</p>"

       "<h3>@BotFather (bot management)</h3>"
       "<ul>"
       "<li><code>/newbot</code> — create a bot.</li>"
       "<li><code>/mybots</code> — list yours; edit name, avatar, commands.</li>"
       "<li><code>/revoke</code> (inside /mybots → API Token) — rotate a token instantly.</li>"
       "<li><code>/setprivacy</code> — control whether the bot reads group messages.</li>"
       "<li><code>/setcommands</code> — the menu users see in the input field.</li>"
       "</ul>"

       "<h3>Scheduling bots (the daily drivers)</h3>"
       "<p>Exact syntax differs — ManyBot is menu-driven, ControllerBot uses inline buttons, "
       "Fast Scheduler read date/message pairs — but the concepts are identical:</p>"
       "<ul>"
       "<li><b>New post:</b> date + time + content (several pairs can go in one message with "
       "batch-style schedulers).</li>"
       "<li><b>Recurring:</b> “every day 9:00” style rule for fixed slots.</li>"
       "<li><b>Queue/list:</b> see what’s pending; edit or reorder before send time.</li>"
       "<li><b>Channels:</b> connect/bind a channel; switch the default posting target.</li>"
       "<li><b>Sender bot:</b> add your BotFather token so posts publish under your brand.</li>"
       "<li><b>Timezone:</b> set it once, verify with a test post — most “wrong time” bugs "
       "live here.</li>"
       "<li><b>Backup/export:</b> periodic full export — every serious scheduler has one.</li>"
       "</ul>"

       "<h3>Moderation (group side)</h3>"
       "<ul>"
       "<li><b>Combot:</b> warn/mute/ban via reply-commands; its web panel holds the "
       "history.</li>"
       "<li><b>Rose:</b> <code>/lock</code>/<code>/unlock</code> for media types, "
       "<code>/ban</code>/<code>/mute</code>, <code>/filters</code> for blacklists.</li>"
       "<li><b>Shieldy:</b> mostly self-driving; config covers captcha strictness and link "
       "rules.</li>"
       "</ul>"

       "<h3>Analytics</h3>"
       "<ul>"
       "<li><b>TGStat / Telemetr:</b> no commands to memorize — they’re web lookups. The "
       "habit to build: check any channel’s stats before swapping, buying or copying "
       "strategy.</li>"
       "<li><b>Your scheduler’s stats screen:</b> weekly review ritual — top post, worst "
       "slot, next week’s plan.</li>"
       "</ul>"

       "<h3>The meta-skill</h3>"
       "<p>Commands are cheap; <b>the pipeline is the skill</b>: write Sunday, queue with "
       "times, review stats, repeat. Every bot above just removes friction from that loop — "
       "which is also exactly how to evaluate any new bot you’re offered: does it remove "
       "friction from the loop, or add a new app to check?</p>"),

   faq=[
       {'q': 'Do I need to learn bot commands to run a channel?',
        'a': 'Only a handful: create/rotate a token at BotFather, the schedule/list/recurring basics in your scheduler, and reply-moderation in your group bots. Everything else is menus.',},
       {'q': 'Which is easier for scheduling: ManyBot, ControllerBot or Fast Scheduler?',
        'a': 'ManyBot for simplicity, ControllerBot for reports, Fast Scheduler for batch workflows (many posts in one message). All three cover the core schedule-list-recurring loop.',},
       {'q': 'How do I rotate a bot token safely?',
        'a': 'BotFather → /mybots → API Token → Revoke, then update the token wherever the bot is connected (scheduler settings). The old token dies instantly.',},
       {'q': 'What commands should a channel owner set for their own bot?',
        'a': 'Minimum: start, help, and whatever your publishing bot needs. /setcommands in BotFather defines the menu users see — five clear entries beat twenty cryptic ones.',},
   ])
