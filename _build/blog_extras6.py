# -*- coding: utf-8 -*-
"""Deep-dive sections for blog articles, part 6 — final batch.

Same editorial rules: real numbers, real mechanics, tools as plain text,
every section a continuation of the article (new material, not a summary).
"""

import blog_extras as _be

_sec = _be._sec

# ============================================================== TOOLS =======

_sec('telegram-bots-for-channel-owners', 'The stack by stage: 0, 1k, 10k subscribers',
     "<p>Bot stacks should match the channel's stage, not the wish list. <b>Launch "
     "(day zero):</b> BotFather (owns the plumbing), one scheduler, nothing else — "
     "every bot added before there's an audience is procrastination with settings. "
     "<b>~1,000 subscribers:</b> add the discussion group plus Combot for analytics "
     "and Rose or Shieldy for moderation, and TGStat's free tracking for your own "
     "channel's public record. <b>~10,000:</b> this is where the load-bearing bots "
     "earn their keep — analytics graduate to TGStat/Telemetr properly, an RSS bridge "
     "may enter the capture pipeline, payment bots (CryptoBot, Stars tooling) join if "
     "monetization started. The stage discipline matters because each bot is a "
     "recurring cost: rights to audit, pings to answer, a failure mode to babysit. "
     "The minimal stack that survives is the one where every bot's removal would "
     "hurt.</p>")

_sec('telegram-bots-for-channel-owners', 'When to stop adding bots',
     "<p>There's a failure pattern in channel admin circles worth naming early: bot "
     "accretion. One bot for polls, another for reactions, a third for cross-posts, "
     "a fourth that \"manages links\" — until the admin list is eight bots deep, "
     "nobody remembers which bot does what, and a post appears twice because two "
     "tools both \"helped\". The audit that stops it: for each bot, write one line — "
     "what it does, when it last did something useful. Anything you can't answer in "
     "ten seconds is a removal candidate: revoke its rights, keep the chat history "
     "(bots can be removed without deleting anything they wrote). The target state "
     "for most channels is five bots or fewer: scheduler, moderation, analytics, "
     "payments (if monetizing), and one utility you actually use weekly. Empty "
     "admin slots aren't a gap — they're headroom.</p>")

_sec('telegram-bot-commands-cheatsheet', 'Designing your own command set (for bots you build)',
     "<p>Once a channel runs a custom bot — a tip line, a member tracker, an internal "
     "tool — the command surface is worth designing like a product. Three rules from "
     "bots that aged well. <b>Group commands by verb, prefix by scope:</b> admin "
     "commands start with a distinctive prefix (/xstat, /xqueue) so they never "
     "collide with other bots in the same group. <b>Every command answers with "
     "usage on wrong input:</b> a bare error trains nobody; \"/xstat takes a "
     "channel username, e.g. /xstat @durov\" trains everyone. <b>One introspection "
     "command:</b> /help that lists what the bot can do — set via BotFather's "
     "<code>/setcommands</code> so it renders in the client's command menu, not just "
     "as a message. And register the set with <code>/setcommands</code> even for a "
     "two-command bot: the autocomplete menu is the difference between a tool the "
     "team uses and one they keep forgetting.</p>")

_sec('telegram-botfather-commands-full-list', 'The five BotFather commands that prevent tickets',
     "<p>Most \"the bot is broken\" messages from users trace to five unset BotFather "
     "settings. <code>/setdescription</code> — the what-is-this text shown before "
     "anyone presses Start; a bot with an empty description gets fewer presses. "
     "<code>/setabouttext</code> — the one-liner in the bot's profile. "
     "<code>/setuserpic</code> — an empty avatar reads as abandoned. "
     "<code>/setcommands</code> — the autocomplete menu; users can't use commands "
     "they can't discover. <code>/setjointogroups</code> and privacy settings — "
     "control whether the bot announces joins and what it reads. Twenty minutes on "
     "these five turns \"what does this bot do?\" DMs into self-serve starts, and "
     "the same five settings are exactly what a reviewer checks before allowing "
     "your bot into a large group.</p>")

_sec('telegram-auto-forward-and-crosspost', 'The single-writer rule',
     "<p>Cross-posting architectures fail in one classic way: two systems believe "
     "they own the same channel, and the audience gets every post twice. The "
     "prevention is a rule stated once and enforced forever: <b>every channel has "
     "exactly one writer</b> — either a human in the composer, or one bot, never "
     "both. Everything else is upstream: sources and drafts flow <i>into</i> the "
     "writer (RSS into the review chat, form submissions into drafts, the sister "
     "channel's posts into a review queue), and the writer is the only thing that "
     "touches <i>publish</i>. The audit is one question per channel: if this post "
     "appears twice next week, which two writers are involved? When the answer is "
     "\"a human and a bot\", pick one — usually the bot, with the human working in "
     "its draft queue instead of beside it.</p>")

# ============================================================= GROWTH =======

_sec('telegram-channel-stats-explained', 'Views decay: reading the curve, not the snapshot',
     "<p>A post's view count is a curve, and reading it at the wrong moment "
     "misleads. The typical shape: 60–75% of a post's first-week views arrive in "
     "the first 24 hours, a long tail follows for a fortnight, and a second bump "
     "appears whenever the post gets forwarded or re-promoted. Two practical "
     "consequences. <b>Don't judge a post at hour three:</b> the \"flop\" you "
     "deleted at noon often outsells the \"hit\" by Sunday — compare posts at a "
     "fixed horizon (48 hours or 7 days) or not at all. <b>Re-promotion is a "
     "views lever:</b> forwarding your own best old post to the channel with a "
     "one-line \"still the best explainer we've made\" reliably adds a bump, "
     "because half your current subscribers weren't subscribed when it first "
     "ran. Channels that never re-promote leave their best work buried by the "
     "feed's own mechanics.</p>")

_sec('telegram-channel-stats-explained', 'Notifications-off readers and the muted majority',
     "<p>Notification mode — the bell each subscriber sets per channel — is the "
     "invisible variable behind every odd view pattern. A subscriber who muted "
     "you still sees posts when they open Telegram; they just never get pulled "
     "in. The tell in your numbers: a channel with strong ERR but flat "
     "hour-one views has a large muted majority (they arrive on their own "
     "schedule, so the first-hour spike softens). The playbook follows: for the "
     "muted, the <b>first line</b> is your notification — it renders as preview "
     "text in the chat list — and the <b>pinned post</b> is your landing page. "
     "For the un-muted, timing matters: send the notification-worthy post when "
     "they're actually free. And never spam the bell: muted readers stay "
     "subscribers precisely because muting works — give them no reason to take "
     "the next step.</p>")

_sec('telegram-privacy-for-channel-owners', 'What subscribers can\u2019t ever see (and where the anxiety is misplaced)',
     "<p>Owner-side privacy anxiety usually targets the wrong list, so here's the "
     "hard boundary: <b>Telegram never exposes</b> your subscriber list (you see "
     "count and recent joiners' public profiles, not a directory), the identity "
     "of who viewed or reacted to a specific post (only aggregate counts), who "
     "muted you, who blocked the channel, or subscriber phone numbers — ever. "
     "The things people fear most — being watched back — don't exist for "
     "channels. What <i>is</i> visible is deliberately narrow: your public "
     "profile as configured, the channel's admin list (unless admins are "
     "anonymous), join/leave events in the discussion group, and anything you "
     "type as yourself in comments. The audit that matters, therefore, isn't "
     "\"what do subscribers know about me\" — it's \"what does my public profile "
     "plus my comment behavior reveal\". Get those two consistent with the "
     "persona you intend, and the rest is already private by design.</p>")

_sec('telegram-seo-and-discovery', 'The findability audit, field by field',
     "<p>One pass, fifteen minutes, in the order search engines read you. "
     "<b>Name:</b> does it contain the words a stranger would type? (Not the "
     "brand — the words.) <b>Username:</b> does it match or contain the same "
     "stem? <b>Description:</b> the first 120 characters carry the promise and "
     "the keywords — written for the snippet, not the slogan. <b>Pinned post:</b> "
     "the web preview shows it first; make it a real introduction with your "
     "best links. <b>First lines of recent posts:</b> they become the indexed "
     "snippets on <code>t.me/s/</code>. <b>Web check:</b> Google "
     "<code>site:t.me/s/yourchannel</code> and see what actually surfaces. "
     "<b>In-app check:</b> search your main term and your sub-term; note the "
     "rank, recheck after any rename. Every field above is editable in two "
     "minutes; the compound effect is the only \"Telegram SEO hack\" that has "
     "ever survived contact with reality.</p>")

_sec('telegram-channel-migration', 'Content-pipeline migration: the checklist owners forget',
     "<p>When a channel changes hands or identity, the audience is half the move "
     "— the pipeline is the other half, and it's the half that fails quietly "
     "in week two. The full checklist: <b>bot rights</b> — the new owner adds "
     "their own scheduler/moderation bots; the old ones get revoked, not just "
     "forgotten; <b>scheduled queues</b> — export or screenshot pending posts "
     "before rights change, because queues live in the old owner's tool; "
     "<b>pinned messages</b> — re-pin under the new administration (pins "
     "survive, but their context may not); <b>linked discussion group</b> — "
     "the link survives, but the group's admin list needs the same cleanup as "
     "the channel's; <b>invite links</b> — old invite links keep working; "
     "expire the ones that are printed anywhere you no longer control; "
     "<b>monetization rails</b> — Stars withdrawals, CryptoBot merchant "
     "settings and ad-network profiles all live outside the channel and must "
     "be re-pointed by hand. A migration that does the audience but not the "
     "pipeline produces a healthy channel that stops publishing eleven days "
     "later — the deadline that slips is always this one.</p>")

_sec('telegram-channel-mistakes', 'The five-minute quarterly audit that catches them all',
     "<p>Every mistake on this list is detectable early by the same ritual. "
     "Quarterly, sit with the channel for five minutes and answer five "
     "questions. <b>1) Ratio:</b> count the last 20 posts — value vs self-"
     "serving — is it past 70/30? <b>2) Rhythm:</b> look at the timestamps — "
     "are there dead hours, multi-post bursts, weeks the channel went dark? "
     "<b>3) ERR trend:</b> views ÷ subscribers on the last ten posts — up, "
     "flat, or sliding? <b>4) The pinned post:</b> open the channel as a "
     "stranger would — does the pin still tell a newcomer what this is and "
     "why to stay? <b>5) The admin list:</b> any bot or human with rights "
     "nobody remembers granting? Five answers, five lines in a note, and the "
     "two or three fixes that fall out go into next month's calendar. "
     "Channels don't die from the mistake nobody warned them about — they "
     "die from the six they noticed and postponed.</p>")

_sec('telegram-channel-mistakes', 'Bought subscribers: the mistake that keeps costing',
     "<p>It deserves its own section because it's the only mistake that "
     "compounds. Purchased subscribers — the thousand-for-$10 accounts — do "
     "four things at once: they crater your ERR (every future ERR-based "
     "decision — ad pricing, swap attractiveness, directory ranking — now "
     "reads worse than reality), they poison Similar Channels (the graph "
     "links you to the other channels those bots pollute), they make every "
     "future analytics decision wrong (you're optimizing for an audience "
     "that doesn't exist), and they're nearly irreversible — Telegram "
     "doesn't offer bulk removal of bots and fakes, so a polluted channel "
     "either culls by hand or lives with the number. The honest growth "
     "arithmetic: 500 real subscribers with a 45% ERR out-earn 5,000 "
     "purchased ones with a 4% ERR in every commercial conversation, every "
     "swap, every month. There is no version of this purchase that pays "
     "for itself.</p>")

_sec('best-time-to-post-telegram', 'The one-week A/B test, concretely',
     "<p>The honest way to find your channel's windows takes seven days and "
     "one spreadsheet. Setup: pick two candidate slots per day-part you "
     "doubt about — say 8:00 vs 11:00 for the morning slot. For the next "
     "five weekdays, alternate posts between the two slots (A, B, A, B, A) "
     "with <i>comparable content</i> — same format class, similar topic "
     "weight; a comparison of a meme vs a 900-word essay measures nothing. "
     "Record 24-hour views ÷ subscribers for each. The winner is whichever "
     "slot wins the majority of pairs by more than ~5% — anything closer is "
     "noise, and noise means the slots don't matter for your audience. "
     "Repeat the exercise once per quarter, because audiences drift: the "
     "8:00 crowd that won in March may be a 9:30 crowd by October as "
     "routines change. One week of discipline replaces years of folklore — "
     "and the spreadsheet it leaves behind becomes the channel's actual "
     "publishing manual.</p>")

# ============================================================= PLATFORM =====

_sec('telegram-groups-vs-whatsapp-vs-discord', 'The migration question (and why nobody finishes it)',
     "<p>Every community eventually asks whether to move platforms, and the "
     "honest answer is that migrations are less common than frustrations — "
     "because the network effect punishes even correct moves. What actually "
     "works when a move is right: <b>run both for a quarter</b> with the new "
     "home explicitly better (a channel structure Discord can't offer, or "
     "bots WhatsApp can't run), never just \"the same thing elsewhere\"; "
     "<b>move the artifacts, not just the chat</b> — the archives, rules, "
     "roles and recurring events recreated before the announcement; "
     "<b>announce the why, not the where</b> — \"we're moving for X\" "
     "converts the invested minority who cause the rest to follow; and "
     "<b>expect 30–50%</b> of active members to make the jump and keep the "
     "old room as a read-only bridge. Communities that announce on Friday "
     "and delete the old server Sunday lose the long tail that never saw "
     "the announcement — and the long tail is most of the community.</p>")

_sec('telegram-comments-and-discussion-groups', 'The first-week protocol that sets the culture',
     "<p>A discussion group's culture is set in its first hundred comments, "
     "and it can be engineered. The protocol: <b>seed before opening</b> — "
     "have two or three friendly accounts (your own team) ready to answer "
     "the first real questions fast, because speed of first reply predicts "
     "whether a second question ever comes; <b>ask answerable questions</b> "
     "— early channel posts end with a specific, low-effort prompt (\"which "
     "of these two — A or B?\"), not \"what do you think?\"; <b>reply as "
     "the channel</b> with the human voice visible — first-person answers "
     "as the brand avatar model the tone; <b>thank the first commenters "
     "explicitly</b> — the first ten people who talk are the core of the "
     "community for a year; and <b>set slow mode early</b> if a post "
     "explodes — a readable thread keeps newcomers from noping out. "
     "Groups that survive their first spam wave and their first flame war "
     "inherit a self-moderating culture; the protocol above is what buys "
     "them that long.</p>")

# ============================================================= CONTENT ======

_sec('telegram-emoji-reactions-guide', 'Custom reactions as a niche in-joke engine',
     "<p>Boosted channels can upload their own reaction packs — and this is "
     "where reactions stop being engagement plumbing and start being brand. "
     "A coding channel with a :ship-it: reaction, a cooking channel with a "
     ":burnt: reaction, a local news channel with a :exactly: — the pack "
     "becomes the community's dialect, and outsiders who forward your posts "
     "carry your in-jokes into their own chats, which is brand distribution "
     "you can't buy. The mechanics: packs are created through a bot "
     "@stickers, uploaded as webm or PNG with transparent edges, and "
     "enabled for the channel once the boost level allows custom sets. "
     "Design rules that matter at 24px: bold silhouettes, one idea per "
     "icon, no text smaller than three characters. Start with five — a "
     "usable set, not a museum — and let usage, not taste, decide which "
     "stickers earn the next batch.</p>")

_sec('telegram-emoji-reactions-guide', 'The weekly reaction review',
     "<p>Reaction counts are free market research if you look at them once a "
     "week. The review, five minutes: list the week's posts with their "
     "reaction mix. <b>Posts where one reaction dominates</b> (>60% of the "
     "total) tell you the audience's verdict is unambiguous — note what "
     "that reaction was: the fire on a tutorial, the thinking-face on a "
     "controversial take. <b>Posts with split reactions</b> are your "
     "discussion fuel — they deserve a follow-up post or a poll, because "
     "the audience literally voted twice. <b>Posts with near-zero "
     "reactions</b> despite normal views are your weakest format — one "
     "more run to confirm, then retire it. Over months this builds "
     "something no analytics tool sells: a per-format map of what your "
     "specific audience feels strongly about, in their own words. "
     "Reactions are the only feedback channel where the cost of feedback "
     "is one tap — treat the data accordingly.</p>")

_sec('telegram-emoji-reactions-guide', 'Reactions and the wider stack',
     "<p>Reactions compose with the other engagement surfaces, and the "
     "composition is where channels get clever. <b>Reactions as a poll "
     "priming layer:</b> post the item, let reactions run for an hour, "
     "then publish the formal poll — voters arrive pre-warmed and turnout "
     "rises. <b>Reactions as a content router:</b> \"react 🔥 if you want "
     "the deep-dive on this, 🤔 if you want the counter-argument\" — the "
     "channel reads its own audience's demand and schedules accordingly; "
     "it's a poll with better UX and zero setup. <b>Reactions as a "
     "moderation signal:</b> in the discussion group, a comment getting "
     "pile-on reactions is visible before any report — a lightweight "
     "early-warning system that costs nothing. The pattern underneath "
     "all three: reactions are the lowest-friction signal your audience "
     "can send; building formats that deliberately harvest them costs "
     "nothing and compounds.</p>")

_sec('telegram-post-formatting-guide', 'The post skeleton, line by line',
     "<p>The anatomy of a post that gets read to the end is stable enough "
     "to template. <b>Line one — the promise:</b> what the reader gets, "
     "concretely, in under 70 characters — this is also the preview text, "
     "so it must work alone. <b>Line two — the turn:</b> why now, or why "
     "you — one sentence of context that earns the read (\"after three "
     "channels asked us the same question...\"). <b>The body — one idea "
     "per paragraph, bolded anchors:</b> bold is the skimmer's map; "
     "three to five anchors per screen, each readable as a summary on "
     "its own. <b>The artifact:</b> screenshot, list or code block — "
     "the thing that survives being screenshotted out of context. "
     "<b>The close:</b> one call to action, never two (a post asking "
     "for a reaction, a comment and a click gets none). Save this as "
     "a draft template in your scheduler once, and every future post "
     "starts at 70% done — formatting discipline you don't have to "
     "re-decide daily.</p>")

_sec('telegram-post-formatting-guide', 'The A/B habit: formatting as a testable variable',
     "<p>Formatting claims deserve the same skepticism as timing claims, "
     "and the test is cheap. Pick one variable per week — emoji section "
     "markers on/off, bold density high/low, quote blocks vs dashes, "
     "caption above vs below media — and alternate across comparable "
     "posts for two weeks. Compare 48-hour views and forwards per "
     "format pair; keep the winner, log it, and move to the next "
     "variable. Three disciplines make the results real: comparable "
     "content (a test between a giveaway post and an essay measures "
     "nothing), one variable at a time, and a fixed judgment horizon. "
     "Ten weeks of this produces something better than any style "
     "guide: a formatting manual derived from your audience's actual "
     "behavior — and the habit of testing, which outlives every "
     "specific finding.</p>")

# ============================================================= PREMIUM ======

_sec('telegram-mini-apps', 'Promoting the Mini App inside the channel',
     "<p>A Mini App nobody opens is a hobby. The promotion patterns that "
     "move the open rate: <b>the concrete hook</b> — every mention names "
     "the outcome (\"check what your delivery window is\"), never the "
     "artifact (\"try our app\"); <b>the recurring slot</b> — a weekly "
     "post that uses the app's output (\"calculator says the cheapest "
     "fill-up day this week is...\") trains opens into a habit; "
     "<b>the button, not the link</b> — attach the app as an inline "
     "button on related posts rather than a bare t.me URL, because the "
     "button opens in-app in one tap; <b>the result share</b> — if the "
     "app produces an outcome (a score, a price, a plan), make sharing "
     "it back into the chat one tap, since shared results are the app's "
     "referral engine. And measure from day one (open rate, completion, "
     "output events — the funnel from the section above), because the "
     "most common Mini App failure isn't technical: it's a genuinely "
     "useful tool that the channel mentioned exactly once.</p>")

# =============================================================== TOOLS ======

_sec('telegram-scheduler-comparison', 'What to automate first: a 30-day graduation path',
     "<p>For owners drowning in manual publishing, the order of adoption "
     "matters more than the tool choice. <b>Week one:</b> move scheduled "
     "publishing itself — all posts enter a queue, nothing is posted "
     "live by hand except true announcements. This single change "
     "captures most of the stress reduction, because the failure mode "
     "it removes (\"I forgot to post today\") is the one that damages "
     "rhythm most. <b>Week two:</b> build the drafts library — pillar "
     "templates and three evergreen posts stored in the tool, so empty "
     "slots have a fallback. <b>Week three:</b> add the media checks — "
     "albums prebuilt and previewed in the queue, not assembled at "
     "publish time. <b>Week four:</b> add the review loop — a weekly "
     "look at what published, what flopped, what's queued. A month in, "
     "the channel runs on rails with the human doing only two things: "
     "writing and deciding. Tools that promise to remove those two are "
     "removing the channel.</p>")

# ============================================================== MONEY =======

_sec('telegram-stars-for-channel-owners', 'Paid content formats that actually sell',
     "<p>Stars' paid-content gate works best on formats with built-in "
     "curiosity, because the reader decides at the preview line. What "
     "converts, observed across channels: <b>the payoff post</b> — the "
     "conclusion of a series the free feed built up (part 4 free, the "
     "final framework paid); <b>the artifact</b> — a template, "
     "database, checklist, preset — where the buyer knows exactly what "
     "they're getting; <b>the deep teardown</b> — \"we audited [well-"
     "known thing], full numbers inside\"; <b>the archive</b> — a "
     "year's best posts curated into one paid message. What reliably "
     "flops: gating opinions (available free everywhere), gating news "
     "(old in an hour), and gating anything the free channel just "
     "covered thoroughly. The pattern: sell <b>artifacts and "
     "payoffs</b>, never <b>coverage</b>. And keep the ratio: one paid "
     "post per five-to-ten free ones — paid content that outnumbers "
     "free content converts nobody and unmutes everyone.</p>")

_sec('telegram-stars-for-channel-owners', 'The withdrawal math, end to end',
     "<p>The Stars ledger has more steps than the price suggests, so "
     "model it before pricing. The chain: a reader buys Stars from "
     "Telegram (Telegram's price, not yours); pays your post's price "
     "in Stars; your balance shows the gross; Telegram's platform "
     "conversion applies when you convert to withdrawals via Fragment "
     "in TON; then exchange and network fees apply on the way to fiat. "
     "The practical consequence: price the paid post at the Stars "
     "figure that nets what you'd actually accept — work backwards "
     "from the take-home, not forwards from a fiat price. Two "
     "operational notes: withdrawal thresholds and regional payment "
     "options change, so check Fragment's current terms before "
     "launching a Stars-heavy product; and keep an ledger sheet from "
     "day one — date, post, Stars gross, converted, net — because "
     "tax authorities in most countries treat this as ordinary "
     "income, and the conversion trail is much easier to reconstruct "
     "monthly than annually.</p>")

_sec('monetize-telegram-channel', "The advertiser's diligence checklist (become the channel that passes it)",
     "<p>Understanding how advertisers screen channels is free leverage: "
     "every item on their list is something you can make true before "
     "the first inquiry. The standard checklist: <b>public stats</b> — "
     "a TGStat page showing stable six-month views and subscriber "
     "growth (spikes are read as purchases); <b>ERR band</b> — "
     "consistent with the channel's size tier; <b>geo match</b> — "
     "audience geography matching the buyer's market; <b>content "
     "adjacency</b> — recent posts topically compatible with the "
     "buyer's product; <b>comment life</b> — real discussion under "
     "posts, which no bot farm fakes convincingly; <b>previous "
     "sponsors</b> — names or a case study; <b>clean price "
     "history</b> — a channel that publicly churns cheap ads trains "
     "buyers to expect cheap ads forever. A channel that arranges "
     "these six before outreach negotiates from evidence instead of "
     "hope — and the difference in closing rate and price is the "
     "largest unpaid dividend in channel monetization.</p>")

_sec('telegram-for-newsletters', 'The email capture that survives the channel',
     "<p>Hybrid channels still need the email list — but the capture "
     "mechanics change on Telegram, and the naive \"link in bio\" "
     "underperforms. What works: <b>the artifact-gated signup</b> — "
     "the checklist or database lives behind an email form, and the "
     "Telegram post hands over the form link; conversion runs "
     "several times higher than \"subscribe to the newsletter\" "
     "because the reader is trading an email for a thing, not for "
     "a promise; <b>the periodic digest anchor</b> — once a week, "
     "the channel post says \"the full version with the links went "
     "out by email — here's the archive link\", which catches "
     "readers who want depth without framing email as the better "
     "channel; <b>the platform-risk post</b> — annually, one "
     "straight post: why the email backup exists, what it contains. "
     "Telegram converts this better than any social platform "
     "because the audience already treats the channel as a "
     "subscription — the email list is simply the same "
     "subscription with a different delivery rail, and saying so "
     "plainly is what makes the dual-subscription frame land.</p>")

try:
    import blog_extras7  # noqa: F401,E402
except ImportError:
    pass
