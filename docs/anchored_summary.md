# Automatic Post Sender — Project Summary

## Current State
All core features implemented. Security monitoring, multi-bot management routing, sender bot privacy/analytics, and comprehensive statistics/reporting engine complete.

## Key Completed Features

### Sender Bot Privacy & Statistics Engine (TASK 5)
- **`src/stats.py` rewritten**: Full isolated statistics engine with 7 tables (`sent_messages`, `message_reactions`, `message_views`, `message_comments`, `stranger_visits`, `stranger_conversions`, `automated_reports`). Thread-safe SQLite with WAL mode. All database writes are non-blocking (sync SQLite with thread lock, called from async handlers).
- **Sender Bot /start — Author View**: Shows detailed metadata (bot username, connected channel, management status, server time) with "👁 Hide Channel" / "👁‍🗨 Show Channel" toggle. `hide_channel` flag persisted in `bot_connections` via `toggle_hide_channel()` / `get_hide_channel()`. When hidden, strangers see "a channel" instead of the actual name.
- **Sender Bot /start — Stranger View**: Silent mode (no operational notifications ever sent). Records every stranger visit via `stats.record_stranger_visit()` with bot_username, channel_id, stranger_id, and timestamp for funnel analytics. Shows feature advertisement with deep link to Main Bot.
- **Statistics Main View**: Accessible from sender bot's menu (when management is moved) via "📊 Statistics" button. Shows per-channel average metrics (views, comments, reactions, total messages sent), most used reactions leaderboard (free feature), and the "Lock-In" warning about using the bot for all posts.
- **Leaderboard Sub-menu (`lb_` callbacks)**: Premium-only. Most Viewed/Most Commented/Most Reacted posts with time filters (Today, Week, Month, Year, All) and row count filters (10, 25, 50, 100). Free users see full Premium upsell.
- **Reports Sub-menu (`reports_`, `report_*` callbacks)**: Automated reporting system. Free users limited to 1 active report (with upsell on exceed). Premium users get unlimited reports. Supports create/view/edit/toggle/delete. Created via text input (`awaiting_report_name` flow).
- **Stats hook in send functions**: Both `send_scheduled_message` and `send_recurring_message` already call `stats.record_sent_message()` after successful send — no changes needed.
- **Admin backdoor**: All statistical data is structured in `stats.db` for future admin audit. `get_stranger_stats()` provides aggregate stranger analytics.

### Multi-Bot Management Routing
- **`managed_by_sender_bot` field** added to each `bot_connections` entry (stored in `user_settings`) — per-channel flag to track whether management is delegated to the sender bot
- **Helper functions**: `is_channel_managed_by_sender_bot()`, `set_channel_managed_by_sender_bot()`, `get_sender_bot_token_for_channel()`, `get_channel_sender_bot_username()`, `get_channels_managed_by_main()`
- **`BOT_IDENTITY` detection**: At startup, `detect_bot_identity()` checks if the current token is the Main Bot's (`MAIN_BOT_TOKEN`) or a sender bot's (looked up in `token_manager`). Sets global `BOT_IDENTITY` to `'main_bot'` or a dict with `{user_id, channel_id, bot_username, managed_by_sender_bot}`.
- **Main Bot `show_channel` UI**: Each channel row now shows management status:
  - No sender bot: unchanged (change/disconnect/set-default buttons)
  - Has sender bot, not managed: adds "Move management to @{bot}" button
  - Managed by sender bot: shows "🤖 @{bot}" badge + "Return to Main Bot" button
- **Move management flow**: Confirmation → sets `managed_by_sender_bot=True` → notifies user via sender bot's token → success screen with link to sender bot
- **Return management flow**: Confirmation → sets `managed_by_sender_bot=False` → success screen
- **Sender Bot `/start` menu**: When a sender bot instance runs (detected via `BOT_IDENTITY`), owner sees either:
  - "Move management to this bot" button (if not yet managed)
  - "Management Active!" with return option (if already managed)
- **Stranger view**: Non-owners see bot info with "Open Main Bot" button
- **Cross-bot notification**: Main Bot sends confirmation via sender bot's token using `Bot(token=...)` directly, no separate service needed
- **Translation keys**: 15 new keys in `en.json` covering move/return flow, managed status display, sender bot welcome screens

### Security Monitoring
- **`src/security_monitor.py`**: Conservative regex scanner for SQL injection, command injection, code execution, token leaks, path traversal. Patterns scored by severity (1-5); only score ≥ 4 triggers admin notification. Rate-limited to 1 notification per 5 minutes per user.
- **Global handler at group -1**: Scans ALL text messages before any handler; does NOT stop message propagation
- **Non-admin /admin**: Logs attempt + calls `handle_random_text()` instead of showing "access denied"

### Bot-Channel Binding
- "🤖 Bots" → "🤖 Connected bots" label change
- `_send_bot_connected_menu`: channel-first prompt, bot list with URL/Change/Remove, "Add new bot" → channel picker (premium) / upsell (free at limit) / hidden (premium at max)
- `change_bot_{i}`: warning → token prompt → replace (stores `replace_bot_index`)
- `addbot_channel_picker`: shows all channels with ✅/❌ bot status; click-with-bot → "Change?"; without bot → normal connect
- Remove flow: last-bot → disconnect downsides + "Reconnect bot"; remaining bots → success + back
- `token_manager.store_token` accepts `channel_id` for binding display
- `onboard_bot.add_bot_token_from_text`: passes `pending_bot_channel` to `store_token`; handles replace (removes old after new stored); bypasses limit check in replace mode; fixed `_t(user_id, 'error')` → `_t(user_id, 'error_occurred')`

### Premium Lifecycle
- **Cancellation**: `set_user_premium` does NOT clear `premium_cancel_requested`; only `extend_user_premium` (new payment) clears it
- **1-week expiry warnings**: Warnings at 7, 3, and 1 day(s) before expiry via `periodic_subscription_check` → `_send_premium_expiry_warning`
- **Re-enable auto-renewal**: `premium_reenable_auto_renew` callback clears `premium_cancel_requested`
- **Expiry cleanup**: `notify_subscription_lost` disconnects excess channels (>1) and bots (>1), logs cleanup

### Free User Limits
- Media storage: max 1 storage, max 100 media items (`media_save_handler` checks both)
- Videos: blocked in storage for non-premium (`has_premium` check in `media_save_handler`)
- Videos in schedules/recurring: max 50 MB enforced with file_size check
- Backup/export: `backup_export = False` for free; premium check added at `export_menu` entry

### Admin Panel
- Username `@` search: `channel_connect_text_handler` no longer intercepts `@` texts (only `https://t.me/` and `-100`)
- `query.data` read-only: all 275 occurrences replaced with `qdata` mutable local in `button_handler`; 3 recursive-call sites use `context.user_data['_btn_qdata']`
- `filename` unbound: fixed in export catch-all with `filename = None` init + `else` error alert
- Username lookup: `admin_block_user_handler`, `admin_send_message_handler` search by `@username` or name
- Admin prompts updated to mention `@username`
- "⭐ Premiums" admin menu: Premium Statistics, Toggle Purchases, Toggle My Premium, Grant/Revoke (enter ID/username), Money Back (enter ID/username, revokes premium, logs refund)
- State definitions: `ADMIN_PREMIUMS_GRANT = 26`, `ADMIN_PREMIUMS_MONEY_BACK = 27`
- Conversation handlers: `admin_premiums_grant_conv`, `admin_premiums_money_back_conv` registered

### Bug Fixes
- SetDate bot `/cancel` resets `context.user_data['broadcast_mode'] = False`
- Recurring messages: `schedule_send_recurring` uses `application.create_task`
- Scheduled messages: `schedule_scheduled_message` and `post_init` periodic tasks use `application.create_task`
- All scheduler-created tasks use `application.create_task` (APScheduler non-async thread)

## Remaining Minor Items
1. Add `can_upload_video: True` to premium limits dict for consistency (video upload in storage uses `has_premium` directly, so not blocking)
2. Update promo/benefit texts to reflect current limits (storages 20 instead of unlimited, etc.)
3. Full end-to-end testing of premium lifecycle, free user limits, backup restriction

## Key Files
- `main.py` (~13007 lines): All handlers, menus, premium lifecycle, admin panel
- `onboard_bot.py` (~270 lines): Token handling with replace logic and channel_id
- `token_manager.py` (~125 lines): `store_token` with `channel_id` parameter
- `SetDate/bot.py` (~2020 lines): `/cancel` clears `broadcast_mode`
- `translations/en.json`: All UI strings

## Critical Architecture Notes
- `qdata = context.user_data.pop('_btn_qdata', None) or query.data` at line ~8225 avoids mutating read-only `query.data`
- `has_premium()` checks both `premium` flag AND expiry date; cancel request does NOT affect it
- `get_user_limit()` at line 1204 returns limits by subscription tier; free (subscribed): channels=1, bots=1, media_storage_count=1, media_items_total=100, backup_export=False; premium: channels=3, bots=3, media_storage_count=20, media_items_total=inf, backup_export=True
- `periodic_subscription_check` runs hourly; checks 7/3/1 day warnings; on expiry: removes premium + cancel request, calls `notify_subscription_lost`
