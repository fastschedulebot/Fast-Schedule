# -*- coding: utf-8 -*-
"""Deep-dive sections for blog articles, part 3 — the ten shortest articles.

Same editorial rules as blog_extras.py: real numbers, real mechanics, real
tools named as plain text. Every section is a continuation — new material,
not a summary — appended to the article body at build time.
"""

import blog_extras as _be

_sec = _be._sec

# ============================================================== MONEY ========

_sec('telegram-affiliate-marketing', 'The unit economics of one affiliate post',
     "<p>Run the numbers before writing a single link. A 3,000-subscriber channel with a "
     "healthy 24% view rate puts a post in front of ~720 people. A well-placed single link "
     "in an artifact-style post gets clicked by 6–10% of viewers — call it 55 clicks. "
     "Software and hosting offers convert 1.5–3% of clicks, so one post produces one or "
     "two conversions: $30–60 at typical $30 recurring commissions. The point is not that "
     "one post is rich — it's that affiliate income on Telegram is a <b>portfolio</b>: ten "
     "evergreen affiliate posts written over a quarter, re-promoted on rotation, stack into "
     "$300–600/month that keeps paying while you sleep. A $50 ad post, by contrast, is "
     "spent once. Judge every affiliate post by its 90-day cumulative revenue, not its "
     "first-day clicks.</p>")

_sec('telegram-affiliate-marketing', 'Recurring vs one-time payouts (and why recurring wins here)',
     "<p>One-time payouts — 30–50% of a course or a hosting signup — pay this month and "
     "never again. Recurring programs — typically 20–30% of a SaaS subscription, monthly, "
     "for the life of the account — compound. Telegram tilts the comparison toward "
     "recurring because posts don't disappear: subscribers re-find old posts through "
     "search-in-chat, pinned index messages and hashtag shelves. Build the shelf "
     "deliberately: tag every affiliate post <code>#deals</code> or <code>#tools</code>, "
     "pin a one-line index post pointing at the tag, and re-promote each affiliate post "
     "once a quarter — roughly 70% of your current subscribers weren't subscribed when it "
     "first ran. Where the program offers promo codes, use them: codes survive screenshots "
     "and word-of-mouth, and they let you attribute sales Telegram's click data can't.</p>")

_sec('telegram-affiliate-marketing', 'The placement hierarchy',
     "<p>Where and how a link appears decides its click rate more than the offer does. The "
     "hierarchy, from strongest to weakest: <b>1)</b> a dedicated problem-post that ends "
     "with the tool you personally use — problem, story, screenshot of your own setup, one "
     "link; <b>2)</b> the quarterly re-promo of that same post; <b>3)</b> a link inside a "
     "digest, on the line where the tool solved a problem you're describing; <b>4)</b> a "
     "link in the comments of your discussion group answering a real question. The "
     "conversion killers: link lists of five alternatives (choice kills conversion — one "
     "tool per post), links in the first line (reads as an ad, gets skimmed), and "
     "undisclosed links (see the ratio rule above). If you can't write the post as advice "
     "you'd give for free, the placement is an ad and it will perform like one.</p>")

_sec('telegram-sponsorships', 'The media kit that answers before it is asked',
     "<p>Sponsors ask the same five questions in every first message. Pre-answer them on "
     "one page: what the channel is and who it's for (one sentence); subscriber count and "
     "30-day ERR; audience geography split; the last five posts' view counts; formats and "
     "rates. The credibility trick: screenshot TGStat's public channel page instead of "
     "self-reporting numbers — advertisers verify anyway, and self-reported stats without "
     "a public source get silently discounted. Add one case-study line as soon as you have "
     "it: <i>\"Previous sponsor: 1,900 clicks from one placement\"</i> is worth more than "
     "any adjective in the kit. Keep the file as a PDF and update the numbers monthly — a "
     "kit with two-month-old ERR reads as a kit you don't check.</p>")

_sec('telegram-sponsorships', 'How to price without guessing',
     "<p>The market prices placements per expected view. Expected views = ERR x subscribers. "
     "A 5,000-subscriber channel with a 30% ERR expects ~1,500 views per post. Niche "
     "buying power sets the per-view rate: crypto, finance and B2B tools pay at the top of "
     "the range, entertainment at the bottom. From that: a realistic first rate card for "
     "the 5,000-sub example is $30–120 per dedicated post depending on niche, with a "
     "30–50% premium for exclusive, deep-fit sponsors. Two rules protect you: never go "
     "below the floor that makes the work feel worth it — desperation pricing resets "
     "expectations and spreads between admins — and raise rates in steps of 20–30% when "
     "your last three placements all sold, not because a calendar month passed.</p>")

_sec('telegram-sponsorships', 'Renewal is the whole business',
     "<p>The money in sponsorships is in the second placement, not the first. Within 24 "
     "hours of a sponsored post going out, send the sponsor a short delivery report: views "
     "at 24 hours, link clicks (use a shortlink or UTM parameters you control), subscriber "
     "movement during the promo window, and one honest sentence on audience fit. Then "
     "schedule a follow-up three weeks out. Sponsors renew on certainty, not reach — a "
     "$50 sponsor who renews four times is worth more than four new $100 sponsors you "
     "hunted down. And sell the calendar, not just the post: when a slot is taken, offer "
     "the next one by date. Scarcity stated honestly — <i>\"this slot opens again on the "
     "15th\"</i> — closes deals that a generic \"rates are negotiable\" never will.</p>")

_sec('telegram-paid-subscriptions', 'What members actually pay for',
     "<p>Before launching, audit your free channel and answer honestly: what does a member "
     "get that a free reader doesn't? It must be one of four things. <b>Signal density</b> "
     "— fewer, deeper posts with the noise stripped. <b>Access</b> — your actual answers, "
     "a members' group, direct questions. <b>Speed</b> — deals, signals or news minutes "
     "before the free feed. <b>Artifacts</b> — templates, databases, recordings, "
     "checklists. If you can't name the artifact, don't launch yet: churn will eat the "
     "channel in month two. The mix that retains: roughly 60% of paid posts are a deeper "
     "version of what performs well free, 30% is access (answers, member threads), 10% "
     "pure extras. Paid channels that are just \"the free channel minus ads\" are the ones "
     "that empty out.</p>")

_sec('telegram-paid-subscriptions', 'The churn math that decides your price',
     "<p>Paid subscription channels typically lose 8–15% of paying members per month in "
     "year one — payment lapses, silent cancels, one-month tourists. At $5/month and 10% "
     "monthly churn you must replace a tenth of your member base just to stand still, "
     "which is why annual pricing at roughly 10x the monthly rate (two months free) is "
     "standard on successful channels: it converts twelve churn decisions a year into "
     "one, and the discount pays for itself. Beware the free-trial trap too: 7-day free "
     "trials attract trial collectors, not members. A cheap paid trial — or Stars' built-in "
     "refund window — filters better, because paying something is the qualification "
     "itself.</p>")

_sec('telegram-paid-subscriptions', 'Launch mechanics that fill the first 50 seats',
     "<p>Founding-member pricing works on Telegram because the channel's early readers are "
     "its most loyal: the first 50 members lock a lower rate forever, which creates real "
     "urgency without countdown timers. Pin a \"what's inside\" post with screenshots of "
     "genuine member content (names redacted) — the single strongest conversion asset is "
     "one free taste: publish a full paid-grade post on the free channel, marked "
     "<i>\"this is what members got today.\"</i> On the mechanics: Telegram Stars "
     "subscriptions renew automatically inside the app — no external card form, which "
     "removes the biggest friction and the biggest drop-off step. If you bill in outside "
     "currency, invite-link bots in the InviteMember style handle the whole loop: pay "
     "wall, auto-invite, expiry reminders, and automatic kick on lapse. Whichever rail "
     "you pick, write the lapse-grace policy down before the first renewal date — the "
     "\"card declined on day 31\" conversation is much easier with a rule than a debate.</p>")

_sec('telegram-referral-programs', 'The three mechanics, costed',
     "<p>Referral growth comes in three shapes with very different economics. "
     "<b>Leaderboards</b> — invite-link counters, Combot-style refs — reward only the top "
     "N participants, so cost is capped and competition does the work. <b>Unlock "
     "ladders</b> — refer three friends, unlock a locked post or report — cost nothing "
     "but content you already made; the reward is status plus an artifact, which is why "
     "ladders consistently outperform their cost. <b>Paid bounties</b> — cash per verified "
     "join — scale linearly and attract the worst traffic. Realistic numbers: a well-run "
     "ladder brings in 2–8% of the participant base as new subscribers per week; cash "
     "bounties bring more raw volume but 30–60% of it ghosts or unmutes within a month. "
     "Start with a ladder. Only pay per join when you can verify quality.</p>")

_sec('telegram-referral-programs', 'Anti-fraud without paranoia',
     "<p>Telegram's multi-account reality is the fraud vector: referral rings of five to "
     "twenty accounts are routine wherever cash is involved. The defenses are boring and "
     "effective. Reward only when the invitee <i>does something</i>: stays a week, reacts "
     "once, comments once. Flag clusters — your bot sees user IDs, and accounts created "
     "the same week that only ever appear through referral links are a ring, not an "
     "audience. Cap rewards per day. And prefer paying in artifacts — locked posts, "
     "reports, a role — over withdrawable cash: a ring that farms a locked PDF costs you "
     "nothing; a ring that farms a $1-per-join bounty costs exactly what it farms. If a "
     "campaign's join quality looks too good, check the week-2 view rate of the "
     "referred cohort before paying the next round.</p>")

_sec('telegram-referral-programs', 'The shareability shortcut most channels skip',
     "<p>The real referral unit on Telegram isn't the invite link — it's the forward. "
     "Posts designed to travel on their own: self-contained value (a checklist, a "
     "mini-report, a single sharp chart) with one soft closing line, \"this came from "
     "[channel]\". A forward arrives carrying social proof from the sender — that's why "
     "forwards convert strangers at a multiple of what cold invite links manage. The "
     "practice: watch the forward count on every post (it's public on any channel post), "
     "identify which format earns the most, and re-run that format monthly with fresh "
     "material. Your most-forwarded post of each month is your best-performing "
     "advertisement — repin it, reference it, and make its sequel.</p>")

# ============================================================= CONTENT ======

_sec('telegram-content-pillars', 'Pillar slots for six common niches',
     "<p>Don't invent a slot table from zero — steal one. <b>Jobs channel:</b> Mon, five "
     "fresh roles; Wed, one salary breakdown; Fri, a hiring tip plus the weekly "
     "sponsored slot. <b>Dev channel:</b> Mon, tool teardown; Wed, one code snippet worth "
     "saving; Fri, the week's digest. <b>Local business:</b> Mon, offer; Wed, "
     "behind-the-scenes; Fri, customer story. <b>Analytics/signals:</b> daily, the one "
     "chart; weekly, a methodology post. <b>News digest:</b> daily, five links; weekly, "
     "the \"what mattered\" essay. <b>Deal channel:</b> as-they-come alerts, plus a "
     "weekly \"best of\" roundup. Every table above survives contact with real life "
     "because each slot has a fixed shape — the filling varies, the mold doesn't.</p>")

_sec('telegram-content-pillars', 'The 70/20/10 mix',
     "<p>Within each week, aim for roughly 70% evergreen value (posts that still make "
     "sense in six months), 20% timely material (news, reactions — expires, but builds "
     "the daily-open habit), 10% offers and calls to action. Channels that invert this "
     "show the classic decay curve: ERR slides a point or two over a quarter as readers "
     "learn the feed is mostly selling. Audit it monthly in ten minutes: export or scroll "
     "your last 30 posts, tag each one with its pillar, and count. If any pillar produced "
     "fewer than one post a week, it isn't a pillar — it's a mood. Fix the calendar, not "
     "the intentions.</p>")

_sec('telegram-content-pillars', 'Pillars as a delegation document',
     "<p>The quiet payoff of the pillar system is that it makes the channel delegable. "
     "A one-page pillar sheet — slot, format, source to mine, one example link, tone "
     "notes — lets a co-admin or ghostwriter produce posts that are 80% right without "
     "ever messaging you. Store the templates where the work happens: keep pillar drafts "
     "saved in your scheduler (Fast Scheduler keeps reusable drafts; ControllerBot-style "
     "bots pin templates in a service chat) so the person filling Tuesday's slot starts "
     "from the mold, not from a blank composer. Consistency on Telegram isn't a "
     "personality trait — it's a stored asset. The channels that survive a vacation are "
     "the ones that wrote down their own shape.</p>")

_sec('telegram-source-curation', 'The intake stack, concretely',
     "<p>A working curator's intake has four parts. <b>1)</b> An RSS reader (Feedly, "
     "Inoreader) holding 60–120 feeds — including your competitor digests, because you "
     "want to read what they read plus what they miss. <b>2)</b> A dedicated Telegram "
     "folder with 30–50 source channels you never forward from without checking the "
     "original. <b>3)</b> A capture chat: forward anything promising to a private "
     "\"inbox\" chat in one tap. <b>4)</b> A weekly sweep of Hacker News and the relevant "
     "subreddits for the long tail. The inbox chat is your product backlog. If capture "
     "takes more than one tap, you'll stop by week three — curation dies of friction, "
     "not of laziness.</p>")

_sec('telegram-source-curation', 'The 5-3-1 daily cut',
     "<p>From a full day of intake, publish the cut: <b>5</b> links that survive the "
     "question \"would my reader act on this today?\", <b>3</b> one-line takes on things "
     "you're not linking formally, <b>1</b> deep item — a teardown, a comparison, a "
     "larger curation. The volume discipline is the product: digests that fire off "
     "fifteen links a day train readers to skim; five links with context train readers "
     "to open. Readers feel the filter before they can articulate it, and your "
     "unsubscribe rate tracks every time you break the cut. When a slow news day "
     "tempts you to pad — don't. A digest that sometimes publishes less is trusted; a "
     "digest that always publishes something is ignored.</p>")

_sec('telegram-source-curation', 'Speed vs correctness — pick a lane, label it',
     "<p>Every curator faces the dilemma: be twenty minutes early with a rumor or three "
     "hours late with a verified story. The solution is formats, not agonizing. Run a "
     "\"fast lane\" post type explicitly labeled <i>unconfirmed</i>, and a \"verified\" "
     "format that only carries checked material — readers forgive labeled speed, never "
     "unlabeled wrongness. And make corrections a feature, not an embarrassment: when "
     "you get something wrong, post the correction in a fixed format the same day. "
     "Curators who visibly correct are trusted; curators who never correct are assumed "
     "to never check. That assumption is the only thing in curation you can't rebuild "
     "after losing it.</p>")

# =============================================================== TOOLS ======

_sec('telegram-moderation-bots', 'Rose: the 20-minute configuration that matters',
     "<p>The practical Rose setup for a discussion group: <code>/settings</code> → "
     "<b>captcha</b> on (button, 120-second timeout) to catch the join-and-spam wave; "
     "<b>locks</b> set to links=admins-only and forwards=off during spam waves; "
     "<b>warns</b> at three, with the action set to a 24-hour mute; media restrictions "
     "on voice notes and video notes if the group is a discussion annex and not a "
     "hangout. The rule of thumb for every lock: you're trading false positives for "
     "spam friction. Start permissive, tighten after incidents, never pre-tighten "
     "\"to be safe\" — over-locked groups moderate ghosts while the real spam adapts "
     "faster than your lock list.</p>")

_sec('telegram-moderation-bots', "Shieldy's philosophy — and when it backfires",
     "<p>Shieldy is aggressive by design: it deletes messages from brand-new members "
     "that contain links or forwards, throws a CAPTCHA at joins, and it does this with "
     "almost no configuration. That default profile is perfect for public channels with "
     "linked groups that catch spam waves right after every promo post. It's wrong for "
     "communities whose members legitimately share links — a dev group posting repos or "
     "a deals group posting shops will get eaten alive by Shieldy's freshness rules. "
     "The honest test: if more than one real member per week loses a message to the bot, "
     "the group has outgrown Shieldy's defaults — move to Rose warns with a human-"
     "reviewable ladder, and keep Shieldy in reserve for the next attack wave.</p>")

_sec('telegram-moderation-bots', 'Combot: moderation as data',
     "<p>Combot's real value isn't its captcha — it's the per-user history. Three uses "
     "that change decisions: spot <b>sleepers</b> (accounts that joined weeks ago, said "
     "nothing, and activate the day your promo goes out); check a loud critic's history "
     "before banning — a two-year member with three thousand messages is not a wave "
     "account; and lean on the global spam database, which flags known scammer accounts "
     "at join time. Pair it with the weekly top-members digest: your most active "
     "participants are your future moderators, and promoting from the data instead of "
     "from who shouts loudest is how groups stay healthy as they grow.</p>")

_sec('telegram-moderation-bots', 'The escalation ladder every group needs',
     "<p>Write the ladder down before you need it: <b>1)</b> automatic — captcha and "
     "obvious spam deleted by the bots; <b>2)</b> <code>/warn</code> — three warnings "
     "trigger an automatic 24-hour mute; <b>3)</b> <code>/mute 1h</code> for heated "
     "violations that shouldn't count as formal warnings; <b>4)</b> <code>/ban</code> "
     "reserved for scams, rings and doxxing; <b>5)</b> always state the reason, "
     "publicly, in one line. Pin the ladder as a single message. Groups die from "
     "moderator mood swings more often than from spam — a published, predictable ladder "
     "makes enforcement boring, and boring enforcement is what members read as "
     "fairness. When someone complains about a mute, you answer with the pinned message, "
     "not with your mood.</p>")

# ============================================================== GROWTH ======

_sec('telegram-advertising-guide', 'The promo post, structurally',
     "<p>Promo posts that convert share a skeleton. <b>Line one</b> is the audience "
     "filter — \"For channel owners who post daily...\" — not the brand name; the reader "
     "decides relevance before they decide interest. <b>Line two</b> is the offer as a "
     "concrete artifact: a free checklist, a trial, a discount code. \"Check out X\" "
     "converts a fraction of what \"grab the free checklist from X\" does. <b>One "
     "screenshot</b> of the product in real use beats any stock image. <b>The link</b> "
     "appears once, at the end. And the whole thing is rewritten in the host channel's "
     "voice — sponsor copy pasted from a press kit underperforms rewritten copy every "
     "time, so ask the channel admin to rewrite it and expect to pay for the edit in "
     "results, not apologies.</p>")

_sec('telegram-advertising-guide', 'The pre-buy checklist, item by item',
     "<p>Before paying anyone: pull their TGStat page — ERR stable over six months (a "
     "three-month spike means bought traffic), subscriber growth smooth (steps mean "
     "purchases), views-to-subscribers above 20% for a healthy channel, and a citation "
     "index that shows other channels referencing it. Check the geo split matches where "
     "your product sells. Then go manual: read the last ten posts — do they get real "
     "comments from named humans? Do previous promo posts hold their views after a week, "
     "or collapse (a collapse means the audience is ad-only)? Ask the admin for the "
     "exact slot — morning placements beat evening by 10–30% in most niches — and for "
     "one previous sponsor you can ask about. An admin who refuses all references has "
     "answered your question.</p>")

_sec('telegram-advertising-guide', 'Telegram Ads vs channel posts',
     "<p>The official Telegram Ads platform sells CPM-based sponsored messages shown in "
     "large channels — bought through agencies in most regions, with meaningful minimum "
     "budgets, strict content policies and comparatively coarse targeting. Its upside is "
     "clean, policy-safe reach inside premium-heavy feeds. For most channel owners doing "
     "either job — growing a channel or buying their first thousand targeted readers — "
     "marketplace posts and direct deals remain the better tool, because you're buying a "
     "specific audience <i>with editorial context</i>: the post appears in a feed the "
     "reader chose and trusts, next to content they came for. CPM impressions can't "
     "carry that. The pragmatic split: Telegram Ads for scale once the funnel "
     "converts, posts and deals for everything before that.</p>")

# ============================================================= CONTENT ======

_sec('telegram-fonts-and-rich-text', 'The entities the mobile composer hides',
     "<p>The composer's B/I menu is a subset. The full entity set includes: "
     "<b>underline</b> (desktop: Ctrl+U), <b>strikethrough</b>, <b>monospace</b> via "
     "triple backticks with syntax highlighting for code, <b>spoilers</b> (hidden-until-"
     "tap text — perfect for solutions, leaks and price reveals), <b>hidden links</b> on "
     "arbitrary words, <b>block quotes</b> with nesting in newer clients, and the "
     "quietly powerful <b>expandable quote</b>: a collapsed \"show more\" block. "
     "Expandable quotes are the digest channel's best formatting weapon — twelve links, "
     "each summarized in a one-line quoted block, stays scannable instead of becoming a "
     "wall. None of these need a bot; most need the desktop app to discover.</p>")

_sec('telegram-fonts-and-rich-text', 'Where each client drops your formatting',
     "<p>Formatting survives differently depending on the path it takes. Forwards "
     "preserve everything. Copy-paste from desktop usually preserves entities but strips "
     "them from media captions. RSS-imported posts can lose nested quotes and custom "
     "emoji. Some third-party Android clients render custom emoji as their fallback "
     "packs. And previews outside Telegram — link cards on Twitter/X or Discord — show "
     "plain text only, which is why the first line of every post must work naked. The "
     "professional habit: keep one \"torture test\" message containing every entity, "
     "post it to a private test channel, forward it through every pipeline you use, and "
     "look at what arrives. Ten minutes of setup answers a year of \"why did that post "
     "look broken?\"</p>")

_sec('telegram-fonts-and-rich-text', 'Bot-side formatting: HTML beats markdown for pipelines',
     "<p>When content flows through bots — schedulers, RSS bridges, cross-posters — the "
     "parse mode decides fidelity. Telegram's markdown mode breaks on unescaped "
     "underscores in URLs and on stray asterisks; HTML mode (<code>&lt;b&gt;</code>, "
     "<code>&lt;i&gt;</code>, <code>&lt;code&gt;</code>, <code>&lt;a href&gt;</code>) is "
     "deterministic and copies cleanly between tools. The working rule: author by hand "
     "in the composer, but store <i>templates</i> in HTML inside your scheduler — Fast "
     "Scheduler accepts formatted drafts, and most bots expose a preview command — so "
     "automated posts never surprise you with literal asterisks published to four "
     "thousand people. Whichever mode you standardize on, standardize: mixed-format "
     "pipelines are where formatting goes to die.</p>")

try:
    import blog_extras4  # noqa: F401,E402
except ImportError:
    pass
