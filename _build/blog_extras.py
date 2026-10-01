# -*- coding: utf-8 -*-
"""Deep-dive sections for blog articles, part 1 (growth + content).

Same editorial rules as blog_articles*.py: real numbers, real mechanics,
real tools named as plain text. Every section is a continuation — new
material, not a summary — and gets appended to the article body at build
time (see build_blog.py), so reading time, search and the TOC pick it up.

Each entry: (heading, html body). A body is a string of <p>/<ul>/<ol> blocks.
"""

EXTRA_SECTIONS = {}
CONTENT_OVERRIDES = {}

def _sec(aid, heading, body):
    EXTRA_SECTIONS.setdefault(aid, '')
    EXTRA_SECTIONS[aid] += f'<h3>{heading}</h3>{body}'

# ================================================================ GROWTH ====

_sec('reach-1000-subscribers-telegram', 'The seeding loop, step by step',
     "<p>The first hundred subscribers almost never come from promotion — they come from "
     "<b>seeding</b>: deliberately placing your channel in front of small, warm audiences "
     "until a base exists that can grow on its own. The loop looks like this:</p>"
     "<ol>"
     "<li><b>List every community you already belong to.</b> Work chats, university groups, "
     "gaming clans, a neighborhood chat, a hobby forum. Most people can name ten without "
     "trying. These are your seeding spots.</li>"
     "<li><b>Give before you link.</b> In each community, spend a week being useful: answer "
     "questions, share things with no signature. People check the profile of anyone who "
     "posts something good — that's why your channel link lives in your bio, not in your "
     "messages.</li>"
     "<li><b>Post the artifact, not the ad.</b> When the channel has something genuinely "
     "valuable — a checklist, a dataset, a teardown — share the artifact itself in the "
     "community where it's relevant. One good artifact outperforms twenty \"subscribe to "
     "my channel\" messages, which get you banned from admins instead.</li>"
     "<li><b>Close the loop with comments.</b> When someone joins from a seed and comments, "
     "reply fast and personally. The first hundred should each feel like they were let "
     "into something.</li>"
     "</ol>"
     "<p>Run the loop for a month and measure honestly: if ten communities produced forty "
     "subscribers, you know your per-seed conversion — and whether the content or the "
     "seeding spots need to change before you scale the effort.</p>")

_sec('reach-1000-subscribers-telegram', 'Swap etiquette that gets you a second swap',
     "<p>Swaps — you post for me, I post for you — are the standard growth currency from "
     "roughly 300 subscribers upward. Most swap requests get ignored not because the "
     "channel is small, but because the request is lazy. The etiquette that gets yeses:</p>"
     "<ul>"
     "<li><b>Match by ERR, not size.</b> A 2,000-subscriber channel with 40% view rates "
     "delivers more real eyeballs than a 10,000 channel at 8%. Quote your <i>average views "
     "of the last ten posts</i>, never the subscriber count.</li>"
     "<li><b>Write the promo post for them.</b> Include the post, the link, and one line of "
     "context on why your audience would care. The fewer decisions your partner has to "
     "make, the faster the deal closes.</li>"
     "<li><b>Post at your best hour and expect the same.</b> A swap buried at 3 a.m. is "
     "wasted on both sides; agree on the slot explicitly.</li>"
     "<li><b>Send a screenshot of the results afterward.</b> Views, taps, joins. Partners "
     "re-swap with channels that report; they ghost the ones that don't.</li>"
     "</ul>"
     "<p>A practical cadence: two swaps per week at the same tier, for six weeks, beats any "
     "paid promo at this stage — it compounds, because every swap partner exposes you to "
     "another admin who now knows your channel exists.</p>")

_sec('telegram-channel-ideas', 'Idea 1 — The job board that answers one question',
     "<p>Take \"jobs channel\" and cut it until only one question remains. Not \"remote "
     "jobs\" — <b>\"remote React jobs, Europe, salary listed, posted the day they appear.\"</b> "
     "That description answers the three things every job-seeker asks: is it for me, is it "
     "real, how old is it. The mechanics that make this class of channel retain:</p>"
     "<ul>"
     "<li><b>A fixed format per post.</b> Role, location, salary range, apply link, one line "
     "on the company. Predictable format lets readers scan in two seconds and makes the "
     "channel feel like infrastructure rather than content.</li>"
     "<li><b>Ruthless freshness.</b> Reposting week-old openings is the fastest way to lose "
     "a job-board audience. Date-stamp everything; delete or mark expired entries.</li>"
     "<li><b>A submission funnel.</b> Recruiters will find you once you're consistent — give "
     "them a bot or a form. Sourced listings also solve your hardest problem at scale: "
     "they're self-replenishing content.</li>"
     "<li><b>The weekly digest.</b> One post per week summarizing the best ten listings. "
     "Digests get forwarded to colleagues, and forwards are this niche's growth engine.</li>"
     "</ul>"
     "<p>Monetization arrives naturally later — featured listings and recruiter promos — but "
     "only after the archive of past posts proves you never posted junk. Job boards live "
     "and die on trust in the filter.</p>")

_sec('telegram-channel-ideas', 'Idea 2 — The hyperlocal channel (the most underrated class)',
     "<p>National channels compete with media giants; a channel for one district of one "
     "city has no competition at all. Hyperlocal is the most defensible niche on Telegram "
     "because the moat is physical presence: you know which playground reopened, which "
     "pharmacy has the medicine, when the hot water goes off. What retains people:</p>"
     "<ul>"
     "<li><b>Utility density.</b> A single useful post — road closures this weekend, the "
     "school's schedule change — gets forwarded into family chats, which is where the "
     "subscribers come from. Parents, in particular, treat a good local channel as a "
     "public service.</li>"
     "<li><b>Civic micro-news.</b> Council decisions, utility works, local business "
     "openings/closings. Boring individually, indispensable in aggregate.</li>"
     "<li><b>A comments culture that stays civil.</b> Local channels attract strong "
     "opinions; a linked discussion group with light moderation keeps the channel "
     "readable. This is the one niche where moderation bots pay for themselves first.</li>"
     "</ul>"
     "<p>The honest difficulty: hyperlocal doesn't scale and doesn't sell to national "
     "advertisers. It monetizes through local businesses — a bakery announcement reaches "
     "exactly the people who can walk there, which is worth real money to the bakery.</p>")

_sec('telegram-channel-ideas', 'Idea 3 — Build-in-public: the retention machine',
     "<p>A build-in-public channel documents one project — a SaaS, a newsletter, a YouTube "
     "channel, even the Telegram channel itself — with real numbers: revenue, costs, "
     "mistakes, decisions. It retains better than almost any other format for one "
     "structural reason: <b>it's a story with unmade episodes</b>. Subscribers don't stay "
     "for the niche; they stay to find out what happens next. What makes it work:</p>"
     "<ul>"
     "<li><b>Real numbers, including unflattering ones.</b> \"MRR: $340, down from $410 — "
     "here's what I think happened\" builds more trust than any highlight reel. The "
     "audience for this format is sophisticated; they can smell curation.</li>"
     "<li><b>A consistent cadence with a structure.</b> A weekly numbers post, plus "
     "as-needed decision posts. The fixed slot turns checking the channel into a habit.</li>"
     "<li><b>Decision points, not just milestones.</b> \"Should I raise prices? Here's the "
     "data, vote in the comments\" — participatory moments convert readers into stakeholders, "
     "and stakeholders don't unsubscribe.</li>"
     "<li><b>An end condition.</b> Paradoxically, naming the finish line — \"until $2,000 "
     "MRR or twelve months\" — increases retention. Open-ended diaries feel like homework; "
     "bounded series feel like a season.</li>"
     "</ul>")

_sec('telegram-channel-ideas', 'Idea 4 — Micro-lessons: the course hiding in a feed',
     "<p>Teaching channels retain because progress is addictive: each post is a small, "
     "completable unit. The format that works isn't essays — it's <b>micro-lessons</b>: "
     "one concept, one example, one exercise, under 150 words. A language channel posts "
     "five words a day with usage examples; a design channel breaks down one layout "
     "choice per post; a finance channel explains one term with a real number. The "
     "mechanics worth stealing:</p>"
     "<ul>"
     "<li><b>Numbered progression.</b> \"Lesson 47\" in the post header creates collection "
     "pressure — people scroll back and read the archive, which is what separates a "
     "channel from a feed.</li>"
     "<li><b>Spaced repetition on purpose.</b> Resurface lesson 12's concept inside lesson "
     "40's example. Readers notice the callback and feel rewarded for paying attention.</li>"
     "<li><b>Exercise posts with next-day answers.</b> The answer post drives next-day "
     "opens, and comments fill with attempts — engagement the algorithm and other "
     "subscribers both reward.</li>"
     "<li><b>A pinned syllabus.</b> One post indexing the whole course, updated as it "
     "grows. New arrivals binge; binging is the strongest subscribe signal there is.</li>"
     "</ul>")

_sec('telegram-channel-ideas', 'Idea 5 — Deals and error-fares: trust is the entire product',
     "<p>Deal channels (gadgets, books, flights, games) have the highest raw engagement of "
     "any class — people act on them — and the most fragile trust. One affiliate-padded "
     "fake deal and the channel is done. The operators who last treat the filter as the "
     "product:</p>"
     "<ul>"
     "<li><b>Post only deals you'd send to a friend.</b> A simple test that eliminates "
     "half the affiliate inventory in any niche. The channel's value is precisely the "
     "deals it <i>doesn't</i> post.</li>"
     "<li><b>Show the math.</b> Price history (""is this actually a discount?""), the "
     "retailer, the catch. Deal-savvy readers check camel-price trackers anyway; get "
     "ahead of them.</li>"
     "<li><b>Speed windows.</b> Error fares and flash deals expire in hours — the channel "
     "needs a posting rhythm fast enough to matter. This is the niche where scheduled "
     "batches don't fit, and where a queue you can fire instantly from your phone does.</li>"
     "<li><b>Disclosure discipline.</b> Affiliate links marked, always. Counter-intuitively, "
     "marked links convert better in this class, because the audience knows exactly what "
     "they're looking at.</li>"
     "</ul>")

_sec('grow-telegram-channel-from-zero', 'Weeks 1–2 in detail: what "set up" actually means',
     "<p>The 90-day plan compresses at week level; here's the un-compressed version of the "
     "first two weeks, because this is where most channels quietly fail:</p>"
     "<ul>"
     "<li><b>Write the first ten posts before inviting anyone.</b> Not five — ten. The "
     "first visitors scroll the whole wall; a wall with ten substantive posts reads as an "
     "institution, one with three reads as an abandoned experiment.</li>"
     "<li><b>Fix the posting slots now.</b> Choose two or three weekly slots based on when "
     "your audience is actually on Telegram (evening hours in their timezone, generally), "
     "and queue the first two weeks against those slots. Scheduled publishing removes the "
     "daily willpower tax, which is the real killer of week three.</li>"
     "<li><b>Set up measurement on day one.</b> Note the baseline: subscribers, views per "
     "post. Every scheduler's stats page plus a simple spreadsheet is enough. The plan's "
     "weekly decisions depend on having honest numbers from the start, not reconstructed "
     "ones later.</li>"
     "<li><b>Seed list of ten places.</b> Written down, with a plan for each. \"I'll be "
     "useful in X for a week before mentioning anything\" is a plan; \"promote everywhere\" "
     "is a wish.</li>"
     "</ul>"
     "<p>Exit criteria for week two: ten posts published, two weeks queued, baseline "
     "recorded, first seeds placed. If any of those slipped, week three's growth work "
     "rests on sand — finish the foundation first.</p>")

_sec('grow-telegram-channel-from-zero', 'The metrics that actually decide the weekly review',
     "<p>The 90-day plan says \"track metrics weekly\"; these are the ones worth a "
     "spreadsheet row, and what each one tells you:</p>"
     "<ul>"
     "<li><b>Views-to-subscribers (V/S).</b> Your content quality signal. Healthy small "
     "channels run 25–60%. If it slides for three consecutive weeks while subscribers "
     "hold, the content has drifted from what joiners expected.</li>"
     "<li><b>Net adds per week, split by source.</b> Seeding, swaps, search, forwards — "
     "even a rough attribution tells you which engine to feed. Most channels discover "
     "one source produces 80% and starve it by spreading effort evenly.</li>"
     "<li><b>Unsubscribe timing.</b> Joins/leaves attached to specific posts (any decent "
     "scheduler shows this). A promo post that reliably triggers leave-waves is costing "
     "more than it pays.</li>"
     "<li><b>The forwarding signal.</b> Which posts get forwarded (Telegram shows forward "
     "counts). Forwards are the only organic distribution on the platform — double down "
     "on whatever earns them.</li>"
     "</ul>"
     "<p>One number to deliberately ignore: subscriber count as a headline. It's the "
     "output of the four metrics above, and staring at it weekly produces exactly the "
     "impatient decisions that stall channels.</p>")

_sec('cross-promotion-telegram-swaps', 'The swap marketplace, mapped',
     "<p>Beyond cold DMs, an actual infrastructure exists for finding swap partners — "
     "knowing the map saves weeks:</p>"
     "<ul>"
     "<li><b>TGStat and Telemetr catalogs</b> are the discovery layer: filter by category, "
     "sort by ERR, and you have a ranked list of every channel in your niche with their "
     "contact buttons. The free tiers are enough for swap-hunting.</li>"
     "<li><b>Swap chats and admin communities</b> — Telegram search for \"swap\" in your "
     "language surfaces dozens of chats where admins post slots. Quality varies wildly; "
     "treat them as lead sources, verify every channel in TGStat before agreeing.</li>"
     "<li><b>Adjacent-niche partners</b> are the underrated move. Two channels for the "
     "same audience compete; two channels for neighboring audiences compound. A channel "
     "about productivity tools and one about remote jobs share a person but not a "
     "subject.</li>"
     "</ul>")

_sec('cross-promotion-telegram-swaps', 'Writing the promo post: a teardown',
     "<p>Compare two swap posts for a fictional jobs channel:</p>"
     "<p><i>Weak:</i> \"Great channel about jobs! Subscribe: @link\" — no reason to care, "
     "no promise, and the reader has to leave the feed to learn anything.</p>"
     "<p><i>Strong:</i> \"Every weekday at 9:00 — 5 remote design jobs with salaries listed, "
     "filtered from 200+ sources. Yesterday's batch had a 90k studio role. @link\" — a "
     "promise with a rhythm, proof of filter quality, and a concrete example.</p>"
     "<p>The structural rules visible in the teardown:</p>"
     "<ul>"
     "<li><b>The first line must work as a notification.</b> Most readers see only the "
     "preview.</li>"
     "<li><b>One proof point beats three adjectives.</b> \"Yesterday's batch had a 90k "
     "role\" is verifiable; \"best jobs channel\" is not.</li>"
     "<li><b>End on the link, once.</b> Multiple links split attention and trip spam "
     "filters in some clients.</li>"
     "</ul>")

_sec('telegram-niche-research', 'The engagement-rate math, with real thresholds',
     "<p>Niche research ultimately reduces to one calculation, and it's worth doing "
     "properly. ERR (engagement rate per post) = average views of the last 10 posts ÷ "
     "subscribers. TGStat and Telemetr both display it; the thresholds that matter:</p>"
     "<ul>"
     "<li><b>Under 5%</b> at any size: dead or inflated audience. If the niche's "
     "leaders all sit here, the niche's audience was bought, not built — a red flag "
     "for the whole category.</li>"
     "<li><b>5–15%</b> for 10k+ channels: normal, healthy media territory.</li>"
     "<li><b>15–40%</b> for channels under 5k: the sweet spot proving an audience "
     "actually reads. This is what a genuine gap looks like on a chart.</li>"
     "<li><b>Over 60%</b> on a big channel: verify before you celebrate — screenshot-"
     "farming and view-pods exist. Cross-check comments-to-views; real channels have "
     "both in proportion.</li>"
     "</ul>"
     "<p>The research routine: list twenty candidate channels in the niche, pull ERR and "
     "growth slope for each, then read the top three by ERR for an hour. You'll leave "
     "knowing the working cadence, the formats that earn forwards, and — the actual "
     "prize — the gap between what audiences engage with and what anyone is providing.</p>")

_sec('telegram-niche-research', 'Validation before commitment: the 10-question checklist',
     "<p>Before writing a single post, the niche should survive ten questions. The first "
     "five are about the audience:</p>"
     "<ol>"
     "<li>Can I name three specific people (not personas) who need this daily?</li>"
     "<li>Do they already gather somewhere I can observe?</li>"
     "<li>What do they currently read instead — and what does it miss?</li>"
     "<li>Would they notice if this channel vanished tomorrow? Why?</li>"
     "<li>Is the need recurring (daily/weekly) or one-time? One-time needs build launch "
     "spikes, not channels.</li>"
     "</ol>"
     "<p>The second five are about you:</p>"
     "<ol start=\"6\">"
     "<li>Can I produce this from material I already read anyway?</li>"
     "<li>Does my format survive my worst week of the year?</li>"
     "<li>Am I one month from burnout on this topic, or one year?</li>"
     "<li>What's my unfair advantage — access, taste, data, speed?</li>"
     "<li>Would I run this if it never passed 500 subscribers?</li>"
     "</ol>"
     "<p>Questions 7 and 10 kill more channels than any competitor. A niche that passes "
     "all ten is rare — that's the point. Most fail on 3 and 8, which means the fix is a "
     "narrower niche, not more willpower.</p>")

# ================================================================ CONTENT ===

_sec('telegram-post-formatting-guide', 'The anatomy of a high-retention post',
     "<p>Formatting decisions compound differently at each layer of a post. A teardown of "
     "the structure that consistently performs:</p>"
     "<ul>"
     "<li><b>Line one (the notification).</b> Telegram truncates previews aggressively; "
     "the first ~60 characters decide whether the post opens at all. Front-load the "
     "specifics: a number, a name, a claim. \"Ticket prices to Georgia dropped 40%\" "
     "beats \"Great news for travelers\" every measurable way.</li>"
     "<li><b>Paragraph rhythm.</b> One to three sentences per paragraph, blank line "
     "between. Mobile screens fit roughly five lines; walls of text get skimmed into "
     "nothing. If a paragraph wraps more than a phone screen, it's two paragraphs.</li>"
     "<li><b>Bold as navigation, not decoration.</b> Bold the phrase a skimmer needs to "
     "find the post's spine — usually one bold phrase per paragraph. Bold whole "
     "sentences and nothing stands out; bold nothing and skimmers leave.</li>"
     "<li><b>The single-link rule.</b> Each post carries one action. Two links halve "
     "clicks on each; three turn the post into a directory nobody finishes.</li>"
     "</ul>")

_sec('telegram-post-formatting-guide', 'Media captions: the limit nobody plans for',
     "<p>Captions have their own rules, and they're stricter than post text: <b>1,024 "
     "characters for a photo caption</b>, 2,048 for some media types, and — the trap — "
     "<b>no formatting entities survive in captions forwarded from some sources</b>, plus "
     "albums show the caption only on the first item. Practical consequences:</p>"
     "<ul>"
     "<li>If a post's text exceeds the caption limit, the pattern is: short caption on "
     "the media, full text as the next standalone post. Some channels put \"1/2\" markers; "
     "cleaner is the album-then-text pair sent as a scheduled sequence.</li>"
     "<li>Album captions belong on the first image — plan which image leads, because it "
     "carries the entire caption.</li>"
     "<li>Link previews and media don't mix: a post with a photo suppresses the link "
     "preview unless you strip the media. When the preview matters more than your own "
     "image, post text-only with the preview.</li>"
     "</ul>")

_sec('telegram-content-calendar', 'A worked example: one month of a real calendar',
     "<p>Abstract calendars don't survive contact with a real channel, so here's a month "
     "for a (fictional but typical) 3-post-week design newsletter, built in one evening:</p>"
     "<ul>"
     "<li><b>Slot structure:</b> Monday = one tool deep-dive; Wednesday = three links "
     "worth your time, one line each; Friday = one teardown of a real design decision.</li>"
     "<li><b>Batch 1 (45 min):</b> list the month's four Monday tools — already known, "
     "they're what you used this month. Draft two-line stubs for each.</li>"
     "<li><b>Batch 2 (60 min):</b> expand each stub into a full post. Writing four "
     "similar posts consecutively is twice as fast as writing them across four weeks — "
     "no context re-loading.</li>"
     "<li><b>Batch 3 (30 min):</b> Wednesday link posts are just the reading list you "
     "already have open; Friday teardowns get drafted from notes you made anyway.</li>"
     "<li><b>Queue (15 min):</b> paste the date/message pairs into the scheduler — with a "
     "batching tool this is one message; with per-post bots, twelve. Done for a month.</li>"
     "</ul>"
     "<p>Total: about 2.5 hours for 12 posts, once a month. The daily alternative costs "
     "roughly the same time spread across 12 switching-costs — and dies the first "
     "busy week.</p>")

_sec('telegram-content-calendar', 'The capture pipeline: where posts come from',
     "<p>The calendar answers <i>when</i>; the capture pipeline answers <i>what</i>. "
     "Channels that batch successfully all have some version of this:</p>"
     "<ul>"
     "<li><b>One inbox, zero judgment.</b> A saved-messages folder (or a private bot "
     "chat) where every candidate lands — links, screenshots, half-thoughts. The only "
     "rule: capture takes under five seconds or it doesn't happen.</li>"
     "<li><b>Weekly triage against slots.</b> Fifteen minutes: drag candidates onto the "
     "calendar's slots. What fills the slot gets written; what doesn't fit any slot "
     "gets deleted without guilt — the slot structure is the filter.</li>"
     "<li><b>Draft in the format of the slot.</b> Monday digests always look the same, "
     "which means drafting is filling a template, not composing from scratch.</li>"
     "</ul>"
     "<p>The measurable payoff: a working capture pipeline means batching day contains "
     "zero blank-page moments. Everything is pre-decided; you're only editing.</p>")

_sec('telegram-series-and-serialized-posts', 'A real series plan: seven days, one case study',
     "<p>Here's a complete series arc that works for almost any niche — a week-long "
     "teardown, one post per day, ~150 words each:</p>"
     "<ul>"
     "<li><b>Day 1 — The setup:</b> the subject, the stakes, what will be examined. End "
     "with the question the week answers. Pin it; every later post links back "
     "implicitly by carrying the series title.</li>"
     "<li><b>Days 2–5 — One facet per day:</b> each post examines one layer (for a "
     "channel teardown: positioning, content mix, promotion, monetization), always "
     "with one concrete observation a stranger could learn from.</li>"
     "<li><b>Day 6 — The synthesis:</b> what the pieces add up to. This post earns the "
     "forwards; make it self-contained so it travels alone.</li>"
     "<li><b>Day 7 — The archive:</b> all seven posts as one long post. Newcomers "
     "arrive from the forwards into a finished artifact instead of a puzzle.</li>"
     "</ul>"
     "<p>Scheduling note: draft all seven before day 1 goes out, then queue them. A "
     "daily series with a missing day breaks the appointment it exists to build.</p>")

_sec('telegram-source-curation', 'Attribution: the currency curators forget',
     "<p>Curated digests live on other people's material, and how you credit it is a "
     "strategic choice, not a courtesy. The practice that compounds:</p>"
     "<ul>"
     "<li><b>Link the original source, always.</b> Yes, it's an outbound link — and "
     "source channels notice referral traffic. Mid-size sources check their analytics "
     "and will mention or swap with curators who send readers.</li>"
     "<li><b>Name the finder when you didn't find it.</b> \"(spotted in @channel)\" costs "
     "eight characters and earns a peer who'll feed you stories later. Curation is a "
     "network disguised as a channel.</li>"
     "<li><b>Add the take, carry the risk.</b> Your one-line read on each item is the "
     "only part that's yours — and the only part that can be wrong in public. That's "
     "fine: curators with a visible stance build audiences; neutral reposters build "
     "nothing.</li>"
     "</ul>")

# Part 2 (tools/premium/platform/money + ideas rewrite) merges itself in
try:
    import blog_extras2  # noqa: F401,E402
except ImportError:
    pass
