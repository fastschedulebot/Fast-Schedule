#!/usr/bin/env python3
"""Upgrade all translation texts with comprehensive, detailed descriptions."""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('translations/en.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# ============================================================================
# PHOTO MODE UPGRADES - Add detailed descriptions of what each mode does
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

# Write the updated file
with open('translations/en.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f"✅ Updated {len(data)} translation keys")
print("All texts have been upgraded with comprehensive descriptions!")
