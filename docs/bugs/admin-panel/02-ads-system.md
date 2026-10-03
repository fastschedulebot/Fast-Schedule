# 02 — ADS SYSTEM (advertiser ads shown to users)

Scope: advertiser-ad creation flow, placement targeting, duration/days,
impression & click tracking, inline buttons, auto-reports.
Read-only investigation. No `src/` edits made.

Legend: ✅ complaint VERIFIED TRUE (bug exists) · ❌ complaint VERIFIED FALSE (works / not a bug)

---

## 1. Architecture: two systems share one name, only one is live

There are **two** parallel implementations that both call themselves the "ad system":

**A. LIVE — one-shot tagged broadcast (the only reachable path).**
Entry: admin presses `admin_broadcast` → `handle_admin_broadcast`
(`src/callbacks/admin/panel.py:110-120`, returns `BROADCAST_MESSAGE`)
→ admin sends message content → `admin_broadcast_handler`
(`src/admin/handlers.py:407-536`, stores `broadcast_text/entities/media`,
then asks `broadcast_ad_prompt` = "Is this an advertisement?")
→ `broadcast_ad_yes` / `broadcast_ad_no`
(`src/callbacks/admin/panel.py:339-374`)
→ target `broadcast_ad_target_free` / `broadcast_ad_target_all`
(`src/callbacks/admin/panel.py:377-390`)
→ orderer-name prompt `_show_ad_orderer_prompt`
(`src/callbacks/admin/panel.py:393-405`)
→ text input handled by `broadcast_ad_orderer_handler`
(`src/admin/handlers.py:738-773`) or skip button
`handle_broadcast_ad_skip_orderer` (`src/callbacks/admin/panel.py:408-427`)
→ auto-deletion choice → recurring choice → `_broadcast_send`
(`src/admin/handlers.py:61-379`).
Wired in `src/register.py:461-516` (`admin_broadcast_conv`) and routed in
`src/callbacks/admin/main.py:274-293` + `src/buttons.py:41-42`
(`broadcast_` prefix → admin module).

**B. DEAD — "Ad System" menu + persistent ad objects (`src/callbacks/admin/broadcasts.py`).**
`handle_broadcast_ad_menu` (`broadcasts.py:204-237`) reads
`bot_data.get('ads', [])` and renders ✏️ edit / ❌ delete per ad plus a
`broadcast_ad_new` button; `handle_broadcast_menu/new/history/info/execute`
(`broadcasts.py:46-440`) implement a separate `broadcast_create` dict with
name/text/audience/buttons/auto_delete/scheduled/recurring.
**None of these functions is imported or routed anywhere:**
`rg` over `src/` + `translations/` shows references only inside
`broadcasts.py` itself — no import in `src/callbacks/admin/main.py`,
`src/buttons.py`, or `src/register.py`; no router branch handles
`broadcast_ad_menu`, `broadcast_ad_new`, `broadcast_ad_edit_*`,
`broadcast_ad_delete_*`, `broadcast_menu`, `broadcast_new`,
`broadcast_history`, `broadcast_info_*`, `broadcast_resend_*`.
So the "📢 Ad System" menu button (`broadcasts.py:78`) is unreachable in
production, and every button it renders is dead.
Additionally the module would crash if it ever ran: `BotData` defines **no
`.get()` method** (`src/core/botdata.py` — only `get_user_scheduled_ids`,
`get_user_recurring_ids`; `rg "def get"` confirms), yet `broadcasts.py:52,
129, 169, 210` calls `bot_data.get('broadcasts', [])` /
`bot_data.get('ads', [])` → `AttributeError`. Likewise `BotData.__init__`
(`botdata.py:542-651`) and `DOMAIN_FILE_MAP` define **no `ads` or
`broadcasts` domain** — there is no persistence, migration, or backup entry
for them (only `broadcast_deletions` exists). Any ad object created there
could never be saved.

Net effect: users see at most **system A** (a broadcast with `[AD]` / `[AD,
<orderer>]` appended to the text). Everything that looks like a real ads
manager lives only in dead code.

---

## 2. Complaint-by-complaint verdicts

### 2.1 "Ad creation breaks after choosing advertiser name (talks about auto-deletion, menu says broadcast)" — ✅ TRUE

Two breakage layers:

1. **Conversation is terminated at exactly that step.** Both orderer paths
   return `ConversationHandler.END` instead of the next state:
   - text input: `src/admin/handlers.py:773` (`return ConversationHandler.END`)
   - skip button: `src/callbacks/admin/panel.py:427` (`return ConversationHandler.END`)
   The `BROADCAST_AD_ORDERER` state definition (`src/register.py:487-490`)
   expects to stay inside the conversation; returning `END` tears it down.
   Continuing only works because `broadcast_ask_delete` / `broadcast_send_now`
   are *also* registered as conversation **entry points**
   (`src/register.py:467,475`), i.e. the flow relies on re-entry, not on a
   continuous state machine. Any stray message sent before pressing the next
   button falls into no-man's-land (no active conversation), and all
   `broadcast_*` context keys survive only by accident of `context.user_data`
   not being cleared until `_broadcast_send` (`admin/handlers.py:373-375`).
2. **Wording/context switch confirms the "menu says broadcast" half.**
   Immediately after the orderer step both handlers show the *generic*
   broadcast prompt, not an ad prompt:
   - `src/admin/handlers.py:768-772`: `t(...,'broadcast_autodelete_prompt')`
     = `"📢 <b>Broadcast: Auto-Deletion</b>\n\nDo you want the broadcast to be
     automatically deleted…"` (`translations/admin/en.json:493`)
   - `src/callbacks/admin/panel.py:421-426`: identical prompt.
   Cancel buttons point to `admin_panel`, later steps ask
   `broadcast_recurring_prompt` ("Make this a recurring broadcast?",
   `en.json:504`) and send via the shared `_broadcast_send`. The
   `broadcast_is_ad` / `broadcast_ad_orderer` flags are stored
   (`panel.py:343,381,389`; `handlers.py:748-750`) but **never change control
   flow** except the `free`-vs-all filter (see §2.2) — an "ad" and a normal
   broadcast take the same remaining path.

### 2.2 "No placement choice (where the ad shows — e.g. like the SetDate ad on schedule message)" — ✅ TRUE

Live ad targeting is a single DM-blast audience flag, not a placement picker:
- Only two live options: `broadcast_ad_target_free` ("🆓 Only Free Users",
  `panel.py:377-382`) and `broadcast_ad_target_all` ("👥 All Users",
  `panel.py:385-390`). `_broadcast_send` (`src/admin/handlers.py:91-98`)
  implements exactly this: `free` → skip premium users, else premium-first
  ordering to **every** `bot_data.all_users` key.
- A third key `broadcast_ad_target_premium` ("⭐ Premium Users Only")
  exists in `translations/admin/en.json:457` but has **no button, no handler,
  no router branch** — dead string.
- There is **no placement enum anywhere** (`rg placement` hits only an
  unrelated disk-capacity doc in `src/core/storage_policy.py:87`). No
  "show on schedule message / on channel-link screen / as DM" choice, no
  per-surface slot, no frequency cap. `_broadcast_send` only sends standalone
  DMs (`send_message/send_photo/video/document/…`, `handlers.py:197-317`).
- The SetDate ad the complaint cites is a **different, hardcoded mechanism**,
  not a placement the advertiser flow can use (see §3).

### 2.3 "No command-vs-button choice" — ✅ TRUE (for ads)

Generic broadcasts *do* have a button builder (`broadcast_button_text_handler`,
`src/admin/handlers.py:542-668`, supports `Label | https://…` URL buttons and
`schedule / recurring / premium / text:…` callback buttons; UI in
`handlers.py:654-664`), and `_broadcast_send` renders `broadcast_buttons`
(`handlers.py:102-128`). **But the live ad path never offers it.** After the
orderer step the only keyboards are auto-deletion (`handlers.py:763-767`,
`panel.py:416-420`) then recurring (`handlers.py:725-729`) then send. The
`BROADCAST_BUTTONS` state (`register.py:478`) is reachable only via the dead
`broadcasts.py` settings menu (`broadcasts.py:292-298`), never from the live
`BROADCAST_AD_ORDERER → …` chain. So an advertiser ad cannot get inline
buttons or a command trigger through the supported flow; `broadcast_buttons`
is simply empty (`[]`) for every ad-tagged send.

### 2.4 "No duration-days setting" — ✅ TRUE

There is no campaign duration / start-end / "run N days" concept:
- The only time control is **one-shot message auto-deletion**: admin types a
  natural-language deletion time (`broadcast_delete_time_handler`,
  `src/admin/handlers.py:674-735`), it is stored as a single
  `broadcast_delete_at` datetime, each sent copy registers
  `{chat_id, message_id, delete_at}` in `bot_data.broadcast_deletions`
  (`handlers.py:321-331`), and `periodic_broadcast_deletion`
  (`src/services/periodic.py:487-512`) deletes them on a 60 s loop.
- No `duration_days`, `starts_at/ends_at`, impression-cap, or rotation fields
  exist on any ad/broadcast record (`rg duration_days|starts_at|ends_at`
  finds nothing ad-related; `broadcasts.py:93-105` dead dict has only
  `auto_delete/scheduled_at/is_recurring/recurring_interval`).
- The dead menu's list shows only `target` + `active` (`broadcasts.py:222-223`)
  and the translation bundle has no duration/expiry strings for ads.

### 2.5 "No view counts" — ✅ TRUE

Zero impression tracking for ads/broadcasts:
- `_broadcast_send` counts only `sent_count / failed_count` from send-call
  success (`handlers.py:88-89,319-356`) — delivery attempts, not views.
- `rg` for `impression|ad_views|ad_clicks|ad_report|ad_stats` across
  `src/` + `SetDate/` returns **no hits**. `src/services/stats.py` tracks
  channel-post engagement (reactions/views/comments for scheduled channel
  posts, `stats.py:226-249`), never DM broadcasts or `[AD]` messages.
- `broadcast_is_ad` is write-only: set in `panel.py:343` / cleared in
  `panel.py:362`, never read except the audience filter; it is not persisted
  on any record and no counter is incremented when a user reads the ad.

### 2.6 "No inline buttons (+colors)" — ✅ TRUE (buttons) · ❌ FALSE (colors — not a real Telegram feature)

- Buttons: per §2.3, ads sent through the live flow carry no
  `reply_markup` (`broadcast_buttons` is always `[]` on that path), so the
  complaint "ads have no inline buttons" is confirmed.
- Colors: Telegram **has no colored inline buttons** — `InlineKeyboardButton`
  supports only `text/url/callback_data`. The `style='success'/'danger'` args
  seen in `broadcasts.py:76,114,226-232` belong to the project's own `btn()`
  menu-render helper (admin-panel cosmetics), not to anything sent to users.
  Expecting per-button colors on the user-facing ad is therefore not an
  implementable requirement; the actionable part is "no buttons at all".

### 2.7 "No click counts" — ✅ TRUE

- The only ad-adjacent callback, `broadcast_reply:<text>`
  (`src/callbacks/admin/panel.py:39-55`), statically edits/shows a canned
  reply — **no counter, no logging, no stats write**.
- `_broadcast_send` builds `reply_markup` from `broadcast_buttons`
  (`handlers.py:102-128`) but registers no callback instrumentation; no
  handler increments a per-button or per-ad click counter.
- `src/services/tracking.py` ("first read and then left in place… served to
  admins via /tracking", `tracking.py:9,149`) covers message-read tracking
  for scheduled content, not broadcast/ad button clicks. No `ad_clicks`
  storage exists.

### 2.8 "No auto-reports" — ✅ TRUE

- `periodic_report_delivery` (`src/services/periodic.py:516-…) delivers
  channel-statistics reports, not advertiser reports; nothing queries
  `broadcast_is_ad` / orderer / clicks / views.
- Broadcast history (dead `broadcasts.py:123-159` → `sent/total`; live flow
  keeps no `broadcasts` list at all — the live `_broadcast_send` only reports
  `sent/failed` once to the admin, `panel.py:505-519`, then wipes
  `context.user_data`, `panel.py:520-521`) has no per-advertiser breakdown, no
  scheduled/daily auto-report, no delivery-to-advertiser path.
- Translation bundle has report strings for channel stats and promo-code
  stats (`promo_stats_*`, `stats_*`) but **none for ads**.

---

## 3. Comparison: how the SetDate ad works, and can it be reused?

The "SetDate ad on schedule message" is a **hardcoded cross-promo follow-up
message**, unrelated to the advertiser/broadcast pipeline:

- Implementation: `_send_setdate_promo(update, user_id)`
  (`src/core/helpers.py:2037-2059`) sends `t(...,'setdate_promo')` as a
  **separate** message with two buttons — `use_setdate` (URL
  `https://t.me/{SETDATE_BOT_USERNAME}?start=from_main_{user_id}`,
  `helpers.py:2044`) and a hide button (`setdate_dont_show_btn` for premium
  vs `setdate_hide_ad_premium_btn` upsell for free, `helpers.py:2047-2050`).
- Placement: it is invoked **after** specific user flows, not as a broadcast —
  call sites: after schedule-photo review (`src/callbacks/scheduler.py:395`),
  after schedule/channel review screens (`scheduler.py:585,666,945`), after
  channel-link screens (`src/callbacks/channels.py:1239,1301`), after
  settings/help entry points (`src/handlers/commands.py:3225,3252,3316,3326,
  3350`). I.e. the "placement mechanism" is simply "call a helper at the end
  of a flow".
- Gating/persistence: per-user `user_settings[uid]['hide_setdate_promo']`
  boolean (`helpers.py:2024-2034`, `scheduler.py:404-414,427-513`);
  `setdate_promo_effective_hidden` force-unhides for non-premium
  (`helpers.py:2030-2033`), and free users pressing hide get a premium upsell
  (`setdate_hide_ad_premium_body`, `scheduler.py:416-424`).
- Tracking: **none** — no impression or click counter is written when the
  promo is shown or its buttons pressed.

**Reuse verdict: pattern — yes; code — not directly.**
The *pattern* (post-flow hook + per-user hide flag + premium-gated hide vs
upsell) is exactly what advertiser placements need and could be generalized
into `show_ad_slot(user_id, placement)` with rotation/targeting/frequency
logic. But today's code is single-tenant (one hardcoded SetDate promo, one
boolean flag, no slot registry, no duration, no metrics), so an advertiser
system cannot "plug into" it — it needs a new slot registry, an `ads` domain
with scheduling, and impression/click logging at each call site.

---

## 4. Other bugs found (ads/broadcast scope)

| # | Severity | Bug | Location | Impact |
|---|----------|-----|----------|--------|
| 1 | 🔴 High | Dead "Ad System" menu + `broadcasts.py` fully unwired; would crash via `bot_data.get()` (no such method) if ever routed | `src/callbacks/admin/broadcasts.py:46-440`; `src/core/botdata.py:542+` (no `get`, no `ads`/`broadcasts` domain) | Admin-facing dead ends; any attempt to "finish" the ad menu on top of this file inherits the crash + no persistence |
| 2 | 🔴 High | `broadcast_ad_orderer_handler` and skip path return `ConversationHandler.END`, fragmenting the create flow into re-entries | `src/admin/handlers.py:773`; `src/callbacks/admin/panel.py:427` | Stray messages lost mid-flow; state survives only via uncleared `user_data`; fragile UX exactly matching complaint 2.1 |
| 3 | 🟡 Medium | Audience asymmetry: `free` filter exists, `all` exists, `premium`-only string exists but is unreachable | `translations/admin/en.json:457` vs `panel.py:377-390`, `handlers.py:91-98`, `register.py:470-471` | Cannot target premium users (e.g. upsell ads); targeting story is half-built |
| 4 | 🟡 Medium | `[AD]` / `[AD, orderer]` tag appended as raw text with explicitly skipped entity-offset handling for the orderer case only; header-prepend logic in `_broadcast_send` shifts `broadcast_entities` by `announcement_header` length (`handlers.py:132-176`) but the AD suffix append (`handlers.py:752-760`, `panel.py:412-415`) documents "no offset adjustment needed" — true only while the tag is plain text; any future formatting of the tag silently breaks entity alignment | `src/admin/handlers.py:752-760`; `panel.py:412-415`; `handlers.py:132-176` | Fragile formatting; advertiser names with HTML chars (`<`, `&`) are interpolated unescaped into an HTML-sent message |
| 5 | 🟡 Medium | Orderer name never validated/sanitized: empty string stored as-is (only exact `skip/-/no` skipped, `handlers.py:744-750`); over-long names unbounded; HTML-injection via `f"[AD, {orderer}]"` then sent with `parse_mode=HTML`/`entities` path | `src/admin/handlers.py:744-758` | Broken rendering or markup injection in every recipient's DM |
| 6 | 🟡 Medium | Button-builder actions allow only `schedule/recurring/premium/text:` + URLs (`handlers.py:600-623`); no `command:` action despite complaint, and ad flow can't reach the builder at all (§2.3) | `src/admin/handlers.py:600-623` | Feature gap + dead-end for "command-vs-button" ask |
| 7 | 🟢 Low | `broadcast_ad_target_premium`, `broadcast_ad_hide_btn`, `broadcast_ad_premium_link`, `broadcast_ad_new_title` strings exist but are unused or orphaned (`translations/admin/missing_admin.txt:259-374` lists several as missing/unused) | `translations/admin/en.json:454-459`; `missing_admin.txt` | i18n drift; future dev may assume premium-targeting works |
| 8 | 🟢 Low | Live broadcasts keep no persistent `broadcasts` history (only dead code does); post-send the only record is the ephemeral admin summary + `broadcast_deletions` entries | `src/admin/handlers.py:61-379` (no `broadcasts` write) vs `broadcasts.py:364-381` | No audit trail for what ads went to whom — blocks any future reporting until a send-log exists |

---

## 5. Minimal fix direction (for the implementing agent, not this report)

1. Decide: delete `src/callbacks/admin/broadcasts.py` ad-menu **or** wire + persist it — never both half-alive. Cheapest consistent path is extending the **live** conversation: keep states instead of `END`, add placement step (DM blast vs named post-flow slots reusing the `_send_setdate_promo` hook pattern), add button step (reuse `BROADCAST_BUTTONS`), add duration-days step, persist a send-log record `{is_ad, orderer, target, placement, buttons, delete_at, sent/failed}`.
2. Add `ads`/send-log domain (or reuse a `broadcast_log` list) + impression/click counters on show/click handlers before promising reports.
3. "Button colors" should be closed as wont-fix with explanation (Telegram limitation); offer emoji-prefixed labels instead.
