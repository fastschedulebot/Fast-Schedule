# -*- coding: utf-8 -*-
"""Deep-dive sections for blog articles, part 5 — the 398–479 word tier.

Same editorial rules: real numbers, real mechanics, tools as plain text,
every section a continuation of the article (new material, not a summary).
"""

import blog_extras as _be

_sec = _be._sec

# ============================================================ PLATFORM ======

_sec('telegram-bot-safety', 'Reading an admin-rights request like a contract',
     "<p>Every bot that publishes to your channel asks for admin rights, and the list it "
     "requests is a contract worth reading. The rights a publishing tool actually needs: "
     "<b>Post messages</b> (and usually <b>Edit messages</b>, so you can fix a typo in a "
     "scheduled post). That's the healthy core. <b>Delete messages</b> is reasonable for "
     "schedulers that replace reposted content, a red flag for a tool that has no reason "
     "to remove anything. <b>Invite users</b> and <b>ban users</b> are moderation rights "
     "— Combot- and Rose-class tools need them in the discussion group; a scheduler "
     "asking for them is overreaching. <b>Add admins</b> should never be granted except "
     "to tools you'd trust with the channel itself. The audit habit: once a quarter, "
     "open the channel's admin list and read each bot's rights against what it does — "
     "and demote anything that collected rights you no longer use. Revoking a bot's "
     "admin rights takes two taps and instantly caps what it can ever do again.</p>")

_sec('telegram-bot-safety', 'Token incidents: the first ten minutes',
     "<p>If a token leaks — committed to a public repo, pasted into a screenshot, or "
     "handed to a shady \"promotion service\" — the response clock matters. <b>Minute "
     "one:</b> open BotFather, <code>/mybots</code> → the bot → API Token → Revoke. The "
     "old token dies mid-sentence; whatever scripts used it start failing, which is the "
     "point. <b>Minutes two to five:</b> update the token in every tool that legitimately "
     "used it — scheduler settings, server environment variables, CI secrets. "
     "<b>Minutes five to ten:</b> audit what the token could do while leaked: if the bot "
     "was a channel admin, scan the channel's recent posts for anything you didn't "
     "publish; if it was a group member with privacy mode off, assume the group's "
     "messages were read. Then the boring permanence: two-step verification on the "
     "account, and tokens treated like passwords from now on — no chats, no screenshots, "
     "no spreadsheets. Bots whose tokens never leak never have incidents.</p>")

_sec('telegram-bot-safety', 'The gray zone: what group bots actually read',
     "<p>Privacy mode is the switch that decides whether a group bot sees ordinary "
     "messages or only commands and replies to it — <code>/setprivacy</code> in "
     "BotFather, or the group settings page for admins. Analytics and moderation bots "
     "(Combot, Rose) must see the traffic to count or filter it, so they run with "
     "privacy off by design. That's the trade: real moderation and real statistics in "
     "exchange for a third party storing your community's messages, often including "
     "member joins and names. Choose that trade deliberately: prefer bots with a "
     "reputation and a track record over an anonymous bot offering identical features, "
     "check whether the bot offers a data-deletion path, and remember that a bot added "
     "to a private work group sees the same things a human member would. The audit "
     "question for every bot in every group is one line: <i>what does this bot see, and "
     "what does it do with it?</i></p>")

# ============================================================ CONTENT =======

_sec('telegram-series-and-serialized-posts', 'The hashtag index: making a series navigable',
     "<p>A series without an index punishes every late joiner and caps how far the "
     "series can travel. The fix is three artifacts, all cheap. <b>Tag every part:</b> "
     "<code>#buildlog 4/12</code> in the footer makes the whole series one tap away "
     "(tapping a hashtag searches the channel for it) and gives readers a progress "
     "marker. <b>Pin or link an index post:</b> one message listing all parts with "
     "links, updated as the series grows — this is what forwarders share. <b>Open each "
     "part with a one-line recap:</b> \"Last time: we shipped the parser; today it "
     "breaks in production.\" New readers buy in at part five if the on-ramp costs ten "
     "seconds; without these artifacts they don't, and a reader who can't catch up "
     "silently waits for the series to end.</p>")

_sec('telegram-series-and-serialized-posts', 'Pacing mechanics: the cliff, the gap and the payoff',
     "<p>Serialized retention is an engineering problem with known parts. <b>Part "
     "length:</b> 300–600 words per part is the sweet spot — long enough to deliver, "
     "short enough that \"I'll read the next one\" never becomes a chore. <b>The "
     "cliff:</b> end on an open loop the reader can feel — an unresolved number, a "
     "decision pending, a failure just discovered — not on a summary (summaries close "
     "loops, and closed loops don't bring anyone back). <b>The gap:</b> one day between "
     "parts builds the check-the-channel habit; a week between parts loses most casual "
     "readers mid-series, so for weekly cadence, make each part self-contained. "
     "<b>The payoff rule:</b> never stretch the finale — readers forgive a short series, "
     "never a padded one. Schedule the whole series in one sitting, gaps included, so "
     "pacing is a decision you made once instead of a mood you had each morning.</p>")

_sec('telegram-series-and-serialized-posts', 'After the finale: the series as an asset',
     "<p>A finished series is an asset, and most channels abandon it the day it ends. "
     "The harvest routine: publish a <b>finale index</b> — the full list with links, "
     "framed as \"the whole story in one place\" — and pin it for a week; it "
     "consistently becomes one of the channel's most-forwarded posts because it's the "
     "format forwarders prefer. Then <b>package</b>: the same parts, lightly edited, "
     "become a PDF, a Notion page or the free artifact that anchors a paid tier — "
     "serialized content is pre-validated long-form, and bundling it costs an evening. "
     "Finally <b>rerun</b>: three months later, re-promote one part per week with a "
     "\"from the archive\" line. On channels that do this, archive reruns routinely "
     "pull view rates close to the original run — because half your current subscribers "
     "weren't there when it first ran.</p>")

# ============================================================ PREMIUM =======

_sec('telegram-mini-apps', 'What a Mini App actually is (thirty seconds of architecture)',
     "<p>Demystifying it helps you scope honestly: a Mini App is a normal web page — "
     "HTML, CSS, JavaScript — opened in a Telegram-styled browser view when a user taps "
     "the bot's menu button, an inline button, or a direct link. Telegram hands the page "
     "a small signed payload identifying the user (so the app knows who's visiting "
     "without a login form) and theme colors (so it matches dark mode automatically). "
     "Everything after that is web development, or no-code site building. The practical "
     "consequence: any static page you can host — a price calculator, a catalog, a form "
     "— can become a Mini App by registering it with BotFather's <code>/newapp</code>. "
     "The ceiling is the web's ceiling; the floor is \"a well-designed mobile page\".</p>")

_sec('telegram-mini-apps', 'The no-code paths that exist today',
     "<p>Three routes get a channel a working Mini App without writing code. <b>Site "
     "builder plus <code>/newapp</code>:</b> publish a mobile-friendly page on Tilda, "
     "Carrd or any builder, then register the URL as the bot's web app — two hours, "
     "full design control, zero code. <b>Bot constructors with app modules:</b> "
     "platforms in the BotMother / PuzzleBot / SendPulse class ship shop and form "
     "templates that publish as Mini Apps — fastest path to a storefront or booking "
     "form, at the cost of their monthly fee and their design limits. <b>Embed-style "
     "tools:</b> calculators, quizzes and schedulers that generate embeddable pages can "
     "be wrapped the same way. The evaluation rule is the same for all three: open the "
     "result on a phone inside Telegram before committing — an app that only looks "
     "right on a desktop browser will quietly leak half its visitors.</p>")

_sec('telegram-mini-apps', 'Measuring a Mini App: the funnel inside the funnel',
     "<p>A Mini App earns its place only if you can see its funnel. Three numbers "
     "matter. <b>Open rate:</b> taps on the app button ÷ views of the post or menu that "
     "promoted it — below 5% on a dedicated post usually means the promise was vague "
     "(\"open our app\") rather than concrete (\"check your delivery window\"). "
     "<b>Completion rate:</b> of those who opened, the share that finished the "
     "calculator, order or form — this is where heavyweight pages die, and where "
     "cutting fields pays. <b>The output event:</b> orders placed, bookings made, "
     "leads captured — tracked with the same UTM or shortlink discipline you'd use on "
     "any external link. Review the three numbers monthly, and treat the app like a "
     "post format: when completion sags, cut steps before you add features. A Mini App "
     "that does one thing flawlessly beats a portal every time.</p>")

_sec('telegram-premium-for-channels', 'The boost economy, in plain terms',
     "<p>Channel boosts are the bridge between Premium users and channel features: a "
     "Premium subscriber can donate a boost to a channel, boosts stack into levels, and "
     "each level unlocks capabilities — more custom emoji slots for the channel, the "
     "ability to post stories, richer description formatting and similar perks. Two "
     "mechanics decide how to think about them. First, <b>boosts decay</b>: they're "
     "tied to active Premium subscriptions, so a level quietly drains if supporters let "
     "Premium lapse — a level is a rent, not a purchase. Second, <b>boosts come from "
     "your audience</b>, which makes asking for them a social contract: channels that "
     "explain what the next level unlocks (\"at this level we get stories — behind-the-"
     "scenes starts Monday\") convert far better than generic \"boost us\" banners. "
     "Honest math: for small channels, the features rarely justify the campaign; treat "
     "boosts as a nice-to-have that your biggest fans may hand you, not a KPI.</p>")

_sec('telegram-premium-for-channels', 'Stories for channels: what they change',
     "<p>Once a channel has the required boost level, it can post stories — the "
     "ephemeral, 24-to-48-hour format that lives on a separate tab. For channels, "
     "stories are a different register than posts: casual, unpolished, mobile-filmed, "
     "and they don't interrupt the feed's rhythm because they don't appear in it. "
     "Working uses: same-day event coverage, \"we're shipping this today\" teasers, "
     "polls about tomorrow's post, and the human faces that a channel feed rarely "
     "shows. The constraint is the catch: the audience that sees stories is the "
     "audience that already opens your channel deliberately — stories reward the "
     "loyal, they don't reach the passive. If your boost level doesn't include "
     "stories, the workarounds are old-fashioned: circles (video messages) and "
     "photo-dump posts carry the same behind-the-scenes energy inside the "
     "feed.</p>")

_sec('telegram-premium-for-channels', 'The reader-side features that quietly help owners',
     "<p>Most Premium benefits are reader-facing, and three of them leak value back to "
     "channels. <b>Ad-free feed:</b> Premium users don't see Telegram's in-feed "
     "sponsored messages — irrelevant unless you buy Telegram Ads, but it means "
     "Premium-heavy audiences are cleaner to reach with your own posts. <b>4 GB "
     "uploads and faster downloads:</b> file-heavy channels (courses, datasets, "
     "templates) serve their best material faster to exactly the subscribers most "
     "likely to share it. <b>Transcription of voice messages:</b> if your channel "
     "posts circles or voice notes, Premium readers get them transcribed — the "
     "accessibility gap narrows itself for the most engaged cohort. None of this "
     "justifies asking your audience to buy Premium for your sake; it just means that "
     "when a chunk of your audience <i>is</i> Premium, the channel quietly works "
     "better for them than the raw feature list suggests.</p>")

# ============================================================== MONEY =======

_sec('telegram-crypto-payments', 'Invoice anatomy: the details that change conversion',
     "<p>Whether the invoice comes from CryptoBot or another processor, the same "
     "details move completion rates. <b>Describe the deliverable in the invoice "
     "itself:</b> \"Signal access — 30 days from payment\" converts better than a bare "
     "product name, because the invoice is the last thing a hesitant buyer reads. "
     "<b>Set an expiry:</b> invoices that expire in 30–60 minutes create honest urgency "
     "and stop price-shopping; invoices that live forever get paid by the 3% who "
     "remember. <b>Price in one currency, display in the buyer's:</b> stablecoin "
     "pricing (USDT-style) avoids the \"it was $15 when I opened it\" support ticket; "
     "showing a fiat equivalent removes the last mental conversion step. <b>Receipt "
     "message on payment:</b> an automatic \"paid — here's what happens next\" line "
     "cuts the \"did it go through?\" messages to nearly zero. None of this is crypto-"
     "specific — it's checkout hygiene, applied to a checkout that settles in "
     "seconds.</p>")

_sec('telegram-crypto-payments', 'Refunds and disputes without a payments team',
     "<p>Crypto payments have no chargeback button, which cuts both ways: buyers can't "
     "reversal-fraud you, and you have no machinery to hide behind when a refund is "
     "genuinely owed — the refund is you, manually. The working policy, written down "
     "before launch: what's refundable (wrong product, double payment, service not "
     "delivered), what isn't (\"changed my mind\" on access already consumed), and a "
     "response window (24–48 hours). Mechanically, refunds on Telegram rails are "
     "returns: CryptoBot can send funds back to the paying user, and Stars purchases "
     "can be refunded by the seller in-app. Publish the policy in the pinned message "
     "and link it from every invoice description — the policy read <i>before</i> "
     "payment prevents the dispute, and the one that arrives anyway gets settled in "
     "one reply because the rule already exists. Sellers who improvise refunds case "
     "by case train their buyers to negotiate.</p>")

_sec('telegram-crypto-payments', 'The scam patterns around in-Telegram payments',
     "<p>Every payment rail attracts its predators, and Telegram's are predictable. "
     "<b>Fake support:</b> minutes after a visible payment, a \"CryptoBot support\" "
     "account DMs about a problem — no real payment service DMs first; real support "
     "lives inside the official bot. <b>Payment-screenshot fraud:</b> a screenshot of "
     "a sent transaction proves nothing until it's confirmed on-chain (or in the bot's "
     "receipt) — sellers who ship on screenshots fund scammers; sellers who check the "
     "confirmation never argue. <b>Address swaps:</b> if you publish a wallet address, "
     "malware on <i>buyers'</i> machines can paste a different address — first "
     "payments to a new wallet deserve a test transaction. <b>The impersonation "
     "shop:</b> cloned channel names selling \"lifetime access\" — your defense is the "
     "pinned trust post and a username nobody else can hold. The common thread: "
     "verification is always one tap away, and every scam is designed to make that "
     "tap feel unnecessary.</p>")

# =============================================================== TOOLS ======

_sec('telegram-analytics-tools-compared', 'ERR honestly: what a good number actually is',
     "<p>ERR (engagement rate of reach — views ÷ subscribers, usually on the last "
     "several posts) is the number everyone quotes and few calibrate. Rules of thumb "
     "admins actually trade on: under 1,000 subscribers, a healthy channel posts ERR "
     "of 50% and up — small audiences are loyal audiences; 1,000–10,000, the 25–45% "
     "band is normal and 30%+ is strong; above 50,000, mature channels live in the "
     "10–25% range and anything higher is suspiciously good. Two calibration rules "
     "matter more than the thresholds. <b>Compare within your niche:</b> a deals "
     "channel's ERR runs structurally lower than a micro-lessons channel's — the "
     "number only means something next to its own species. <b>Watch the trend, not "
     "the value:</b> an ERR sliding from 32% to 24% over a quarter is the loudest "
     "retention alarm you have; a stable 18% is a fine, honest channel. Advertisers "
     "price on ERR because it's the closest thing to \"how many real humans see this\" "
     "— keeping yours honest keeps every future negotiation honest too.</p>")

_sec('telegram-analytics-tools-compared', 'The weekly 15-minute metrics ritual',
     "<p>Analytics that doesn't end in a decision is procrastination with charts. The "
     "ritual that fits in a coffee break: <b>1)</b> pull the last seven posts' views "
     "and compute views ÷ subscribers — the ERR trend line; <b>2)</b> note the best "
     "and worst post of the week and write one sentence on why (format? topic? time?) "
     "— this is where the editorial instinct gets data; <b>3)</b> check joins vs "
     "leaves for the week, and if leaves spiked, find the post that caused it; "
     "<b>4)</b> check forwards and reactions on the top post — the formats worth "
     "repeating; <b>5)</b> glance at the scheduler's upcoming queue and confirm next "
     "week exists. Five numbers, five minutes of notes, one decision: what next week "
     "gets more of and less of. The ritual compounds precisely because it's boring — "
     "channels that \"check stats when curious\" get curious twice a quarter.</p>")

_sec('telegram-analytics-tools-compared', 'Link tracking inside Telegram: the honest limits',
     "<p>Per-post link attribution is the weakest link in the Telegram analytics "
     "chain, and knowing its edges prevents bad decisions. Channel posts are forwarded "
     "and re-viewed for months, so click counts accumulate slowly and a \"flop\" post "
     "at 48 hours can be the quarter's best click-source at day 60 — judge link posts "
     "on a 30-day window. UTMs work fine (Telegram's in-app browser preserves "
     "parameters), but they don't survive screenshots and re-typing, which is where "
     "promo codes earn their keep: a code is attribution that travels by word of "
     "mouth. Shortlinks you control (a branded short domain) let you recount clicks "
     "later and see the decay curve; raw destination URLs hide it. And when comparing "
     "channels for paid promos, remember the numbers asymmetry: TGStat estimates views "
     "publicly, but clicks on your own links are the only number you can fully "
     "trust — which is why serious sponsors ask for a test post with a tracked link "
     "before any bundle deal.</p>")

_sec('telegram-rss-bots', 'Filters and templates: making the feed yours',
     "<p>The difference between an RSS bot that helps and one that floods is the two "
     "configuration layers most people skip. <b>Filters:</b> per-feed keyword rules — "
     "only post entries matching \"russia*-related terms\" or your product names, "
     "block anything tagged \"sponsored\" — cut a firehose to a stream; the global "
     "block list (competitor names, words that always mean noise in your niche) does "
     "the rest. <b>Templates:</b> per-feed post formatting — a title line, a one-"
     "sentence rule, the link, and a hashtag for the source — turns machine output "
     "into something that reads like your channel. Budget the regex-level effort for "
     "an evening, not an afternoon: feeds drift, and a filter list reviewed quarterly "
     "catches the source that quietly changed its RSS structure and started posting "
     "raw HTML. The bot's job is plumbing; the curation still has to be "
     "yours.</p>")

_sec('telegram-rss-bots', 'The hybrid feed: automation with a human gate',
     "<p>For channels where voice matters more than speed, the setup that works is "
     "RSS-to-<i>review</i>, not RSS-to-publish: the bot posts new feed items into a "
     "private editor's chat instead of the channel, and a human promotes the ones "
     "worth publishing — one tap to forward into the scheduler's draft flow, two taps "
     "to publish immediately. You keep the machine's completeness (nothing is ever "
     "missed) while the channel keeps its voice (nothing is published unread). The "
     "cost is honest: five to fifteen minutes a day at realistic feed volumes, which "
     "is exactly the job a curation channel claims to do manually anyway. Channels "
     "that outgrow the hybrid usually demote it in a predictable order: news they "
     "always publish goes fully automated, analysis stays human, and the review chat "
     "shrinks to a checklist — automation earning its autonomy one verified pattern "
     "at a time.</p>")

_sec('telegram-rss-bots', 'When RSS is the wrong tool',
     "<p>Some sources don't fit the pipe, and forcing them creates worse output than "
     "manual posting. <b>JS-heavy sites</b> with no real feed publish summaries so "
     "stripped the bot posts ellipses — those sources deserve a manual slot or a "
     "different bridge. <b>Paywalled outlets</b> export headline-plus-paywall links, "
     "which reads as teasing content you can't deliver. <b>Social feeds</b> "
     "(Twitter/X, YouTube channels) have unstable or rate-limited bridges that break "
     "silently; for YouTube specifically, channels and playlists usually work better "
     "through dedicated notification bots than generic RSS. And <b>sources that "
     "matter in minutes</b> — breaking news, price alerts — are a polling-frequency "
     "problem RSS bots handle poorly. The mature stack admits the gap: RSS for the "
     "steady 80%, manual or specialized tools for the moments where speed or context "
     "is the product.</p>")

_sec('telegram-verification-and-scams', 'The impersonation playbook (so you can spot it)',
     "<p>Channel-targeting scams follow scripts, and knowing the scripts defuses them. "
     "<b>The fake admin:</b> a copy of your username with one swapped character (l for "
     "I, an extra underscore) DMs your subscribers about \"account verification\" or "
     "an exclusive drop — real admins don't DM first, ever, which is the line worth "
     "pinning. <b>The paid-verification pitch:</b> someone offers to sell your channel "
     "a blue check or a listing — Telegram's verified badge is issued to notable "
     "entities, not sold to askers; every \"buy verification\" offer is theft or "
     "impersonation prep. <b>The merger scam:</b> \"we want to buy/promote your "
     "channel, add this admin bot first\" — the bot gets rights and the channel gets "
     "emptied. <b>The clone shop:</b> full copies of your channel name and avatar "
     "selling something in the description. The countermeasures are structural: pin "
     "the \"we never DM first\" line, check the exact username of anyone claiming to "
     "be you, and report impersonators to Telegram's abuse channels — clones that "
     "survive a week start collecting your subscribers' money.</p>")

_sec('telegram-verification-and-scams', 'Protecting your audience: the pinned trust post',
     "<p>You can't stop scams targeting your audience, but you can pre-empt the ones "
     "that borrow your face. The pinned trust post, kept current, answers the three "
     "questions every scam exploits: <b>who is us</b> — the exact usernames of the "
     "channel, the discussion group and any official accounts, so a look-alike is "
     "checkable in five seconds; <b>what we'll never do</b> — DM you first, ask for "
     "payment outside the methods listed in the channel, offer \"verification\", ask "
     "for codes or logins; <b>what to do if unsure</b> — ask in the discussion group "
     "publicly, where the scammer can't follow. When a wave hits, don't delete the "
     "trust post to make room — that's when it earns its pin. Channels that train "
     "their audiences this way convert scam attempts into community moments: "
     "subscribers screenshot the fake, post it in the group, and the audience learns "
     "its reflexes together.</p>")

_sec('telegram-scheduler-comparison', 'The native composer: what it does and where it stops',
     "<p>Telegram's built-in scheduling deserves its due before any tool comparison: "
     "it's free, offline-proof, and the scheduled post is editable up to the moment "
     "it sends — for a one-off post tomorrow at nine, nothing beats it. Where it "
     "stops is a short list that defines every scheduler's pitch. <b>No queue "
     "overview:</b> the composer shows one scheduled post per open chat, not a "
     "calendar of what's coming — planning a week means scrolling. <b>No drafts "
     "library:</b> reusable templates, pillar skeletons and evergreen posts live in "
     "your notes app, not in the tool. <b>No cross-channel view:</b> two channels "
     "means two composers and a memory. <b>No analytics:</b> scheduling natively "
     "means stats come from somewhere else. If you publish twice a week, the native "
     "scheduler is the right tool; the moment the question \"what's queued for "
     "Thursday?\" appears, a tool with a queue earns its keep.</p>")

_sec('telegram-scheduler-comparison', 'Migrating between schedulers without double-posting',
     "<p>Switching tools has one classic disaster — the old scheduler and the new one "
     "both fire the same post. The safe migration order: <b>freeze</b> (stop adding "
     "to the old queue a week before the switch), <b>export</b> (copy pending drafts "
     "out — most tools at least show scheduled posts; a screenshots-plus-notes export "
     "is undignified but complete), <b>revoke</b> (remove the old tool's admin rights "
     "and, for token-based tools, reissue the token — a live token in an abandoned "
     "tool is a safety issue, not a tidiness one), <b>rebuild</b> the queue in the "
     "new tool from the exported plan, and <b>overlap for one week</b> with the old "
     "tool idle before deleting anything. The one-week overlap is the insurance: "
     "queues don't always export, tokens don't always transfer, and discovering "
     "either on day one of a fresh tool is how gaps happen. Migrations done this way "
     "are boring, which is the goal.</p>")

_sec('telegram-scheduler-comparison', 'The small print that decides daily happiness',
     "<p>The comparison tables miss the details that decide whether a scheduler "
     "becomes part of your hands. <b>Timezone honesty:</b> the tool must show "
     "<i>your audience's</i> local time or a fixed home zone — \"9:00\" in whose "
     "morning? Daylight-saving drift has silently moved more channels' schedules than "
     "any hack. <b>Silent send:</b> a toggle per post, not a global setting — night "
     "posts to other timezones shouldn't ring phones. <b>Preview fidelity:</b> you "
     "need to see the post as subscribers will — media order, caption truncation, "
     "link preview — because the preview is the last QA gate. <b>Edit-after-schedule:"
     "</b> real life edits posts after they're queued; tools that force delete-and-"
     "resend lose small fixes. <b>Draft storage:</b> where do your pillar templates "
     "live? Inside the tool beats a notes app by a mile. Test these five in the free "
     "tier before comparing price — they're the difference between a tool you open "
     "daily and one you abandon by February.</p>")

try:
    import blog_extras6  # noqa: F401,E402
except ImportError:
    pass
