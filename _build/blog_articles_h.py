# -*- coding: utf-8 -*-
"""Blog articles, part 8 — long-form expansion batch 2 (3 articles, ~1,100+ words).

Same editorial rules as blog_articles*.py: real numbers, real mechanics,
real tools named as plain text — no links, no affiliate sugar. Fast Scheduler
is mentioned only where a normal expert would name the tool they use.
"""

BLOG_ARTICLES_H = []

def _a(i, **kw):
    kw['id'] = i
    BLOG_ARTICLES_H.append(kw)

# ============================================================ PLATFORM ======

_a('telegram-community-management',
   category='platform',
   title='Managing a Telegram Community: The Owner\u2019s Playbook for the First Year',
   description='Running a Telegram community that survives growth: culture-setting in the first 90 days, moderation ladders, conflict triage, rituals that retain, and the systems that keep it from consuming you.',
   date='2026-09-27',
   content=(
       "<p>A Telegram channel is a broadcast; a Telegram community is a living "
       "thing — and the difference is the discussion group, where the audience "
       "talks back. Communities compound (members recruit members, culture "
       "self-moderates, the group becomes the product) and they collapse "
       "(the founder becomes the bottleneck, the spam wave wins, the "
       "conversation curdles). The difference between the two outcomes is "
       "rarely luck — it's a handful of systems installed early. This is the "
       "playbook for the first year, in the order the systems are needed.</p>"

       "<h3>The first 90 days: setting the culture on purpose</h3>"
       "<p>Culture is easiest to set when everyone can see everyone. <b>Days "
       "1–30: the seeding window.</b> Personally welcome every joiner by "
       "name (at this size you can), answer every question within hours, "
       "and be publicly generous to the first regulars — the people who "
       "watch you treat the first ten members well are deciding how to "
       "treat the next hundred. <b>Days 31–60: the standards window.</b> "
       "Pin the two artifacts that do twenty jobs: a rules post (five "
       "rules maximum — more is a sign nothing is enforced) and a "
       "\"what this group is for\" post with one concrete example of a "
       "great exchange. <b>Days 61–90: the delegation window.</b> Promote "
       "your first moderator from the members who already do the work "
       "unasked — the person who answers newbies, not the loudest "
       "commenter. A moderator promoted at 300 members scales with the "
       "community; a moderation crisis at 3,000 members without one "
       "scales too.</p>"

       "<h3>The moderation ladder (written down, pinned, boring)</h3>"
       "<p>Enforcement that improvises is enforcement that gets called "
       "unfair. The standard ladder, from the automation section of the "
       "moderation guide: bots catch the mechanical layer — captcha on "
       "join (Rose or Shieldy), obvious spam deleted, link floods "
       "filtered. Humans handle the human layer with graduated steps: "
       "<b>1)</b> a public one-line nudge; <b>2)</b> <code>/warn</code> "
       "(three warnings auto-mute for 24 hours); <b>3)</b> a short "
       "<code>/mute</code> for heat without malice; <b>4)</b> "
       "<code>/ban</code> for scams, rings and doxxing — always with "
       "the reason stated. The multiplier that makes this work is "
       "<b>predictability</b>: a pinned ladder turns every moderation "
       "decision into \"the rule\", not \"the moderator's mood\", and "
       "complaints get answered with the pin instead of an argument. "
       "Review the ladder quarterly — as the community ages, the "
       "violations change shape.</p>"

       "<h3>The feedback engine: questions, rituals and the weekly beat</h3>"
       "<p>Communities die of silence, not of conflict — most members "
       "never post unless something pulls them. The pulls that work: "
       "<b>the weekly ritual</b> (the same feature, same day: wins "
       "Monday, stupid-questions Friday, the monthly \"what should we "
       "cover\" poll) — rituals give lurkers a known moment to surface; "
       "<b>answerable questions</b> — channel posts that end with a "
       "choice, not an essay prompt (\"A or B?\" beats \"thoughts?\"); "
       "<b>the first-reply rule</b> — no question sits unanswered for "
       "more than a few hours, because the speed of the first reply "
       "predicts whether a second question ever gets asked; and "
       "<b>visible impact</b> — when a member's suggestion changes the "
       "channel, say so by name. Members who see their fingerprints on "
       "the community become its glue. At 1,000+ members, add the "
       "structure layer: topics for the big chat, or a small "
       "breakout group for the regulars who carry the culture.</p>"

       "<h3>Conflict triage: the four fires</h3>"
       "<p>Community conflict comes in four shapes, and each has a "
       "different tool. <b>The blowup</b> (a heated thread forming): "
       "slow mode on, one de-escalating channel post, take it to DMs "
       "if two people are locked in — public threads never resolve, "
       "they just recruit. <b>The chronic complainer</b>: one direct "
       "conversation about what would change their mind; if nothing "
       "would, stop engaging — the group watches how you handle this "
       "more than anything. <b>The value-drain</b> (someone whose "
       "every post makes the room worse without breaking a rule): "
       "the quiet tools exist — mute, restricted mode — use them "
       "without ceremony. <b>The pile-on</b> (the group against one "
       "member): this is the one you act on fast, because it's the "
       "culture-defining moment; protect the target publicly, "
       "privately tell the pile-on leaders to stand down, and post "
       "the boundary afterward as a rule. Communities remember their "
       "worst week. Make sure it's handled well.</p>"

       "<h3>The founder's trap (and the handoff ladder)</h3>"
       "<p>Every healthy community eventually confronts the same "
       "bottleneck: everything routes through one person, and that "
       "person burns out or vanishes. The systems that prevent it are "
       "unglamorous: <b>documented ops</b> — the posting calendar, the "
       "moderation ladder and the bot configs written down where a "
       "co-admin can find them (a scheduler with stored drafts and "
       "queues means the channel publishes correctly even when the "
       "founder is offline for a week); <b>a co-admin with real "
       "rights</b> by month six — not as a favor but as continuity "
       "insurance; <b>the founder's manual</b> — a one-page document: "
       "what this community is, who the regulars are, what the "
       "rituals are, where the bodies are buried. Communities that "
       "survive their founder's vacation, job change or burnout were "
       "all built the same way: deliberately redundant from the "
       "start.</p>"

       "<h3>The metrics of a living community</h3>"
       "<p>Channel metrics (views, ERR) barely apply to the group "
       "side. The numbers that matter for a community: <b>week-4 "
       "activity</b> — of the members who joined this month, what "
       "share has said or reacted to anything (5–10% active is "
       "normal for a healthy group; below 2% it's a graveyard with "
       "notifications); <b>the answer latency</b> — median time "
       "before a member question gets any reply (hours, not days); "
       "<b>the regulars count</b> — the ~20 people who produce most "
       "of the conversation, tracked by name, because losing two of "
       "them changes the whole room; and <b>mod actions per week</b> "
       "— trending up means a spam problem, spiking after a promo "
       "means the promo audience, flat means healthy. Fifteen "
       "minutes a week on these four numbers is the difference "
       "between managing a community and discovering its autopsy.</p>"),

   faq=[
       {'q': 'How many moderators does a Telegram community need?',
        'a': 'A practical rule: one active moderator per 500–1,000 '
             'active members, with a minimum of two humans who can act '
             '(never rely on the founder alone — illness and vacations '
             'happen). Bots handle the mechanical layer regardless of '
             'size: captcha, link filters and obvious spam deletion '
             'scale infinitely, which is why the human count stays low '
             'while the bot count stays at one or two.'},
       {'q': 'Should the discussion group have topics enabled?',
        'a': 'Not at first — topics add a click of friction, and small '
             'communities live on drive-by replies. Switch topics on '
             'when the single-thread room becomes genuinely hard to '
             'follow, which usually shows up somewhere past a few '
             'hundred active members: questions getting buried within '
             'minutes, regulars asking for channels by topic. When you '
             'do, create few topics (five or so) and pin the mapping '
             '— too many topics fragments a community faster than no '
             'topics at all.'},
       {'q': 'How do I deal with a member who dominates every conversation?',
        'a': 'First check whether the dominance is actually harmful — '
             'a prolific regular who answers questions is a feature, '
             'not a bug, even if they are loud. If it is harmful (they '
             'crowd out others, make every thread about them), talk to '
             'them directly once, specifically, with examples. If '
             'nothing changes, use the quiet tools: restricted mode '
             'with a timer, or slow mode for the whole group, which '
             'spreads the floor without a public confrontation.'},
       {'q': 'Can a community survive without the founder being active daily?',
        'a': 'Yes — if the systems exist: a scheduler running the '
             'channel rhythm from a filled queue, co-admins with real '
             'rights, a pinned moderation ladder, and rituals that run '
             'on a schedule rather than on the founder\u2019s presence. '
             'Members stay for the other members, not for the founder, '
             'once the culture is set — the founder\u2019s real job is '
             'building the machine that makes them unnecessary.'}])

# ================================================================ TOOLS =====

_a('telegram-automation-guide-2026',
   category='tools',
   title='The Complete Telegram Automation Guide for 2026: From First Bot to Self-Updating Channel',
   description='Every automation layer a Telegram channel can have — scheduling, feeds, moderation, cross-posting, analytics — with the architecture that stays reliable, the invariants that prevent disasters, and what never to automate.',
   date='2026-09-27',
   content=(
       "<p>Every channel owner ends up automating something — the question is "
       "whether it happens accidentally, one fragile script at a time, or "
       "deliberately, as an architecture. This is the deliberate version: "
       "every automation layer a Telegram channel can have in 2026, the order "
       "to adopt them, the one invariant that keeps the whole system safe, "
       "and the failure modes that take down automations that looked solid. "
       "The goal is a channel that keeps its voice while the plumbing runs "
       "itself.</p>"

       "<h3>The layer map: what can be automated, in adoption order</h3>"
       "<p><b>Layer 1 — publishing (adopt first, saves the most stress):</b> "
       "every post goes through a scheduler's queue — ManyBot, ControllerBot, "
       "Fast Scheduler, whatever fits — so publishing stops depending on "
       "someone remembering. The queue view replaces the mental load, and "
       "the weekly review becomes possible because next week is already "
       "visible. <b>Layer 2 — intake:</b> sources flow into a review chat "
       "automatically — RSS bridges for feeds, form-to-chat bridges for "
       "submissions, forwarding rules for the channels you monitor. Nothing "
       "publishes from intake; it <i>arrives</i>. <b>Layer 3 — moderation:</b> "
       "captcha-on-join, link filters and duplicate detection (Rose, Shieldy, "
       "Combot) run unsupervised; humans handle the ladder above them. "
       "<b>Layer 4 — distribution:</b> cross-posting to sister channels or "
       "out to other platforms, through one writer. <b>Layer 5 — measurement:"
       "</b> weekly stats collection, ERR tracking, the ritual report — a "
       "spreadsheet fed by exports beats a dashboard nobody opens. Five "
       "layers, adopted in this order, take a channel from personality-"
       "driven to system-driven in about a quarter.</p>"

       "<h3>The single-writer rule: the invariant that prevents disasters</h3>"
       "<p>Every automation horror story traces to one violation: two "
       "systems that both believe they own the publishing tap. The fix is "
       "an invariant worth writing on a sticky note: <b>every channel has "
       "exactly one writer</b> — a human in the composer or one bot, never "
       "both, and nothing else holds admin rights to post. Everything else "
       "is upstream of the writer: feeds and forms flow into the review "
       "chat, drafts flow into the scheduler, analytics reads what "
       "published. Audit it quarterly: list every bot with post rights in "
       "every channel and ask, for each, \"is this the writer?\" — any "
       "answer that isn't yes-or-expired-rights is a duplicate-post "
       "accident waiting for a quiet week to happen in. Related hygiene: "
       "when you retire a tool, revoke its rights the same day (a live "
       "token in an abandoned tool is a safety issue, not clutter) — "
       "BotFather's <code>/revoke</code> takes ten seconds.</p>"

       "<h3>Idempotency: the boring property that saves reputations</h3>"
       "<p>Automations fail and get retried — the professional property "
       "that makes retries safe is <b>idempotency</b>: the same input "
       "applied twice produces one post, not two. The classic failure is "
       "the RSS bridge that re-reads a feed after a GUID change and "
       "republishes everything as new, overnight, to four thousand "
       "people. Defenses, cheapest first: bridges that deduplicate on "
       "the feed's item ID (most decent ones do — verify yours by "
       "re-adding a feed once and watching); a duplicate check in your "
       "review flow (search the channel for the headline before "
       "promoting); and the queue as the last gate — a post that "
       "already exists in the queue shouldn't be addable again. You "
       "can't prevent every double-publish, but you can make them rare "
       "enough that the apology post stays hypothetical.</p>"

       "<h3>The failure modes that take real channels down</h3>"
       "<p>Automations fail <i>silently</i>, which is what makes them "
       "dangerous. The gallery: <b>the DST drift</b> — daylight saving "
       "moves the \"9:00\" post to 10:00 for a month before anyone "
       "notices (fix: pin the channel's home timezone in the scheduler; "
       "check one scheduled post after each clock change). <b>The "
       "regenerated token</b> — a token revoken in BotFather turns every "
       "dependent tool mute at once (fix: the weekly ping command in "
       "your health check). <b>The silent bridge death</b> — a source "
       "site changes its feed structure and your intake quietly goes "
       "empty (fix: the Friday queue check includes \"did intake "
       "arrive this week?\"). <b>The rate-limit wall</b> — a broadcast "
       "bot that ignores <code>retry_after</code> gets throttled for "
       "hours mid-announcement (fix: tools that queue and back off "
       "properly — roughly one message per second per chat is the "
       "ceiling). Each failure is findable in two minutes a week, "
       "which is what the health check below actually is.</p>"

       "<h3>The weekly health check (five checks, two minutes)</h3>"
       "<p>1) <b>The queue</b> — next week's slots exist and nothing is "
       "scheduled into dead hours. 2) <b>The published log</b> — last "
       "week's posts show no duplicates, no dead-hour sends, no "
       "naked-markdown accidents. 3) <b>The ping</b> — send each "
       "automation bot one status command; anything that doesn't answer "
       "gets fixed before it matters. 4) <b>Intake freshness</b> — the "
       "review chat received material this week. 5) <b>The trend</b> — "
       "ERR against last week, leaves against the month. Two minutes "
       "every Friday; every item on this list has caught a real failure "
       "on real channels before the audience saw it. The health check is "
       "the price automation charges for its convenience, and it's the "
       "cheapest insurance in the whole stack.</p>"

       "<h3>What never to automate</h3>"
       "<p>The list is short because it's important. <b>The voice:</b> "
       "AI-assisted drafts are a tool, but posts that published without "
       "a human reading them will eventually embarrass the channel — "
       "the approval gate is one tap and it's the whole job. <b>Community "
       "replies:</b> automated welcome messages and canned answers read "
       "as absence; members can smell the difference, and the first ten "
       "seconds of a conversation set its ceiling. <b>Apologies and "
       "corrections:</b> when something goes wrong, the response must "
       "be human — automating sincerity is sincerity's cancellation. "
       "And <b>the decision itself:</b> automation decides when, how "
       "and in what order things publish; it should never decide "
       "<i>whether</i> — the publish button's human is the channel's "
       "editor, and keeping that seat occupied is what keeps a "
       "self-updating channel from becoming a self-deleting one.</p>"),

   faq=[
       {'q': 'Which automation should a small channel set up first?',
        'a': 'Scheduling, without question. Moving all posts through a '
             'queue is an afternoon of work, costs nothing, and removes '
             'the most damaging failure mode small channels have — the '
             'forgotten posting day that breaks the habit loop. Intake '
             'automation and moderation bots come next, in that order; '
             'cross-posting is rarely worth it until there are two '
             'worthwhile destinations.'},
       {'q': 'How do I stop my RSS bot from double-posting?',
        'a': 'Use a bridge that deduplicates on the feed item ID, '
             're-add one of your feeds once as a test and watch what '
             'happens, and route automated items through a review chat '
             'rather than straight to the channel. If a feed keeps '
             'regenerating IDs, filter it out — that source is not '
             'bridge-safe, and no amount of retry logic will make it '
             'one.'},
       {'q': 'Is it safe to give one bot all the admin rights?',
        'a': 'It is safe only if that bot is your writer and the rights '
             'match its job: a scheduler needs post and edit rights, '
             'nothing more. Distribution of rights should follow the '
             'single-writer rule — one bot publishes, moderation bots '
             'live only in the discussion group with moderation rights, '
             'and analytics bots need to read, not post. Quarterly, '
             'revoke anything whose purpose you cannot name.'},
       {'q': 'Can AI writing tools run a Telegram channel end to end?',
        'a': 'They can draft, summarize feeds and fill template slots — '
             'and channels that publish AI output unreviewed develop a '
             'noticeable voice drift that audiences and advertisers '
             'both detect. The working pattern is AI-prepared, '
             'human-approved: drafts enter the queue, a person edits '
             'and releases. The voice is the product; automation can '
             'surround it, but the moment it replaces the reading '
             'human, the channel starts dying politely.'}])

# ================================================================ MONEY =====

_a('telegram-monetization-mistakes',
   category='money',
   title='The 5 Monetization Mistakes That Kill Telegram Channels',
   description='The money decisions that destroy channels in hindsight — launching too early, pricing from subscriber count, the discount spiral, mixed payment rails — and the sequencing that avoids all five.',
   date='2026-09-27',
   content=(
       "<p>Channel monetization failures are weirdly consistent: the same five "
       "mistakes show up in every post-mortem, and all five are visible in "
       "advance. None of them are about choosing the wrong model — ads, Stars, "
       "subscriptions, affiliate and your own product all work at the right "
       "moment. They're about sequencing, pricing psychology and trust "
       "accounting. Here they are, with the sequencing that avoids each.</p>"

       "<h3>Mistake 1: launching monetization before retention exists</h3>"
       "<p>The instinct says strike while the feed is hot; the data says "
       "monetization tests your ERR before it tests your audience's wallet. "
       "A channel with a 40% ERR can run one promo post in ten and lose "
       "nothing measurable; the same promo on a 15% ERR channel visibly "
       "accelerates the slide — the audience was already half-gone, and "
       "selling to them is what finished the job. The prerequisite, "
       "concretely: three months of stable or rising ERR, a weekly open "
       "habit you can see in view patterns, and at least one format the "
       "audience demonstrably loves (forwards are the receipt). If that "
       "list reads like your channel's opposite, monetization isn't the "
       "next project — retention is. Money amplifies whatever exists; it "
       "does not create an audience that wants to hear from you.</p>"

       "<h3>Mistake 2: pricing from the subscriber count</h3>"
       "<p>The owner of 10,000 subscribers asks \"what do 10k channels "
       "charge?\" — and anchors to a number that describes the wrong "
       "asset. Advertisers buy expected views (ERR × subscribers), "
       "audience quality and niche buying power; two 10k channels in "
       "the same niche can differ five-fold in real price because one "
       "holds a 35% ERR and the other a 7% one that giveaway traffic "
       "diluted. The correct pricing sequence: compute expected views, "
       "find your niche's per-view band from comparable public channels "
       "(TGStat's ERR data makes this a ten-minute exercise), set a "
       "floor you won't go under, and put the subscriber count last "
       "where it belongs — as a sanity check, not an input. Owners who "
       "price from the count systematically underprice strong channels "
       "and overprice weak ones; the market quietly fixes both, at "
       "your expense.</p>"

       "<h3>Mistake 3: the discount spiral</h3>"
       "<p>The first sponsor negotiates 30% off, the second hears about "
       "it, the third assumes the list price was fiction — six months "
       "later the channel runs ads at half its healthy rate and can't "
       "climb back, because ad pricing is remembered, not re-derived. "
       "The defenses are structural, not heroic: a written rate card "
       "(even a two-line one) that exists outside negotiations; "
       "<b>value added instead of price cut</b> when pushing back is "
       "wrong — a bundle, a second slot, a longer runtime; and the "
       "two-strikes rule — discounts happen for strategic reasons "
       "(a flagship sponsor, a test slot) at most twice a year, never "
       "in consecutive negotiations. The same spiral applies to your "
       "own products: the Star-priced guide you sold at 50% off in "
       "month one set its real price in every buyer's mind. Channels "
       "that hold their pricing signal scarcity and confidence, and "
       "both compound.</p>"

       "<h3>Mistake 4: mixing the rails (and the money)</h3>"
       "<p>Stars for one product, CryptoBot invoices for another, a "
       "friend's bank transfer for a third, a subscription bot for a "
       "fourth — each works alone, and together they create the three "
       "costs owners never budgeted: <b>reconciliation debt</b> (four "
       "ledgers, none matching, tax season becomes archaeology), "
       "<b>support debt</b> (every rail has its own failure modes and "
       "refund flows — you become the payments department for each), "
       "and <b>trust erosion</b> (buyers who paid three different ways "
       "for three products wonder which one is real). The fix is one "
       "primary rail per product type: Stars for low-friction digital "
       "goods, one processor for subscriptions, one method for big "
       "tickets — and a single ledger sheet from day one (date, "
       "product, rail, gross, net). Two rails is a strategy; five is "
       "an accident that pays worse than either.</p>"

       "<h3>Mistake 5: treating the first sponsor as the ceiling</h3>"
       "<p>The channel lands its first paid placement, celebrates, and "
       "then... waits for the next inquiry, which comes when it comes. "
       "The mistake is structural: sponsorships are a pipeline, not a "
       "mailbox. The channels that grow ad income quarter over quarter "
       "all do the same boring things: they keep a <b>one-page media "
       "kit</b> with public-stat screenshots updated monthly; they "
       "<b>proactively pitch</b> adjacent products with a specific slot "
       "(\"your tool + our Tuesday deep-dive slot in March\") instead "
       "of advertising availability; they send a <b>delivery report</b> "
       "within 24 hours of every placement (views, clicks, the honest "
       "sentence on fit) — because renewal is cheaper than acquisition; "
       "and they <b>sell the calendar</b>, offering the next open slot "
       "by date, which converts scarcity into urgency without a single "
       "fake countdown. A sponsorship program is a sales funnel with "
       "five stages; channels that run all five double their ad revenue "
       "at the same audience size, which is the cheapest growth in the "
       "entire monetization catalog.</p>"

       "<h3>The order that works</h3>"
       "<p>Sequencing solves what willpower can't. The pattern that "
       "reliably ends well: <b>months 0–3</b> — no monetization at all; "
       "build the habit, the ERR floor and the formats (the audience "
       "remembers what the channel was before it sold anything). "
       "<b>Months 3–6</b> — the soft layer: Stars tips on the best "
       "posts, one affiliate mention inside genuinely useful content, "
       "nothing that interrupts. <b>Months 6–12</b> — the structured "
       "layer: a rate card, one to two dedicated sponsor slots a month "
       "maximum, a delivery report after each. <b>Year two</b> — the "
       "owned layer: the paid product or membership built on a year of "
       "trust data about what this audience actually pays for. Every "
       "layer assumes the previous one's trust was banked and spent "
       "slowly — that's the whole secret, and it's why the five "
       "mistakes above are all, at root, the same mistake: spending "
       "trust faster than the channel earns it.</p>"),

   faq=[
       {'q': 'How many subscribers do I need before monetizing a Telegram channel?',
        'a': 'There is no magic number — the real threshold is '
             'engagement, not size: three months of stable or rising '
             'ERR, a visible daily-open habit and at least one format '
             'that reliably earns forwards. A 2,000-subscriber channel '
             'with 45 percent ERR and a loyal niche monetizes better '
             'than a 15,000 one at 8 percent. That said, practical ad '
             'deals become routine somewhere past a few thousand real, '
             'engaged subscribers, because advertisers want meaningful '
             'absolute reach too.'},
       {'q': 'What is a realistic starting rate card for channel promos?',
        'a': 'Compute expected views first (ERR times subscribers), '
             'then apply your niche\u2019s per-view band — crypto, '
             'finance and B2B tools sit at the top, entertainment at '
             'the bottom. As a rough anchor, a 5,000-subscriber channel '
             'with 30 percent ERR in a mid-value niche starts around '
             '$30–120 per dedicated post. Set a floor you will not go '
             'under, and raise prices 20–30 percent only when your last '
             'three placements have all sold.'},
       {'q': 'Should I use Telegram Stars or an external payment provider?',
        'a': 'Use Stars where friction matters most — small digital '
             'goods, tips and paid posts, because the purchase happens '
             'inside Telegram in two taps. Use an external rail for '
             'subscriptions and bigger tickets where recurring billing, '
             'invoices or fiat settlement matter. The mistake is not '
             'choosing one over the other — it is running five rails '
             'at once, which multiplies reconciliation and support '
             'debt for no extra revenue.'},
       {'q': 'How do I approach sponsors instead of waiting for inquiries?',
        'a': 'Pitch specific, not general: name the product, the slot '
             'and the date (\u201cyour analytics tool in our March 12 '
             'teardown slot\u201d), attach a one-page media kit with '
             'public-stat screenshots, and lead with one concrete '
             'audience-fit sentence. Follow up once after a week, and '
             'after every delivered placement send a 24-hour delivery '
             'report — sponsors renew on certainty, and the renewal '
             'conversation starts the day the first post performs.'}])
