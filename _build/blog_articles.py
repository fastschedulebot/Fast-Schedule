# -*- coding: utf-8 -*-
"""Blog articles for the Fast Scheduler blog — general Telegram knowledge,
not support docs.

Editorial rules for every article:
  * Answers the search intent behind a real Telegram query in full.
  * Names real, widely known tools (ManyBot, ControllerBot, Combot, Rose,
    Shieldy, BotFather, CryptoBot, TGStat…) as plain text — no links, no
    affiliate sugar. A guide that never names alternatives reads as an ad
    and helps nobody.
  * Mentions Fast Scheduler only where a normal expert would name the tool
    they actually use, in the same plain-text register.
"""

BLOG_ARTICLES = []

def _a(i, **kw):
    kw['id'] = i
    BLOG_ARTICLES.append(kw)

# ============================================================ GROWTH & START ==
_a('how-to-create-telegram-channel-2026',
   category='growth',
   title='How to Create a Telegram Channel in 2026: A Step-by-Step Guide',
   description='A current, honest walkthrough of creating a Telegram channel in 2026 — settings most guides skip, the first five posts that matter, and how to set up a publishing rhythm from day one.',
   date='2026-09-26',
   content=(
       "<p>Telegram passed the billion-user mark a while ago, and the channel format is still the "
       "best deal in social media: no algorithm deciding who sees your posts, no boosted-content "
       "rules, subscribers get everything you publish. That’s also why the first hour of setup "
       "matters — most of it is one-way. Here is the full walkthrough, including the settings "
       "nobody checks until it’s too late.</p>"

       "<h3>Creating the channel (60 seconds)</h3>"
       "<ul>"
       "<li>1. In Telegram, tap the <b>pencil / compose icon</b> → <b>New Channel</b>.</li>"
       "<li>2. Give it a name and a one-line description with the promise, not the topic: "
       "“Daily remote-job picks” beats “Jobs channel”.</li>"
       "<li>3. Add a 640×640 logo — a bold letter or symbol, not a photo (it renders at 20 px in "
       "most chats).</li>"
       "<li>4. Choose <b>Public</b> if you plan to grow; pick a short @link you can say out loud. "
       "Private works for communities, courses and inner circles.</li>"
       "</ul>"

       "<h3>The settings most guides skip</h3>"
       "<ul>"
       "<li><b>Sign messages with channel name</b> — Settings → Channel → toggle it on. Readers "
       "in forwards see the channel name on every message; it’s free distribution.</li>"
       "<li><b>Discussion group</b> — attach one from the same screen. Comments make the "
       "difference between a billboard and a community, and Telegram shows commented posts to "
       "group members.</li>"
       "<li><b>Slow mode</b> — for the discussion group only. Comments move fast; the channel "
       "itself never needs slow mode.</li>"
       "<li><b>Administrators</b> — add only people who need posting rights. Every extra admin is "
       "an anonymous-posting identity your readers can’t tell apart.</li>"
       "</ul>"

       "<h3>The first five posts that make or break a channel</h3>"
       "<p>People who find the channel scroll its last ten messages before deciding to subscribe. "
       "Before you invite anyone, publish:</p>"
       "<ul>"
       "<li>1. A <b>pin intro</b>: what the channel is, posting rhythm, who’s behind it.</li>"
       "<li>2. Your single best piece of content — the one you’d show a stranger.</li>"
       "<li>3. A post that proves <b>consistency</b> (“Every weekday at 9:00 — the digest”).</li>"
       "<li>4. Something with <b>comments</b>: a poll or question. Dead channels look dead.</li>"
       "<li>5. A second genuinely valuable post, so the “Recent” wall doesn’t look like a lobby.</li>"
       "</ul>"

       "<h3>Set the rhythm before the first subscriber arrives</h3>"
       "<p>The mistake isn’t choosing a bad niche — it’s posting daily for two weeks, burning out, "
       "and going dark. Decide your realistic cadence first, then <b>separate writing from "
       "publishing</b>: draft in one sitting, let the posts go out on schedule. Telegram itself "
       "only offers short-horizon scheduled sending in the composer, so for a real queue you’ll "
       "want one of the scheduling bots — ManyBot and ControllerBot are the long-established "
       "generalists. Pick any of them; the point is the rhythm, not the brand.</p>"

       "<h3>Then, and only then, growth</h3>"
       "<p>With rhythm in place: cross-post in relevant discussion groups (value first, links "
       "rarely), add the channel link to every bio you own, and consider a modest ad buy in "
       "comparable channels. Growth amplifies what exists — an empty or chaotic channel amplifies "
       "into a churn problem.</p>"),

   faq=[
       {'q': 'Can I change a public channel link later?',
        'a': 'Yes — the public @link can be edited anytime in channel settings. Changing it breaks old t.me links, so pick a name you can live with, but don’t fear mistakes.',},
       {'q': 'How much does a Telegram channel cost?',
        'a': 'Nothing. Creating and running a channel is free; costs appear only if you buy ads, hire editors, or pay for premium tools.',},
       {'q': 'Public or private channel?',
        'a': 'Public for anything you want discovered and shared; private for paid or invite-only communities. Public channels are searchable in Telegram and indexed by search engines.',},
       {'q': 'How many admins should a new channel have?',
        'a': 'One or two. Fewer identities posting keeps the channel voice consistent — and every admin needs the same minimal permission set, not all rights.',},
   ])

_a('reach-1000-subscribers-telegram',
   category='growth',
   title='How to Get Your First 1,000 Telegram Subscribers (Without Paid Ads)',
   description='A practical playbook for the hardest part of Telegram growth: the first 1,000 subscribers. Seeding loops, swap etiquette, comment tactics, and retention tricks that actually compound.',
   date='2026-09-26',
   content=(
       "<p>The first 1,000 subscribers are the hardest — nobody shares you yet because nobody’s "
       "seen you. Paid ads would shortcut it, but the channels built without them keep their "
       "subscribers longer. Here’s the playbook.</p>"

       "<h3>Week 0: build the landing surface</h3>"
       "<p>Before any promotion: pinned intro, 10+ posts of proven content, attached comment "
       "group, message signature with the channel name. Someone who stumbles in must be able to "
       "understand the promise in five seconds.</p>"

       "<h3>The seeding loop (your first 100–300)</h3>"
       "<ul>"
       "<li>1. List every place your future readers already hang out: WhatsApp groups, Discord "
       "servers, subreddits, Facebook groups, your own chats.</li>"
       "<li>2. Participate for real. Answer questions for a week before mentioning the channel — "
       "self-promo without reputation gets you banned, and it should.</li>"
       "<li>3. Mention the channel only when the answer genuinely needs it: “I keep a running "
       "list of these in my channel — here’s this week’s.”</li>"
       "</ul>"

       "<h3>Swaps: the engine of Telegram growth</h3>"
       "<p>Channel cross-promotion (“swaps”) powers most of Telegram’s ecosystem. The unwritten "
       "rules:</p>"
       "<ul>"
       "<li>Match <b>engagement, not subscriber count</b>. A 2K channel with 400 views/post beats "
       "a 10K zombie.</li>"
       "<li>Before agreeing to anything, look the partner up on <b>TGStat</b> or <b>Telemetr</b> "
       "— the two standard channel-analytics services. They show real view dynamics and "
       "subscriber churn, which nobody’s screenshot ever does.</li>"
       "<li>Offer comparable slots: your post in their channel, theirs in yours, same week.</li>"
       "<li>Write the swap post to <b>save</b>, not to sell: a checklist, a link vault, a "
       "mini-case. View rates on value posts run 2–3× higher.</li>"
       "</ul>"

       "<h3>Giveaways — with the safety on</h3>"
       "<p>Prize draws spike subscriptions cheaply, but Telegram is full of “giveaway hunters” "
       "who leave the day the winner is announced. If you run one, use a giveaway bot with "
       "entry-verification (subscribe-to-enter checks, random draws, anti-cheat) — several "
       "established ones exist; pick by how well they filter, not by how loud their ads are. "
       "And measure the channel a month later, not the spike.</p>"

       "<h3>Comments are the hidden growth channel</h3>"
       "<p>Be genuinely helpful in the comment threads of big adjacent channels. People click "
       "profiles; the profile links to the channel. It’s slower than a swap but compounds "
       "forever and costs nothing.</p>"

       "<h3>Retention: the metric that decides if 1,000 is possible</h3>"
       "<p>Growth without retention is a leaky bucket. Two things cut Telegram churn hard:</p>"
       "<ul>"
       "<li><b>Rhythm.</b> Subscribers who know when you post don’t leave between posts. Set a "
       "cadence and keep it — any of the scheduling bots (ManyBot, ControllerBot, Fast "
       "Scheduler) will hold the cadence through your bad weeks; that’s what they’re for.</li>"
       "<li><b>First-hour engagement.</b> Post when your audience is awake, ask one question per "
       "discussion post, and reply to comments within the hour. Comments breed comments.</li>"
       "</ul>"

       "<h3>A realistic timeline</h3>"
       "<ul>"
       "<li>Weeks 1–4: seeding + comments — first 100–300.</li>"
       "<li>Months 2–3: swaps at your size class — 300–800.</li>"
       "<li>Months 4–6: bigger swaps, content that gets shared — 1,000.</li>"
       "</ul>"
       "<p>Slower than ads, but the people who arrive stay.</p>"),

   faq=[
       {'q': 'How fast should a healthy channel grow?',
        'a': 'For organic growth, 2–5% net subscriber growth per month is solid for a niche channel. Spikes from swaps are normal; the number to watch is the churn between spikes.',},
       {'q': 'Are Telegram subscriber services worth it?',
        'a': 'No. Bot subscribers never open posts, destroy your view ratio (which swaps and advertisers check), and Telegram purges them regularly. Organic seeding compounds; purchased numbers decay.',},
       {'q': 'What’s a good view-to-subscriber ratio?',
        'a': '20–40% is healthy for most channels. Below 15% usually means stale audience — a signal for swap partners and advertisers alike. TGStat and Telemetr both show this at a glance for any public channel.',},
       {'q': 'How long does reaching 1,000 subscribers take without ads?',
        'a': 'Typically 3–6 months of consistent posting plus weekly seeding and swaps. Channels that fail usually quit at week six — the plateau is psychological, not structural.',},
   ])

_a('telegram-bots-for-channel-owners',
   category='tools',
   title='Top Telegram Bots Every Channel Owner Should Know in 2026',
   description='The actual bot stack behind successful Telegram channels — named: BotFather, ManyBot, ControllerBot, Combot, Rose, Shieldy, FeedBridge-style RSS bots, TGStat, CryptoBot — and what each is for.',
   date='2026-09-26',
   content=(
       "<p>Channels run on a small stack of bots. Here are the ones that actually matter, by "
       "category — including the names you’ll hear in every serious channel-owner chat.</p>"

       "<h3>1. The bot that creates bots: @BotFather</h3>"
       "<p>Telegram’s official bot factory. Every custom tool on this list starts here: BotFather "
       "mints your own bot (name, username, token), which you then connect to services. Two "
       "things people miss: you can give your bot a channel-avatar persona via BotFather’s "
       "pictures, and the token it issues is a full password — treat it like one.</p>"

       "<h3>2. Scheduling &amp; publishing bots</h3>"
       "<p>The foundation. Telegram’s built-in scheduling tops out at short horizons; a "
       "scheduling bot lets you batch-create posts and publish on time, every time.</p>"
       "<ul>"
       "<li><a href=\"https://t.me/ManyBot\" target=\"_blank\" rel=\"noopener\"><b>ManyBot</b></a> — "
       "the veteran. Free, dead simple, does scheduled posts and menus. Fine for a single "
       "channel with modest needs.</li>"
       "<li><a href=\"https://t.me/ControllerBot\" target=\"_blank\" rel=\"noopener\"><b>ControllerBot</b></a> — "
       "a channel-owner favorite for years: scheduling, view/engagement reports, delayed "
       "posts, multi-channel from one chat.</li>"
       "<li><b>Fast Scheduler</b> — batch scheduling (send several date/message pairs in one "
       "message), recurring slots, publishing through your own bot, per-post stats.</li>"
       "</ul>"
       "<p>Any of the three beats manual posting; they differ in limits and interface, not in "
       "the core promise.</p>"

       "<h3>3. Analytics: TGStat, Telemetr, Combot</h3>"
       "<ul>"
       "<li><b>TGStat</b> — the reference point for channel stats: views, ERR (engagement rate "
       "per reach), subscriber dynamics, citation index. Swap partners will quote it; you "
       "should too.</li>"
       "<li><b>Telemetr</b> — the other major analytics service, strong on ad-placement "
       "analytics and channel comparisons.</li>"
       "<li><b>Combot</b> — the standard for <i>groups</i>: activity rankings, member stats, "
       "moderation logs. If your channel has a linked discussion group, Combot is the "
       "default choice there.</li>"
       "</ul>"

       "<h3>4. Moderation for the discussion group</h3>"
       "<ul>"
       "<li><b>Combot</b> (again) — moderation plus analytics in one.</li>"
       "<li><b>Rose</b> — the power-user moderation bot: locks, filters, approval modes, "
       "captcha. Deep config, huge install base.</li>"
       "<li><b>Shieldy</b> — the classic anti-spam gatekeeper: makes newcomers complete a "
       "captcha and deletes flood/links. Set-and-forget.</li>"
       "<li><b>GroupHelp</b> and <b>MissRose-style alternatives</b> cover similar ground; "
       "differences are in interface taste, not capability.</li>"
       "</ul>"

       "<h3>5. Comments &amp; engagement helpers</h3>"
       "<p>Quiz and giveaway bots run polls, drawings and entry-verification contests in the "
       "discussion group — several established brands compete here. Engagement feeds Telegram’s "
       "recommendation surfaces, so a weekly quiz pays for its setup time. For plain comment "
       "hygiene, Shieldy + Combot already cover 90% of needs.</p>"

       "<h3>6. Payments &amp; monetization bots</h3>"
       "<ul>"
       "<li><b>CryptoBot</b> — Telegram’s wallet bot; the standard rail for peer payments, "
       "tip jars and paying for services in Telegram.</li>"
       "<li><b>Telegram Stars</b> — native in-app payments for digital goods and channel "
       "subscriptions; no separate bot needed, Telegram handles it in the interface.</li>"
       "</ul>"

       "<h3>7. Utility bots everyone forgets</h3>"
       "<ul>"
       "<li><b>RSS-to-channel bridges</b> (FeedBridge-style bots) — auto-post news feeds. "
       "Curate or your channel becomes a feed dump.</li>"
       "<li><b>Webpage-preview and link tools</b> — trim and prettify links before posting.</li>"
       "<li><b>Backup/export</b> — a full export of your scheduled content. Most schedulers "
       "include one; if yours doesn’t, that’s a real gap, because a channel’s asset is its "
       "content pipeline.</li>"
       "</ul>"

       "<h3>The minimal stack, by stage</h3>"
       "<ul>"
       "<li><b>0–1K:</b> a scheduler (ManyBot / ControllerBot / Fast Scheduler) + Shieldy in "
       "the discussion group. Discipline beats tooling.</li>"
       "<li><b>1K–10K:</b> add Combot or Rose for moderation, TGStat for benchmarking.</li>"
       "<li><b>10K+:</b> all of it, plus CryptoBot/Stars when you monetize.</li>"
       "</ul>"),

   faq=[
       {'q': 'Do bots need admin rights in my channel?',
        'a': 'A publishing bot needs Post Messages (and ideally Edit Messages) rights. Nothing else. Never grant Delete Messages to a bot you don’t fully trust.',},
       {'q': 'Are Telegram bots free?',
        'a': 'The good ones are freemium — ManyBot’s core is free, the bigger schedulers run a single channel on free plans, and Combot, TGStat and Rose charge for depth. A new channel can run entirely free.',},
       {'q': 'Can a bot post from my own bot’s name?',
        'a': 'Yes — create a bot via @BotFather, add it as a channel admin, and connect its token to a scheduler that supports “sender bots” (ControllerBot and Fast Scheduler both do). Your brand signs every post.',},
       {'q': 'Is it safe to give a scheduler my bot token?',
        'a': 'The token gives full control of that bot, so treat it like a password. Reputable schedulers store it encrypted and let you revoke/rotate anytime via BotFather. Never paste tokens into unknown websites.',},
   ])

_a('best-time-to-post-telegram',
   category='growth',
   title='The Best Time to Post on Telegram: What Actually Works in 2026',
   description='Real posting windows by audience type, why local time beats global advice, how to run a one-week A/B test with scheduled posts, and the one metric that decides the winner.',
   date='2026-09-26',
   content=(
       "<p>“Post at 9 AM” advice is recycled guesswork — it ignores the only variable that "
       "matters: <b>when your subscribers are awake</b>. Here’s the evidence-based version, plus "
       "a test you can run this week.</p>"

       "<h3>Windows that generally work (in your audience’s local time)</h3>"
       "<ul>"
       "<li><b>8:00–10:00</b> — commute scan. News, digests, short lists.</li>"
       "<li><b>12:30–14:00</b> — lunch dip. Light, skimmable, single-idea posts.</li>"
       "<li><b>19:00–22:00</b> — prime time. The strongest window for most channels; long-form "
       "and media belong here.</li>"
       "</ul>"
       "<p>If your audience spans timezones, anchor to your largest cluster’s evening and let the "
       "rest catch up in the morning. A scheduler with a proper timezone setting converts for "
       "you — one reason “I’ll just post manually” quietly fails for international channels.</p>"

       "<h3>The little-known part: spacing beats bursts</h3>"
       "<p>Notification fatigue is real. Three posts at 20:00, 20:05 and 20:10 get treated as one "
       "annoyance; the same three posts at 9:00 / 13:00 / 20:00 get three separate reads. Channels "
       "that “dump the queue at midnight” train subscribers to mute them. If you’ve batch-written "
       "a week of content, schedule the <b>spacing</b>, not just the publishing.</p>"

       "<h3>Consistency beats cleverness</h3>"
       "<p>Subscribers learn your rhythm. A channel that posts daily at 9:00 trains people to "
       "show up at 9:00 — visible in view-rate stability within two weeks. This is the strongest "
       "argument for scheduled publishing over manual posting: the schedule becomes part of the "
       "product. Recurring “every weekday at 9:00” rules are a one-command setup in every major "
       "scheduler — ControllerBot calls them delayed/auto posts, Fast Scheduler calls them "
       "recurring messages; the name doesn’t matter, the daily pulse does.</p>"

       "<h3>How to test slots properly in one week</h3>"
       "<ul>"
       "<li>1. Pick two candidate slots, e.g. 9:00 vs 20:00.</li>"
       "<li>2. Alternate similar-strength content between them for 7–10 days.</li>"
       "<li>3. Compare <b>views in the first hour</b>, not totals — that’s when your regulars "
       "arrive.</li>"
       "<li>4. Keep the winner as a recurring rule; re-test quarterly. Audiences drift with "
       "seasons and habits.</li>"
       "</ul>"
       "<p>For benchmarks beyond your own channel, TGStat’s channel pages show when comparable "
       "channels publish and how their views respond — useful for calibrating the test before "
       "you run it.</p>"

       "<h3>How many posts per day is healthy?</h3>"
       "<p>2–4 for most content channels. Beyond that, watch unsubscribes — the metric that "
       "punishes oversharing fastest. Quality ceiling beats quantity ceiling on Telegram faster "
       "than on any other platform.</p>"),

   faq=[
       {'q': 'What is the single best time to post on Telegram?',
        'a': '19:00–22:00 in your audience’s dominant local time is the strongest general window. But per-channel testing matters more than any global average — first-hour views are the honest signal.',},
       {'q': 'Does Telegram show what time a post was published?',
        'a': 'Every message carries its timestamp, and channel views are tallied continuously, so first-hour performance is measurable. Scheduler stats screens (ControllerBot, Fast Scheduler and similar) chart view dynamics per post.',},
       {'q': 'How do I schedule posts for different time zones?',
        'a': 'Set the channel’s timezone in your scheduler and write times in that zone, or use a scheduler that publishes per-subscriber local time. Scheduling bots convert your chosen time through the channel timezone automatically.',},
       {'q': 'Is it bad to post multiple times a day?',
        'a': 'No, if spaced hours apart and each post earns its slot. Three spaced posts outperform six stacked ones; stacking is what triggers mutes and unsubscribes.',},
   ])

_a('telegram-channel-ideas',
   category='growth',
   title='50 Telegram Channel Ideas That Actually Keep Subscribers',
   description='Not just ideas — the niches with proven retention on Telegram, how to pick a lane you can sustain, and the positioning formula that separates growing channels from ghost towns.',
   date='2026-09-26',
   content=(
       "<p>Everyone lists channel ideas. Nobody tells you which ones people actually <b>stay</b> "
       "in. Retention — not novelty — decides whether a channel lives, because Telegram has no "
       "algorithm dragging readers back. Here are ideas grouped by the reason they retain.</p>"

       "<h3>Channels that save time (highest retention class)</h3>"
       "<ul>"
       "<li>Curated job boards for one specific role or city</li>"
       "<li>Daily deal/error-fare alerts for a niche (flights, gadgets, books)</li>"
       "<li>“One useful thing” — a tool, article or trick per day</li>"
       "<li>Digests of one industry’s news, filtered to what matters</li>"
       "</ul>"

       "<h3>Channels that teach (engagement class)</h3>"
       "<ul>"
       "<li>Micro-lessons: one concept per post, a course in a feed</li>"
       "<li>Language learning with daily vocabulary drops</li>"
       "<li>Build-in-public diaries: revenue, mistakes, decisions</li>"
       "<li>Exam-prep channels with daily questions</li>"
       "</ul>"

       "<h3>Channels that entertain (shareability class)</h3>"
       "<ul>"
       "<li>Hyperlocal memes — a city, a university, a profession</li>"
       "<li>Theme pages: mid-century design, brutalist buildings, vintage maps</li>"
       "<li>Daily puzzles with next-day answers (comments do the work)</li>"
       "</ul>"

       "<h3>Channels that connect (community class)</h3>"
       "<ul>"
       "<li>Local events and civic notices for a district or small city</li>"
       "<li>Parent/family logistics: school closures, kids’ activities</li>"
       "<li>Niche professional communities with an attached discussion group</li>"
       "</ul>"

       "<h3>How to pick your lane (the honest test)</h3>"
       "<p>Ask: can I produce value for this topic <b>daily for a year</b>, mostly from material "
       "I already read anyway? The niche that survives that question is yours. Enthusiasm for a "
       "topic you’d consume anyway is the only sustainable fuel.</p>"

       "<h3>Study the niche before entering it</h3>"
       "<p>Before committing, spend an evening on TGStat’s catalog or Telemetr’s channel "
       "directories: search your topic, sort by engagement rate rather than size, and read the "
       "top three. You’ll learn the posting rhythm that works, the formats subscribers reward, "
       "and — crucially — the gap nobody fills. Entering a niche with data beats entering it "
       "with enthusiasm alone.</p>"

       "<h3>The positioning formula</h3>"
       "<p><b>[Specific audience] + [narrow promise] + [rhythm]</b>. “Freelance designers in "
       "Europe: three briefs worth quoting daily, weekdays at 9” — that description alone "
       "converts three times better than “Design channel”. Put the rhythm in the pinned intro "
       "and honor it — an unfailing schedule is the quiet moat of every long-lived channel, and "
       "it’s cheap to keep with any scheduling bot doing the remembering (ManyBot, "
       "ControllerBot, Fast Scheduler — the free tiers all cover a single channel).</p>"),

   faq=[
       {'q': 'What type of Telegram channel grows fastest?',
        'a': 'Deal-alert and curated-list channels in high-intent niches (jobs, discounts, tools) grow fastest because sharing is built into the content. But growth ≠ retention; teaching channels keep subscribers longest.',},
       {'q': 'Can a Telegram channel make money?',
        'a': 'Yes — via ads from other channel owners, Telegram Stars paid posts, affiliate links, or selling your own product. Realistic earnings start after ~1–5K engaged subscribers with a consistent view ratio.',},
       {'q': 'Which channels have the worst retention?',
        'a': 'Aggregation-only feeds (auto-RSS dumps) and news channels without a distinct voice — subscribers replace them the moment a similar channel appears. Personality and curation are the moat.',},
       {'q': 'How often should a new channel post?',
        'a': 'Whatever cadence you can sustain at your worst week, not your best. One post daily on schedule beats five posts today and silence next week.',},
   ])

_a('telegram-post-formatting-guide',
   category='content',
   title='How to Format Telegram Posts Like a Professional Editor',
   description='Telegram formatting that lifts view rates: bold discipline, emoji as section markers, captions that don’t truncate, link previews, and the little-known media-caption limits.',
   date='2026-09-26',
   content=(
       "<p>Telegram gives you typography most networks would envy — and most channels squander "
       "it. Formatting is a retention tool: the same content, formatted well, measurably holds "
       "more readers. The rules below come from watching what survives in channels with 30%+ "
       "view rates.</p>"

       "<h3>Bold is a headline, not an emphasis spray</h3>"
       "<p>Bold works as a <b>scanning layer</b>: a reader should reconstruct the post’s argument "
       "from the bolded lines alone. One bolded takeaway per paragraph — not five words per "
       "sentence. Channels that bold half of every post train readers that bold means nothing.</p>"

       "<h3>Emoji are section markers, not confetti</h3>"
       "<ul>"
       "<li>One emoji per section header — 1️⃣ 📌 ✅ — creates a visual rail down long posts.</li>"
       "<li>Never mid-sentence. Never three in a row. The professional look is <i>restraint</i>: "
       "readers associate emoji-stacks with spam.</li>"
       "</ul>"

       "<h3>Captions have their own rules (the part everyone trips on)</h3>"
       "<p>Media captions are limited to <b>1024 characters</b> — text posts allow 4096 — and the "
       "caption is what shows in the push preview. So: front-load the hook in the first 60 "
       "characters, put links and details in the first line, or move long text below the media as "
       "a follow-up message. Telegram’s “keep media and caption together” behavior means a long "
       "caption can force awkward layout — for anything over ~3 lines, publish media + a "
       "separate text post a minute later.</p>"

       "<h3>Link previews: crop them or kill them</h3>"
       "<p>A bare URL auto-generates a preview card. Two pro moves:</p>"
       "<ul>"
       "<li>Disable the preview for chat-style messages and groups of links — the wall of cards "
       "reads as forwarded junk.</li>"
       "<li>Or <b>customize</b> the preview — Telegram’s composer lets you edit the shown "
       "title/description on desktop, and most scheduling bots expose preview fields too. A "
       "rewritten preview gets more clicks than the site’s default meta description.</li>"
       "</ul>"

       "<h3>Formatting that only bots expose cleanly</h3>"
       "<p>The clients hide a few tricks: monospace for prices, dates and code; underline+bold "
       "combos; spoiler formatting (tap-to-reveal) that doubles as a curiosity hook (“the answer "
       "is behind the spoiler — guess first”). The in-app composer menus cover the basics, but "
       "keeping formatting intact through edits and scheduling is where dedicated tools earn "
       "their keep — ControllerBot and Fast Scheduler both preview the final formatting before "
       "anything goes live, which the native scheduler doesn’t.</p>"

       "<h3>A pre-publish checklist</h3>"
       "<ul>"
       "<li>Can the argument be reconstructed from bolded lines alone?</li>"
       "<li>Is the first 60 characters of every caption a hook?</li>"
       "<li>One emoji per header, zero mid-sentence?</li>"
       "<li>Every link has an intentional preview state?</li>"
       "</ul>"),

   faq=[
       {'q': 'What is the character limit for Telegram posts?',
        'a': '4096 characters for text messages and 1024 characters for media captions. Long-form content should be a text post, not a giant caption.',},
       {'q': 'How do I add bold or code formatting to a Telegram post?',
        'a': 'Use the built-in composer menu on mobile/desktop, or Telegram’s markdown-style shortcuts. Scheduling bots accept the same formatting entities and show a preview before the post goes out.',},
       {'q': 'What is a spoiler in Telegram formatting?',
        'a': 'A tap-to-reveal region. Used well it’s an engagement hook for answers, reveals and punchlines; used too often it’s annoying.',},
       {'q': 'Why do my links show a broken preview?',
        'a': 'The target site lacks proper Open Graph tags or blocks crawlers. Either rewrite/customize the preview (desktop composer or a bot that supports it), or disable preview rendering for that message.',},
   ])

_a('grow-telegram-channel-from-zero',
   category='growth',
   title='Telegram Channel Growth in 2026: A 90-Day Plan from Zero',
   description='A week-by-week 90-day plan to grow a Telegram channel from zero: content phases, first swaps, metrics to track weekly, and the retention traps that stall most channels.',
   date='2026-09-26',
   content=(
       "<p>Most growth advice is a list of tactics with no timeline. Here’s the sequence that "
       "actually compounds, day by day, for 90 days.</p>"

       "<h3>Days 1–14: build before you broadcast</h3>"
       "<ul>"
       "<li>Ship 10–15 posts of “greatest hits” quality before inviting anyone.</li>"
       "<li>Pin the intro; open the discussion group; set message signatures.</li>"
       "<li>Choose a fixed daily time slot and put it on a schedule. Non-negotiable: the "
       "<b>pipeline</b> is the product. Write in batches, publish on autopilot.</li>"
       "</ul>"

       "<h3>Days 15–30: the seeding sprint</h3>"
       "<ul>"
       "<li>Do the seeding loop daily: 15 minutes in communities where your readers live, value "
       "first, channel mentioned only when it’s genuinely the answer.</li>"
       "<li>Track <b>subscriber source</b> anecdotally — ask new people where they came from; "
       "double down on what works.</li>"
       "</ul>"

       "<h3>Days 31–60: swaps and systems</h3>"
       "<ul>"
       "<li>At ~300 subs with a 20%+ view ratio, start swaps with same-size channels. Find "
       "partners through owner chats and catalog sites; vet every candidate on TGStat or "
       "Telemetr before offering anything.</li>"
       "<li>One swap post per week, written to <b>save</b> (checklists, collections), not to "
       "sell.</li>"
       "<li>Start a simple weekly review: which posts got the most first-hour views? Make more "
       "like those. (Your scheduler’s stats screen — ControllerBot’s reports or Fast Scheduler’s "
       "per-post dynamics — already answers this.)</li>"
       "</ul>"

       "<h3>Days 61–90: compounding</h3>"
       "<ul>"
       "<li>Repackage your best posts into shareable assets: mega-guides, link vaults — the "
       "posts people forward.</li>"
       "<li>Pitch slightly bigger channels for swaps; your ratio is proof you deliver.</li>"
       "<li>Consider a small paid boost in a highly-matched channel to test paid acquisition — "
       "only now, when retention data exists. Ad marketplaces like Telega.in list sellable "
       "slots; cross-check every seller’s TGStat before paying.</li>"
       "</ul>"

       "<h3>Metrics that matter weekly</h3>"
       "<ul>"
       "<li><b>Net subscribers</b> (joins − leaves) — the honest number.</li>"
       "<li><b>First-hour views</b> — the engagement signal that predicts everything.</li>"
       "<li><b>View-to-sub ratio</b> — your currency for swaps and ads.</li>"
       "</ul>"

       "<h3>The three traps that stall 80% of channels</h3>"
       "<ul>"
       "<li><b>The burnout cliff:</b> manual daily posting collapses around week 6. Batch + "
       "schedule is the fix, not “more discipline”.</li>"
       "<li><b>The vanity loop:</b> chasing subscriber count while views rot. Watch ratios, not "
       "totals.</li>"
       "<li><b>The topic drift:</b> chasing what’s hot instead of the promise you made. "
       "Subscribers came for a promise; drift mutes you.</li>"
       "</ul>"),

   faq=[
       {'q': 'How long until a Telegram channel earns money?',
        'a': 'With steady execution: first swap/ad income around 3–6 months at 1–5K engaged subscribers. Selling your own product can be profitable earlier — the channel is a distribution asset, not the revenue engine itself.',},
       {'q': 'What growth rate is realistic for a new channel?',
        'a': '2–5% net monthly growth organically; spikes from swaps on top. If 90 days of honest effort yields ~500–1,000 real subscribers with a 20%+ view ratio, you have a healthy asset that scales.',},
       {'q': 'Should I buy Telegram ads for a new channel?',
        'a': 'Not before retention data exists. Ads amplify what you have — spend them on a channel that already proves it keeps subscribers, usually after 60+ days of history.',},
       {'q': 'How do I keep posting consistently without burning out?',
        'a': 'Separate writing from publishing: one weekly writing session, batch-create posts, schedule the week, review stats Sunday. Any scheduling bot makes the cadence survive sick days and vacations.',},
   ])

_a('telegram-seo-and-discovery',
   category='growth',
   title='Telegram SEO: How Channels Get Discovered in 2026',
   description='Where Telegram search actually looks, why Google indexes public channels, the directory and catalog landscape (TGStat, Telemetr, Telegramic), and how to make your channel findable.',
   date='2026-09-26',
   content=(
       "<p>Telegram has no algorithmic feed — which makes <b>search</b> the platform’s most "
       "underestimated growth surface. Discoverability in 2026 runs on three rails: Telegram’s "
       "own search, external catalogs, and Google.</p>"

       "<h3>Rail 1: Telegram’s in-app search</h3>"
       "<ul>"
       "<li>Public channels are searchable by <b>name and @username</b>, not by description — "
       "so the channel name should contain the words people type. “Daily Remote Jobs” wins; "
       "“The Weekly Compass” loses.</li>"
       "<li>Search favors accounts with activity: an empty or dormant channel ranks poorly.</li>"
       "<li>Local results can dominate for geo queries — if your channel is location-based, put "
       "the city in the name.</li>"
       "</ul>"

       "<h3>Rail 2: catalogs, directories and promo platforms</h3>"
       "<p>This is where Telegram’s actual infrastructure lives, and it’s worth knowing the big "
       "names:</p>"
       "<ul>"
       "<li><b>TGStat</b> — the de-facto catalog + analytics service; its channel listings rank "
       "in Google too. A listing here is table stakes.</li>"
       "<li><b>Telemetr</b> — the second major catalog/analytics platform; similar deal.</li>"
       "<li><b>Telegramic</b> and similar submission directories — free listings, modest but "
       "real traffic.</li>"
       "<li><b>Telega.in</b> — the big ad marketplace: it’s where advertisers browse channels "
       "by category, so being listed (even before you sell) is passive discovery.</li>"
       "</ul>"
       "<p>Ignore anything promising “10,000 subscribers” — that’s bot-farm pricing, and bots "
       "wreck your view ratio (the number every one of these platforms displays publicly).</p>"

       "<h3>Rail 3: Google — the quiet giant</h3>"
       "<p>Google indexes <b>public</b> Telegram channels and their posts — t.me pages and "
       "aggregator sites both. That means:</p>"
       "<ul>"
       "<li>Your channel name and description are ranking text — write them for searchers.</li>"
       "<li>Posts with concrete, keyword-rich text (“How to X”, named tools, named places) can "
       "surface in Google results and funnel strangers into the channel.</li>"
       "<li>An attached public website or landing page compounds this: it’s the SEO surface "
       "channels don’t control directly.</li>"
       "</ul>"

       "<h3>The word-of-mouth rail (still #1)</h3>"
       "<p>Forwards are Telegram’s true recommendation engine. Posts that get forwarded share a "
       "shape: self-contained value (a complete list, a finished template), no “go to my channel "
       "for part 2” bait, and a channel signature so the forward advertises you. That signature "
       "toggle in channel settings — <i>sign messages</i> — is the single highest-leverage "
       "checkbox for discovery.</p>"

       "<h3>A one-hour discoverability audit</h3>"
       "<ul>"
       "<li>Does the channel name contain searchable words? (Rename if not.)</li>"
       "<li>Is the description a promise a stranger would search for?</li>"
       "<li>Is “sign messages” on?</li>"
       "<li>Are 5+ evergreen posts keyword-rich and complete?</li>"
       "<li>Listed on TGStat / Telemetr / a directory or two?</li>"
       "<li>Is the publishing rhythm machine-steady? Catalogs rank dead-looking channels down — "
       "a scheduler keeps the pulse honest (ManyBot, ControllerBot and Fast Scheduler all do "
       "it free).</li>"
       "</ul>"),

   faq=[
       {'q': 'Can people find my Telegram channel on Google?',
        'a': 'Yes, if it’s public — Google indexes public channel pages, t.me links and catalog listings. Keyword-rich names, descriptions and evergreen posts turn Google into a passive subscriber source.',},
       {'q': 'How does Telegram search ranking work?',
        'a': 'It matches primarily against channel name and username, with activity level as a secondary factor. Descriptions are not indexed in-app, but they are indexed by external search engines and catalog sites.',},
       {'q': 'Do Telegram directories still bring subscribers?',
        'a': 'In most markets, modest but real traffic — worth an hour of submissions once the channel looks alive. TGStat and Telemetr listings matter most because they rank in Google themselves.',},
       {'q': 'How do I make my posts more shareable on Telegram?',
        'a': 'Make each post self-contained value (complete lists, templates), avoid “part 2” bait, and enable channel message signatures so every forward carries your channel name.',},
   ])
