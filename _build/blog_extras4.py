# -*- coding: utf-8 -*-
"""Deep-dive sections for blog articles, part 4 — the 311–391 word tier.

Same editorial rules: real numbers, real mechanics, tools as plain text,
every section a continuation of the article (new material, not a summary).
"""

import blog_extras as _be

_sec = _be._sec

# ============================================================= CONTENT ======

_sec('telegram-video-content-guide', 'Length sweet spots, by format',
     "<p>Watch-through is the metric that matters for channel video, and it collapses with "
     "length. Native vertical/horizontal video in a channel feed: the 45–90 second band "
     "holds the majority of full watches; past two minutes, completion typically drops "
     "below a third even for engaged audiences. Video circles (the round, camera-recorded "
     "format) are a different animal — under a minute, personal, and they read as "
     "presence rather than production, which is why they work for build-in-public and "
     "behind-the-scenes posts. Explainers that genuinely need five minutes should become "
     "two parts: a 60-second summary post, and \"full version\" as a link or a second "
     "part — the split usually outperforms the single long upload on both views and "
     "replies.</p>")

_sec('telegram-video-content-guide', 'Design for sound-off viewing',
     "<p>Channel video autoplays muted as you scroll — the majority of first views happen "
     "with no audio. Videos that assume sound lose the scroll-by viewer: the first two "
     "seconds decide whether thumbs stop, and a talking head with no captions is a "
     "black box. The fixes are cheap: burn captions into the frame (most editing apps do "
     "it automatically now), put the topic as text in the first second, and make the "
     "first frame a designed card rather than a mid-motion blur. Then check your own "
     "channel the way subscribers see it — scroll your feed with sound off and watch "
     "which of your own videos would stop you. If the honest answer is none, the "
     "problem was never the editing.</p>")

_sec('telegram-video-content-guide', 'The thumbnail is the first frame',
     "<p>Telegram doesn't give videos a separate thumbnail picker the way YouTube does — "
     "for most uploads the preview frame is taken from the video itself, which means "
     "<b>you engineer the preview when you edit</b>: put a clean, high-contrast title "
     "card in the first frame, or cut the video so frame one is the money shot. For "
     "videos where the first frame matters and you can't re-edit, sending the file as a "
     "document (uncompressed) shows a generic file card instead — sometimes the honest "
     "option, rarely the better one. Channels that treat every video's frame one as a "
     "thumbnail get measurably more taps; it's the closest thing to free reach the "
     "format offers.</p>")

_sec('telegram-channel-vs-group', 'The admin-rights model that keeps both sane',
     "<p>Channel and group rights are granular and worth five minutes of deliberate "
     "configuration. On the channel: give co-admins exactly <i>post messages</i> and "
     "<i>edit messages of others</i> if they draft, but reserve <i>delete messages</i> "
     "and <i>ban subscribers</i> for the owner — deletion history is the one thing you "
     "can't audit after the fact. On the linked group: moderators get invite-by-link, "
     "delete and mute; ban stays with the owner. Two details people miss: <b>anonymous "
     "admin</b> lets a group admin act under the group's identity rather than their "
     "own, and posting <i>as the channel</i> inside the discussion group is a toggle "
     "any channel admin has — that's how the brand answers comments without exposing "
     "which human pressed send.</p>")

_sec('telegram-channel-vs-group', 'Supergroups, topics and the 200-member line',
     "<p>Plain groups convert to supergroups automatically when they cross 200 members "
     "(or when you flip certain settings); there's no downgrade. For larger communities, "
     "the feature that changes everything is <b>topics</b> (forum mode): the group "
     "becomes threads — support, showcase, off-topic, announcements — instead of one "
     "river. Discussion groups linked to channels are usually better <i>without</i> "
     "topics while small (a topic UI adds a click of friction to drive-by comments), but "
     "past a few hundred active members, topics are the difference between a community "
     "and noise. Pair topics with slow mode of one to five minutes for the general "
     "thread during launches — the firehose becomes readable, and quality arguments "
     "survive.</p>")

_sec('telegram-channel-vs-group', 'When you need to switch (and why you usually can\u2019t)',
     "<p>There is no convert button in either direction — a channel can't become a group "
     "and a group can't become a channel. The honest workarounds: a group that has "
     "accidentally outgrown its purpose becomes a channel by creating the channel, "
     "pinning a pointer, and letting the old group go quiet (or handing it to the "
     "community as the chat annex); a channel that needs conversation doesn't convert — "
     "it creates a discussion group and links it. Plan the structure before you grow: "
     "the cost of a wrong-shaped container rises with every thousand members, because "
     "the audience — not the settings — is what's hard to move.</p>")

# ============================================================== GROWTH ======

_sec('telegram-for-local-business', 'The neighborhood seeding plan',
     "<p>Local channels grow through local gravity, not ads. The sequence that works: "
     "list every district chat, building group and community channel within your "
     "catchment area (most towns have dozens; search the city name in Telegram and check "
     "the local folder that residents share); join as yourself, be useful for two weeks, "
     "then start publishing the artifact-shaped posts your channel exists for — the "
     "\"what's actually open on Monday\" post, the honest price list, the heads-up about "
     "the street closure. Partner with two or three non-competing local businesses for "
     "cross-posts: the bakery's channel mentions your workshop, yours mentions theirs. "
     "And print the bridge: a QR code on the counter, the receipt and the door that "
     "opens <code>t.me/yourchannel</code> converts the walk-in traffic you already "
     "have — that's the cheapest subscriber you will ever acquire, and they're the "
     "highest-retention kind because they know your face.</p>")

_sec('telegram-for-local-business', 'The offer calendar for a small channel',
     "<p>With a few hundred local subscribers, promo discipline matters more than with "
     "ten thousand — every post is a noticeable share of their week, and the channel "
     "competes with their family chats for attention. The pattern that holds: one "
     "pure-value post midweek (the tip, the local news, the story), one offer post at "
     "the natural buying moment (Thursday/Friday for weekend businesses, Monday for "
     "service bookings), and everything else between is presence — arrivals, "
     "behind-the-scenes, staff faces. Two offers a week is the ceiling under 500 "
     "subscribers; a third measurably raises mutes. Post the offer <i>with</i> the "
     "booking path in the same message — \"reply here or call, we confirm today\" — "
     "because the extra reply step is where local sales actually die.</p>")

_sec('telegram-for-local-business', 'Why the channel beats the WhatsApp broadcast list',
     "<p>Local businesses often already have a WhatsApp broadcast list — and it has "
     "three structural problems a Telegram channel fixes. Broadcast messages only "
     "arrive if the customer saved your number, so half the list silently doesn't "
     "exist. There's no public link to hand out — growth stops at the counter. And "
     "there's no way for a message to be seen twice (no views, no pinned archive, no "
     "search). A Telegram channel fixes all three: anyone with the t.me link can join "
     "without your phone number, every post has a visible view count so you finally "
     "learn what customers actually read, and old offers stay findable via search and "
     "pins. Keep WhatsApp for one-to-one customer service; move the broadcasting to the "
     "channel. That split — private channel for conversation, public channel for "
     "publishing — is the local-business stack.</p>")

_sec('telegram-subscriber-retention', 'The mute problem: churn you can\u2019t see',
     "<p>The subscriber count lies quietly. Muted subscribers — people who left the "
     "notifications on but stopped reading, or silenced you on purpose — still count, "
     "still show in the member list, and never view anything. That's why ERR (views ÷ "
     "subscribers) is the real retention metric: a channel whose subscriber line grows "
     "while its ERR slides from 40% to 18% is bleeding readers into mute, not growing. "
     "The counters to mute-creep are specific: posts whose first line carries a promise "
     "(muted readers see the preview text, not the notification), the pinned post kept "
     "genuinely useful (pins are the one thing muted readers check), and a weekly "
     "signature format — the same feature at the same time — because habit, not "
     "notification sound, is what re-opens a muted channel.</p>")

_sec('telegram-subscriber-retention', 'Cohort views: measuring the first seven days',
     "<p>Raw weekly views mix old and new subscribers, so they hide the leak. The "
     "cohort view finds it: note your subscriber count, watch a specific post's 48-hour "
     "views, and compute views-per-post against the subscriber base at posting time "
     "every week for a month. Three patterns tell you where you stand: if <i>new</i> "
     "weeks' posts hold the same ERR as older ones, retention is fine and growth is "
     "real; if ERR holds but views-per-day decay within hours of posting, your problem "
     "is reach timing, not content; if each week's posts underperform the last, "
     "subscribers are muting faster than the channel grows — fix the feed before "
     "spending another hour on acquisition. Ten minutes a week with a spreadsheet "
     "answers which of the three diseases you have, and the treatments don't "
     "overlap.</p>")

_sec('telegram-subscriber-retention', 'The quarterly cull that raises ERR',
     "<p>Once a quarter, consider removing the dead weight: bots, abandoned accounts, "
     "and — if you ever bought growth — the fake subscribers still dragging your view "
     "rate down. It feels backwards to delete \"subscribers\", but every downstream "
     "number improves: your ERR rises, which is the number advertisers read and the "
     "number swap partners ask about; your per-post expectations become honest; and "
     "Telegram's recommendation surfaces weigh engagement, not raw count. The "
     "exceptions: never cull after a paid-promo wave (let the window settle), and "
     "don't confuse quiet real people with fakes — check the member list for accounts "
     "with no avatar, no username and no activity before removing anything. A 5,000 "
     "channel that reads as 40% ERR beats a 9,000 channel that reads as 15% in every "
     "commercial conversation.</p>")

# =============================================================== TOOLS ======

_sec('how-to-create-a-telegram-bot', 'Polling vs webhooks (and what hosting actually costs)',
     "<p>Every bot moves messages one of two ways. <b>Polling</b>: your program asks "
     "Telegram \"any new updates?\" every second or two — trivial to run from a laptop, "
     "a home server or a free-tier worker, and fine for personal or small-audience "
     "bots. <b>Webhooks</b>: Telegram pushes each update to your HTTPS URL — the "
     "professional setup, needs a domain with a valid certificate, but uses zero "
     "resources when idle. The cost ladder for a hobby bot: free (polling on a spare "
     "machine or a free serverless tier), then a $4–6/month VPS when the bot must be "
     "always-on. BotFather's <code>/setwebhook</code> and <code>/deletewebhook</code> "
     "switch between the modes. The mistake to avoid: running polling and webhook "
     "simultaneously — updates split between them and the bot appears to \"lose\" "
     "messages.</p>")

_sec('how-to-create-a-telegram-bot', 'The rate limits every bot eventually hits',
     "<p>Telegram's Bot API is generous but not unlimited: a bot may send about 30 "
     "messages per second overall, but only roughly one message per second to the same "
     "chat (about 20 per minute inside groups), and file uploads cap around 50 MB with "
     "downloads via the standard API around 20 MB. The limits bite exactly when a bot "
     "gets popular — a channel bot that announces to 500 personal chats will finish "
     "its queue in ~8 minutes at one message per second, which is why serious "
     "sender tools queue with retry-on-429 built in. If you're building, read the "
     "<code>retry_after</code> field the API returns and sleep for exactly that long; "
     "hammering through it is how bots get throttled for hours. Knowing the numbers up "
     "front is the difference between a bot that scales and one that dies on its first "
     "good day.</p>")

_sec('how-to-create-a-telegram-bot', 'From toy to tool: the graduation path',
     "<p>The no-code ceiling arrives sooner than expected, and the path past it is "
     "well-worn. First graduation: <b>commands with state</b> — a bot that remembers "
     "what a user did last time (their city, their plan) needs a database, even a "
     "single-file one. Second: <b>inline mode</b> — your bot answering inside any chat "
     "as @yourbot query — needs BotFather's <code>/setinline</code> plus a handler. "
     "Third: <b>web apps</b> — BotFather's <code>/newapp</code> wraps a website as a "
     "Mini App opened from the bot's menu button. The pattern through all three: the "
     "BotFather side is five minutes; the logic side is real programming. Most useful "
     "bots die at graduation one, not because Telegram is hard but because the author "
     "underestimated the boring part — persistence. Budget for it.</p>")

_sec('automate-telegram-channel-workflow', 'The automation audit: where the hours go',
     "<p>Before automating anything, spend one week logging where publishing time "
     "actually goes. The typical channel's split: writing and thinking ~60%, sourcing "
     "material ~20%, formatting and attaching media ~10%, the mechanical act of "
     "publishing ~10%. The mistake is automating in the order of annoyance rather than "
     "the order of ROI: scheduling (the easy 10%) is worth automating <i>first</i> "
     "because it costs an afternoon and pays daily — but it saves minutes. The capture "
     "pipeline and reusable templates (the 20% and the formatting 10%) save hours per "
     "month. The 60% — writing — is the only block where automation reliably <i>costs</i> "
     "you the channel, because readers subscribe to a voice. Automate the plumbing, "
     "keep the writing human, and your automation stack is complete.</p>")

_sec('automate-telegram-channel-workflow', 'No-code bridges: sheet, form, queue',
     "<p>You don't need to write code to wire the channel into your tools — the Bot API "
     "is just HTTP, which automation platforms speak natively. Three bridges cover most "
     "needs: a <b>form</b> (Google Forms, Tally) whose submissions appear as draft "
     "posts — this is how guest submissions and tip lines work; a <b>spreadsheet</b> "
     "where each row becomes a queued post with its slot and category — the poor "
     "person's content calendar, and a good one; and a <b>calendar trigger</b> that "
     "nudges the human when a slot is empty. The architecture that survives contact "
     "with reality is draft-then-queue: automation <i>prepares</i>, a human approves, "
     "the scheduler <i>publishes</i>. Direct form-to-feed pipelines eventually publish "
     "something embarrassing — the approval step is not bureaucracy, it's the "
     "insurance premium.</p>")

_sec('automate-telegram-channel-workflow', 'The failure modes (and the weekly health check)',
     "<p>Automation fails silently, which is what makes it dangerous. The classics: the "
     "RSS bridge posts the same story twice after a feed's GUID changes; a token gets "
     "regenerated in BotFather and the sender bot goes mute for a week; a timezone "
     "setting drifts after daylight saving and the \"9:00\" post lands at 10:00 for a "
     "month; a cross-poster keeps forwarding to a channel that was renamed or deleted. "
     "The countermeasure is a two-minute Friday ritual: check the queue has next "
     "week's slots filled, scan the published log for duplicates and dead-hour posts, "
     "send the bot one ping command and confirm it answers, and glance at ERR against "
     "last week. Every one of those checks has caught a real failure on real channels "
     "— and each one takes seconds before Monday's audience sees it.</p>")

# ============================================================= PLATFORM =====

_sec('telegram-algorithm-explained', '\u201cSimilar channels\u201d: the surface you can actually optimize',
     "<p>Open any large channel and the Similar Channels row under the header is "
     "Telegram's clearest recommendation product — and the one you can deliberately "
     "earn your way onto. The mechanism (observable, if not officially documented): "
     "Telegram groups channels whose subscriber bases overlap — the people who joined "
     "channel A also joined channel B — and ranks the list by that overlap and "
     "activity. The practical consequence: you get recommended <i>next to</i> channels "
     "you share subscribers with. Grow through swaps with channels in your exact niche "
     "and you appear in their Similar row; grow through giveaways in unrelated niches "
     "and you get recommended next to giveaway channels, which is audience poison. "
     "Niche purity isn't just editorial discipline — it's literally the graph you're "
     "building.</p>")

_sec('telegram-algorithm-explained', 'In-app search ranking: the fields that count',
     "<p>Telegram search matches against a short list of fields: the channel's "
     "<b>name</b>, its <b>username</b>, and — with much weaker weight — description "
     "text. Subscriber count and recent activity act as the tiebreaker, which is why "
     "head terms (\"crypto\", \"news\") are unwinnable for a new channel and long-tail "
     "terms (\"remote react jobs europe\") are wide open. The audit takes five "
     "minutes: search your niche's main term, then your specific sub-term; note who "
     "ranks and what's in their names. If the head term's results are all 50k+ "
     "channels, your name belongs to the sub-term — the one searchers can still see "
     "you in. And re-check monthly after renames: search re-ranking lags by days, "
     "which is another argument for renaming rarely.</p>")

_sec('telegram-algorithm-explained', 'Reactions, forwards and the folklore problem',
     "<p>Because Telegram has never published ranking weights, folklore fills the gap: "
     "\"react within the first hour\", \"forwards boost search\", \"posting time "
     "programs the algorithm\". Separate what's observable from what's myth. "
     "<i>Observable:</i> forwards and reactions make a post travel — forwards carry "
     "your channel name into new feeds, which is distribution; high-engagement posts "
     "correlate with more Similar Channels presence over time. <i>Myth-shaped:</i> "
     "any hack that promises to trick a ranking system nobody has reverse-engineered "
     "— reaction pods, view-boosting services, engagement rings. The services are "
     "worse than useless: inflated reaction counts with flat views are the exact "
     "signature advertisers and directories screen for. The only lever with "
     "documented, compounding effect is the boring one: posts that real people "
     "forward.</p>")

_sec('best-time-to-post-telegram', 'Timezone stacks for international audiences',
     "<p>When the audience spans continents, one prime time doesn't exist — but a stack "
     "does. First, read your geo split (TGStat shows it, or infer from language and "
     "comment times): anchor your main post to the plurality timezone. Second, for the "
     "second-largest block, don't repost the same content at its prime — <b>schedule a "
     "different angle</b>: the morning digester for Europe gets the full post at 9:00 "
     "CET; the evening scroller in the US gets the discussion angle six hours later. "
     "Same material, different framing, and you learn which framing belongs to which "
     "crowd. What not to do: post for the smallest geo at its ideal hour — a channel "
     "that is 70% Europe should never let a 15% US block dictate the schedule. The "
     "scheduler's timezone handling (set the channel's home zone once) is exactly what "
     "makes this a set-and-forget decision instead of a daily arithmetic problem.</p>")

_sec('best-time-to-post-telegram', 'Designing for the muted majority',
     "<p>The uncomfortable stat most channels discover: 50–80% of subscribers have "
     "notifications off, and they never see your timing at all — they see your "
     "<b>preview text</b> when they open Telegram for their own reasons. This reframes "
     "\"best time to post\": timing buys you the vocal minority; the first line buys "
     "everyone else. The practice: write the first line as a standalone promise (it "
     "renders as the preview under the channel name in the chat list), keep the "
     "channel pinned post current (muted readers check pins when they arrive), and use "
     "one deliberate notification-worthy post per week — the announcement, the "
     "drop, the big story — so notifications, when they do fire, carry weight instead "
     "of noise. Channels that notify daily train their audience to mute; channels that "
     "notify rarely get their pings opened like letters.</p>")

_sec('best-time-to-post-telegram', 'Weekends are a different country',
     "<p>Weekend behavior inverts by niche, and channels that treat Saturday like "
     "Tuesday leak engagement. B2B, jobs, finance and tooling channels typically see "
     "ERR drop 20–40% on Saturday–Sunday — the audience is offline, and posting your "
     "best material into the drop wastes it. Entertainment, food, local and hobby "
     "channels often see the opposite: weekend ERR holds or rises. The move in both "
     "cases is the same: <b>move your format, not just your timing</b>. B2B channels: "
     "weekends are for the weekly digest, the lighter take, the community post — "
     "scheduled Friday evening to publish without you. Entertainment channels: "
     "weekends are for the long-form piece your weekday scrollers won't read. Test it "
     "for four weekends before believing it for your channel — but stop publishing "
     "your Thursday-quality work into a Saturday you haven't measured.</p>")

_sec('telegram-privacy-for-channel-owners', 'The five-minute visibility audit',
     "<p>Open <b>Settings → Privacy and Security</b> and walk the list as a stranger "
     "would. <b>Phone number</b>: set to <i>Nobody</i> (or Contacts) — channel "
     "subscribers never need it, and \"who can find me by my number\" should be "
     "<i>My contacts</i>. <b>Last seen &amp; online</b>: set to Contacts or Nobody; "
     "the precision matters — \"last seen recently\" is fine, an exact timestamp to "
     "strangers is a routine. <b>Profile photos</b>: Contacts-only if your face on the "
     "channel persona is a decision you haven't made. <b>Calls</b>: Nobody or Contacts "
     "— channel fame invites voice spam. <b>Forwarded messages</b>: choosing "
     "<i>Nobody</i> hides your account when posts forwarded from your personal chat "
     "spread. Finish with <b>Settings → Devices</b>: terminate any session you don't "
     "recognize, and turn on two-step verification with a real recovery email — the "
     "account <i>is</i> the channel.</p>")

_sec('telegram-privacy-for-channel-owners', 'Posting as the channel, not as yourself',
     "<p>Telegram gives owners two identities in one place, and mixing them is the "
     "common leak. In the discussion group of your channel, any admin can post "
     "<b>as the channel</b> — the avatar, the name, the brand — and that should be the "
     "default for every official reply. The moment you answer a comment from your "
     "personal account, every member of that group can tap through to your private "
     "profile, your phone-number-adjacent details, and everything else you haven't "
     "audited. Same rule for admin visibility: group admins can be made anonymous "
     "(hidden behind the group identity), so moderators who don't want their personal "
     "accounts tied to moderation decisions stay anonymous. The channel identity is "
     "the product; the human identities are staff. Keep the layers in that order, and "
     "review them every time you add an admin.</p>")

_sec('telegram-privacy-for-channel-owners', 'The persona account, built deliberately',
     "<p>Channels run at scale usually deserve a dedicated owner account: a separate "
     "Telegram account with its own username that exists for the channel, the bots and "
     "the admin duties. The discipline that makes it safe: a username that doesn't "
     "reuse your personal handle (cross-platform handle search is the first doxxing "
     "move), a profile photo and bio consistent with the channel rather than the "
     "person, and personal accounts never logged into it. Telegram's multi-account "
     "support makes switching between them a two-tap affair — the friction argument "
     "died years ago. Two things stay true regardless of setup: whoever holds the "
     "account holds the channel (so two-step verification and a recovery email are "
     "non-negotiable), and bots you add see what their rights allow — the audit from "
     "the section above applies to the persona account with even more reason.</p>")

_sec('telegram-seo-and-discovery', 'Google indexes your channel whether you like it or not',
     "<p>Public channels have web-preview pages at <code>t.me/s/channelname</code> — "
     "plain, crawlable HTML — and Google indexes them. This is the quiet third rail of "
     "Telegram discovery: posts on a 2,000-subscriber channel routinely outrank "
     "dedicated blog pages for long-tail queries, because the channel page accumulates "
     "freshness and internal links with every post. The practical playbook: make sure "
     "the channel name and description contain the terms searchers would type; write "
     "posts whose first lines stand alone as snippets (the preview page shows them as "
     "text); and check <code>site:t.me/s/yourchannel</code> in Google after a few "
     "weeks to see what's indexed. Private channels and deleted posts drop out of the "
     "preview — which is also the lever if you ever need something de-indexed. For a "
     "creator, this reframes the channel: it's not just a feed, it's a fast-indexing "
     "publication.</p>")

_sec('telegram-seo-and-discovery', 'Directories: ten minutes that keep paying',
     "<p>The catalog rail costs one hour a year and pays a trickle forever. Submit the "
     "channel to TGStat's catalog (the submission also makes your stats verifiable to "
     "advertisers — the real reason to bother), Telemetr's base, and the general "
     "Telegram directories and catalogs that still accept submissions; then find the "
     "two or three <i>niche-specific</i> catalogs in your field — they send fewer but "
     "far better-fitting subscribers. Expectations: a listing might bring 5–30 "
     "subscribers a month, mostly long-tail searchers. That's not a growth strategy; "
     "it's infrastructure — the point is that someone searching a catalog for your "
     "niche in six months finds you, and that advertisers cross-checking your numbers "
     "find a public, consistent record. Do it once, note the date, move on to the "
     "rails that actually compound.</p>")

# ============================================================= CONTENT ======

_sec('schedule-posts-with-photos-and-video', 'Album captions: what the composer can\u2019t do',
     "<p>The native composer applies one caption to a whole album — it shows under the "
     "first photo, and that's the only choice you get. Bots have more rights than the "
     "app here: the Bot API's album methods accept a <b>separate caption per photo</b>, "
     "which unlocks the gallery formats native posting can't produce — a ten-photo "
     "album where each image carries its own line of commentary, step-by-step "
     "tutorials where every photo has its instruction attached, or a before/after set "
     "labeled in place. This is one of the quiet reasons channel owners end up using a "
     "scheduler even when they're at their desk: the composer is a subset of what the "
     "platform can do. If you schedule albums through a bot, check that it preserves "
     "per-photo captions on preview — not every tool exposes them, and the ones that "
     "do change what you can publish.</p>")

_sec('schedule-posts-with-photos-and-video', 'The 10-item ceiling and how to work around it',
     "<p>Albums cap at ten items — a hard limit in both the app and the API — and mixed "
     "albums (photos and videos together) are allowed, which matters for event "
     "recaps. Beyond ten items, the working patterns: <b>split into parts</b> and say "
     "so honestly (\"part 2 below\" — albums post in sequence, so two albums two "
     "minutes apart read as one gallery); <b>promote the overflow to a document</b> "
     "(a ZIP of the full set as one file after the album — photographers do this for "
     "clients); or <b>choose the ten best</b>, which is usually the editorially "
     "correct answer anyway. GIFs complicate albums: Telegram converts them to "
     "looping MP4s, and inside an album they behave like silent videos — fine, but "
     "check the preview, because a GIF that autoplayed as a GIF in the draft may "
     "appear as a static-video card in the album on some clients.</p>")

_sec('schedule-posts-with-photos-and-video', 'Scheduling media: the three checks before publish',
     "<p>Media posts fail differently from text posts, so the pre-publish pass has "
     "three media-specific checks. <b>Preview the album order</b> — some pipelines "
     "re-sort by file name or upload order, and a recipe whose steps arrive shuffled "
     "is worse than no post; drag or rename until the queue shows the right sequence. "
     "<b>Check the silent-send choice</b> — scheduled night posts and time-zone "
     "crossers should usually go out without notification (bots can send silently), "
     "reserving the ping for content that earns it. <b>Confirm the media survived the "
     "pipeline</b> — compression, format conversion and caption stripping happen at "
     "transfer, not at compose; the preview step in a scheduler exists precisely "
     "because a 2 a.m. album that posted without its captions can't be fixed at 2 a.m. "
     "by anyone asleep. Thirty seconds of preview is cheaper than any apology "
     "post.</p>")

try:
    import blog_extras5  # noqa: F401,E402
except ImportError:
    pass
