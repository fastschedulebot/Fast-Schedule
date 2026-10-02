# -*- coding: utf-8 -*-
"""Batch 2 of web-only SEO articles for the Fast Scheduler Help Center.

Same node shape as ``seo_articles.py``; merged in by ``build_help.py`` at
build time. Every claim is grounded in the bot code (handlers, plans, legal
pages) as of 2026-09; placeholders are filled from ``get_help_kwargs()``.
"""

ARTICLES_B = []

def _b(i, **kw):
    kw['id'] = i
    ARTICLES_B.append(kw)

# --------------------------------------------------------------- CHANNELS ----
_b('qa_private_channel_connect',
   category='channels',
   title='How Do I Connect a Private Telegram Channel to Fast Scheduler?',
   description='Private Telegram channels work with Fast Scheduler too. Four ways to connect one — @username, forwarding a post, an invite link, or the -100 ID.',
   content=(
       "<p>Private channels are fully supported — the bot never needs to be able to "
       "<i>search</i> your channel, it only needs to be <b>inside</b> it as an admin. "
       "There are four accepted ways to point Fast Scheduler at a private channel, and "
       "at least one of them will take you under a minute.</p>"
       "<h3>Before you start: give the bots admin rights</h3>"
       "<ul>"
       "<li>Open your private channel → <b>Administrators</b> → <b>Add Admin</b>.</li>"
       "<li>Add <b>@FastSchedulerBot</b> with the <b>Post Messages</b> permission. That "
       "single permission is enough to schedule and publish.</li>"
       "<li>Then, inside Fast Scheduler, pair a <b>sender bot</b> and make it an admin of "
       "the same channel. This step is mandatory: every scheduled post is published "
       "<i>through your sender bot</i>, never through the main bot, so nothing in the "
       "scheduling flow unlocks until each connected channel has one.</li>"
       "</ul>"
       "<h3>Four ways to connect the channel</h3>"
       "<p>Open the bot → <b>Channels</b> → <b>Connect Channel</b>, then send "
       "whichever of these is easiest for you:</p>"
       "<ul>"
       "<li><b>@username</b> — private channels have no @username, so this one is mostly "
       "for public channels.</li>"
       "<li><b>Forward any post</b> from the channel to the bot. This is the fastest way "
       "for private channels: open the channel, long-press any message, Forward → "
       "Fast Scheduler Bot. The bot reads the source channel from the forward.</li>"
       "<li><b>An invite link</b> — copy <i>Invite Link</i> from the channel menu and "
       "paste it into the chat.</li>"
       "<li><b>The channel ID</b> — the numeric <code>-100…</code> identifier "
       "(e.g. <code>-1001234567890</code>) if you know it from another tool.</li>"
       "</ul>"
       "<h3>Why the invite-link and forward methods are equivalent</h3>"
       "<p>Both simply resolve your private channel to its internal ID. Fast Scheduler "
       "stores that ID plus your admin status; the channel&rsquo;s privacy settings "
       "never matter again after the connection is made. You can rename the channel, "
       "change its link, or toggle &ldquo;slow mode&rdquo; — the connection survives all "
       "of it.</p>"
       "<h3>If connecting fails</h3>"
       "<ul>"
       "<li><i>Bot is not an admin</i> — re-check step one; the permission check runs "
       "live against Telegram.</li>"
       "<li><i>Invite link revoked or set to &ldquo;join request&rdquo;</i> — regenerate "
       "the link, or forward a post instead.</li>"
       "<li><i>You are not the owner</i> — the connector must hold admin rights in the "
       "channel under the account that talks to the bot.</li>"
       "</ul>"
       "<p>Free plan: {channels_free} channel. Premium raises this to {channels_prem}, "
       "each with its own sender bot, time zone and statistics.</p>"),
   faq=[
       {'q': 'Can Fast Scheduler post to a private channel?',
        'a': 'Yes. Private channels are connected by forwarding a post from the channel, pasting an invite link, or sending the -100 channel ID. The channel being private does not affect scheduling in any way.',
        'links': ['channel_add']},
       {'q': 'Does the sender bot also need admin rights in a private channel?',
        'a': 'Yes. The main bot needs Post Messages to verify and manage, and your sender bot needs Post Messages because it is the account that actually publishes every scheduled post.',
        'links': ['bot_sender']},
       {'q': 'How many channels can I connect on the Free plan?',
        'a': 'Free includes {channels_free} channel with {monthly_sent_free} sent messages per month. Premium raises the limit to {channels_prem} channels with unlimited sends.',
        'links': ['limit_daily']},
   ],
   links=['channel_add', 'channels', 'bot_sender', 'bot_add', 'qa_add_channel_guide', 'qa_sender_bot_required'])

# ---------------------------------------------------------------- PREMIUM ----
_b('qa_refund_how',
   category='premium',
   title='How Do I Get a Refund on My Fast Scheduler Premium Purchase?',
   description='Paid with Telegram Stars and changed your mind? Here is exactly how to request a refund: the email, what to include, the 30-day window and processing times.',
   content=(
       "<p>Refunds are handled personally, not by a faceless form. If a purchase went "
       "wrong — a double charge, an accidental renewal, Premium that never activated — "
       "you write one email and a human sorts it out. Here is the whole procedure, "
       "step by step.</p>"
       "<h3>What to send</h3>"
       "<p>Email <b>fastschedulebot@gmail.com</b> with three things:</p>"
       "<ul>"
       "<li>Your <b>transaction ID</b> — Telegram shows it in the Stars payment "
       "confirmation and in Settings → Payments.</li>"
       "<li>Your <b>Telegram username</b> (or user ID) so the purchase can be matched "
       "to your account.</li>"
       "<li>The <b>reason</b> — one honest sentence is enough, plus the purchase date "
       "and the account or email used, where applicable.</li>"
       "</ul>"
       "<h3>The 30-day window and what happens next</h3>"
       "<p>Refund requests are accepted within <b>30 days</b> of the charge. Requests "
       "are acknowledged within <b>7 business days</b>, and approved refunds are "
       "returned through the original payment method — for Telegram Stars that means "
       "back to your Stars balance. Refunds are discretionary rather than guaranteed "
       "for every situation, which is exactly why a short, honest reason helps: "
       "accidental purchases and technical failures the team could not fix are the "
       "classic approved cases.</p>"
       "<h3>Cancelling so you are not charged again</h3>"
       "<p>Monthly Stars plans renew automatically until cancelled. You cancel inside "
       "the bot: open <b>/premium</b> → <b>❌ Cancel Premium</b>. Cancelling "
       "stops future billing; the period you already paid for stays active until its "
       "end date, and Premium switches off at that boundary rather than mid-plan. "
       "The 3-month, 6-month and yearly packs are one-time purchases — they simply "
       "expire and never auto-charge.</p>"
       "<h3>What not to do: chargebacks</h3>"
       "<p>Opening a card or Apple/Google chargeback instead of emailing is treated as "
       "abuse: the account loses Premium immediately and the subscription fee is "
       "forfeited. Emailing first is always faster — most refund conversations end "
       "within a couple of messages.</p>"
       "<p>One more nuance: deleting your data or stopping use of the bot does not "
       "automatically refund anything, so if you want both, request the refund "
       "<i>before</i> asking for account deletion.</p>"),
   faq=[
       {'q': 'How long does a Fast Scheduler refund take?',
        'a': 'Requests are acknowledged within 7 business days. Once approved, Stars refunds return to your Telegram Stars balance; the total time depends on Telegram, typically a few days.',
        'links': ['premium_buy']},
       {'q': 'Can I cancel Premium and keep it until the period ends?',
        'a': 'Yes. Cancelling via /premium stops auto-renewal, and Premium stays active until the end of the paid period. Downgrade happens at that boundary, not immediately.',
        'links': ['premium']},
       {'q': 'I was charged twice. What do I do?',
        'a': 'Email fastschedulebot@gmail.com with both transaction IDs and your Telegram username. Duplicate charges are the clearest refund case and are resolved quickly.',
        'links': ['premium_buy']},
   ],
   links=['premium', 'premium_buy', 'qa_pay_stars_crypto', 'qa_which_plan', 'qa_premium_worth'])

# --------------------------------------------------------------- TIMEZONE ----
_b('qa_timezone_wrong_time',
   category='timezone',
   title='Why Was My Scheduled Telegram Post Published at the Wrong Time?',
   description='A post set for 9:00 went out at 6:00 or 12:00? The cause is almost always a time-zone mismatch. Here is how Fast Scheduler resolves times and how to fix it.',
   content=(
       "<p>When a scheduled message fires at an unexpected hour, the clock itself is "
       "almost never wrong — the <i>time zone</i> used to interpret &ldquo;9:00&rdquo; "
       "is. Fast Scheduler resolves every time through two settings, and a mismatch "
       "between them explains nearly every &ldquo;wrong time&rdquo; report.</p>"
       "<h3>The two clocks: user time zone and channel time zone</h3>"
       "<ul>"
       "<li>Your <b>user time zone</b> — set once via <code>/timezone</code> and used "
       "whenever you type a time into the scheduling conversation.</li>"
       "<li>Each channel&rsquo;s <b>own time zone</b> — set per channel, because the "
       "audience that reads the channel may live in a different zone than you do. "
       "Schedules for that channel are interpreted in the <i>channel&rsquo;s</i> zone.</li>"
       "</ul>"
       "<p>If your user zone says UTC+3 but the channel zone says UTC+0, a message you "
       "schedule for 9:00 is stored as 9:00 channel time — and lands six hours earlier "
       "than you visually expected. Check both: <code>/timezone</code> for yourself, "
       "and the channel settings inside the bot for the channel.</p>"
       "<h3>Daylight saving time</h3>"
       "<p>Zones with DST shift by one hour twice a year. Fast Scheduler stores "
       "schedules in absolute terms, so a post that crossed a DST boundary can appear "
       "to &ldquo;move&rdquo; by an hour. If you live in a DST zone and noticed the "
       "shift right after the clocks changed, re-check the channel&rsquo;s zone — "
       "picking a zone like <i>Europe/Berlin</i> (which follows DST rules) versus a "
       "fixed UTC offset produces different results across the year.</p>"
       "<h3>Quick diagnosis checklist</h3>"
       "<ul>"
       "<li><b>Off by a round number of hours</b> (3, 4, 6…) → time-zone mismatch; fix "
       "the channel time zone or your user zone.</li>"
       "<li><b>Off by exactly one hour</b> right after late March / late October → DST; "
       "confirm the zone uses the right convention.</li>"
       "<li><b>AM/PM confusion</b> — schedule with the 24-hour clock (14:00, not 2:00) "
       "to remove ambiguity entirely.</li>"
       "<li><b>Around midnight</b> — double-check you scheduled the day you meant; the "
       "date picker always shows the resolved local date and time for final "
       "confirmation before saving.</li>"
       "</ul>"
       "<p>One more tip: the confirmation screen before saving shows the exact send "
       "time. Reading that single line — not the input you typed — is the ground truth "
       "for when the post will fire.</p>"),
   faq=[
       {'q': 'Does each Telegram channel have its own time zone in Fast Scheduler?',
        'a': 'Yes. Every channel carries its own time zone, and schedules for that channel are interpreted in the channel zone. Your personal /timezone setting applies to how you enter times while chatting with the bot.',
        'links': ['timezone_set', 'timezone_list']},
       {'q': 'How do I change the time zone of a channel?',
        'a': 'Open the bot, go to the channel settings, and set its time zone there. Existing scheduled messages keep their stored times, so new schedules pick up the change immediately.',
        'links': ['timezone_set']},
   ],
   links=['timezone_set', 'timezone_list', 'qa_timezones', 'faq_schedule', 'qa_post_not_sent'])

# ------------------------------------------------------------------ STATS ----
_b('qa_stats_views',
   category='tools',
   title='How Can I See Views, Reactions and Comments on My Telegram Channel Posts?',
   description='Fast Scheduler tracks views, comments and reactions for every post it publishes — with per-channel dashboards and Premium leaderboards of your top content.',
   content=(
       "<p>Telegram shows view counts under every channel post, but it never shows you "
       "<i>trends</i>: which topics overperform, what time of day your audience "
       "actually reads, which posts collected the most reactions. Fast Scheduler "
       "records the metrics of every post it publishes and turns them into dashboards "
       "you can browse in seconds.</p>"
       "<h3>Where the numbers live</h3>"
       "<p>Open <b>Statistics</b> on the bot&rsquo;s main menu (page 2) or send "
       "<code>/stats</code>. You get:</p>"
       "<ul>"
       "<li><b>Usage totals</b> — lifetime messages sent, messages sent today, and how "
       "many schedules and recurring messages are currently active.</li>"
       "<li><b>Per-channel dashboards</b> — for every connected channel: average views, "
       "comments and reactions per post, plus the top reactions your audience uses.</li>"
       "<li><b>Leaderboards (Premium)</b> — your top posts ranked by the metric you "
       "pick: Views, Comments, Reactions or Top Commenters. Each board shows "
       "10 entries per page and can be filtered by period (day, week, month, year or "
       "all time).</li>"
       "</ul>"
       "<h3>What is counted — and what is not</h3>"
       "<p>Statistics are recorded when <b>Fast Scheduler publishes a post</b> and "
       "Telegram reports back the post&rsquo;s metrics. Manually posted content that "
       "never passed through the bot is deliberately excluded, so the numbers describe "
       "your scheduled content honestly. Comments made in the discussion group under a "
       "channel post are picked up too, which is what powers the Comments metric and "
       "the Top Commenters board.</p>"
       "<h3>Three ways to actually use this</h3>"
       "<ul>"
       "<li><b>Find your format.</b> Sort by Views for a month: if the top five posts "
       "share a pattern (length, media type, topic), schedule more of it.</li>"
       "<li><b>Time your channel.</b> Compare identical formats posted at different "
       "hours, then move recurring messages toward the winning window — "
       "the best posting times guide below has the general playbook.</li>"
       "<li><b>Watch reactions, not just views.</b> Views measure reach; reactions and "
       "comments measure resonance. A post with half the views but double the reaction "
       "rate is usually the better template.</li>"
       "</ul>"),
   faq=[
       {'q': 'Does Fast Scheduler track posts I publish manually?',
        'a': 'No. Only posts published through Fast Scheduler are recorded, which keeps your dashboards focused on your scheduled content strategy.',
        'links': ['statistics']},
       {'q': 'Are statistics leaderboards free?',
        'a': 'Per-channel averages and usage totals are available to everyone. Leaderboards that rank your top posts by views, comments or reactions are part of Premium.',
        'links': ['premium']},
       {'q': 'What metrics can leaderboards rank by?',
        'a': 'Views, comments, reactions and top commenters — each filterable by day, week, month, year or all time, with up to 50 posts per page.',
        'links': ['statistics']},
   ],
   links=['statistics', 'search', 'premium', 'tg_best_posting_times', 'qa_media_storage_guide'])

# --------------------------------------------------------------- SCHEDULING --
_b('qa_media_types',
   category='scheduling',
   title='What Types of Content Can You Schedule With Fast Scheduler?',
   description='Photos, videos, GIFs, voice messages, stickers, polls, documents, locations — every media type Fast Scheduler can schedule to a Telegram channel.',
   content=(
       "<p>A scheduling bot is only as good as the content it can carry. Fast "
       "Scheduler handles the full Telegram media palette, so your editorial plans "
       "never have to shrink to fit the tool.</p>"
       "<h3>Everything you can attach to a scheduled post</h3>"
       "<ul>"
       "<li><b>Photos</b> — compressed automatically for fast delivery without visible "
       "quality loss.</li>"
       "<li><b>Videos</b> — including size limits that scale with your plan "
       "({videos_msg_free} on Free, {videos_msg_prem} on Premium).</li>"
       "<li><b>Video notes</b> (round videos) and <b>voice messages</b>.</li>"
       "<li><b>Audio files</b> — full tracks with cover art preserved.</li>"
       "<li><b>Documents</b> — PDFs, archives, anything Telegram accepts.</li>"
       "<li><b>Animations</b> — GIFs and MP4 loops.</li>"
       "<li><b>Stickers</b> — from any of your packs.</li>"
       "<li><b>Polls and quizzes</b> — scheduled like any other post.</li>"
       "<li><b>Locations and venues</b> — supported for per-post content.</li>"
       "</ul>"
       "<h3>Albums and media groups</h3>"
       "<p>Multiple photos or videos sent together are scheduled as one album and "
       "publish as a single media group — exactly how your followers expect it. You "
       "can also build a <b>randomized pool</b>: attach a mix of photos, videos, "
       "documents or any files and let the "
       "scheduler pick one per send, which is perfect for daily wallpaper or quote "
       "channels where variety matters.</p>"
       "<h3>Text always travels with media</h3>"
       "<p>Captions keep their formatting (bold, italic, links, spoilers) and your "
       "configured <b>signature</b> is appended to media posts as well. Inline URL "
       "buttons attach to media posts too, so a &ldquo;Read more&rdquo; button under a "
       "photo works out of the box.</p>"
       "<h3>Limits that matter</h3>"
       "<ul>"
       "<li>Uploads: up to <b>{max_media_free}</b> on Free, <b>{max_media_prem}</b> on "
       "Premium.</li>"
       "<li>Videos: <b>{videos_msg_free}</b> on Free, <b>{videos_msg_prem}</b> on "
       "Premium.</li>"
       "<li>Media Storage boxes: {storage_count_free} box with {storage_items_free} "
       "items on Free — Premium multiplies both, so reusable assets live in the "
       "bot instead of your camera roll.</li>"
       "</ul>"
       "<p>Anything Telegram itself refuses (for example, a corrupted file) is "
       "rejected at scheduling time with a clear message — never discovered silently "
       "on the day of publishing.</p>"),
   faq=[
       {'q': 'Can I schedule Telegram polls with Fast Scheduler?',
        'a': 'Yes. Polls and quizzes are scheduled like any other message and publish through your sender bot at the set time.',
        'links': ['faq_schedule']},
        {'q': 'Can I schedule an album of photos?',
         'a': 'Yes. Photos and videos sent together are scheduled as one media group. You can also attach a pool of mixed files and let the scheduler pick one randomly per send.',
         'links': ['media_storage']},
       {'q': 'What is the maximum video size for scheduled messages?',
        'a': 'Videos {videos_msg_free} on the Free plan and {videos_msg_prem} with Premium, in line with Telegram bots own upload limits.',
        'links': ['limit_media']},
   ],
   links=['faq_schedule', 'media_storage', 'ms_limits', 'signature', 'inline_buttons', 'qa_edit_scheduled_post'])

# ----------------------------------------------------------------- PRIVACY ---
_b('qa_delete_data',
   category='privacy',
   title='How Do I Delete My Fast Scheduler Account and All My Data?',
   description='Want everything removed? Here is how account deletion works, what exactly gets erased, why you should export a backup first, and what happens on Telegram side.',
   content=(
       "<p>You can leave Fast Scheduler completely — no subscriptions to cancel by "
       "email, no dark patterns, no &ldquo;are you sure&rdquo; maze. One message, and "
       "everything tied to your Telegram account is erased.</p>"
       "<h3>How to request deletion</h3>"
       "<p>Contact <b>@MaximalXP</b> in Telegram and ask to delete your account. "
       "Deletion is permanent and covers <b>all</b> data associated with your user "
       "ID: scheduled and recurring messages, media storage, sender-bot tokens, "
       "channel connections, settings, statistics and referral records.</p>"
       "<h3>Export first — deletion has no undo</h3>"
       "<p>Before deleting, create a backup with <code>/backup</code> (a Premium "
       "toolkit) or export individual lists, so your content plan survives the "
       "account. Once deletion runs, there is no recovery path — the data no longer "
       "exists to restore.</p>"
       "<h3>What happens on Telegram&rsquo;s side</h3>"
       "<ul>"
       "<li>Your <b>sender bots</b> keep existing in @BotFather — they are your bots, "
       "created with your account. If you want them gone too, revoke or delete them "
       "there after deletion. Revoke first if you plan to keep using them elsewhere.</li>"
       "<li>The bot loses admin rights relevance immediately, but you can also remove "
       "<b>@FastSchedulerBot</b> and your sender bot from your channels&rsquo; admin "
       "lists yourself — a good hygiene step that takes ten seconds per channel.</li>"
       "<li>Already-published posts stay in your channel, of course — deletion cannot "
       "rewrite history.</li>"
       "</ul>"
       "<h3>How long data is kept normally</h3>"
       "<p>While you are an active user, every category of data is kept only while it "
       "is useful: schedules until they are deleted or sent, bot tokens until you "
       "disconnect the bot, and account records until you delete the account. The "
       "Privacy Policy&rsquo;s retention table lists each category with its exact "
       "lifetime.</p>"),
   faq=[
       {'q': 'Who do I contact to delete my Fast Scheduler account?',
        'a': 'Message @MaximalXP on Telegram and request account deletion. The deletion is permanent and removes all data linked to your Telegram ID.',
        'links': ['privacy_delete', 'privacy_data']},
       {'q': 'Can I delete everything but keep the bot?',
        'a': 'Yes — you can delete individual schedules, media and sender bots from inside the bot without deleting your account. Full deletion is only for leaving the service entirely.',
        'links': ['privacy_data']},
       {'q': 'Should I export a backup before deleting?',
        'a': 'Definitely. After deletion there is no way to restore anything, so create a backup with /backup first if there is any chance you will return.',
        'links': ['backup_create', 'qa_backup_full_guide']},
   ],
   links=['privacy_delete', 'privacy_data', 'backup_create', 'security_data', 'qa_backup_full_guide'])

# --------------------------------------------------------------------- FAQ ---
_b('qa_setdate_bulk',
   category='faq',
   title='How Do I Schedule Many Telegram Posts at Once? (Bulk Scheduling with SetDate)',
   description='Queue dozens of channel posts in minutes: prepare them in the SetDate companion bot, pick dates and times, and import everything into Fast Scheduler in one click.',
   content=(
       "<p>Scheduling one post is quick. Scheduling <i>thirty</i> — a week of content "
       "for a news channel, a course drip, a product launch sequence — needs a "
       "different tool: <b>SetDate</b>, the companion bot built for exactly this.</p>"
       "<h3>The five-minute bulk workflow</h3>"
       "<ul>"
       "<li><b>1. Open SetDate.</b> Open <b>@SetDate_bot</b> directly — or tap <b>📅 Use SetDate Bot</b> whenever Fast Scheduler suggests it.</li>"
       "<li><b>2. Feed it content.</b> Send your messages one after another — text, "
       "photos, videos, anything you would schedule normally.</li>"
       "<li><b>3. Choose a start date</b> and how many posts should go out per day.</li>"
       "<li><b>4. Define posting times</b> — for example 09:00, 14:00 and 18:00 — and "
       "SetDate distributes your messages across that grid.</li>"
       "<li><b>5. Send the batch back.</b> One tap and every message appears in Fast "
       "Scheduler as a normal scheduled post, fully editable afterwards.</li>"
       "</ul>"
       "<h3>Why this beats scheduling by hand</h3>"
       "<ul>"
       "<li><b>One sitting instead of thirty.</b> You write all content while you are "
       "in the writing mood, then let the grid place it.</li>"
       "<li><b>Perfect for recurring formats.</b> A daily tip at 10:00 for the next "
       "two weeks is two fields in SetDate, not fourteen conversations.</li>"
       "<li><b>Everything stays editable.</b> After import, each post is a regular "
       "scheduled message — search it, edit it, delete it, or move it in the "
       "calendar.</li>"
       "</ul>"
       "<h3>Bulk for repeated content: recurring messages</h3>"
       "<p>If the <i>same</i> message should repeat — a weekly digest, a daily "
       "reminder — you do not need bulk import at all: create a <b>recurring "
       "message</b> once and it reschedules itself. Free plans run "
       "{recurring_free} recurring message; Premium removes the cap "
       "({recurring_prem}) and its rules never expire.</p>"
       "<p>Tip: before importing a large batch, glance at your channel&rsquo;s time "
       "zone (see the time-zone guide) so the grid lands on the hours you actually "
       "meant.</p>"),
   faq=[
       {'q': 'What is the SetDate bot?',
        'a': 'SetDate is Fast Scheduler’s companion bot for bulk scheduling: you prepare many messages there, choose a start date and daily posting times, and import them all into Fast Scheduler in one click.',
        'links': ['setdate']},
       {'q': 'Can I edit posts after bulk import?',
        'a': 'Yes. Imported messages become ordinary scheduled messages — open the Message List or calendar and edit, move or delete any of them individually.',
        'links': ['qa_edit_scheduled_post']},
       {'q': 'How many posts can I import at once?',
        'a': 'Imported messages count against your scheduled-message limit ({scheduled_free} pending on Free, unlimited on Premium), so a batch that fits your queue can be imported in one go.',
        'links': ['limits_free']},
   ],
   links=['setdate', 'qa_schedule_many_at_once', 'recurring_uses', 'faq_schedule', 'qa_edit_scheduled_post'])

_b('tg_channel_vs_group',
   category='faq',
   title='Telegram Channel vs Group: What Is the Difference and Which One Do You Need?',
   description='Channels broadcast, groups converse. A practical comparison for creators — and how Fast Scheduler fits each, including discussion-group comments.',
   content=(
       "<p>New Telegram creators constantly mix these up, and picking wrong shapes "
       "everything after it — including how you schedule. Here is the short, practical "
       "version.</p>"
       "<h3>The one-line difference</h3>"
       "<p>A <b>channel</b> is a megaphone: only admins publish, everyone else reads. "
       "A <b>group</b> is a round table: every member can post and reply. A channel "
       "can have a linked <b>discussion group</b>, which adds a comment thread under "
       "every channel post — the best of both worlds.</p>"
       "<h3>Choose a channel when…</h3>"
       "<ul>"
       "<li>You publish content <i>to</i> an audience: news, deals, tutorials, "
       "drops.</li>"
       "<li>You want a clean feed readers can scroll without chatter.</li>"
       "<li>You care about per-post <b>view counts</b> — channels show them, groups "
       "do not.</li>"
       "</ul>"
       "<h3>Choose a group when…</h3>"
       "<ul>"
       "<li>Conversation <i>is</i> the product: support, community, coordination.</li>"
       "<li>You want members to see each other and reply freely.</li>"
       "</ul>"
       "<h3>The classic combo</h3>"
       "<p>Most serious projects end up with <b>both</b>: a channel for polished "
       "posts, plus a linked discussion group for the conversation under them. "
       "Telegram links them in the channel settings; from then on every channel post "
       "automatically gets a comment thread.</p>"
       "<h3>Where Fast Scheduler fits</h3>"
       "<p>Fast Scheduler publishes to <b>channels</b> — that is where scheduled "
       "broadcast content belongs. Because it also tracks the discussion-group "
       "<b>comments</b> under the posts it publishes, your statistics cover the "
       "conversational side too: average comments per post and Top Commenters "
       "leaderboards work with the combo setup out of the box. The practical recipe: "
       "plan and queue polished posts in the channel, and let the linked group absorb "
       "the discussion they spark.</p>"),
   faq=[
       {'q': 'Can Fast Scheduler post to groups?',
        'a': 'Fast Scheduler schedules to channels, which is the broadcast use case it is built for. For community discussion, create a channel with a linked discussion group — comments there are tracked in your statistics.',
        'links': ['channels', 'statistics']},
       {'q': 'What is a discussion group in Telegram?',
        'a': 'A group linked to your channel in channel settings. Every channel post gets a comment thread in that group, giving readers a place to reply without polluting the channel feed.',
        'links': ['tg_channels_explained']},
   ],
   links=['tg_channels_explained', 'channels', 'qa_add_channel_guide', 'statistics', 'tg_best_posting_times'])

# --------------------------------------------------------------- SCHEDULING --
_b('qa_formatting',
   category='scheduling',
   title='How Do I Format Telegram Posts? (Bold, Italic, Links, Spoilers and Buttons)',
   description='Everything about formatting scheduled Telegram posts: entities preserved from your drafts, spoiler markup, custom emoji, and inline URL buttons with simple syntax.',
   content=(
       "<p>Formatting is what separates a channel that looks professional from one "
       "that looks like a group chat. Fast Scheduler keeps every bit of it intact "
       "between scheduling and publishing.</p>"
       "<h3>Rich text survives the whole pipeline</h3>"
       "<p>Write a message anywhere — bold headlines, italic asides, "
       "<u>underlined</u> warnings, <s>struck-through</s> corrections, monospace "
       "code — and schedule it. Formatting is stored as Telegram <b>entities</b>, not "
       "flat text, so what publishes is pixel-identical to what you wrote: no "
       "mangled asterisks, no lost links, no broken emoji.</p>"
       "<h3>Spoilers</h3>"
       "<p>Wrap part of the text in spoiler markup and it publishes as a real "
       "Telegram spoiler — blurred until a reader taps it. Perfect for giveaways, "
       "answers, and sensitive details. The bot validates spoiler markup while you "
       "type, so unclosed pairs are caught at scheduling time, not in front of your "
       "audience.</p>"
       "<h3>Inline URL buttons</h3>"
       "<p>Add tappable buttons to any post with one syntax: "
       "<code>[Button Text](https://example.com)</code>. Use them for call-to-action "
       "links — &ldquo;Read the guide&rdquo;, &ldquo;Buy now&rdquo;, "
       "&ldquo;Join the chat&rdquo;. Buttons attach to text posts and to media posts "
       "alike. Keep button labels short (two or three words read best) and test one "
       "post before scheduling a whole campaign.</p>"
       "<h3>Custom emoji</h3>"
       "<p>Premium Telegram emoji in your drafts are preserved on publish, so your "
       "brand&rsquo;s custom smileys do not degrade into defaults.</p>"
       "<h3>Signatures: formatting that stamps itself</h3>"
       "<p>Configure a <b>signature</b> once — a footer with your links, hashtags or "
       "contact — and every scheduled post carries it automatically, on text and "
       "media alike. Signatures keep their own formatting, and you can override the "
       "signature per post when a particular message should go out clean.</p>"
       "<h3>A checklist for polished posts</h3>"
       "<ul>"
       "<li>One bold hook line first — most readers see only it in notifications.</li>"
       "<li>Links as buttons where possible; they out-click inline links.</li>"
       "<li>Spoilers for anything the reader should opt into.</li>"
       "<li>A signature so every post quietly advertises your next channel.</li>"
       "</ul>"),
   faq=[
       {'q': 'Does Telegram formatting survive scheduling in Fast Scheduler?',
        'a': 'Yes. Bold, italic, underline, strikethrough, code, links, spoilers and custom emoji are stored as Telegram entities and publish exactly as written.',
        'links': ['faq_schedule']},
       {'q': 'How do I add buttons to a scheduled Telegram post?',
        'a': 'Use the syntax [Button Text](https://your-link.com) in the message. The bot converts it into a tappable inline URL button on the published post.',
        'links': ['inline_buttons']},
       {'q': 'Can every scheduled post have an automatic signature?',
        'a': 'Yes. Create a signature once and it is appended to every scheduled and recurring post automatically, keeping its own formatting. Individual posts can override it.',
        'links': ['signature']},
   ],
   links=['inline_buttons', 'signature', 'faq_schedule', 'qa_signature_guide', 'qa_edit_scheduled_post'])

# --------------------------------------------------------------------- FAQ ---
_b('qa_what_is_fast_scheduler',
   category='faq',
   title='What Is Fast Scheduler? The Telegram Post Scheduling Bot Explained',
   description='Fast Scheduler is a Telegram bot that schedules and auto-publishes posts to your channels: queues, recurring messages, sender bots, statistics and backups. Here is the full picture.',
   content=(
       "<p><b>Fast Scheduler</b> (@FastSchedulerBot) is a Telegram bot that plans and "
       "publishes posts to your channels on a schedule — the missing native feature "
       "Telegram never shipped properly. You write content when inspiration strikes; "
       "the bot delivers it at the hour your audience actually reads.</p>"
       "<h3>How it works in three roles</h3>"
       "<ul>"
       "<li><b>The main bot</b> (@FastSchedulerBot) is your control room: every "
       "conversation, every schedule, every statistic happens here.</li>"
       "<li><b>Your channel</b> — connect it once by making the bots admins; the bot "
       "verifies rights and tracks it from then on.</li>"
       "<li><b>A sender bot</b> — a small bot of your own (created in @BotFather in "
       "two minutes) that actually publishes the posts, so your channel&rsquo;s "
       "byline is your brand, not ours. Connecting one is required: scheduling "
       "unlocks only after each channel has a sender bot.</li>"
       "</ul>"
       "<h3>What you can do with it</h3>"
       "<ul>"
       "<li><b>Schedule anything</b> — text, photos, videos, GIFs, voice, stickers, "
       "documents, polls, albums, with full formatting, spoilers and URL "
       "buttons.</li>"
       "<li><b>Recurring messages</b> — a post that repeats daily, weekly or on "
       "custom patterns without re-scheduling.</li>"
       "<li><b>Bulk import</b> — prepare a week of content in the SetDate companion "
       "bot and import it in one click.</li>"
       "<li><b>Statistics</b> — views, comments and reactions per channel, with "
       "leaderboards of your top posts.</li>"
       "<li><b>Team features</b> — admin permissions, shared channel limits, "
       "ownership transfer with confirmation phrases.</li>"
       "<li><b>Backups &amp; export</b> — encrypted .fspback backups, JSON/CSV "
       "exports, migration between accounts.</li>"
       "</ul>"
       "<h3>Free vs Premium, honestly</h3>"
       "<ul>"
       "<li><b>Free</b>: {channels_free} channel and sender bot, {scheduled_free} "
       "pending scheduled messages, {monthly_sent_free} sends per channel per month, "
       "{recurring_free} recurring message — enough to run one channel "
       "seriously.</li>"
       "<li><b>Premium ({premium_monthly}/mo or {premium_yearly}/yr)</b>: {channels_prem} channels and "
       "sender bots, unlimited scheduled queue, unlimited sends, unlimited recurring "
       "messages, bigger uploads ({max_media_prem}), leaderboards, backups, inline "
       "buttons and more.</li>"
       "</ul>"
       "<h3>Who it is for</h3>"
       "<p>News channels that publish on rhythm, creators who batch their week in "
       "one sitting, shops running drops at precise hours, and community managers "
       "who share channels with a team. If you have ever set a 3 a.m. alarm to post "
       "manually — this bot is the cure.</p>"
       "<p>Start here: open <a href=\"https://t.me/FastSchedulerBot?start=start__website_help\">"
       "@FastSchedulerBot</a>, press Start, connect your channel, pair a sender bot, "
       "and schedule your first post before your coffee cools.</p>"),
   faq=[
       {'q': 'Is Fast Scheduler free?',
        'a': 'Yes — the Free plan runs one channel with {scheduled_free} pending scheduled messages and {monthly_sent_free} sends per channel per month, forever. Premium at {premium_monthly}/mo lifts every cap and adds statistics leaderboards, backups and bigger uploads.',
        'links': ['limits_free', 'premium']},
       {'q': 'Why does Fast Scheduler need a sender bot?',
        'a': 'Your sender bot publishes the posts, so your channel’s byline is your own brand instead of a third-party bot. It is created by you in @BotFather and connected in two minutes.',
        'links': ['bot_sender']},
       {'q': 'Can Fast Scheduler send messages to a Telegram channel automatically?',
        'a': 'Yes. That is its core purpose: scheduled messages publish automatically at their set time through your sender bot, including media, formatting and buttons.',
        'links': ['qa_sender_bot_required', 'faq_schedule']},
   ],
   links=['qa_free_limits', 'qa_premium_worth', 'qa_which_plan', 'channels', 'bot_sender', 'setdate'])

print(f'[ok] {len(ARTICLES_B)} batch-2 articles defined')
