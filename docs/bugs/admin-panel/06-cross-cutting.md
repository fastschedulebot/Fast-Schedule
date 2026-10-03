# Admin Panel — 06 Cross-Cutting: translation keys, dead buttons, data-source audit

Scope: admin panel + broadcast (old flow) + ads/bulk screens, promos, users, stats/exports screens.
Method: read-only code inspection + scripted key/callback enumeration (scripts in
`C:\Users\MAX\AppData\Local\Temp\opencode\audit_keys2.py`, `audit_cb.py`).
Live wiring is `src/register.py` → `src/buttons.py:_PREFIX_DISPATCH` → `src/callbacks/admin/main.py:handle()`
(entry: `src/main.py:648` → `src/register.py:1164 run()` → `build_app()`).

---

## A. Translation keys (`t()` resolution, EN + RU)

`t()` fallback chain (`src/core/i18n.py:122-160`): for admins, `translations/admin/<lang>` →
`translations/admin/en` → `translations/<lang>` → `translations/en` → raw key.
`translations/admin/ru.json` contains **only 26 keys** (getdata/deleteuser strings) vs hundreds of
nested keys in `translations/admin/en.json`.

### A1. EN — 2 true raw-key renders (key shown literally to the user)
Both keys are used in `src/handlers/export.py:455,461,629,638` and exist in **neither**
`translations/en.json` nor `translations/admin/en.json` (verified by direct lookup):

- `import_quota_exceeded`
- `import_too_many_messages`

Reachable via the shared import flow (`/import`, photo/file import quota guards). The admin
getdata/restore path reuses these import handlers, so an admin restoring a large backup also hits
the raw key. (Overlap note for the downloads agent.)

### A2. RU — no raw keys, but the entire admin panel renders in English for RU admins
673 `t()` keys used across `src/callbacks/admin/*.py`, `src/admin/handlers.py`,
`src/admin/helpers.py`, `src/handlers/promos.py`, `src/handlers/export.py` were resolved against
(admin_ru, admin_en, main_ru, main_en) with the exact `_resolve()` semantics (flat + dotted +
first-underscore split + `btn`/`button` label rule). Result:

- **EN-missing: 2** (A1 above — the only raw renders).
- **RU-missing (falls back to `admin/en` English): 437.** Every admin screen is affected, including
  all broadcast/ads keys: `broadcast_ad_yes/no/prompt/tag/target_*`, `broadcast_autodelete_*`,
  `broadcast_recurring_*`, `broadcast_send_now`, `broadcast_video_note_detected`,
  `broadcast_poll_detected`, `admin_broadcast_*`, `admin_prem_*`, `admin_syshealth_*`,
  `admin_revenue_*`, `admin_security_*`, `admin_sub_*`, `admin_promo_*`, `dd_*`, `issue_*`,
  `admin_dashboard_*`, etc. (full list reproducible via `audit_keys2.py`).
- So: **RU admin sees English everywhere in the admin panel; nothing renders as a raw key**
  (EN fallback always hits), except the 2 keys in A1 which are raw in *all* languages.
- `translations/admin/missing_admin.txt` (20 KB) already acknowledges part of this gap.

### A3. Broadcast/ads screens specifically
All `broadcast_*` / `admin_broadcast_*` keys resolve in EN (`panel.py`, `admin/handlers.py` usage).
In RU they render in English (per A2). No raw-key render on these screens. One adjacent find:
`src/admin/handlers.py:648-650` uses a hardcoded English string
(`"You can add more buttons or click <b>Done</b>…"`) instead of `t()` — untranslatable in all languages.

---

## B. Dead buttons (`callback_data` with no registered handler)

Dead = emitted by live UI, matches no `_PREFIX_DISPATCH` branch with a real sub-handler, matches no
explicit `CallbackQueryHandler` pattern, and `callbacks/admin/main.py:handle()` falls through to
`return None` (line 362) — spinner dismisses, **nothing happens, no error shown**.
(`src/buttons.py:750-789`: prefix loop → no match → legacy-alias check → `internal_error_alert`
only for non-admin legacy aliases; admin callbacks returning None stay silent.)

### B1. CONFIRMED DEAD (live UI emits, no handler)
1. **`promo_remove_{code}`** — emitted by the live promocodes menu
   (`src/callbacks/admin/panel.py:237`). `_PREFIX_DISPATCH` routes `promo_remove_` → `admin_cb`
   (`src/buttons.py:91`), but `main.py:handle()` has **no** `promo_remove_` branch → returns None.
   The "Remove promo" button on the promocodes menu is a silent no-op.
   `confirm_remove_promo_*` (`src/buttons.py:92`) is doubly dead: no emitter *and* no branch.
2. **`aev_{i}`** (encrypted-file viewer) — emitted `src/admin/handlers.py:1900`. Prefix `aev_`
   routes to `admin_cb`, no branch in `handle()` → clicking a file in the Encrypted Data Manager
   does nothing.
3. **`admin_enc_list`** ("back to file list") — emitted `src/admin/handlers.py:2008`. No branch →
   dead back button after saving an enc file.
4. **`admin_sub_add`** ("Add" on subscription-channels screen) — emitted
   `src/callbacks/admin/subscription.py:37`. The conversation entry
   (`src/register.py:542-553`) calls `button_handler`, which dispatches to `admin_cb.handle()` →
   no branch → returns None → `ADMIN_SUB_ADD` state is **never entered**, so
   `admin_sub_add_handler` (`src/admin/handlers.py:2846`) is unreachable. "Add" silently dies.
5. **`broadcast_add_url` / `broadcast_add_callback` / `broadcast_buttons_done`** — emitted
   `src/admin/handlers.py:656-660` (button-builder step). They are *both* conversation entries
   (`src/register.py:464-466`) and fallbacks (`:502-504`), all via `button_handler` → no branch in
   `handle()` → returns None → **clicking Add-URL / Add-callback / Done kills the broadcast flow
   silently**. (Overlap: broadcast-compose agent owns the flow fix; the wiring defect is recorded here.)

### B2. ORPHANED modules (reachable code that no UI links to — not clickable, but rots/confuses)
- `src/callbacks/admin/broadcasts.py` — full new broadcast menu (`broadcast_menu/new/history/
  info_/audience_*/confirm_send/execute/schedule/add_buttons/add_media/ad_menu/ad_new/ad_edit_/
  ad_delete_/delete_/resend_`). Zero imports of any `handle_broadcast_*` from it; no branch in
  `main.handle()`; panel links only to the old `admin_broadcast` flow (`src/keyboards.py:419`).
  Note: its `_get_user_count()` (`broadcasts.py:26-34`) supports a `premium` audience the live flow
  never offers (live: all/free only).
- `src/callbacks/admin/promos.py` detail screens (`promo_info_/stats_/edit_/delete_/
  delete_confirm_/edit_field_`) — no branch in `main.handle()` **and** no `_PREFIX_DISPATCH`
  match (`promo_info_` ≠ `promo_remove_`/`premium_` prefixes) → if ever emitted, falls through to
  `internal_error_alert`. Currently unemitted.
- `dlb_` prefix (`src/buttons.py:90`): no emitters anywhere, no branch — stale.

### B3. Verified NOT dead (spot-checked branches/prefixes + explicit patterns)
`admin_panel(_2)`, `admin_dashboard/system_health/issue_log/audit_log/bot_fleet/revenue/
security_log/global_messages/backup/expiring_premiums`, `admin_stats/encrypted_mgr/toggle_storage/
view_mode/promocodes_menu/deep_link_builder/clear_cache/privacy_mode*`, users search
(`admin_advanced_search/search_premium/free/blocked/lang`, `admin_all_users_*` pagination,
`admin_user_info(_show_)/block/send/set_limit`, `admin_toggle_premium_/block_` + confirms,
`admin_prof_reset_/unblock_`, `admin_user_sig_(back)`), premiums menu/grant/money-back/
`admin_prem_start_now/custom`, ratings menu/list/about/reply(+send), feedback chains
(`filter_/view_/reply_/mark_spam/close_/delete_` + confirms, `reply_to_admin_`,
`view/show_own_feedback_`, conversations), `admin_subscription` + toggle/remove/enable/disable/
noop, `admin_bulk_*`, `admin_token_health`, `admin_csv_export`, `admin_recent_users`,
`admin_getdata_*` (dedicated `handle_admin_getdata_callback`, `main.py:129-131`),
`dd_*` + `admin_ud_yes/no`, old broadcast flow (`broadcast_ad_yes/no/target_free/target_all/
skip_orderer/recurring_yes/no/ask_delete/send_now`, `broadcast_reply:`), `admin_ratings_*`,
`admin_issue_*` (own dispatcher `issues.py:25-59` covers view/user/fixed/soon/custom +
`_target_` variants), export/import/`seq_/`/`skip_hint`/`msg_list_menu`/`backup_restore_*`/
`confirm_import_photos`/`premium_emoji_*`/`import_tz_*` (generic `export_`/`import_` branches in
`src/callbacks/export.py`), `tz_*/set_lang_/set_ch_tz_/tz_set_for_/show_channel/addbot_prompt/
connect_channel/change_channel_/disconnect_channel_confirm_` (cross-module homes),
`promo_add_start` (explicit conv entry `register.py:660`, bypasses `button_handler`).

---

## C. Data-source audit ("is every shown number correct?")

| # | Screen / number | Query (file:line) | Verdict |
|---|---|---|---|
| C1 | Revenue total + monthly breakdown | `collect_revenue_stats`, `src/admin/helpers.py:693-713`, shown `analytics.py:159-174` | **WRONG — always $0.00 / empty.** Reads `premium_purchase_cents` / `premium_purchased_at`, which **no writer ever sets** (payment success writes `premium_purchases[]` + `last_premium_bought_at`, `src/payments/__init__.py:1711-1729`, amount never persisted). Monthly dict therefore always empty → `admin_revenue_empty`. |
| C2 | Money-back accounting | `helpers.py:706-707` `total_revenue_cents -= 0` | **NO-OP.** Refunds never decrement revenue even if C1 is fixed. |
| C3 | "Paying users" (revenue screen), premium counts (panel/dashboard/stats/users list) | `has_premium`, `src/services/models.py:1221-1233` | **UNDERCOUNTS when expiry is naive.** Admin date-grant stores naive `datetime.strptime(...)` (`admin/handlers.py:1725-1726` → `premium.py:28` `.isoformat()` without tz). Reader compares naive vs `datetime.now(TIMEZONE)` (aware) → `TypeError` → `except` → `False`. Such users read as Free everywhere (counts, `premium` flags in `collect_users`, free-target ad audience). Aware expiries (Stars path, `premium.py:30,82`) are fine. Same naive/aware `TypeError` propagates **uncaught** out of `is_in_grace_period` (`premium.py:156-160`) → handler crash → global error path. |
| C4 | Stats → "DB size" | `panel.py:132-153` sums 7 legacy JSON paths (`config.py:168-174`) | **WRONG — always 0.00 KB.** Post-migration those files don't exist (`data/users/` holds only `referrals.json`; store is `bot.db` ~5 MB incl. WAL). System Health (`helpers.py:618-642`, shown `analytics.py:64-87`) reads the real `bot.db`/`stats.db` → **the two screens disagree** with each other. |
| C5 | Panel "Scheduled"/"Recurring" lines | `panel.py:79-80` renders `t('admin_scheduled')` / `t('admin_recurring')` with **no count args** | **Missing numbers.** Keys resolve to bare labels (`admin/en`: `"Scheduled"`, `"Recurring"`). Only the combined `total_messages` carries a number. |
| C6 | Feedback dashboard buckets | `collect_dashboard_summary`, `helpers.py:50-55` buckets open/replied/spam | **INCOMPLETE.** Writers also set `closed` (`callbacks/admin/feedback.py:254,465`, `web_server.py:449`) → closed items inflate `all` but sit in no bucket, so open+replied+spam ≠ all. |
| C7 | `messages.csv` admin export (Status / Next Run / Total Uses) | `callbacks/export.py:1233-1238` reads `job.get('status'/'run_at'/'next_run'/'uses')` | **COLUMNS ALWAYS EMPTY — schema mismatch.** Scheduled records use `datetime/channel_id/content` (`channels/helpers.py:468-489`); recurring use `channel/cron`. Compare `collect_all_messages_global` (`helpers.py:773-800`), which uses the right keys. |
| C8 | Per-user scheduled/recurring counts | `admin/handlers.py:1112-1114`, `helpers.py:231-232` (`==` without `str()`), vs `collect_user_details` `helpers.py:178-179` (with `str()`) | **INCONSISTENT conventions, currently benign.** Current writers store `user_id` as str (`channels/helpers.py:469`), so counts match today; any non-str legacy record silently drops out of the first two but not the third. |
| C9 | Users count, blocked count, scheduled/recurring totals, bot fleet, expiring premiums, audit/issue/security lists, backups | `helpers.py:41-99`, `analytics.py`, `collect_bot_fleet/token_manager`, `collect_expiring_premiums` (fromisoformat, H26-fixed) | **CORRECT as-queried** (simple `len()`/sums over live in-memory state; no double counting found). Caveats: `collect_*` snapshot under `BOT_DATA_LOCK` while renderers re-read without it (dashboard vs screen can skew by one write under concurrency — cosmetic); `top_senders` trusts `user_stats.sent_total` increments (scheduler path, not re-verified here). No global channels count exists on any screen (only per-user label + fleet list) — flagged, not a bug. |
| C10 | Translations ZIP export | `callbacks/export.py:1192-1204` `glob('translations/*.json')` | **INCOMPLETE.** Misses `translations/admin/*.json`, so the "translations backup" restores only user strings, not the admin strings that A2 shows are the fragile ones. (Overlap: downloads agent.) |
| C11 | Broadcast sent/failed counts | `_broadcast_send`, `admin/handlers.py:88-98,319-357` | **Mostly correct; known skews:** `blocked_users` are skipped silently (counted in neither sent nor failed); `video_note`/poll double-sends count once; RetryAfter-exhausted targets count failed once. Audience denominator shown pre-send comes from `len(all_users)`-style counts that *include* blocked users, so sent+failed < shown audience is expected, not a bug — but no screen explains the gap. |

## Likely-missed-by-others notes (explicit)
- C1+C2 (revenue always $0 + refund no-op) and C4 (stats DB size 0 KB vs syshealth) are pure
  cross-cutting data bugs no flow agent would hit.
- B1.1 (`promo_remove_` dead on the live promocodes menu) sits between promos UI and dispatch —
  easy for both sides to assume the other handles it.
- A2 (whole admin panel in English for RU admins) affects every screen; A1's two raw keys live in
  the shared import path, reachable from admin restores.
- C10 (translations ZIP drops `admin/` strings) couples exports to the translation gap.

## Repro / verification pointers (read-only, no edits made)
- Keys: run `audit_keys2.py` in the project dir; EN-missing == 2, RU-fallback-missing == 437.
- Dead buttons: run `audit_cb.py`; cross-check any `CB:`/`DYN:` value against branches in
  `src/callbacks/admin/main.py:111-362` and `_PREFIX_DISPATCH` in `src/buttons.py:33-321`.
- Revenue: `rg premium_purchase_cents src/` → only the reader in `helpers.py`; no writer.
- DB size: `ls data/users data/messages` vs `panel.py:136-141` file list; compare with syshealth.
- Naive expiry: `admin/handlers.py:1725` (`strptime`, naive) → `has_premium` `models.py:1229-1233`.
- messages.csv: `callbacks/export.py:1236-1238` key names vs `channels/helpers.py:468-489` record keys.
