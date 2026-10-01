# -*- coding: utf-8 -*-
"""Web-only SEO article set for the Fast Scheduler Help Center.

These nodes do NOT exist in the bot's help tree — they are injected by
``website/_build/build_help.py`` at build time. Every claim is grounded in
``src/core/plans.py`` and the handler code; placeholders like {monthly_sent_free}
are filled automatically from ``get_help_kwargs()``.

Node shape (mirrors translations nodes):
    id, title, description (meta/SEO), content (HTML-lite: b/i/code/u/s, p, ul),
    faq: [{q, a}], links (related ids), category (parent category id).
"""

# NOTE: articles are plain strings so the module stays dependency-free.

SEO_ARTICLES = []

def _a(i, **kw):
    kw['id'] = i
    SEO_ARTICLES.append(kw)

# ============================================================ BACKUP & FILES ==
_a('qa_fsback_vs_fspback',
   category='backup',
   title='What Is the Difference Between .fsback and .fspback?',
   description='Fast Scheduler saves backups as .fsback or .fspback files. Here is exactly what each format contains, when to pick which, and how to restore them.',
   content=(
       "<p>Short answer: <b>both are the same complete backup</b> — the only difference is the "
       "<b>password</b>. A <code>.fspback</code> file is a password-protected <code>.fsback</code> "
       "file. The extra “p” stands for <i>protected</i>.</p>"
       "<h3>What each format is</h3>"
       "<ul>"
       "<li><b>.fsback</b> — a full backup of your Fast Scheduler data with <b>no password</b>. "
       "Anyone who gets the file can restore it, so treat it like a plain-text secret.</li>"
       "<li><b>.fspback</b> — the <b>same backup, encrypted</b>. Restoring asks for the password you "
       "set when creating it. Without the password the data inside cannot be read.</li>"
       "</ul>"
       "<p>When you tap <b>Create Backup</b> (or send <code>/backup</code>), the bot asks whether you "
       "want password protection. Choosing <b>no password</b> produces <code>.fsback</code>; setting a "
       "password (and an optional hint) produces <code>.fspback</code>. A Premium feature — backups are "
       "part of the <b>Export &amp; Backup</b> toolkit that unlocks with Premium.</p>"
       "<h3>What is inside either file</h3>"
       "<p>Both formats package your selected data — scheduled messages, recurring messages, settings, "
       "and more — into one archive you can download, store in the cloud, or move to another account. "
       "Media you saved in Media Storage is referenced, not re-uploaded, so files stay small.</p>"
       "<h3>Which one should you pick?</h3>"
       "<ul>"
       "<li>Restoring to your own account right now? <b>.fsback</b> is fine and faster to use.</li>"
       "<li>Keeping the file long-term, sending it to a teammate, or migrating to a new phone? "
       "<b>.fspback</b> — the password protects your scheduled content from strangers.</li>"
       "</ul>"
       "<h3>Restoring a file</h3>"
       "<p>Send <code>/import</code> to the bot, attach the <code>.fsback</code> or <code>.fspback</code> "
       "file, enter the password if asked, then choose <b>Overwrite</b> (replace current data) or "
       "<b>Add</b> (merge with current data). Export a fresh backup before you overwrite anything.</p>"),
   faq=[
       {'q': 'Is .fspback more secure than .fsback?',
        'a': 'Yes. A .fspback file is encrypted with the password you set; a .fsback file is not protected at all. If the backup contains bot tokens or private content, prefer .fspback.',
        'links': ['backup_password']},
       {'q': 'I lost the password to my .fspback file. Can it be recovered?',
        'a': 'No. The password cannot be reset or bypassed — not even by support. Keep the password (and the hint you optionally set) together with the file. Without it the backup is unreadable.',
        'links': ['backup_restore']},
       {'q': 'Can I convert .fsback to .fspback (or back)?',
        'a': 'Indirectly: restore the .fsback file into your account, then create a new backup and choose password protection to get a .fspback file. There is no direct file-conversion command.',
        'links': ['backup_create']},
       {'q': 'Which formats can I import besides these?',
        'a': 'Imports also accept .json, .csv, .txt, .rtf and .odt files (and SetDate bundles). Those carry messages only, while .fsback/.fspback carry your full configuration.',
        'links': ['import_formats']},
   ],
   links=['backup_create', 'backup_password', 'backup_restore', 'import_formats'])

_a('qa_backup_full_guide',
   category='backup',
   title='How to Back Up All Scheduled Posts in Telegram (and Restore Them Anywhere)',
   description='A complete, human-friendly guide to backing up scheduled Telegram posts with Fast Scheduler: what gets saved, password protection, cloud storage of files, and clean restore.',
   content=(
       "<p>Rebuilding a month of scheduled posts by hand is nobody's idea of fun. Fast Scheduler's "
       "backup system exists so you never have to: one file captures everything, and restoring it on "
       "any account takes about a minute.</p>"
       "<h3>What a backup contains</h3>"
       "<p>A <code>.fsback</code> / <code>.fspback</code> file packages the parts of your account you "
       "select — typically:</p>"
       "<ul>"
       "<li><b>Scheduled messages</b> — every queued post with its exact send time.</li>"
       "<li><b>Recurring messages</b> — repeat rules (daily, weekly, custom intervals) and their "
       "expiry settings.</li>"
       "<li><b>Settings</b> — language, time zone, signatures, channel preferences.</li>"
       "<li><b>Media Storage references</b> — saved photos, videos and documents with their boxes.</li>"
       "</ul>"
       "<p>What is <b>not</b> included: user backups exclude sender-bot tokens, "
       "and payment history never leaves Telegram's systems. The export screen "
       "lets you review what goes into the file before you confirm.</p>"
       "<h3>Creating a backup — step by step</h3>"
       "<p>Backups are a <b>Premium</b> feature. With Premium active:</p>"
       "<ul>"
       "<li>1. Open the menu → <b>Data</b> → <b>Export</b> (or send <code>/backup</code>).</li>"
       "<li>2. Pick what to include (scheduled, recurring, all).</li>"
       "<li>3. Choose <b>password protection</b>: none for <code>.fsback</code>, or set a password + "
       "hint for <code>.fspback</code>.</li>"
       "<li>4. The bot packs the archive and sends the file. Save it somewhere real — cloud drive, "
       "local disk, anywhere that survives losing your phone.</li>"
       "</ul>"
       "<h3>Restoring — the safe way</h3>"
       "<p>Send <code>/import</code>, attach the file, enter the password if prompted. The bot then "
       "asks how to apply it:</p>"
       "<ul>"
       "<li><b>Overwrite</b> — replaces your current data with the backup's content. Anything not in "
       "the backup disappears.</li>"
       "<li><b>Add</b> — merges the backup into your current data, keeping what you already have.</li>"
       "</ul>"
       "<p><b>Golden rule:</b> export a fresh backup <i>before</i> restoring an older one. It is your "
       "undo button if the result surprises you.</p>"
       "<h3>Good backup habits</h3>"
       "<ul>"
       "<li>Take a fresh backup before deleting a channel, rotating a bot, or bulk-editing posts.</li>"
       "<li>Keep at least one <code>.fspback</code> with a strong password — shared drives get opened "
       "by more people than you think.</li>"
       "<li>After switching phones or accounts, restore + verify the Message List before the real "
       "posting week starts.</li>"
       "</ul>"),
   faq=[
       {'q': 'Is backup free or Premium?',
        'a': 'Creating .fsback/.fspback backups is part of the Export & Backup toolkit, which requires Premium. Importing files (/import) works on Free, so anyone can restore a backup received from someone else.',
        'links': ['premium_buy']},
       {'q': 'Where should I store the backup file?',
        'a': 'Anywhere outside Telegram: a cloud drive, your computer, or an encrypted notes app. Telegram keeps the file in your chat too, but Saved Messages is not a backup strategy.',
        'links': ['backup_download']},
       {'q': 'How big is a backup file?',
        'a': 'Small — usually kilobytes to a few megabytes, because media is referenced rather than embedded. Text and schedules compress extremely well.',
        'links': ['backup_size']},
       {'q': 'Can I move my schedules to another Telegram account?',
        'a': 'Yes. Create a backup on the old account, log into the new one, connect the channel and a sender bot, then restore the backup with Add mode. This is the standard migration path.',
        'links': ['faq_migration']},
   ],
   links=['qa_fsback_vs_fspback', 'backup_create', 'backup_restore', 'import_data'])

# ============================================================ MIGRATION =======
_a('qa_move_channel_account',
   category='faq',
   title='How to Move Fast Scheduler to a New Phone or Another Telegram Account',
   description='Step-by-step migration guide: back up, reconnect the channel and sender bot, restore schedules on a new device or account — without losing posting times.',
   content=(
       "<p>Fast Scheduler stores your schedules in the cloud (on the bot's server), not on your "
       "phone. That makes moving house surprisingly painless — the only thing that really matters "
       "is <b>which Telegram account owns the schedules</b>.</p>"
       "<h3>Same account, new phone</h3>"
       "<p>Do nothing. Open Telegram on the new phone, log in, and chat with "
       "<b>@FastSchedulerBot</b> — your channels, bots, schedules and settings are exactly where you "
       "left them. There is no local app and nothing to sync.</p>"
       "<h3>Different account (new number, team handover, second project)</h3>"
       "<p>Schedules belong to the Telegram account that created them, so a new account starts empty. "
       "The clean path:</p>"
       "<ul>"
       "<li>1. On the old account: <code>/backup</code> → include everything → save the "
       "<code>.fsback</code>/<code>.fspback</code> file.</li>"
       "<li>2. On the new account: <code>/start</code> the bot, connect the <b>channel</b>, then pair "
       "its <b>sender bot</b> (this is mandatory — the sender bot is what actually posts).</li>"
       "<li>3. Send <code>/import</code> with the backup file, choose <b>Add</b> or <b>Overwrite</b>.</li>"
       "<li>4. Check the Message List and Calendar; confirm the time zone matches, then skim the first "
       "few upcoming posts.</li>"
       "</ul>"
       "<p>If you are on Free and your setup has more than one channel, temporarily move the extra "
       "channels out or upgrade — the restore brings everything over, but Free limits apply on the "
       "new account.</p>"
       "<h3>Handing a channel to someone else permanently</h3>"
       "<p>The same flow works for handovers: the new owner connects their own account to the same "
       "channel (they need admin rights in it), pairs a sender bot, and imports the backup you send "
       "them. After they confirm the Message List looks right, you can delete your own schedules to "
       "avoid double-posting — <b>two accounts scheduling the same channel will post twice</b>.</p>"),
   faq=[
       {'q': 'Will my schedules keep firing while I migrate?',
        'a': 'Yes — the old account keeps posting until you delete its schedules or the channel/bot setup changes. Pause or delete there before going live on the new account to avoid duplicates.',
        'links': ['qa_duplicate_posts']},
       {'q': 'Do I need Premium on the new account to restore?',
        'a': 'No. Importing a backup is free. Premium is only needed for creating backups and for the extra channels/bots the backup may contain.',
        'links': ['premium_buy']},
   ],
   links=['qa_fsback_vs_fspback', 'qa_duplicate_posts', 'getting_started', 'faq_migration'])

# ============================================================ SCHEDULING =====
_a('qa_duplicate_posts',
   category='faq',
   title='Why Is My Telegram Channel Posting Twice? (Duplicate Posts, Explained)',
   description='Duplicated scheduled posts almost always mean two schedulers own the channel, or a sender bot got re-added. Here is how to find the cause and stop double-posting.',
   content=(
       "<p>Double posts are annoying for subscribers and make a channel look automated in the worst "
       "way. The good news: the cause is nearly always one of four things.</p>"
       "<h3>1. Another account still schedules the channel</h3>"
       "<p>The most common cause after a migration or team handover: the old account's schedules were "
       "never removed. Both accounts happily queue posts for the same time. Fix: in the <i>other</i> "
       "account, open <b>Message List</b> and delete its schedules (or disconnect the channel). If you "
       "cannot access the old account, remove the bot from the channel's admin list — that stops the "
       "posting immediately.</p>"
       "<h3>2. Two sender bots are admin in the channel</h3>"
       "<p>Every channel must pair with exactly one sender bot, and that bot should be the only bot "
       "with posting rights. If you created a second bot and added it as admin, posts may arrive from "
       "both. Keep one sender bot per channel as admin; remove extra bots from the channel.</p>"
       "<h3>3. The message got scheduled twice</h3>"
       "<p>Easy to do when re-sending the same text after an edit, or when importing while old "
       "schedules exist. Open the Message List for the day and scan for same-time twins before the "
       "posting window. The <b>Calendar</b> view makes clusters obvious.</p>"
       "<h3>4. The recurrence rule was duplicated, not edited</h3>"
       "<p>Creating a new daily rule instead of editing the existing one produces two identical posts "
       "every day. Check the recurring list — if two rules share the same text and time, delete one.</p>"
       "<h3>Still posting twice?</h3>"
       "<p>Send <code>/stats</code> to see what is queued, then use <code>/feedback</code> with the "
       "channel name and two timestamps of a duplicate pair. Support can trace which connection "
       "produced each post.</p>"),
   faq=[
       {'q': 'Does Fast Scheduler retry a post that failed, causing doubles?',
        'a': 'A retry only happens when the send did not confirm. If Telegram accepted the post but the confirmation was lost (rare network hiccup), you can get one duplicate. It does not re-send confirmed posts.',
        'links': ['errors']},
       {'q': 'Can I merge two accounts scheduling the same channel?',
        'a': 'Yes — export from the old account, import with Add on the new one, then clear the old account. Never leave both active.',
        'links': ['qa_move_channel_account']},
   ],
   links=['qa_move_channel_account', 'multichannel', 'errors', 'tools'])

_a('qa_timezones',
   category='timezone',
   title='Why Did My Post Go Out at the Wrong Time? Time Zones, Explained Simply',
   description='Scheduled posts firing an hour early or late? The channel time zone, daylight-saving shifts, and per-channel settings explain 99% of these surprises.',
   content=(
       "<p>“I scheduled 9:00 and it posted at 12:00” — before anything else, check which clock the "
       "number 9:00 belongs to. Fast Scheduler schedules posts in a <b>time zone</b>, and the zone "
       "that matters is the one set for the channel, not the one on your watch.</p>"
       "<h3>How the bot decides “when 9:00 is”</h3>"
       "<ul>"
       "<li>Every channel has a <b>time zone setting</b>. When you schedule 9:00, the bot stores "
       "9:00 in the channel's zone and converts it to UTC behind the scenes.</li>"
       "<li>If the zone is <b>UTC</b> (the default) and you are in, say, New York, your 9:00 local is "
       "13:00 or 14:00 UTC — the post will “move” by 4–5 hours from your point of view.</li>"
       "<li>Set the channel's zone to your own city once, and from then on 9:00 means <i>your</i> 9:00, "
       "every time.</li>"
       "</ul>"
       "<h3>The daylight-saving trap</h3>"
       "<p>Zones that observe DST shift twice a year. A post scheduled for 9:00 in March may land at "
       "8:00 or 10:00 relative to the wall clock in November, depending on how the zone handles the "
       "shift. If your audience notices a one-hour drift in spring or autumn, that is why. The "
       "schedule did not break — the zone's definition of 9:00 changed. Reschedule around the shift "
       "week if you post at a strict local hour.</p>"
       "<h3>Checking and fixing the zone</h3>"
       "<p>Open <b>Time Zone</b> in the bot (or <code>/timezone</code>), pick the channel, and choose "
       "the city/zone that matches your audience — the list uses proper zone names like "
       "<code>Europe/Berlin</code>, so DST is handled by the same rules your phone uses. Upcoming "
       "posts keep their stored times; only <i>new</i> schedules use the new zone, so double-check "
       "anything queued for the same day you change it.</p>"
       "<h3>Quick diagnosis table</h3>"
       "<ul>"
       "<li><b>Off by a whole number of hours, constant</b> — wrong zone set for the channel.</li>"
       "<li><b>Off by one hour, only in spring/autumn</b> — DST shift; the zone is working correctly.</li>"
       "<li><b>Off by a few minutes, growing over weeks</b> — rare; send <code>/feedback</code> with "
       "two examples.</li>"
       "</ul>"),
   faq=[
       {'q': 'Does changing the time zone move my scheduled posts?',
        'a': 'No. Existing posts keep their stored times; the new zone applies to schedules you create afterwards. Verify the next few posts after changing the zone.',
        'links': ['timezone_set']},
       {'q': 'What time zone should I pick for an international audience?',
        'a': 'Pick the zone of your largest audience segment, or UTC if you think in UTC. Consistency matters more than the specific zone.',
        'links': ['timezone_list']},
   ],
   links=['timezone_set', 'timezone_list', 'errors'])

_a('qa_edit_scheduled_post',
   category='scheduling',
   title='Can I Edit a Scheduled Post After Scheduling It?',
   description='Yes — text, media, and send time all stay editable until the moment the post goes out. Here is what can be changed, what cannot, and how retries work.',
   content=(
       "<p>Nothing about a scheduled post is carved in stone. Until the moment Telegram accepts the "
       "send, every part of it can change — that is the whole point of keeping a queue instead of "
       "posting immediately.</p>"
       "<h3>What you can change</h3>"
       "<ul>"
       "<li><b>Text and formatting</b> — fix a typo, rewrite the hook, add links. Bold, italic, "
       "underline, strikethrough, spoilers and code all survive edits.</li>"
       "<li><b>Media</b> — swap the image, replace the video, add or remove an album item.</li>"
       "<li><b>Send time</b> — move the post earlier or later, or to another day entirely.</li>"
       "<li><b>Target channel</b> — re-point a post to a different connected "
       "channel.</li>"
       "</ul>"
       "<p>Open the <b>Message List</b> (or <code>/list</code>), tap the post, choose <b>🔄 Replace</b>. "
       "The familiar schedule flow reopens with the post's current content pre-filled — change what "
       "you need and confirm.</p>"
       "<h3>What editing cannot do</h3>"
       "<ul>"
       "<li><b>Change a post that already published.</b> Once the sender bot delivers the message to "
       "Telegram, it is a normal Telegram message — edit it with Telegram's own tools, not here.</li>"
       "<li><b>Edit recurring posts “in place”.</b> A recurring rule is a single template that "
       "fires on its pattern — there are no separate per-day copies. Edit the "
       "<i>rule</i> so all future sends change.</li>"
       "</ul>"
       "<h3>A workflow that actually works</h3>"
       "<p>Channel operators who stay sane usually: schedule the week on Sunday, review the Calendar "
       "Monday, and treat edit as the normal verb — improving copy as the news moves. Edits are free, "
       "instant, and never notify subscribers. The only deadline is the send time itself.</p>"),
   faq=[
       {'q': 'How late can I edit a post?',
        'a': 'Any time before the send moment. If the bot is mid-delivery, the edit may not apply — that is the only race. For a post due within seconds, delete and reschedule instead.',
        'links': ['edit']},
       {'q': 'Can I edit a post that already went out?',
        'a': 'Not from the bot — it is a regular Telegram message now. Telegram itself lets admins edit posted messages in channels; use Telegram for that.',
        'links': ['delete']},
       {'q': 'Does editing reset the monthly send counter?',
        'a': 'No. The counter counts actual sends, not edits. Editing costs nothing.',
        'links': ['limit_daily']},
   ],
   links=['edit', 'delete', 'recurring', 'tools'])

# ============================================================ LIMITS =========
_a('qa_free_limits',
   category='limits',
   title='What Do I Get With Fast Scheduler for Free? (Exact Limits)',
   description='The complete Free plan breakdown: 1 channel, 1 sender bot, 100 pending scheduled messages, 100 sends per channel monthly, 1 recurring rule, storage and media caps.',
   content=(
       "<p>Free is a real plan, not a trial — it never expires and has no daily caps. Here is exactly "
       "what you get, with numbers you can plan around.</p>"
       "<h3>The numbers</h3>"
       "<ul>"
       "<li><b>{channels_free} channel</b> with <b>{bots_free} sender bot</b>.</li>"
       "<li><b>Up to {scheduled_free} scheduled messages pending at once</b> — your working queue. "
       "As posts go out, space frees up; this is not a monthly allowance.</li>"
       "<li><b>{monthly_sent_free} sent messages per channel per calendar month</b> — the actual "
       "sending quota. Resets on the 1st.</li>"
       "<li><b>{recurring_free} recurring message</b> — one repeating rule (daily, weekly, every N "
       "hours…). Recurring rules on Free expire after {recurring_expiry_days} days and need "
       "re-confirming.</li>"
       "<li><b>Media Storage: {storage_count_free} box with {storage_items_free} items</b>, no video "
       "in storage.</li>"
       "<li><b>Uploads up to {max_media_free}</b>, videos {videos_msg_free}.</li>"
       "</ul>"
       "<h3>What “100/month per channel” means in practice</h3>"
       "<p>If you post 3 times a day, that is ~90 posts a month — Free covers a light daily cadence "
       "on one channel. Posting 5+ times a day, or running several channels, is where Premium starts "
       "to make sense. The counter counts <i>sends by the sender bot</i>; edits, previews and deleted "
       "schedules are free.</p>"
       "<h3>There is no daily cap</h3>"
       "<p>Older versions of the bot had daily limits; they are gone. On Free you can schedule and "
       "send every single day — the only quotas are the pending-queue size and the monthly send "
       "count. Check both any time with <code>/stats</code>.</p>"
       "<h3>Hitting a limit gracefully</h3>"
       "<p>The queue limit blocks <i>new</i> schedules, never deletes old ones; the monthly cap "
       "pauses sends until the 1st (the bot tells you). Both warn you in advance with clear messages "
       "and a one-tap upgrade path. Nothing is silently dropped.</p>"),
   faq=[
       {'q': 'Do unused sends carry over to next month?',
        'a': 'No. The monthly counter resets to zero on the 1st; unused sends do not roll over. The pending-queue space is also not a quota to “use up” — it just caps how far ahead you can stockpile.',
        'links': ['limit_daily']},
       {'q': 'Is the free plan time-limited or feature-crippled?',
        'a': 'It never expires. Scheduling, recurring, statistics, search and the calendar all work on Free. Premium removes quantity limits and adds the Export/Backup toolkit, signatures and bigger media.',
        'links': ['premium']},
       {'q': 'How do I check my current usage?',
        'a': 'Send /stats. It shows your queue size, monthly sends, recurring rules and storage at a glance.',
        'links': ['statistics']},
   ],
   links=['limit_daily', 'limit_scheduled', 'premium', 'statistics'])

_a('qa_premium_worth',
   category='premium',
   title='Is Fast Scheduler Premium Worth It? An Honest Breakdown',
   description='What Premium actually unlocks — 3 channels, unlimited queue and sends, unlimited recurring, 50MB video, signatures, export/backup — and who genuinely needs it.',
   content=(
       "<p>Premium costs {premium_monthly} a month (or {premium_yearly} a year) and removes the ceiling on almost "
       "everything Free limits. Here is an honest map of who needs which part.</p>"
       "<h3>What Premium changes, concretely</h3>"
       "<ul>"
       "<li><b>{channels_prem} channels, {bots_prem} sender bots</b> — run a network (main channel, "
       "announcements, chat-announcements mirror) from one account.</li>"
       "<li><b>Unlimited scheduled queue and unlimited sends</b> — no {scheduled_free}-post queue, no "
       "monthly cap on any channel.</li>"
       "<li><b>Unlimited recurring rules</b> — and they never expire; Free's single rule stops after "
       "{recurring_expiry_days} days.</li>"
       "<li><b>Bigger media</b>: uploads to {max_media_prem}, video to {videos_msg_prem}, "
       "{storage_count_prem} storage boxes × {storage_items_prem} items <i>with video allowed</i>, "
       "plus 4K-photo handling and higher bitrate media that Free compresses harder.</li>"
       "<li><b>Signatures</b> — a footer (credit, promo, hashtags) auto-appended to every post of a "
       "channel.</li>"
       "<li><b>Export &amp; Backup toolkit</b> — <code>.fsback</code>/<code>.fspback</code> backups, "
       "JSON/CSV/TXT/RTF/ODT exports: own your content.</li>"
       "</ul>"
       "<h3>Who does not need it</h3>"
       "<p>One channel, a couple of posts a day, no video-heavy content — Free covers that "
       "indefinitely. Premium's first meaningful gate for such a setup would be the monthly send cap, "
       "and even that takes ~4 posts/day to hit.</p>"
       "<h3>Who feels the difference on day one</h3>"
       "<ul>"
       "<li><b>Multi-channel admins</b> — the 3×3 pairing is the headline feature.</li>"
       "<li><b>Video channels</b> — 25MB → 50MB video and video-in-storage change the workflow.</li>"
       "<li><b>Anyone whose content is their business</b> — backups and full exports are the "
       "difference between “my queue” and “my archive”.</li>"
       "<li><b>Automation lovers</b> — unlimited recurring rules turn the bot into a true "
       "publishing engine.</li>"
       "</ul>"
       "<h3>Terms worth knowing</h3>"
       "<p>Premium attaches to your Telegram account, covers all your channels at once, and can be "
        "paid with Telegram Stars. Multi-month terms cost less per month (3/6-month "
        "discounts), and if something goes wrong the refund policy is linked in the footer — premium "
        "status is visible any time with <code>/premium</code>.</p>"),
   faq=[
       {'q': 'Does Premium apply to all my channels or per channel?',
        'a': 'Per account. One subscription unlocks the higher limits for every channel you connect while it is active.',
        'links': ['premium_buy']},
       {'q': 'What happens to my schedules when Premium expires?',
        'a': 'Nothing is deleted. Limits revert to Free: extra channels/bots beyond 1×1 stop scheduling until you disconnect them or renew, the queue cap applies again, and recurring rules beyond the first pause.',
        'links': ['premium_expiry']},
        {'q': 'Can I pay with Telegram Stars?',
         'a': 'Yes — Stars are billed at the official rate and are currently the only payment method. The Premium menu always shows current prices.',
         'links': ['payment_stars']},
   ],
   links=['premium', 'premium_buy', 'qa_free_limits', 'signature'])

# ============================================================ CHANNELS =======
_a('qa_add_channel_guide',
   category='channels',
   title='How to Connect a Telegram Channel to Fast Scheduler (Full Walkthrough)',
   description='Every step to connect a channel: admin rights the bot needs, public vs private channels, invite links, sender bot pairing, and fixing the classic errors.',
   content=(
       "<p>Connecting a channel is a two-part handshake: the bot needs <b>admin rights in the "
       "channel</b>, and the channel needs to be <b>registered in the bot</b>. Here is the whole "
       "dance, including the steps people miss.</p>"
       "<h3>Part 1 — make the bot an admin of your channel</h3>"
       "<ul>"
       "<li>1. Open your channel in Telegram → <b>Manage Channel</b> → <b>Administrators</b> → "
       "<b>Add Admin</b>.</li>"
       "<li>2. Search for <b>@FastSchedulerBot</b> and add it.</li>"
       "<li>3. Give it at least <b>Post Messages</b>. If you plan to schedule on behalf of other "
       "admins or use anonymous admin, keep the defaults sane.</li>"
       "</ul>"
       "<h3>Part 2 — register the channel in the bot</h3>"
       "<ul>"
       "<li>1. In the bot, tap <b>Connect Channel</b>.</li>"
       "<li>2. Give the bot what it asks for — any of these works:"
       "<ul>"
       "<li>the channel's <b>@username</b> for public channels,</li>"
       "<li>a <b>forwarded message</b> from the channel,</li>"
       "<li>an <b>invite link</b> (<code>t.me/+…</code> or <code>t.me/joinchat/…</code>) for private "
       "channels.</li>"
       "</ul></li>"
       "<li>3. Confirm. The bot verifies that it really is an admin there.</li>"
       "</ul>"
       "<h3>Part 3 — pair the sender bot (mandatory)</h3>"
       "<p>Every channel needs a <b>sender bot</b> — your own bot created via @BotFather — before "
       "anything can be scheduled. This is not optional: the sender bot is the account that actually "
       "<i>publishes</i> your posts, under its name. Fast Scheduler's main bot coordinates the "
       "schedule; the sender bot delivers. The in-bot wizard creates and pairs one in a minute; see "
       "the sender-bots guide for the detailed flow.</p>"
       "<h3>The classic errors, decoded</h3>"
       "<ul>"
       "<li><b>“Channel not found”</b> — typo in the username, or the bot was not added as admin "
       "<i>before</i> you tried to connect. Add first, then connect.</li>"
       "<li><b>“Not an admin”</b> — the admin rights were granted to a different bot than the one "
       "you connected.</li>"
       "<li><b>“Invalid token”</b> — the sender-bot token got truncated on copy. Copy the whole "
       "thing: digits, colon, the rest.</li>"
       "</ul>"),
   faq=[
       {'q': 'Can I connect a private channel?',
        'a': 'Yes — via invite link or by forwarding any message from the channel during connection. Public username is not required.',
        'links': ['channel_add']},
       {'q': 'Why do I need my own bot just to post?',
        'a': 'Telegram architecture: messages in a channel are sent by a bot account, not by your user account. Pairing your own sender bot also means posts appear under your brand, not a generic one.',
        'links': ['bot_sender']},
       {'q': 'The channel connects but posts fail. First checks?',
        'a': 'Sender bot still admin? Post Messages permission on? Bot not revoked in @BotFather? Those three cover nearly all post failures.',
        'links': ['errors']},
   ],
   links=['channel_add', 'bot_add', 'bot_sender', 'qa_sender_bot_required'])

_a('qa_sender_bot_required',
   category='bots',
   title='Do You Need a Sender Bot to Schedule Posts? (Yes — Here Is Why)',
   description='Fast Scheduler requires a sender bot for every channel: what it does, why the main bot cannot post alone, how to create one in 60 seconds, and security notes.',
   content=(
       "<p>Short answer: <b>yes</b> — a sender bot is required for scheduling and sending. The "
       "scheduling menu stays locked until every connected channel has one paired. Here is the why "
       "and the 60-second setup.</p>"
       "<h3>Why the main bot cannot just post itself</h3>"
       "<p>Two reasons, one technical and one yours:</p>"
       "<ul>"
       "<li><b>Architecture:</b> channel posts are delivered by a bot account with admin rights. If "
       "@FastSchedulerBot delivered them, every message on every customer channel would carry the "
       "same name — and one bot hitting rate limits would slow thousands of channels.</li>"
       "<li><b>Your brand:</b> with your own sender bot, posts appear from <i>your</i> bot's name and "
       "avatar. Subscribers see your brand, and your bot's admin rights are yours to revoke.</li>"
       "</ul>"
       "<h3>Creating one in 60 seconds</h3>"
       "<ul>"
       "<li>1. Open <b>@BotFather</b> → <code>/newbot</code> → pick a name and username.</li>"
       "<li>2. Copy the token (digits, colon, letters — the whole string).</li>"
       "<li>3. In Fast Scheduler: <b>Bots</b> → <b>➕ Add Another Bot</b>, pick the channel when asked, paste the token. Pairing is automatic.</li>"
       "<li>4. Make the new bot an <b>admin</b> of the channel with <b>Post "
       "Messages</b> permission — or let Fast Scheduler promote it automatically when it can. Scheduling unlocks instantly.</li>"
       "</ul>"
       "<p>The in-bot wizard walks these exact steps and checks each one, so you cannot get the "
       "order wrong.</p>"
       "<h3>Security, briefly</h3>"
       "<p>Your token is stored encrypted and used only to deliver your posts. You can rotate it any "
       "time via @BotFather (<code>/revoke</code>) and update it in the bot — or remove the bot "
       "entirely, which deletes the token from Fast Scheduler's storage. If a token leaks, revoke it "
       "in BotFather first; a revoked token is dead everywhere.</p>"
       "<h3>One bot per channel (Premium: 3×3)</h3>"
       "<p>Free pairs {bots_free} sender bot with {channels_free} channel; Premium allows "
       "{bots_prem} bots across {channels_prem} channels. Multiple channels can share one sender "
       "bot, but the clean setup — one bot per channel — keeps branding separate and failures "
       "isolated.</p>"),
   faq=[
       {'q': 'Can one sender bot serve two channels?',
        'a': 'Yes, a sender bot can be paired with multiple channels you own. One bot per channel is still recommended for cleaner branding and simpler troubleshooting.',
        'links': ['bot_fleet']},
       {'q': 'What happens if I remove the sender bot from the channel?',
        'a': 'Scheduling locks (no sender paired for that channel) and queued sends fail until you re-add the bot as admin. The schedules themselves stay saved.',
        'links': ['bot_remove']},
       {'q': 'Is my bot token safe with Fast Scheduler?',
        'a': 'Tokens are stored encrypted and never displayed in full after saving. Rotating the token in @BotFather instantly invalidates the old one everywhere.',
        'links': ['bot_rotate']},
   ],
   links=['bot_add', 'bot_sender', 'qa_add_channel_guide', 'bot_permissions'])

# ============================================================ TOOLS/QA =======
_a('qa_schedule_many_at_once',
   category='scheduling',
   title='How to Schedule Many Telegram Posts at Once (Bulk Workflow)',
   description='Three proven ways to schedule in bulk: SetDate import for prepared batches, recurring rules for repeatable slots, and the queue workflow for content weeks.',
   content=(
       "<p>Scheduling one post at a time is fine for a meme; for a content calendar you want "
       "<b>batch</b> workflows. Fast Scheduler gives you three, and a full week can be set up in "
       "minutes.</p>"
       "<h3>Way 1 — import a batch with SetDate</h3>"
       "<p>The <b>SetDate bot</b> is the bulk tool: prepare messages as a set (text, times), then "
       "import them into Fast Scheduler in one click. It shines when you write copy in advance or "
       "migrate from another scheduler. Prepare → import → review in the Message List → done.</p>"
       "<h3>Way 2 — let recurring rules do the repeating</h3>"
       "<p>Anything that repeats should be a <b>rule</b>, not N one-off posts: “every day at 9:00”, "
       "“Mondays 18:30”, “every 6 hours”. Premium users get unlimited rules and no expiry; Free has "
       "one rule. Combined with a signature, a daily digest literally runs itself.</p>"
       "<h3>Way 3 — stock the queue ahead</h3>"
       "<p>The queue lets you stack up to {scheduled_free} pending posts on Free (unlimited on "
       "Premium). The classic pattern: one writing session → schedule the whole week → check the "
       "<b>Calendar</b> view for holes and collisions → go live your life. Edits are free and instant, "
       "so the queue is your draft folder as much as your pipeline.</p>"
       "<h3>Checking your work</h3>"
       "<p>Three tools keep bulk work honest:</p>"
       "<ul>"
       "<li><b>Calendar</b> — month at a glance; tap a day to see that day's posts.</li>"
       "<li><b>Message List</b> — per-channel queue with previews; catch same-time twins here.</li>"
       "<li><b>Search</b> — keyword search across everything scheduled, with per-result preview and edit "
       "for cleanup.</li>"
       "</ul>"),
   faq=[
       {'q': 'Is there a true “upload a CSV of posts” feature?',
        'a': 'Close: SetDate handles prepared batches, and /import accepts .json/.csv/.txt/.rtf/.odt files of messages. For calendar-scale bulk entry, SetDate is the intended tool.',
        'links': ['setdate', 'import_formats']},
       {'q': 'How far ahead can I schedule?',
        'a': 'As far as your queue limit allows — up to 100 pending posts on Free, unlimited on Premium. Times years out are fine.',
        'links': ['limit_scheduled']},
   ],
   links=['setdate', 'recurring', 'qa_edit_scheduled_post', 'tools'])

# ============================================================ TELEGRAM FAQ ====
_a('tg_channels_explained',
   category='faq',
   title='Telegram Channels vs Groups vs Bots: The Difference That Actually Matters',
   description='A plain-English explainer of Telegram channel, group and bot roles — written for people who schedule content, with practical notes on admin rights and posting.',
   content=(
       "<p>Telegram has three kinds of “places”, and content creators mix them up constantly. "
       "Here is the mental model that sticks.</p>"
       "<h3>A channel is a megaphone</h3>"
       "<p>One-way broadcasting: admins post, subscribers read. No reply threads by default "
       "(though a discussion group can be attached), unlimited subscribers, and posts carry the "
       "<b>channel's</b> name — or the name of the posting bot if “Sign messages with a bot” is "
       "on. Channels are where scheduled content lives.</p>"
       "<h3>A group is a campfire</h3>"
       "<p>Everyone talks. Groups are for community; up to 200k members in supergroups, full message "
       "history, topics if enabled. You do not “schedule to a group” the way you do to a channel — "
       "that is what channels are for.</p>"
       "<h3>A bot is a worker</h3>"
       "<p>Bots are accounts run by software. In your channel's context, a bot is the <b>hands</b> "
       "that type the message: a bot must be an admin with <b>Post Messages</b> for anything to be "
       "published. That is exactly why Fast Scheduler pairs a sender bot with your channel — your "
       "bot posts, under your brand.</p>"
       "<h3>Why this matters for scheduling</h3>"
       "<ul>"
       "<li>Want posts to appear at fixed times? <b>Channel + scheduler + sender bot.</b></li>"
       "<li>Want subscribers to discuss the posts? Attach a <b>linked discussion group</b> to the "
       "channel — comments live there automatically.</li>"
       "<li>Want automation, menus, and commands? That is the <b>bot</b> layer — the part Fast "
       "Scheduler turns into a full publishing workflow.</li>"
       "</ul>"
       "<p>One nuance worth knowing: Telegram shows <i>signed</i> posts as “via bot” only when the "
       "admin chooses to sign with the bot; otherwise the post simply appears under the channel "
       "name. Either way, the sender bot did the typing.</p>"),
   faq=[
       {'q': 'Can a scheduled post go to a group?',
        'a': 'Fast Scheduler targets channels (including chat-announcement channels). Groups are conversational — schedule announcements to a channel instead.',
        'links': ['channels']},
       {'q': 'Do subscribers see which bot posted?',
        'a': 'By default a channel post shows just the channel name. If the channel enables signing posts with the admin bot, the sender bot is credited.',
        'links': ['qa_sender_bot_required']},
   ],
   links=['channels', 'qa_sender_bot_required', 'tg_best_posting_times'])

_a('tg_best_posting_times',
   category='tips',
   title='The Best Times to Post in Telegram (and How to Test Them Properly)',
   description='Evidence-based posting windows for Telegram channels by audience type, why consistency beats perfect timing, and how to A/B test slots with scheduled posts.',
   content=(
       "<p>“Post at 9:00” advice is usually recycled guesswork. Here is what actually moves the "
       "needle on Telegram, plus a testing method you can run with a scheduler in one week.</p>"
       "<h3>Windows that generally work</h3>"
       "<ul>"
       "<li><b>Morning commute</b> — 8:00–10:00 local time. News, digests, “start of day” content.</li>"
       "<li><b>Lunch dip</b> — 12:30–14:00. Light, skimmable posts do well.</li>"
       "<li><b>Evening prime time</b> — 19:00–22:00. The strongest window for most channels; "
       "long-form and media belong here.</li>"
       "</ul>"
       "<p>The key word is <b>local</b>. If your audience spans zones, anchor to your largest "
       "cluster's evening, and let the channel's time zone setting do the conversion for you.</p>"
       "<h3>Consistency beats cleverness</h3>"
       "<p>Subscribers learn your rhythm. A channel that posts daily at 9:00 trains its audience to "
       "show up at 9:00 — measurable in view-rate stability. This is the strongest argument for "
       "scheduling (and recurring rules) over manual posting: the schedule becomes a product "
       "feature.</p>"
       "<h3>How to test slots properly</h3>"
       "<ul>"
       "<li>1. Pick two candidate slots (e.g. 9:00 vs 20:00) and alternate similar content between "
       "them for 7–10 days.</li>"
       "<li>2. Compare <b>views in the first hour</b>, not totals — that is when your regulars "
       "arrive. Fast Scheduler's statistics screen shows view dynamics per post.</li>"
       "<li>3. Keep the winner as a recurring rule, and re-test quarterly. Audiences drift with "
       "seasons and habits.</li>"
       "</ul>"
       "<h3>Small things that quietly help</h3>"
       "<ul>"
       "<li>Don't stack posts 5 minutes apart — spacing beats bursts for notification fatigue.</li>"
       "<li>Media posts slightly outperform text-only at equal times in most niches.</li>"
       "<li>Skip the “dump 6 posts at midnight” pattern; Telegram's own limits and your "
       "subscribers' patience both prefer a steady drip.</li>"
       "</ul>"),
   faq=[
       {'q': 'Does Telegram show “time of post” that I can use for testing?',
        'a': 'Views are timestamped; compare first-hour views across slots. The statistics screen gives you per-post numbers without extra tools.',
        'links': ['statistics']},
       {'q': 'How many posts per day is healthy?',
        'a': '2–4 for most content channels. Beyond that, watch unsubscribes — the metric that punishes oversharing fastest.',
        'links': ['tg_channels_explained']},
   ],
   links=['statistics', 'tg_channels_explained', 'qa_schedule_many_at_once'])

# ============================================================ PREMIUM/PAY ====
_a('qa_pay_stars_crypto',
   category='premium',
   title='How to Pay for Fast Scheduler Premium (Stars and What Happens After)',
   description='Paying for Premium step by step: Telegram Stars at the official rate, plan terms, activation timing, and what to do if payment succeeded but nothing changed.',
   content=(
       "<p>Premium attaches to your Telegram account and covers every channel you connect while it "
       "is active. Payment lives in the bot's <b>Premium</b> menu and uses <b>Telegram Stars</b> only.</p>"
       "<h3>Telegram Stars</h3>"
       "<p>Stars are Telegram's in-app currency. The bot converts the USD price at the official rate "
       "and shows the exact Star amount before you confirm — buy Stars in Telegram "
       "if your balance is short, approve, and Premium activates the moment the invoice clears. "
       "Refunds of Stars purchases follow Telegram's own flow, which is also why the bot asks you to "
       "double-check the term before paying.</p>"
       "<h3>Plan terms</h3>"
       "<p>The monthly Stars plan <b>renews automatically</b> until cancelled. Prepaid 3-month, "
       "6-month, and yearly plans are <b>one-time purchases</b> (with up-front 3/6-month discounts) "
       "and never auto-renew.</p>"
       "<h3>Right after payment</h3>"
       "<ul>"
       "<li>Premium flags appear instantly in the menus; <code>/premium</code> shows status and "
       "expiry date.</li>"
       "<li>If you paid but see no change: <b>restart the bot with <code>/start</code></b> — status "
       "is refreshed on launch. Still stuck? <code>/feedback</code> with the payment date and method "
       "gets a human on it the same day.</li>"
       "</ul>"
       "<h3>Terms, renewals, refunds</h3>"
       "<p>Multi-month terms cost proportionally less (built-in 3/6-month discounts), and expiry is "
       "shown everywhere Premium matters. When a prepaid term ends, limits quietly "
       "return to Free — nothing is deleted. The refund policy is linked in the site footer; "
       "genuine failures (double payment, activation glitch) are refunded by support.</p>"),
   faq=[
       {'q': 'Can I pay for a friend’s account?',
        'a': 'Premium binds to the Telegram account that activates it. To gift Premium, have them open the Premium menu and pay there, or transfer Stars — the bot cannot attach Premium to a different account after payment.',
        'links': ['premium_buy']},
       {'q': 'Will Premium renew automatically?',
        'a': 'The monthly Stars plan renews automatically until cancelled. Prepaid 3-month, 6-month, and yearly plans never auto-renew — when one ends, limits revert to Free and you can extend any time from the Premium menu.',
        'links': ['premium_expiry']},
   ],
   links=['premium_buy', 'payment_stars', 'premium_expiry', 'payment_status'])

_a('qa_which_plan',
   category='premium',
   title='Free vs Premium: Which Fast Scheduler Plan Fits Your Channel?',
   description='A decision guide, not a feature dump: how posting volume, channel count, video weight and backup needs map to the right plan — with the exact numbers.',
   content=(
       "<p>Feature tables tell you <i>what</i> differs; this tells you <i>when it matters</i>. Four "
       "questions decide the plan.</p>"
       "<h3>1. How many channels do you run?</h3>"
       "<p>One channel works great on Free ({channels_free} channel, {bots_free} sender bot). Two or "
       "three channels — or plans to get there — is the cleanest Premium trigger: Premium pairs "
       "{channels_prem} channels with {bots_prem} sender bots from one account.</p>"
       "<h3>2. How much do you post?</h3>"
       "<p>Multiply daily posts by 30. Under ~90 sends/month, Free's {monthly_sent_free}-per-channel "
       "cap rarely bites. A 3+/day cadence, or channels where every send counts (news, trading, "
       "drops), wants Premium's unlimited sends and queue.</p>"
       "<h3>3. Is your content video-heavy?</h3>"
       "<p>Free uploads top out at {max_media_free} with video at {videos_msg_free}, no video in "
       "Media Storage, and stronger compression. If your posts live on video, Premium's "
       "{max_media_prem} uploads, {videos_msg_prem} video, and video-in-storage are not a luxury — "
       "they are the workflow.</p>"
       "<h3>4. Do you need backups, exports or signatures?</h3>"
       "<p>The Export &amp; Backup toolkit (<code>.fsback</code> archives, JSON/CSV exports) and "
       "auto-signatures are Premium-only. If the queue <i>is</i> your business — client channels, "
       "monetized content — backups stop being optional the first time you restructure a month of "
       "posts.</p>"
       "<h3>The short version</h3>"
       "<ul>"
       "<li><b>Stay Free</b> if: one channel, ≤3 posts/day, text-and-photo content, no archive "
       "needs.</li>"
       "<li><b>Go Premium</b> if: 2–3 channels, 3+ posts/day, video content, recurring automation "
       "beyond one rule, or you want backups and signatures.</li>"
       "<li><b>Either way</b>: you can start Free and upgrade the moment a limit touches you — "
       "nothing you built on Free breaks when Premium ends.</li>"
       "</ul>"),
   faq=[
       {'q': 'Can I try Premium and go back to Free?',
        'a': 'Yes. On expiry, limits revert to Free and nothing is deleted — disconnect extra channels if you keep more than one, and the first recurring rule keeps running.',
        'links': ['premium_expiry']},
       {'q': 'Does Premium change how fast posts send?',
        'a': 'Send speed is the same — Telegram delivery does not differ by plan. Premium removes quantity limits and media compression, not latency.',
        'links': ['premium']},
   ],
   links=['qa_free_limits', 'qa_premium_worth', 'premium_buy'])

# ============================================================ ERRORS =========
_a('qa_post_not_sent',
   category='errors',
   title='Scheduled Message Didn’t Post? The 6 Real Causes, In Order of Likelihood',
   description='A ranked troubleshooting checklist for missed Telegram posts: sender bot admin rights, revoked tokens, permissions, channel changes, rate limits and the monthly cap.',
   content=(
       "<p>When a post misses its slot, the cause is almost always in the delivery chain — the "
       "schedule itself is the least likely suspect. Work this list top to bottom; each item fixes "
       "the majority of cases.</p>"
       "<h3>1. The sender bot lost its admin seat</h3>"
       "<p>Someone cleaned up admins and removed your sender bot. Check <b>Manage Channel → "
       "Administrators</b>: your sender bot must be there with <b>Post Messages</b>. Re-add it, and "
       "the queue resumes.</p>"
       "<h3>2. The token was revoked or replaced</h3>"
       "<p>A <code>/revoke</code> in @BotFather kills the old token everywhere instantly. If the bot "
       "shows the sender as disconnected, open <b>Bots</b> → <b>🔁 Replace Token</b> under the bot and paste the fresh token.</p>"
       "<h3>3. Permissions were narrowed</h3>"
       "<p>Admin exists but without <b>Post Messages</b> — a silent killer after permission "
       "tightening. Open the admin entry and re-enable posting.</p>"
       "<h3>4. The channel changed identity</h3>"
       "<p>Username changed or the channel was converted — the old link no longer resolves. "
       "Reconnect the channel; schedules are kept.</p>"
       "<h3>5. Telegram rate limits on bursts</h3>"
       "<p>Telegram throttles aggressive posting bursts channel-wide. If several posts fire close "
       "together and one fails, it is usually this. Space posts by minutes, not seconds — the "
       "scheduler already does, but third-party bots added to the channel can collide with it.</p>"
       "<h3>6. The monthly send cap (Free)</h3>"
       "<p>On Free, sends pause at {monthly_sent_free} per channel per month until the 1st. The bot "
       "warns you before the cap; <code>/stats</code> shows the counter. Premium lifts the cap "
       "entirely.</p>"
       "<h3>Fastest diagnosis</h3>"
       "<p>Send <code>/stats</code> (status of everything) and check the sender-bot status screen. "
       "Still mysterious? <code>/feedback</code> with the channel and the missed time — support can "
       "see delivery attempts and will tell you exactly which step failed.</p>"),
   faq=[
       {'q': 'Will missed posts send later automatically?',
        'a': 'A post that failed delivery is marked failed, not silently retried forever. Fix the underlying cause, then delete it and schedule it again.',
        'links': ['errors']},
       {'q': 'How do I know if it was the monthly cap?',
        'a': 'The bot notifies you at the cap, and /stats shows monthly usage per channel. If neither shows the cap, it was delivery-side — start the checklist from the top.',
        'links': ['limit_daily']},
   ],
   links=['errors', 'error_rate', 'bot_status', 'limit_daily'])

# ============================================================ TOOLS ==========
_a('qa_signature_guide',
   category='config',
   title='How to Add an Automatic Signature to Every Telegram Post',
   description='Set up a Premium auto-signature — credit line, promo, or hashtags — appended to every post of a channel, with formatting, per-channel control, and clean removal.',
   content=(
       "<p>A signature is the footer that appears under every post in a channel: credit, CTA, "
       "hashtags, promo. Set it once in Fast Scheduler and every scheduled message carries it — "
       "you stop copy-pasting “@yourchannel” to the end of everything.</p>"
       "<h3>Setting it up</h3>"
       "<ul>"
       "<li>1. Open <b>Signature</b> via <code>/signature</code> (or tap <b>📝 Signature</b> on the review screen). "
       "Premium feature.</li>"
       "<li>2. Pick the channel — signatures are <b>per channel</b>, so your main channel can carry "
       "a promo while the announcements channel stays clean.</li>"
       "<li>3. Send the text. Formatting works: <b>bold</b>, <i>italic</i>, links, even emoji-free "
       "minimalism if that is your style.</li>"
       "</ul>"
       "<p>From the next send onward, the signature is appended to every post in that channel. "
       "Existing scheduled posts pick it up automatically at send time — no need to reschedule "
       "anything.</p>"
       "<h3>What belongs in a good signature</h3>"
       "<ul>"
       "<li><b>The channel handle</b> — the classic “@yourchannel” line, since forwarded copies "
       "keep the credit.</li>"
       "<li><b>One action</b> — “Reply to buy”, “Details: link”. A signature with three CTAs has "
       "zero.</li>"
       "<li><b>Hashtags for navigation</b> — if the channel uses tag-indexing, the signature is the "
       "perfect place for the constant ones.</li>"
       "</ul>"
       "<h3>Changing and removing</h3>"
       "<p>The same menu edits or clears the signature; clearing stops appending immediately "
       "(again, applied at send time, so posts already published keep their footer — that is a "
       "feature, not a bug). Per-channel control means experimenting is cheap.</p>"),
   faq=[
       {'q': 'Can I use different signatures for different channels?',
        'a': 'Yes — signatures are configured per channel. Each connected channel gets its own text (or none).',
        'links': ['signature']},
       {'q': 'Does the signature count toward the message length?',
        'a': 'It is part of the final message text, so extremely long signatures can hit Telegram’s 4096-character limit on top of long posts. Short signatures are better anyway.',
        'links': ['signature']},
   ],
   links=['signature', 'premium_buy', 'qa_premium_worth'])

_a('qa_media_storage_guide',
   category='media_storage',
   title='What Is Media Storage and How Do You Use It Without Losing Your Mind?',
   description='Media Storage explained: boxes, saved photos/videos/documents, reusing assets across scheduled posts, storage limits on Free vs Premium, and cleanup workflow.',
   content=(
       "<p>Media Storage is your in-bot asset library: save a photo, video, or document once, then "
       "reuse it in any scheduled post without re-uploading. If you repost evergreen content or "
       "reuse brand imagery, this is the feature that saves the most time per week.</p>"
       "<h3>Boxes: folders with a purpose</h3>"
       "<p>Assets live in <b>boxes</b> — named containers like “Brand”, “Memes”, “Product shots”. "
       "Free gets <b>{storage_count_free} box with {storage_items_free} items</b> (no video in "
       "storage); Premium gets <b>{storage_count_prem} boxes × {storage_items_prem} items</b> with "
       "video support. Boxes keep the picker fast and your library mentally organized — one box per "
       "campaign is a good default.</p>"
       "<h3>Saving and reusing</h3>"
       "<ul>"
       "<li><b>Save:</b> forward or upload media to the storage, or save straight from a scheduled "
       "message you are composing.</li>"
       "<li><b>Reuse:</b> while scheduling, open the storage instead of attaching a file — pick the "
       "asset, done. Telegram file references are reused, so nothing is re-uploaded and quality is "
       "not recompressed per post.</li>"
       "<li><b>Organize:</b> move items between boxes, rename, delete.</li>"
       "</ul>"
       "<h3>The limits that actually matter</h3>"
       "<ul>"
       "<li><b>Item count</b> — the {storage_items_free}-item Free box fills fast with albums; "
       "delete stale assets or upgrade.</li>"
       "<li><b>Video on Free</b> — storage refuses video on Free; schedule videos directly instead, "
       "or move to Premium for video-in-storage.</li>"
       "<li><b>Size</b> — same upload caps as messages: {max_media_free} on Free, {max_media_prem} "
       "on Premium.</li>"
       "</ul>"
       "<h3>A cleanup cadence that works</h3>"
       "<p>Once a month: open each box, delete anything unused in 60 days, archive campaign boxes "
       "by renaming with a date prefix. Two minutes, and the picker stays a joy instead of an "
       "archaeology dig.</p>"),
   faq=[
       {'q': 'Does deleting a media item break scheduled posts using it?',
        'a': 'Posts keep working — a scheduled message holds its own reference to the media. Deleting from storage only removes it from the library for future posts.',
        'links': ['ms_manage']},
       {'q': 'Can I share a box with another admin?',
        'a': 'Storage is per account. To share assets, export them as part of a backup or send the files directly — the other account saves them into their own storage.',
        'links': ['qa_fsback_vs_fspback']},
   ],
   links=['ms_boxes', 'ms_save', 'ms_manage', 'limit_media'])

# ============================================================ TIPS ===========
_a('qa_recurring_guide',
   category='scheduling',
   title='How to Automate Recurring Posts in Telegram (Daily Digests, Weekly Roundups)',
   description='Recurring rules done right: every supported interval, expiry behavior, combining recurrences with signatures, and real channel patterns that run themselves.',
   content=(
       "<p>Anything your channel repeats should never be scheduled by hand twice. Recurring rules "
       "encode the pattern once — “daily at 9:00”, “every Monday 18:30”, “every 6 hours” — and the "
       "bot keeps generating posts on time, forever (or until the rule expires).</p>"
       "<h3>Creating a rule</h3>"
       "<ul>"
       "<li>1. Tap <b>🔄 Recurring Messages</b> in the bot (or send <code>/recurring</code>) and follow the flow.</li>"
       "<li>2. Compose the message — text, media, the works — exactly like a normal post.</li>"
       "<li>3. Pick the pattern: daily, weekly (with weekday picker), or custom interval.</li>"
       "<li>4. Set the time in the <b>channel's time zone</b> and confirm.</li>"
       "</ul>"
       "<p>The rule's future posts expand in the <b>Calendar</b> like any others, and the rule itself "
       "is listed with your recurring messages — so there is always a truthful picture of what will publish.</p>"
       "<h3>Expiry — the part people forget</h3>"
       "<p>On <b>Free</b>, the single recurring rule runs for <b>{recurring_expiry_days} days</b>, "
       "then expires with a notice — create a new rule to continue. It is the anti-zombie mechanism: dead rules can't silently "
       "post forever. <b>Premium</b> rules never expire, and you can run unlimited rules — one per "
       "content type is the usual pattern.</p>"
       "<h3>Patterns that work in real channels</h3>"
       "<ul>"
       "<li><b>Daily digest</b> — a template message (“Top 3 of the day”) with the signature "
       "carrying credit; edit the rule weekly, not daily.</li>"
       "<li><b>Weekly roundup</b> — Monday 9:00 rule; combine with the calendar to dodge holidays.</li>"
       "<li><b>Scheduled reminders</b> — every-6-hours service posts for community managers; "
       "Premium's unlimited rules shine here.</li>"
       "</ul>"
       "<h3>Editing and stopping</h3>"
       "<p>Rules are editable — change text, time, or pattern, and future instances follow. Pause "
       "or delete when a campaign ends. Deleting a rule never deletes already-posted messages.</p>"),
   faq=[
       {'q': 'Why did my recurring rule stop working?',
        'a': 'On Free, rules expire after 365 days and you get an expiry notice — create a new rule to continue. Premium rules never expire. Also check the sender bot is still admin — a failed delivery stops the chain.',
        'links': ['recurring', 'qa_post_not_sent']},
       {'q': 'Can two rules post at the same time?',
        'a': 'Yes, and they will — in the order created. If they are too close together, Telegram may throttle the burst; space rules by a few minutes.',
        'links': ['qa_duplicate_posts']},
   ],
   links=['recurring', 'premium', 'qa_edit_scheduled_post', 'signature'])

_a('qa_bot_management',
   category='bots',
   title='How to Manage Your Sender Bots: Rotate, Rename, and Keep Them Healthy',
   description='Day-to-day sender bot management: checking status, rotating a compromised token, renaming the public face of your bot, one-bot-per-channel hygiene, and removal.',
   content=(
       "<p>Your sender bot is the public face of every post, so a little hygiene goes a long way. "
       "Everything below lives in <b>Sender Bots</b> (or <code>/bots</code>) in Fast Scheduler.</p>"
       "<h3>Check status before you check anything else</h3>"
       "<p>The bots screen shows each bot's connection state and which channels it serves. If a "
       "send ever fails, this is the first screen: a bot showing disconnected means a revoked "
       "token or a BotFather change — fix it there, not in the schedule.</p>"
       "<h3>Rotating a token (the right way)</h3>"
       "<ul>"
       "<li>1. @BotFather → <code>/mybots</code> → your bot → <b>Revoke current token</b>.</li>"
       "<li>2. Copy the new token.</li>"
       "<li>3. Fast Scheduler → <b>Bots</b> → <b>🔁 Replace Token</b> under the bot → paste.</li>"
       "</ul>"
       "<p>The swap is instant and schedules keep running. Do it the other way around (revoke and "
       "forget) and every send fails until you paste the new token.</p>"
       "<h3>Rename = rebrand</h3>"
       "<p>A bot's public name and avatar come from @BotFather (<code>/setname</code>, "
       "<code>/setuserpic</code>) — change them there and every future post instantly carries the "
       "new look. No re-pairing needed; Fast Scheduler stores the token, not the cosmetics.</p>"
       "<h3>Fleet hygiene</h3>"
       "<ul>"
       "<li><b>One bot per channel</b> keeps branding separate and failures isolated (Premium: "
       "up to {bots_prem} bots).</li>"
       "<li><b>Remove</b> bots you no longer use — removal deletes the token from storage; the bot "
       "account itself lives on in BotFather.</li>"
       "<li>After any BotFather change, glance at the status screen once — 10 seconds that prevent "
       "a silent failed-post day.</li>"
       "</ul>"),
   faq=[
       {'q': 'Can I use the same bot for multiple channels?',
        'a': 'Yes — a sender bot can serve several of your channels. Separate bots per channel remain the cleaner default for branding and debugging.',
        'links': ['bot_fleet']},
       {'q': 'I deleted a bot in BotFather. What happens in Fast Scheduler?',
        'a': 'Its sends fail with an invalid-token error and the status screen shows it disconnected. Remove the bot from Sender Bots and pair a replacement.',
        'links': ['bot_remove']},
   ],
   links=['bot_manage', 'bot_rotate', 'bot_status', 'bot_remove'])
