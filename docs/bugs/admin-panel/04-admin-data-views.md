# Admin Data Displays — Investigation Report (Agent 4/6)

Scope: admin-panel data views only. READ-ONLY investigation; no `src/` edits made.
Date: 2026-10-02.

Complaints: (a) users list misses most usernames/names; (b) stats show incorrect data;
(c) "view mode" button should be deleted; (d) sender-bots screen says none connected /
doesn't list all; (e) token health shows wrong data.

Verdict summary: (a) TRUE · (b) TRUE (multiple causes) · (c) confirmed locatable for
removal · (d) TRUE (root cause found) · (e) TRUE (root cause found).

---

## 1. Users list — why most names/usernames are missing — TRUE

### Resolution chain (file:line)

- List renderer: `src/admin/helpers.py:102-152` (`collect_users`) → profile via
  `_get_user_profile` at `src/admin/helpers.py:22-30`:
  reads ONLY `bot_data.all_users[uid]` merged with `bot_data.user_info_cache[uid]`.
  **It never calls Telegram** — no `get_chat` fallback in the list path.
- Live lookup exists but is single-user only: `cache_user_info` at
  `src/services/models.py:23-47` (`await bot.get_chat(user_id)`, 1h TTL). Used by
  `build_admin_user_info_text_and_keyboard` (`src/admin/helpers.py:227`),
  `admin_view_user_handler` (`src/admin/handlers.py:1108`),
  `_render_admin_user_info` paths — never by `collect_users`.
- Writer side: `BotData.register_user` at `src/core/botdata.py:1159-1214` stores
  `first_seen`/`last_seen`(`last_active`) and merges `user_data` **only if the
  caller passes it**. The hottest call site passes nothing:
  `src/buttons.py:514` → `bot_data.register_user(user_id)` (every button press).
  So the majority of users get an `all_users` record shaped like
  `{'first_seen': …, 'last_seen': …}` with **no** `first_name`/`last_name`/`username`
  keys (verified: only `register_user` writes `all_users`, lines 1207-1213; the
  only writers that pass names are `cache_user_info` at `src/services/models.py:34-38`,
  `terms_gate.py:53`, and the one-off backfill in `src/callbacks/channel_admins.py:286`).
- Cache poisoning on failure: `src/services/models.py:39-45` — when `get_chat`
  throws (normal for users who never started the bot, privacy-restricted, or
  during flood limits), it caches `{'first_name': 'Unknown', 'last_name': '',
  'username': ''}` for a full hour, so even a later successful path is blocked
  by the TTL check at line 24-25.
- `_resolve_user_input` (`src/admin/helpers.py:324-336`) has the same blind spot:
  username/name search only scans `all_users`, so users missing names there are
  unfindable by name (ID still works).

Why "most" and not "all": users who recently opened a single-user view (or hit
the one backfill path) have warm `user_info_cache` entries and do display.

Related truncation bugs (same screen family):
- `handle_admin_all_users` (`src/callbacks/admin/users.py:225-256`): `page`
  variable is actually an **offset** (`collect_users(limit=15, offset=page)`,
  nav steps ±15) — works but misnamed; no total-pages indicator.
- Advanced search (`src/callbacks/admin/users.py:50-118`): premium/free filters
  call `collect_users(limit=50)` then filter **within the first 50 rows**, so
  reported counts are counts-of-first-50, not global. Lang breakdown uses
  `limit=500` — same truncation at scale. Recent-users (`:123-139`) caps at 15.
- `_format_full_name` (`src/admin/helpers.py:33-34`) yields `''` for missing
  names; list falls back to raw ID (`users.py:231,239`), matching the complaint.

### Evidence
`botdata.py:1207-1213` (all_users shape) × `buttons.py:514` (nameless writer) ×
`helpers.py:22-30` (list reads only those two stores) × `models.py:23-47`
(live lookup exists but is not used by the list).

---

## 2. Stats — what each number counts and why it's wrong — TRUE (several independent bugs)

### 2a. Admin stats screen (`src/callbacks/admin/panel.py:125-156`, `handle_admin_stats`)

| Line | Displayed as | Counts | Why wrong |
|---|---|---|---|
| 132 | total users | `len(bot_data.all_users)` | Includes nameless/presence-only rows (see §1); counts every key ever registered, never pruned. |
| 133 | premium users | `sum(has_premium)` | `has_premium` (`src/services/models.py:1221-233`) does `datetime.fromisoformat(expires) > datetime.now(TIMEZONE)`. Expiries granted via `admin_premiums_date_handler` (`src/admin/handlers.py:1724-1726`: `datetime.strptime(text,'%Y-%m-%d')` → **naive**) then stored verbatim (`src/services/premium.py:15-28`, `.isoformat()` keeps it naive). Naive-vs-aware comparison raises `TypeError` → `except → return False`. Every custom-date grant is therefore counted as Free. Lifetime grants (`premium_expires=None`) are unaffected. Same flaw in `get_user_limit` (`models.py:168-184`). |
| 134 | active jobs | `len(job_queue.jobs())` | Counts PTB `JobQueue` jobs, not the APScheduler jobs that actually send schedules (`src/core/config.py: scheduler`). Typically 0 or unrelated (periodic maintenance), so the number disagrees with dashboard/queue lengths. |
| 136-141 | DB size | sums `SCHEDULED_FILE…ALL_USERS_FILE` on disk | Persistence moved to `filesystem_db`/`bot.db`; legacy JSON files may be absent/stale → reports ~0 KB or a stale sum. Compare `collect_system_health` (`src/admin/helpers.py:618-642`) which correctly measures `DATA_DIR/'bot.db'` + `stats.db`. |
| 143 | total sent | `sum(sent_total)` over `user_stats` | Source (`update_user_stats`, `models.py:234-259`) only increments on `'sent'`/`'created'` actions from scheduler/send paths; imports, restores, admin grants, and failed sends never increment. Undercounts by construction. |
| 149-150 | scheduled / recurring | `len(bot_data.scheduled_messages)` / `len(recurring)` | Raw dict sizes: include past-due, orphaned (channel deleted), and frozen-premium leftovers; no "active vs overdue" split. |

### 2b. Dashboard screen (`src/callbacks/admin/analytics.py:41-59` ← `collect_dashboard_summary`, `src/admin/helpers.py:41-99`)

- Same `total/premium/blocked/scheduled/recurring` caveats as above.
- `sent_today` (`helpers.py:142,176`): `update_user_stats` (`models.py:244-246`) resets `sent_today` **lazily, only when that user triggers another action**. No daily rollover job exists, so a user with yesterday's sends still shows yesterday's `sent_today` all day today. Stale-cache bug → TRUE.
- `top_sent`/`top_created` (`helpers.py:61-86`): sorted from the same undercounted `user_stats`; ties unordered; dashboard prints top 5, helper computes top 10 — cosmetic only.
- `premium_purchase_blocked` comes from payments module — outside this agent's scope, not verified.

### 2c. Revenue screen (adjacent; flagged, not in complaint scope)
`collect_revenue_stats` (`helpers.py:693-713`): sums `premium_purchase_cents` but
`money_back_refunded_at` branch does `total_revenue_cents -= 0` (line 707) — refunds
never subtract. Monthly bucketing keys on `premium_purchased_at[:7]` with no
validation. Severity: medium (money numbers).

---

## 3. "View mode" button — what it does and where it is (for removal)

- Definition: `src/keyboards.py:430` — `[btn(t(user_id,'admin_view_mode'), callback_data='admin_view_mode')]` inside `keyboard_page2` of `get_admin_keyboard` (admin panel page 2).
- Handler: `handle_admin_view_mode` at `src/callbacks/admin/panel.py:192-218`. Toggles `bot_data.admin_mode[user_id]`; when enabling, renders the **regular user main keyboard** (`get_main_keyboard`) plus an appended exit row (`panel.py:212`: `keyboard.inline_keyboard.append([btn(...'admin_view_mode_exit'...)])`); when disabling, re-renders the admin keyboard.
- Routing: `src/callbacks/admin/main.py:58,300-301` (`handle_admin_view_mode` import + `elif qdata == 'admin_view_mode'` branch).
- Strings to remove: `admin_view_mode`, `admin_view_mode_exit`, `admin_view_mode_activated` in `translations/admin/en.json` (and `ru` counterpart if present).
- State residue: `bot_data.admin_mode` dict — after removal, existing `True` entries are harmless (nothing reads them except this handler) but a one-off clear is tidy.
- No other callers found (grep `admin_view_mode` hits only the four sites above). Safe to delete: keyboard row + handler + import/branch + strings.

---

## 4. Sender-bots screen ("none connected") — TRUE, root cause: shape mismatch

- Screen: `handle_admin_bot_fleet` (`src/callbacks/admin/analytics.py:137-154`) ← `collect_bot_fleet` (`src/admin/helpers.py:661-690`).
- Authoritative store: `token_manager.list_tokens()` (`src/services/token_manager.py:457-464`) returns **`Dict[user_id, List[entry]]`**. Other callers handle it correctly (e.g. `detect_bot_identity`, `models.py:1042-1043`, iterates `.items()`).
- Bug (`helpers.py:667-677`, duplicated in `src/callbacks/admin/token.py:39-49`):
  ```python
  tokens = await list_tokens()          # dict {uid: [entries]}
  if isinstance(tokens, dict):
      tokens = tokens.get('tokens', []) # key 'tokens' never exists → []
  ```
  The `.get('tokens', [])` collapses the whole fleet to an **empty list**, so the
  screen renders `admin_botfleet_empty` ("none connected") regardless of how many
  bots exist. The second `isinstance(tokens, dict)` branch below it is dead code.
  This single bug fully explains complaint (d). Additionally the screen caps at
  `bots[:20]` with no pagination (`analytics.py:145`), explaining "doesn't list all".
- Secondary field-mapping bugs in the same function (wrong-but-nonempty data once the shape bug is fixed):
  - `helpers.py:683`: reads `token_data.get('channel', 'N/A')` but entries store **`channel_id`** (`token_manager.py:246-250`) → channel always "N/A".
  - `helpers.py:684`: reads `token_data.get('subscription', 'free')` but `store_token` no longer writes `subscription` (removed per M15 comment, `token_manager.py:251-253`) → always "free". Correct source is `get_subscription()` / `has_premium` (`token_manager.py:445-454`).
  - Validity flag inconsistency: fleet collector defaults missing → `True` (`helpers.py:686`), but the renderer (`analytics.py:149`) uses bare `bot.get('is_valid')` (no default) → `None` is falsy → shows **REVOKED for every bot**. And no writer ever sets `is_valid` (see §5), so both are fabrications.
- Per-user vs global is NOT the bug: `list_tokens` is correctly global here; per-user `get_tokens(user_id)` is used appropriately elsewhere (e.g. `_check_sender_bots_health`).

---

## 5. Token health — TRUE, checks nothing live

- Handler: `handle_admin_token_health` (`src/callbacks/admin/token.py:35-63`), keyboard entry `src/keyboards.py:460`, route `src/callbacks/admin/main.py:96,264-265`.
- What it actually does: same broken `.get('tokens', [])` unpack as §4 (lines 39-49) → usually `tokens == []` → reports Total 0 / Valid 0 / Invalid 0. If the shape bug were fixed, it would report Total N / Valid N / Invalid 0 always, because:
  - it counts the **`is_valid` dict field** (`token.py:51-52,59`), which **no code path ever writes** (grep `is_valid` across `src/`: only readers in `token.py`, `analytics.py`, `helpers.py`; writers: none — `store_token`/`update_token_entry`/`set_management_status` never set it).
  - it performs **zero network validation** — the live checker `_check_bot_token_valid` (`src/bots/helpers.py:588-595`, `Bot(token).get_me()`) and the per-user sweeper `check_token_validity` (`token_manager.py:524-545`, which correctly skips `token_error` entries per C10) both exist but are never called from this screen.
- Correct behavior would be: iterate flattened `list_tokens().values()`, skip `token_error` entries, `await _check_bot_token_valid(decrypted token)` per bot (with concurrency cap + caching — live `get_me` per bot on every admin click is expensive and rate-limit-sensitive), and label decrypt-failures as "unknown/key issue", never "revoked" (cf. C10 comments at `token_manager.py:71-88, 531-534`).

---

## 6. Other bugs found (severity + impact)

1. **[High] Fleet/health dict-shape collapse** (`helpers.py:667-669`, `token.py:39-41`): admin sees zero bots / zero tokens. Impact: operators believe fleet is empty; revocations invisible. Fix: flatten `{uid: [entries]}` with `user_id` backfill instead of `.get('tokens')`.
2. **[High] Naive-vs-aware premium expiry** (`handlers.py:1724-1726` × `models.py:1221-233`, `168-184`): custom-date premium grants instantly read as Free. Impact: paying users lose premium features; stats undercount. Fix: localize (`expires.replace(tzinfo=TIMEZONE)` or parse with tz) at write time + harden `has_premium` to assume `TIMEZONE` for naive values (as `collect_expiring_premiums` already does at `helpers.py:756-758`).
3. **[Medium] Revenue ignores refunds** (`helpers.py:706-707`, `-= 0`): refunded revenue still counted. Impact: overstated earnings.
4. **[Medium] `sent_today` never rolls over** (`models.py:234-259`, no cron reset): stale daily counters in users list/detail. Impact: misleading activity stats.
5. **[Medium] Fleet validity rendering inverted** (`analytics.py:149` bare `.get('is_valid')` vs `helpers.py:686` default-True): after any shape fix, all bots would show REVOKED. Impact: false revocation panic. Fix together with #1/#5.
6. **[Medium] Fleet field mapping** (`helpers.py:683-684`): channel always "N/A", subscription always "free". Impact: useless columns. Fix: `channel_id`, `get_subscription/has_premium`.
7. **[Low] Search counts truncated** (`users.py:50-118` limits 50/500): filter counts are sample counts. Impact: misleading "N users" lines. Fix: query full dataset or label as sample.
8. **[Low] DB-size metric reads legacy paths** (`panel.py:136-141`): reports ~0 KB post-migration. Impact: confusion only; `collect_system_health` already does it right.
9. **[Low] `active_jobs` measures wrong scheduler** (`panel.py:134`): PTB JobQueue vs APScheduler. Impact: number disagrees with reality.
10. **[Low] Cache-clear wipes `user_info_cache`** (`panel.py:279`) with no warm-up: immediately after "clear cache", all single-user views pay `get_chat` latency and failures cache as "Unknown" for an hour (§1). Impact: transient Unknown spike after admin maintenance.

## Files of record (all `file:line` verified by read)

- `src/admin/helpers.py:22-30, 41-99, 102-184, 226-227, 661-690, 693-713, 744-770`
- `src/services/models.py:23-47, 168-184, 234-259, 1221-233`
- `src/core/botdata.py:1159-1214`
- `src/buttons.py:514`
- `src/callbacks/admin/panel.py:125-156, 192-218, 279`
- `src/callbacks/admin/analytics.py:41-59, 137-154`
- `src/callbacks/admin/users.py:50-139, 225-256`
- `src/callbacks/admin/token.py:35-63`
- `src/callbacks/admin/main.py:58, 96, 264-265, 300-301`
- `src/keyboards.py:430, 460`
- `src/services/token_manager.py:246-253, 445-464, 524-545`
- `src/bots/helpers.py:588-595, 631-650`
- `src/admin/handlers.py:1108, 1724-1726`
- `src/services/premium.py:15-28`
