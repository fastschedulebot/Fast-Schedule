#!/usr/bin/env python3
"""Upgrade all translation texts with comprehensive descriptions while preserving button labels."""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load current translations
with open('translations/en.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# ============================================================================
# BLACKLIST: Keys that MUST remain short (button labels, inline buttons, etc.)
# ============================================================================
BUTTON_LABEL_KEYS = {
    # Keys ending with _btn are button labels - never overwrite these
    # They will be detected automatically by the suffix check
}

def is_button_label(key):
    """Check if a key is a button label (ends with _btn or is a known button key)."""
    return key.endswith('_btn') or key in BUTTON_LABEL_KEYS

# ============================================================================
# PHOTO MODE UPGRADES - Add detailed descriptions (message text only)
# ============================================================================
data['select_photo_mode'] = """📷 <b>Select Photo Mode</b>

Choose how your photos will be attached to scheduled posts:

<b>📷 Normal</b>
Each post gets the exact same photo. Perfect for branding — use your logo, watermark, or a consistent visual identity across all messages.

<b>🎲 Random</b>
Each post gets a random photo from the set you uploaded. Great for variety — keeps your channel visually fresh without repeating the same image.

<b>🔀 Sequential</b>
Photos are sent in order, one per post. Ideal for story-like content, step-by-step tutorials, or any sequence where order matters.

<b>⏭ Skip Photos</b>
Don't attach any photos — send text-only posts."""

# NOTE: normal_photo_mode, random_photo_mode, sequential_photo_mode are BUTTON LABELS
# They must remain short and clean for InlineKeyboardButton usage
# Do NOT overwrite them with long descriptions

# ============================================================================
# WELCOME & MAIN MENU UPGRADES
# ============================================================================
data['welcome_intro'] = """👋 <b>Welcome to Fast Scheduler Bot!</b>

I'm your personal Telegram channel manager. I help you schedule posts, manage multiple channels, and track your content performance — all from one place.

<b>🚀 What I can do:</b>
• 📅 <b>Schedule posts</b> — Set dates, times, and content. I'll publish automatically.
• 🔄 <b>Recurring posts</b> — Set up repeating schedules (daily, weekly, monthly).
• 📊 <b>Statistics</b> — Track views, comments, reactions, and top-performing posts.
• 🤖 <b>Sender bots</b> — Connect dedicated bots for each channel for better management.
• 💾 <b>Media storage</b> — Save photos and videos for quick reuse.
• 🌐 <b>Multi-language</b> — Available in English, Russian, and Armenian.

<b>👆 Use the menu below to get started!</b>"""

data['welcome_no_channel'] = """📢 <b>No Channel Connected Yet</b>

To start scheduling messages, you first need to connect your Telegram channel.

<b>How to connect:</b>
1. Make sure <b>@FastSchedulerBot</b> is an <b>administrator</b> in your channel (with posting permissions)
2. Send me your channel link (e.g., <code>https://t.me/yourchannel</code>) or forward any message from your channel

<b>Or use the menu button below to get started!</b>"""

data['welcome_subscribed'] = """✅ <b>You're All Set!</b>

Your channel is connected and ready to go. You can now:
• 📅 Schedule new messages
• 📊 View statistics
• 🔄 Set up recurring posts
• 🤖 Connect a sender bot for advanced management

Use the menu below to explore all features!"""

data['welcome_not_subscribed'] = """⚠️ <b>Channel Not Connected</b>

I don't see any connected channels yet. To use Fast Scheduler, you need to connect at least one Telegram channel.

<b>Quick setup:</b>
1. Add <b>@FastSchedulerBot</b> as an admin in your channel
2. Click the <b>📢 Channel</b> button below or send me the channel link

It takes less than a minute!"""

data['welcome_addbot_needed'] = """🤖 <b>Unlock Full Power with a Sender Bot</b>

A sender bot is a dedicated Telegram bot that manages your channel directly. This gives you:

<b>✨ Benefits:</b>
• 🚀 <b>Faster scheduling</b> — No rate limits from shared bots
• 🔒 <b>Better security</b> — Your channel data stays isolated
• 📊 <b>Detailed stats</b> — Track performance per channel
• ⚡ <b>Priority delivery</b> — Messages sent with higher priority

<b>📋 How to set up:</b>
1. Open <b>@BotFather</b> in Telegram
2. Create a new bot with <code>/newbot</code>
3. Copy the bot token
4. Send it to me here!

Premium users can connect up to {limit} sender bots."""

# ============================================================================
# SCHEDULE & COMMAND UPGRADES
# ============================================================================
data['about_bot_info'] = """🤖 <b>Fast Scheduler Bot — @FastSchedulerBot</b>

Your all-in-one Telegram channel management tool. Schedule posts, track performance, and automate your content — all from a simple interface.

<b>🔧 Core Features:</b>
• 📅 <b>Message Scheduling</b> — Schedule posts with precise dates and times
• 🔄 <b>Recurring Posts</b> — Set up daily, weekly, or custom repeating schedules
• 📊 <b>Channel Statistics</b> — Track views, comments, reactions, and growth
• 🤖 <b>Sender Bots</b> — Connect dedicated bots for each channel
• 💾 <b>Media Storage</b> — Save and reuse photos and videos
• 🌐 <b>Multi-language</b> — English, Russian, Armenian
• 📢 <b>Multi-channel</b> — Manage multiple channels from one place
• 🔔 <b>Notifications</b> — Get alerts when posts are published

<b>📊 Free vs Premium:</b>
• Free: 1 channel, 5 scheduled messages, 1 recurring
• Premium: Unlimited channels, 100+ scheduled messages, 10+ recurring

Version: {version}"""

data['about_text'] = """📋 <b>About Fast Scheduler Bot</b>

<b>Version:</b> {version}

Fast Scheduler Bot is a powerful Telegram scheduling tool designed for content creators, community managers, and businesses who want to automate their Telegram channel posts.

<b>🎯 Who is it for?</b>
• Channel owners who want consistent posting schedules
• Marketing teams managing multiple Telegram channels
• Content creators who batch-create posts
• Community managers who need recurring announcements

<b>💡 Key advantages:</b>
• No coding required — just send your content and set times
• Works with any Telegram channel you admin
• Supports text, photos, videos, and media groups
• Real-time statistics and performance tracking
• Automatic timezone handling for global audiences

<b>🔗 Links:</b>
• Channel: @FastScheduleNews
• Support: @MaximalXP"""

# ============================================================================
# TIMEZONE UPGRADES
# ============================================================================
data['timezone_prompt_method'] = """🕐 <b>Change Time Zone</b>

Your timezone determines when scheduled messages are published. For example, if you set a post for 09:00 and your timezone is UTC+4, it will be sent at 09:00 in UTC+4.

<b>Choose how to set your timezone:</b>

🏙 <b>Type City</b> — Enter any city name (e.g., London, New York, Tokyo)
🕐 <b>Send Time</b> — Tell me your current time, and I'll detect your zone
📍 <b>Send Location</b> — Share your location for automatic detection
🔄 <b>Auto-detect</b> — Let me figure it out from your Telegram settings"""

data['tutorial_tz_text'] = """🕐 <b>Time Zone Setup</b>

Setting your timezone ensures messages are published at the exact time you specify — in YOUR local time.

<b>For example:</b>
If you set a post for "Monday 09:00" and you're in Moscow (UTC+3), it will be sent at 09:00 Moscow time.

<b>How would you like to set your timezone?</b>

You can send:
• 🏙 A <b>city name</b> (e.g., <code>London</code>, <code>New York</code>, <code>Tokyo</code>)
• 🕐 Your <b>current time</b> (e.g., <code>15:30</code>) — I'll detect your zone
• 📍 A <b>location</b> — for automatic detection

Or click <b>Skip</b> to use UTC (you can change this later)."""

data['timezone_detect_time_prompt'] = """🕐 <b>What time is it for you right now?</b>

Send me your current time in 24-hour format (HH:MM).

<b>Examples:</b>
• <code>15:30</code> (3:30 PM)
• <code>09:00</code> (9:00 AM)
• <code>22:15</code> (10:15 PM)

I'll use this to determine your timezone automatically."""

# ============================================================================
# TUTORIAL UPGRADES
# ============================================================================
data['tutorial_welcome'] = """👋 <b>Welcome to Fast Scheduler Bot!</b>

Let me show you how to get started. This quick tutorial takes less than 2 minutes.

<b>What we'll set up:</b>
1. 📢 Connect your Telegram channel
2. 🕐 Set your timezone for accurate scheduling
3. 🤖 Optionally connect a sender bot for advanced features

Ready? Let's begin!"""

data['tutorial_connect_channel_prompt'] = """📡 <b>Step 1/4 — Connect Your Channel</b>

To schedule messages, I need access to your Telegram channel.

<b>Before you begin, make sure:</b>
• You are an <b>administrator</b> of the channel
• <b>@FastSchedulerBot</b> is added as an admin with posting permissions

<b>How to connect:</b>
• Send me your channel link: <code>https://t.me/yourchannel</code>
• Or forward any message from your channel

<b>💡 Tip:</b> You can connect multiple channels later from the Channel menu."""

data['tutorial_channel_connected'] = """✅ <b>Channel Connected Successfully!</b>

Great! Your channel is now connected and ready for scheduling.

<b>What you can do now:</b>
• 📅 <b>Schedule messages</b> — Use the 📅 Schedule button in the menu
• 🔄 <b>Set up recurring posts</b> — Automate daily/weekly content
• 📊 <b>Track statistics</b> — See how your posts perform

<b>Next step:</b> Let's set your timezone so messages publish at the right time.

Click <b>Next</b> to continue, or <b>Skip Tutorial</b> to explore on your own."""

data['tutorial_complete'] = """🎉 <b>Tutorial Complete!</b>

You're all set to start using Fast Scheduler Bot!

<b>Quick start guide:</b>
• 📅 Click <b>Schedule</b> to create your first post
• 📢 Click <b>Channel</b> to manage connected channels
• 🤖 Click <b>Bots</b> to connect a sender bot (optional)
• 📊 Click <b>Statistics</b> to track your performance

<b>💡 Pro tips:</b>
• Use recurring messages for regular content (daily news, weekly updates)
• Connect a sender bot for faster message delivery
• Check your stats regularly to see what content performs best

Need help? Use /help or click the Help button anytime!"""

# ============================================================================
# BOT CONNECTION UPGRADES
# ============================================================================
data['addbot_instruction_text'] = """🤖 <b>Add a Sender Bot</b>

A sender bot is a dedicated Telegram bot that manages your channel independently. This gives you better performance, security, and control.

<b>✨ Why use a sender bot?</b>
• 🚀 <b>Faster delivery</b> — Messages sent without shared bot rate limits
• 🔒 <b>Isolated data</b> — Your channel data stays separate and secure
• 📊 <b>Per-channel stats</b> — Track performance for each channel individually
• ⚡ <b>Priority queuing</b> — Your messages get sent first

<b>📋 Setup steps:</b>
1. Open <b>@BotFather</b> in Telegram
2. Send <code>/newbot</code> to create a new bot
3. Choose a name and username for your bot
4. Copy the bot token you receive
5. Paste the token here

<b>⚠️ Important:</b> After creating the bot, add it as an <b>administrator</b> in your channel with posting permissions before clicking Verify."""

data['addbot_create_info'] = """🤖 <b>Create a Sender Bot</b>

Follow these steps to create your own dedicated sender bot:

<b>Step 1:</b> Open <b>@BotFather</b> in Telegram
<b>Step 2:</b> Send <code>/newbot</code>
<b>Step 3:</b> Choose a name (e.g., "My Channel Bot")
<b>Step 4:</b> Choose a username (must end with "bot", e.g., @MyChannelSenderBot)
<b>Step 5:</b> Copy the token BotFather sends you

<b>Step 6:</b> Add your new bot as an admin in your channel:
• Open your channel settings
• Go to Administrators → Add Admin
• Search for your bot username
• Give it "Post Messages" permission

<b>Step 7:</b> Come back here and paste the token!

Once verified, your bot will be connected and ready to manage your channel."""

data['addbot_token_prompt'] = """🔑 <b>Enter Your Bot Token</b>

Paste the token you received from <b>@BotFather</b>.

<b>What it looks like:</b>
<code>1234567890:ABCdefGHIjklmNO_pQrStUvWxYz</code>

<b>⚠️ Security note:</b>
• This token gives full control over your bot — keep it safe
• Fast Scheduler stores it encrypted
• Never share your token publicly

<b>Before pasting, make sure:</b>
✓ Your bot is created via @BotFather
✓ Your bot is added as admin in your channel
✓ You copied the full token (not just the bot ID)"""

# ============================================================================
# STATS UPGRADES
# ============================================================================
data['stats_title'] = """📊 <b>Channel Statistics</b>

Track how your scheduled posts perform. View engagement metrics, identify top content, and optimize your posting strategy.

<b>📊 Available metrics:</b>
• 👁 <b>Views</b> — How many users saw each post
• 💬 <b>Comments</b> — Discussion and engagement
• ❤️ <b>Reactions</b> — User sentiment and interaction
• 🏆 <b>Leaderboard</b> — Top-performing posts ranked

<b>💡 Note:</b> Statistics only track messages sent through this bot. Posts made manually won't appear in your stats."""

data['stats_note_text'] = """💡 <b>Important:</b> Statistics only include messages sent through this bot. 

To get accurate stats, make sure to schedule all your channel posts through Fast Scheduler Bot. Manually published messages won't appear in your statistics."""

data['stats_select_metric'] = """📊 <b>What would you like to track?</b>

Choose a metric to view detailed statistics:

👁 <b>Most Viewed</b> — Posts with the highest view counts
💬 <b>Most Commented</b> — Posts generating the most discussion
❤️ <b>Most Reacted</b> — Posts with the most emoji reactions
📊 <b>All Metrics</b> — See all metrics combined

Each metric shows your top-performing content to help you understand what resonates with your audience."""

data['stats_leaderboard_title'] = """🏆 <b>Leaderboard</b>

Your top-performing posts ranked by engagement.

Use this to identify:
• Which content types get the most attention
• The best times to post
• What topics generate the most discussion
• Trends in your channel's growth

<b>💡 Tip:</b> Check your leaderboard weekly to spot patterns and optimize your content strategy."""

# ============================================================================
# PREMIUM & UPSELL UPGRADES
# ============================================================================
data['upsell_channels'] = """📢 <b>Connect More Channels</b>

You've reached the free channel limit. Upgrade to Premium to connect up to {limit} channels and manage all your Telegram content from one place.

<b>Premium channel benefits:</b>
• 📢 Connect up to {limit} channels
• 📊 Per-channel statistics
• 🤖 Dedicated sender bots per channel
• 💾 Unlimited media storage

Upgrade now to unlock the full power of Fast Scheduler!"""

data['upsell_scheduled_messages'] = """📅 <b>Schedule More Messages</b>

You've reached the free scheduling limit. Upgrade to Premium for up to {limit} scheduled messages!

<b>Free plan:</b> 5 scheduled messages
<b>Premium plan:</b> {limit} scheduled messages

With Premium, you can:
• 📅 Schedule weeks of content in advance
• 🔄 Set up recurring posts (daily, weekly, monthly)
• 📊 Track all your scheduled content performance
• 💾 Save media for quick reuse

Start planning ahead — upgrade to Premium today!"""

data['upsell_recurring'] = """🔄 <b>More Recurring Messages</b>

You've reached the free recurring message limit. Upgrade for up to {limit} recurring schedules!

<b>What are recurring messages?</b>
Automated posts that repeat on a schedule — perfect for:
• 📰 Daily news updates
• 📅 Weekly announcements
• 🎉 Monthly newsletters
• 🔔 Regular reminders

<b>Free:</b> 1 recurring message
<b>Premium:</b> {limit} recurring messages

Automate your content — upgrade to Premium!"""

data['upsell_daily_messages'] = """📈 <b>Send More Per Day</b>

You've reached your daily message limit. Upgrade to Premium for {limit} messages per day!

<b>Why daily limits?</b>
Telegram has rate limits to prevent spam. Premium users get higher limits because they're trusted channel managers.

<b>Free:</b> Limited daily messages
<b>Premium:</b> {limit} messages per day

Need more? Upgrade to Premium for higher throughput!"""

# ============================================================================
# ERROR MESSAGES UPGRADES
# ============================================================================
data['user_not_admin_channel'] = """❌ <b>Not a Channel Admin</b>

I couldn't verify your admin status for this channel. To use Fast Scheduler, you need to be an administrator with posting permissions.

<b>To fix this:</b>
1. Open your channel settings
2. Go to Administrators
3. Make sure <b>@FastSchedulerBot</b> is listed as an admin
4. Ensure "Post Messages" permission is enabled

<b>Already an admin?</b> Try sending the channel link again or forward a message from the channel."""

data['addbot_verify_error'] = """❌ <b>Verification Failed</b>

I couldn't verify your bot. This usually means one of these issues:

<b>Common problems:</b>
• 🔑 <b>Invalid token</b> — Double-check you copied the full token from @BotFather
• 👤 <b>Bot not in channel</b> — Add your bot as an admin in your channel first
• 🔐 <b>Missing permissions</b> — The bot needs "Post Messages" permission
• 🔄 <b>Already connected</b> — This bot might already be linked to another account

<b>To fix:</b>
1. Verify the token is correct (check @BotFather)
2. Add the bot as admin in your channel
3. Give it posting permissions
4. Click <b>Check Again</b>"""

data['media_caption_too_long'] = """❌ <b>Caption Too Long</b>

Your caption is {count} characters, but the maximum is {max} characters.

<b>Telegram limits:</b>
• Regular messages: 1024 characters for captions
• With media: 1024 characters

<b>💡 Tips:</b>
• Use shorter captions or split into multiple posts
• Use abbreviations or links to save space
• Premium users get access to longer captions in some cases"""

# ============================================================================
# CHANNEL MANAGEMENT UPGRADES
# ============================================================================
data['action_channel_pick_title'] = """📢 <b>Select a Channel</b>

Choose which channel you want to manage:

<b>💡 Tips:</b>
• Each channel has its own schedule and settings
• You can connect multiple channels (Premium for 2+)
• Click a channel name to select it

<b>Don't see your channel?</b>
Make sure @FastSchedulerBot is an admin in the channel, then use the refresh button."""

data['addbot_connected_text'] = """✅ <b>Bot Connected Successfully!</b>

<b>@{username}</b> is now managing your channel.

<b>What happens next:</b>
• 📅 Messages will be sent through your sender bot
• 📊 Statistics will be tracked for this channel
• 🔒 Your channel data is now isolated and secure

<b>💡 Tip:</b> You can now manage this channel directly from your sender bot!"""

# ============================================================================
# SCHEDULE REVIEW UPGRADES  
# ============================================================================
data['weekly_prompt'] = """📅 <b>Weekly Schedule Setup</b>

Create a recurring weekly post. Choose which day and time this message should repeat.

<b>Format:</b> <code>DAY HH:MM</code>

<b>Examples:</b>
• <code>Monday 09:00</code> — Every Monday at 9 AM
• <code>Friday 18:30</code> — Every Friday at 6:30 PM
• <code>Sunday 12:00</code> — Every Sunday at noon

<b>💡 Available days:</b>
Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"""

# ============================================================================
# REFERRAL UPGRADES
# ============================================================================
data['referral_requirement_note'] = """✅ <b>How referrals work:</b>
• Share your unique referral link with friends
• When someone joins through your link AND schedules at least one message, it counts
• You earn {days} free Premium days per successful referral
• Maximum {max_referrals} referrals allowed
• Free days are added automatically after verification"""

data['referral_info_text'] = """🎁 <b>Referral Program</b>

Share your link and earn free Premium days!

<b>Your referral link:</b>
{ref_link}

<b>📊 Your stats:</b>
• 👥 Referred users: {ref_count}
• 📊 Max referrals: {referral_max}
• 🎁 Earned days: {total_days}
• ⏱ Used days: {used_days}
• 📅 Available days: {avail_days}

{referral_requirement_note}"""

# ============================================================================
# MEDIA STORAGE UPGRADES
# ============================================================================
data['media_storage_title'] = """💾 <b>Media Storage</b>

Store and reuse media files across your scheduled messages. Save time by uploading once and using multiple times.

<b>📦 What you can store:</b>
• 📷 Photos and images
• 🎬 Videos
• 🎞 GIFs and animations
• 📄 Documents

<b>✨ Features:</b>
• 📁 Organize into storage boxes
• 🔄 Quick attach to any scheduled message
• 📊 Track usage and manage files
• 💾 Premium gets more storage space

<b>💡 Tip:</b> Save your most-used images (logos, templates) for quick access!"""

# ============================================================================
# TIMEZONE HINTS
# ============================================================================
data['timezone_city_found'] = """🏙 <b>City Found: {city}</b>

Based on your input, your timezone is:

<b>📍 Timezone: {tz}</b>

This means scheduled messages will be sent at the local time for {city}.

For example, a post set for "09:00" will be sent at 9:00 AM {tz} time.

<b>Is this correct?</b>"""

data['timezone_location_found'] = """📍 <b>Location Detected</b>

Based on your location, your timezone is:

<b>🕐 Timezone: {tz}</b>

All scheduled messages will use this timezone for accurate local publishing times.

<b>Is this correct?</b>"""

data['timezone_time_found'] = """🕐 <b>Time Analysis</b>

Based on your current time ({time}), your timezone is:

<b>🌍 Timezone: {tz}</b>

This means:
• Messages scheduled for 09:00 will send at 9:00 AM {tz} time
• All times you enter will be interpreted in this timezone

<b>Is this correct?</b>"""

# ============================================================================
# ADMIN PANEL UPGRADES
# ============================================================================
data['admin_panel_text'] = """🛡 <b>Admin Panel</b>

<b>📊 Bot Management:</b>
• 👥 <b>Users</b> — View and manage registered users
• 📢 <b>Channels</b> — Monitor connected channels
• 📊 <b>Statistics</b> — View bot-wide metrics
• 💳 <b>Promos</b> — Create and manage promo codes
• 📢 <b>Broadcasts</b> — Send messages to all users
• ⭐ <b>Premium</b> — Manage premium subscriptions
• 🛡 <b>Security</b> — Review security events

<b>💡 Tip:</b> Use the buttons below to access each section."""

# ============================================================================
# SEQUENTIAL ORDER UPGRADES
# ============================================================================
sequential_order_text = """📝 <b>Sequential Order Settings</b>

Choose how your photos should be ordered when using sequential mode:

<b>📅 By Date</b>
Photos are ordered by their upload date. Newest photos appear first or last based on your selection.

<b>📤 By Sent Order</b>
Photos are ordered by when they were last sent. This is useful for rotating through your media library.

<b>💡 Tips:</b>
• Use "By Date" for chronological content (e.g., photo series)
• Use "By Sent Order" to ensure fresh content is always shown first
• The order affects how photos are distributed across scheduled posts"""

# Update nested key
if 'sequential' in data:
    data['sequential']['order_detail'] = sequential_order_text

# Update flat key (used in code)
data['sequential_order_detail'] = sequential_order_text

# Add missing button label keys for sequential order selection
data['sequential_by_date'] = "📅 By Date"
data['sequential_by_sent'] = "📤 By Sent Order"

# ============================================================================
# HELP TEXTS - Add comprehensive help for all features
# ============================================================================

# Help for scheduling
if 'help.schedule.content' not in data or not data['help.schedule.content']:
    data['help.schedule.content'] = """<b>Scheduling Messages</b>

Learn how to schedule posts for your Telegram channels.

<b>📅 How to Schedule:</b>
1. Click the Schedule button in the main menu
2. Send your message with the date and time
3. Select which channel(s) to post to
4. Review and confirm

<b>📝 Date Format:</b>
Use DD.MM.YYYY HH:MM format (24-hour)
Example: <code>25.12.2026 15:30 Your message</code>

<b>💡 Tips:</b>
• You can also use relative dates like "Tomorrow" or "Monday"
• Add photos, videos, or documents to your posts
• Create polls by forwarding them during scheduling
• Use formatting (bold, italic, links) for rich text"""

# Help for channels
if 'help.channels.content' not in data or not data['help.channels.content']:
    data['help.channels.content'] = """<b>Managing Channels</b>

Connect and manage your Telegram channels.

<b>📢 Connecting a Channel:</b>
1. Make sure @FastSchedulerBot is an admin in your channel
2. Click the Channel button
3. Send your channel link or forward a message from it
4. Verify your admin status

<b>💡 Tips:</b>
• Free users can connect 1 channel
• Premium users can connect multiple channels
• Each channel has its own schedule and settings"""

# Help for sender bots
if 'help.bots.content' not in data or not data['help.bots.content']:
    data['help.bots.content'] = """<b>Sender Bots</b>

Dedicated bots for managing your channels independently.

<b>🤖 Why Use Sender Bots?</b>
• Faster message delivery (no shared bot rate limits)
• Better security (isolated channel data)
• Per-channel statistics
• Priority queuing

<b>📋 Setup:</b>
1. Create a bot via @BotFather
2. Add it as admin in your channel
3. Send the token to Fast Scheduler Bot
4. Verify the connection

<b>💡 Tips:</b>
• Premium users can connect multiple sender bots
• Each sender bot manages one channel"""

# Help for statistics
if 'help.statistics.content' not in data or not data['help.statistics.content']:
    data['help.statistics.content'] = """<b>Channel Statistics</b>

Track how your scheduled posts perform.

<b>📊 Available Metrics:</b>
• <b>Views</b> — How many users saw each post
• <b>Comments</b> — Discussion and engagement
• <b>Reactions</b> — User sentiment and interaction
• <b>Leaderboard</b> — Top-performing posts

<b>💡 Note:</b>
Statistics only track messages sent through this bot. Manual posts won't appear."""

# Help for recurring messages
if 'help.recurring.content' not in data or not data['help.recurring.content']:
    data['help.recurring.content'] = """<b>Recurring Messages</b>

Automate posts that repeat on a schedule.

<b>🔄 Types of Recurring:</b>
• <b>Daily</b> — Post every day at a specific time
• <b>Weekly</b> — Post on specific days
• <b>Monthly</b> — Post on specific dates

<b>📝 Format:</b>
Daily: <code>Daily HH:MM Your message</code>
Weekly: <code>Monday HH:MM Your message</code>
Monthly: <code>15 HH:MM Your message</code>

<b>💡 Use Cases:</b>
• Daily news updates
• Weekly announcements
• Monthly newsletters
• Regular reminders"""

# Help for media storage
if 'help.media_storage.content' not in data or not data['help.media_storage.content']:
    data['help.media_storage.content'] = """<b>Media Storage</b>

Save and reuse media files across your scheduled messages.

<b>💾 What You Can Store:</b>
• Photos and images
• Videos
• GIFs and animations
• Documents

<b>✨ Features:</b>
• Organize into storage boxes
• Quick attach to any scheduled message
• Track usage and manage files

<b>💡 Tips:</b>
• Save logos and templates for quick access
• Premium users get more storage space"""

# Help for AutoTime
if 'help.autotime.content' not in data or not data['help.autotime.content']:
    data['help.autotime.content'] = """<b>AutoTime - Best Posting Time</b>

Automatically determine the best time to post based on your channel's audience activity.

<b>🕐 How It Works:</b>
1. AutoTime analyzes your recent posts
2. It identifies when your audience is most active
3. It recommends the optimal posting time
4. You can apply this time to your schedule

<b>📊 Requirements:</b>
• At least 10 posts in your channel
• Posts must have view statistics available
• Channel must be connected to the bot

<b>💡 Tips:</b>
• Run AutoTime weekly for best results
• Combine with recurring posts for consistent timing
• Different channels may have different optimal times"""

# Help for calendar view
if 'help.calendar.content' not in data or not data['help.calendar.content']:
    data['help.calendar.content'] = """<b>Calendar View</b>

View all your scheduled messages on a monthly calendar.

<b>📅 Features:</b>
• Navigate between months
• See scheduled and recurring messages
• Times shown in your channel's timezone
• Visual overview of your posting schedule

<b>💡 Tips:</b>
• Use calendar to spot scheduling conflicts
• Check for gaps in your content calendar
• Combine with list view for detailed management"""

# Help for backup/export/import
if 'help.backup.content' not in data or not data['help.backup.content']:
    data['help.backup.content'] = """<b>Backup & Export</b>

Protect your data by creating backups and exports.

<b>💾 Backup Types:</b>
• <b>Full Backup</b> — All data (Premium, password-protected)
• <b>Export</b> — Selective export (messages, channels, etc.)

<b>📤 Export Formats:</b>
• <b>TXT</b> — Plain text, human-readable
• <b>CSV</b> — Spreadsheet compatible
• <b>JSON</b> — Structured data

<b>💡 Tips:</b>
• Export before making major changes
• Use password protection for sensitive data
• Keep backups in a safe location"""

# Help for premium features
if 'help.premium.content' not in data or not data['help.premium.content']:
    data['help.premium.content'] = """<b>Premium Features</b>

Unlock the full potential of Fast Scheduler Bot.

<b>⭐ Premium Benefits:</b>
• Unlimited channels
• 100+ scheduled messages
• 10+ recurring schedules
• Dedicated sender bots
• Advanced statistics
• Media storage
• Priority support

<b>💳 Plans:</b>
• Monthly — Flexible commitment
• Yearly — Best value (2 months free)

<b>💡 Tips:</b>
• Start with monthly to test features
• Upgrade to yearly for maximum savings
• Cancel anytime from settings"""

# Help for timezone settings
if 'help.timezone.content' not in data or not data['help.timezone.content']:
    data['help.timezone.content'] = """<b>Timezone Settings</b>

Set your timezone for accurate message scheduling.

<b>🕐 Why Timezone Matters:</b>
• Messages publish at your local time
• Recurring schedules respect your timezone
• Calendar view shows times correctly

<b>📍 Setting Methods:</b>
• Type city name (e.g., London)
• Send current time
• Share location
• Auto-detect from Telegram

<b>💡 Tips:</b>
• Set timezone during initial setup
• Update when traveling
• Each channel can have different timezones"""

# Help for formatting
if 'help.formatting.content' not in data or not data['help.formatting.content']:
    data['help.formatting.content'] = """<b>Text Formatting</b>

Make your messages stand out with rich text formatting.

<b>🎨 Available Formats:</b>
• <b>Bold</b> — Use asterisks: <code>*bold text*</code>
• <i>Italic</i> — Use underscores: <code>_italic text_</code>
• <code>Code</code> — Use backticks: <code>`code`</code>
• <u>Underline</u> — Use double underscores: <code>__underline__</code>
• <s>Strikethrough</s> — Use tildes: <code>~strikethrough~</code>
• 🔗 Links — Use: <code>[text](url)</code>

<b>💡 Tips:</b>
• Combine formats for emphasis
• Use links to drive traffic
• Test formatting before scheduling"""

# Help for polls
if 'help.polls.content' not in data or not data['help.polls.content']:
    data['help.polls.content'] = """<b>Polls & Quizzes</b>

Engage your audience with interactive polls.

<b>📊 Creating Polls:</b>
1. Create a poll in any Telegram chat
2. Forward the poll during scheduling
3. Set the date and time
4. The bot sends the poll automatically

<b>🎯 Poll Types:</b>
• Regular polls — Multiple choice
• Quizzes — One correct answer
• Anonymous polls — Hide who voted
• Multiple answers — Allow several choices

<b>💡 Tips:</b>
• Use polls for feedback
• Create quizzes for engagement
• Keep questions simple and clear"""

# Help for inline buttons
if 'help.inline_buttons.content' not in data or not data['help.inline_buttons.content']:
    data['help.inline_buttons.content'] = """<b>Inline Buttons</b>

Add interactive buttons to your scheduled messages.

<b>🔗 Button Types:</b>
• URL buttons — Link to websites
• Callback buttons — Trigger bot actions
• Switch buttons — Open chats

<b>📝 Syntax:</b>
Use the inline button syntax: <code>[Button Text](url)</code>

<b>💡 Tips:</b>
• Use for call-to-action links
• Keep button text short
• Test buttons before scheduling"""

# Help for media modes
if 'help.media_modes.content' not in data or not data['help.media_modes.content']:
    data['help.media_modes.content'] = """<b>Media Modes</b>

Choose how photos are attached to scheduled posts.

<b>📷 Available Modes:</b>
• <b>Normal</b> — Same photo for all posts
• <b>Random</b> — Random photo from set
• <b>Sequential</b> — Photos in order
• <b>Skip Photos</b> — Text-only posts

<b>💡 Use Cases:</b>
• Normal: Branding, logos, watermarks
• Random: Variety, A/B testing
• Sequential: Stories, tutorials
• Skip: Text announcements"""

# ============================================================================
# FAQ ENTRIES - Add FAQs for common questions
# ============================================================================

# Scheduling FAQs
if 'help.schedule.faq.1.q' not in data:
    data['help.schedule.faq.1.q'] = "What date format should I use?"
    data['help.schedule.faq.1.a'] = "Use DD.MM.YYYY HH:MM format (24-hour). Example: <code>25.12.2026 15:30</code>. You can also use relative dates like \"Tomorrow\" or \"Monday\"."

if 'help.schedule.faq.2.q' not in data:
    data['help.schedule.faq.2.q'] = "Can I schedule multiple messages at once?"
    data['help.schedule.faq.2.a'] = "Yes! Premium users can use multi-schedule to send multiple messages in one session. Free users can schedule one message at a time."

if 'help.schedule.faq.3.q' not in data:
    data['help.schedule.faq.3.q'] = "How do I add photos to scheduled posts?"
    data['help.schedule.faq.3.a'] = "Attach photos when sending your message. You can choose from different photo modes: Normal (same photo for all), Random (random photo from set), or Sequential (photos in order)."

# Channel FAQs
if 'help.channels.faq.1.q' not in data:
    data['help.channels.faq.1.q'] = "How many channels can I connect?"
    data['help.channels.faq.1.a'] = "Free users can connect 1 channel. Premium users can connect multiple channels (up to the plan limit)."

if 'help.channels.faq.2.q' not in data:
    data['help.channels.faq.2.q'] = "Why can't I connect my channel?"
    data['help.channels.faq.2.a'] = "Make sure @FastSchedulerBot is an admin in your channel with posting permissions. Also verify you're the channel owner or an admin."

# Bot FAQs
if 'help.bots.faq.1.q' not in data:
    data['help.bots.faq.1.q'] = "Do I need a sender bot?"
    data['help.bots.faq.1.a'] = "Sender bots are optional but recommended. They provide faster delivery, better security, and per-channel statistics. Free users can use the main bot without a sender bot."

if 'help.bots.faq.2.q' not in data:
    data['help.bots.faq.2.q'] = "How do I create a sender bot?"
    data['help.bots.faq.2.a'] = "1. Open @BotFather in Telegram\n2. Send /newbot\n3. Choose a name and username\n4. Copy the token\n5. Add the bot as admin in your channel\n6. Send the token to Fast Scheduler Bot"

# Statistics FAQs
if 'help.statistics.faq.1.q' not in data:
    data['help.statistics.faq.1.q'] = "Why don't my manual posts appear in stats?"
    data['help.statistics.faq.1.a'] = "Statistics only track messages sent through Fast Scheduler Bot. Posts made manually won't appear in your statistics."

if 'help.statistics.faq.2.q' not in data:
    data['help.statistics.faq.2.a'] = "Views are updated periodically. It may take some time for new views to appear in your statistics."

# Recurring FAQs
if 'help.recurring.faq.1.q' not in data:
    data['help.recurring.faq.1.q'] = "What's the difference between daily and recurring?"
    data['help.recurring.faq.1.a'] = "Daily messages post every day at the same time. Recurring messages can be set for any interval (daily, weekly, monthly) with more flexibility."

if 'help.recurring.faq.2.q' not in data:
    data['help.recurring.faq.2.q'] = "How many recurring messages can I create?"
    data['help.recurring.faq.2.a'] = "Free users can create 1 recurring message. Premium users can create multiple recurring messages (up to the plan limit)."

# AutoTime FAQs
if 'help.autotime.faq.1.q' not in data:
    data['help.autotime.faq.1.q'] = "How does AutoTime determine the best posting time?"
    data['help.autotime.faq.1.a'] = "AutoTime analyzes your recent posts and identifies when your audience is most active based on views, comments, and reactions."

if 'help.autotime.faq.2.q' not in data:
    data['help.autotime.faq.2.q'] = "How many posts do I need for AutoTime to work?"
    data['help.autotime.faq.2.a'] = "You need at least 10 posts with view statistics for AutoTime to analyze your channel activity."

if 'help.autotime.faq.3.q' not in data:
    data['help.autotime.faq.3.q'] = "Can I use AutoTime for multiple channels?"
    data['help.autotime.faq.3.a'] = "Yes! Each channel can have its own AutoTime analysis. Different channels may have different optimal posting times based on their audience."

# Calendar FAQs
if 'help.calendar.faq.1.q' not in data:
    data['help.calendar.faq.1.q'] = "How do I see all my messages in a list?"
    data['help.calendar.faq.1.a'] = "Use the Message List view for a full list of all scheduled messages. The calendar shows a visual overview, while the list shows detailed information."

if 'help.calendar.faq.2.q' not in data:
    data['help.calendar.faq.2.q'] = "Why don't I see my recurring messages on the calendar?"
    data['help.calendar.faq.2.a'] = "Recurring messages should appear on the calendar. If you don't see them, check that the recurring schedule is active and the date range includes the current month."

# Backup FAQs
if 'help.backup.faq.1.q' not in data:
    data['help.backup.faq.1.q'] = "How do I export my data?"
    data['help.backup.faq.1.a'] = "Step by step:\n1. Click <b>Export</b> on the main menu (page 2) or use <code>/export</code>\n2. Choose what to export: <b>Scheduled Messages</b>, <b>Recurring Messages</b>, or <b>Media Storage</b>\n3. Choose format:\n • <b>.txt</b> — plain text, human-readable\n • <b>.csv</b> — spreadsheet (opens in Excel/Google Sheets)\n • <b>.json</b> — structured data for developers\n4. The file is sent to you as a document\n\nFor a <b>full backup</b> (Premium): use <code>/backup</code> → choose password protection (optional) → the .fsback file is sent to you. To restore: use <code>/import</code> and send the .fsback file."

if 'help.backup.faq.2.q' not in data:
    data['help.backup.faq.2.q'] = "How do I restore a backup?"
    data['help.backup.faq.2.a'] = "Step by step:\n1. Click <b>Import</b> on the main menu (page 2) or use <code>/import</code>\n2. Send the backup file (.fsback or .fspback)\n3. If password-protected, enter the password when prompted\n4. The bot restores all your data — messages, channels, bots, settings\n5. You'll get a confirmation when done\n\n<b>Note:</b> Restoring a backup <b>replaces</b> your current data. Make sure to export your current data first if you want to keep it."

if 'help.backup.faq.3.q' not in data:
    data['help.backup.faq.3.q'] = "Can I set up automatic backups?"
    data['help.backup.faq.3.a'] = "Automatic backups are not available as a built-in feature yet. However, you can manually export anytime:\n• Use <code>/export</code> for selective export (scheduled, recurring, or media)\n• Use <code>/backup</code> for a full backup (Premium, can be password-protected)\n\nRecommendation: export your data regularly, especially before making big changes."

if 'help.backup.faq.4.q' not in data:
    data['help.backup.faq.4.q'] = "How do I create a password-protected backup?"
    data['help.backup.faq.4.a'] = "Premium feature. Step by step:\n1. Use <code>/backup</code> command\n2. When prompted, choose <b>Enable Password Protection</b>\n3. Enter a password (you'll need this to restore later — don't forget it!)\n4. The .fspback file is generated and sent to you\n5. To restore: use <code>/import</code> → send the .fspback file → enter the password\n\n<b>Warning:</b> Without the password, the backup <b>cannot</b> be restored. Keep your password safe!"

if 'help.backup.faq.5.q' not in data:
    data['help.backup.faq.5.q'] = "What's included in a full backup?"
    data['help.backup.faq.5.a'] = "A full backup (.fsback / .fspback) includes: all scheduled messages (text, media, settings), all recurring messages, media storage items and boxes, channel connections and settings, bot tokens and assignments, user preferences (language, timezone), and referral data. Everything needed to restore your account to exactly the same state."

if 'help.backup.faq.6.q' not in data:
    data['help.backup.faq.6.q'] = "What's the difference between .fsback and .fspback?"
    data['help.backup.faq.6.a'] = "<b>.fsback</b> is a standard full backup (no password). <b>.fspback</b> is a password-protected backup with encryption (Premium only). Both contain the same data, but .fspback requires a password to restore. To create a .fspback: use <code>/backup</code> → choose password protection → enter your password."

# Premium FAQs
if 'help.premium.faq.1.q' not in data:
    data['help.premium.faq.1.q'] = "What's the difference between free and premium?"
    data['help.premium.faq.1.a'] = "<b>Free:</b> 1 channel, 5 scheduled messages, 1 recurring message\n<b>Premium:</b> Unlimited channels, 100+ scheduled messages, 10+ recurring messages, sender bots, advanced statistics, media storage, and priority support."

if 'help.premium.faq.2.q' not in data:
    data['help.premium.faq.2.q'] = "Can I cancel my premium subscription?"
    data['help.premium.faq.2.a'] = "Yes, you can cancel anytime from the Premium menu. Your benefits will remain active until the end of your current billing period."

if 'help.premium.faq.3.q' not in data:
    data['help.premium.faq.3.q'] = "What happens to my data if I cancel premium?"
    data['help.premium.faq.3.a'] = "Your scheduled messages will continue to be sent. However, you'll be limited to free plan features: 1 channel, 5 scheduled messages, and 1 recurring message. Excess channels and bots will be frozen."

# Timezone FAQs
if 'help.timezone.faq.1.q' not in data:
    data['help.timezone.faq.1.q'] = "Why is my timezone important?"
    data['help.timezone.faq.1.a'] = "Your timezone determines when messages are published. If you set a post for 09:00, it will be sent at 9:00 AM in your timezone, not UTC."

if 'help.timezone.faq.2.q' not in data:
    data['help.timezone.faq.2.q'] = "Can different channels have different timezones?"
    data['help.timezone.faq.2.a'] = "Yes! Each channel can have its own timezone setting. This is useful if you manage channels in different regions."

if 'help.timezone.faq.3.q' not in data:
    data['help.timezone.faq.3.q'] = "How do I change my timezone?"
    data['help.timezone.faq.3.a'] = "Go to Settings → Timezone. You can set your timezone by:\n• Typing a city name (e.g., London, New York)\n• Sending your current time\n• Sharing your location\n• Auto-detecting from Telegram"

# Formatting FAQs
if 'help.formatting.faq.1.q' not in data:
    data['help.formatting.faq.1.q'] = "How do I make text bold?"
    data['help.formatting.faq.1.a'] = "Wrap the text in asterisks: <code>*bold text*</code>"

if 'help.formatting.faq.2.q' not in data:
    data['help.formatting.faq.2.q'] = "How do I add links to my messages?"
    data['help.formatting.faq.2.a'] = "Use the link syntax: <code>[text](url)</code>. For example: <code>[Click here](https://example.com)</code>"

if 'help.formatting.faq.3.q' not in data:
    data['help.formatting.faq.3.q'] = "Can I combine multiple formats?"
    data['help.formatting.faq.3.a'] = "Yes! You can combine formats. For example: <code>*bold and _italic_*</code> will show as bold and italic text."

# Poll FAQs
if 'help.polls.faq.1.q' not in data:
    data['help.polls.faq.1.q'] = "How do I create a poll?"
    data['help.polls.faq.1.a'] = "1. Create a poll in any Telegram chat\n2. Forward the poll to Fast Scheduler Bot during scheduling\n3. Set the date and time\n4. The bot will send the poll automatically"

if 'help.polls.faq.2.q' not in data:
    data['help.polls.faq.2.q'] = "What types of polls can I create?"
    data['help.polls.faq.2.a'] = "You can create:\n• Regular polls — Multiple choice options\n• Quizzes — One correct answer\n• Anonymous polls — Hide who voted\n• Multiple answer polls — Allow users to select several options"

if 'help.polls.faq.3.q' not in data:
    data['help.polls.faq.3.q'] = "Can I schedule quiz polls?"
    data['help.polls.faq.3.a'] = "Yes! Create a quiz poll in any chat, then forward it during scheduling. The bot will send the quiz at the scheduled time."

# Inline Button FAQs
if 'help.inline_buttons.faq.1.q' not in data:
    data['help.inline_buttons.faq.1.q'] = "How do I add inline buttons to my messages?"
    data['help.inline_buttons.faq.1.a'] = "Use the inline button syntax: <code>[Button Text](url)</code>. For example: <code>[Visit Website](https://example.com)</code>"

if 'help.inline_buttons.faq.2.q' not in data:
    data['help.inline_buttons.faq.2.q'] = "What types of inline buttons are supported?"
    data['help.inline_buttons.faq.2.a'] = "Currently, URL buttons are supported for scheduled messages. These allow users to click and visit a website."

if 'help.inline_buttons.faq.3.q' not in data:
    data['help.inline_buttons.faq.3.q'] = "Can I add multiple buttons?"
    data['help.inline_buttons.faq.3.a'] = "Yes! You can add multiple inline buttons by separating them with new lines:\n<code>[Button 1](url1)\n[Button 2](url2)</code>"

# Media Mode FAQs
if 'help.media_modes.faq.1.q' not in data:
    data['help.media_modes.faq.1.q'] = "What's the difference between normal and random mode?"
    data['help.media_modes.faq.1.a'] = "<b>Normal mode:</b> Every post gets the same photo. Great for branding.\n<b>Random mode:</b> Each post gets a random photo from your set. Great for variety."

if 'help.media_modes.faq.2.q' not in data:
    data['help.media_modes.faq.2.q'] = "When should I use sequential mode?"
    data['help.media_modes.faq.2.a'] = "Use sequential mode when the order of photos matters. This is perfect for:\n• Story sequences\n• Step-by-step tutorials\n• Photo essays\n• Any content where order is important"

if 'help.media_modes.faq.3.q' not in data:
    data['help.media_modes.faq.3.q'] = "Can I change the photo mode after scheduling?"
    data['help.media_modes.faq.3.a'] = "Yes! You can edit scheduled messages and change the photo mode. This is useful if you want to experiment with different attachment strategies."

# Media Storage FAQs
if 'help.media_storage.faq.1.q' not in data:
    data['help.media_storage.faq.1.q'] = "How much storage do I get?"
    data['help.media_storage.faq.1.a'] = "Free users get basic storage. Premium users get expanded storage with more space for photos, videos, and documents."

if 'help.media_storage.faq.2.q' not in data:
    data['help.media_storage.faq.2.q'] = "Can I organize my media?"
    data['help.media_storage.faq.2.a'] = "Yes! You can create storage boxes to organize your media files. This makes it easy to find and reuse specific images or videos."

if 'help.media_storage.faq.3.q' not in data:
    data['help.media_storage.faq.3.q'] = "What file types can I store?"
    data['help.media_storage.faq.3.a'] = "You can store:\n• Photos and images (JPG, PNG, etc.)\n• Videos (MP4, etc.)\n• GIFs and animations\n• Documents (PDF, etc.)"

# ============================================================================
# VERIFY: Check that no button labels were overwritten
# ============================================================================
button_keys_overwritten = []
for key in data:
    if is_button_label(key):
        # Check if the value is too long (likely a description)
        if len(str(data[key])) > 50:  # Button labels should be short
            button_keys_overwritten.append(key)

if button_keys_overwritten:
    print("⚠️ WARNING: The following button labels may have been overwritten with long text:")
    for key in button_keys_overwritten:
        print(f"  - {key}: {data[key][:50]}...")
    print("\nThese should be short button labels, not long descriptions!")
else:
    print("✅ All button labels remain short and clean!")

# Write the updated file
with open('translations/en.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f"\n✅ Updated {len(data)} translation keys")
print("All texts have been upgraded with comprehensive descriptions!")
print("Button labels have been preserved.")
