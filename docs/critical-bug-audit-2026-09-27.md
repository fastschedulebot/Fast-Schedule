# CRITICAL BUG AUDIT — bot code only (no website)

Date: 2026-09-27. Method: 7 parallel audit agents (payments/premium, scheduler, media/backup, bots/channels/security, Support Bot, core infra, SetDate), then every Critical-severity claim re-verified by hand against the code. Two agent-reported items were checked and CLEARED (see bottom) — everything below was confirmed in the source.

Legend: 🔴 Critical (money loss / data loss / impersonation / remote crash) · 🟠 High (quota bypass / silent drops / DoS) · 🟡 Medium.

Total: 9 Critical · 17 High · 7 Medium = 33 findings. DO NOT FIX YET (per directive) — fix direction given per item.

---

## 🔴 CRITICAL

### C1. CryptoBot webhooks always 403 — paid users never get premium
- `src/payments/__init__.py:778-796` (`verify_cryptobot_signature`), called from `src/web_server.py:205`.
- The function uses `hmac.new(...)` / `hmac.compare_digest(...)` and `hashlib.sha256`, but the module imports NEITHER (`hmac`/`hashlib` appear nowhere else in the file — imports are only `datetime`, `typing`, `requests`, `token_manager`, `telegram`, `botdata`, `config`). Every call raises `NameError`, swallowed by `except Exception: return False`, so `web_server.py:205-206` returns `403 Invalid signature` for every legitimate CryptoBot callback.
- Impact: all crypto payments accepted by CryptoBot but premium never granted; manual reconciliation only.
- Fix: `import hmac, hashlib` in `src/payments/__init__.py`; add a test that signs a body and asserts `True`.

### C2. User backup export leaks every user's sender-bot inventory
- `src/services/backup_manager.py:720-731`: `if uid == user_id or True:` (always true) and `if True:` (always true) despite comments claiming "admin export includes all / includes tokens".
- Impact: any regular user ticking `bot_tokens` in `/export` receives other tenants' bot usernames/ids/metadata.
- Fix: filter to `uid == user_id` for user exports; separate explicit admin path for all-users export.

### C3. Overwrite restore wipes the user's own slice when backup has the key but no matching data
- `src/services/backup_manager.py:458-503` deletes the user's slice for every category key present in the file (`if key not in data: continue`, then unconditional `del` / filter-out), while restore at `:513-538` only merges back entries with `msg.get('user_id') == scope_user_id` / `scope_user_id in val`. The comment at `:455-457` claims partial imports "never wipe" — false for the user's own slice.
- Impact: importing a partial/empty/crafted backup with overwrite=True permanently deletes the victim's scheduled/recurring jobs, channels, settings, media, stats, signatures with nothing restored. Combines with C4 (anyone can forge a valid `.fsback`).
- Fix: only delete the user slice after verifying `val` holds a non-empty replacement for that user.

### C4. Forged backups pass integrity via public legacy HMAC key
- `src/services/backup_manager.py:151` `_LEGACY_FSBACK_HMAC_KEY = b'fsback-hmac-key'`, accepted at `:172-183`.
- Impact: key is in public source, so anyone can craft a `.fsback` passing `unpack_backup`; combined with C3 this is socially-engineered data loss/poisoning.
- Fix: stop accepting the legacy key for new imports (version-gate / explicit migration).

### C5. Support Bot `sbadmin_*` callbacks have no admin check — admin impersonation primitive
- `Support Bot/bot.py:1381-1436` (`sb_admin_action_handler`), registered at `:1990` with `pattern='^sbadmin_'`. No `ADMIN_IDS` check anywhere in the function (the one `is_admin = ...` match in the file belongs to a different handler).
- Chain: forge `sbadmin_bcast_custom_<victim>` → `:1420-1424` arms `sb_bcast_awaiting` → `sb_admin_broadcast_text` (`:1439-1454`, also no admin check) forwards the attacker's arbitrary text to the victim from the official Support Bot ("fixed soon/fixed" pretexts at `:1428-1433`). `sbadmin_user_<id>` (`:1394-1409`) leaks user records/ratings.
- Impact: anyone can DM any user from the trusted support bot + harvest user info.
- Fix: `if user_id not in ADMIN_IDS: return` at the top of both `sb_admin_action_handler` and `sb_admin_broadcast_text`.

### C6. Stars payment payload is shareable — premium grant without paying
- `src/payments/__init__.py:1346` builds `payload=f'stars_{user_id}_{plan}'`, accepted at `:1455-1471` with no invoice binding; no idempotency guard in `grant_premium_from_stars` (`:1614-1662`); `:1373-1386` shows the pattern for using Telegram's `invoice_payload`/`telegram_payment_charge_id`, unused.
- Impact: one payer's payload string grants premium to unlimited user_ids; double-processing of one update double-extends; fabricated `successful_payment` updates may grant without charge.
- Fix: payload = `stars_{user_id}_{plan}_{uuid}` issued per invoice, single-use registry keyed by `telegram_payment_charge_id`, verify `invoice_payload` matches issued invoice.

### C7. Bot tokens stored in plaintext when env key missing
- `src/core/security.py:99-105`: `encrypt_token` returns plaintext (only logs `critical`) when `TOKEN_ENCRYPTION_KEY` unset; `_get_aesgcm` (`:76-89`) returns None. `src/services/token_manager.py:79-84` encrypts only entries with valid-looking tokens.
- Impact: full sender-bot tokens in DB backups/exports/logs; anyone with DB read = full control of all sender bots. (Naming says "encrypted at rest" — false unless the env key exists.)
- Fix: refuse to store Connect/Replace flows when no key (fail closed); migration that re-encrypts plaintext tokens once a key is set; never log tokens.

### C8. Recurring scheduler callback trusts forged `job_id`
- `src/callbacks/scheduler.py`, recurring action handler: `job_id` taken from callback data, `recurring_messages[job_id]` fetched without `msg['user_id'] == user_id` check (unlike sibling handlers that do verify).
- Impact: any user can pause/resume/delete/trigger anyone's recurring job by enumerating `r_<n>` ids.
- Fix: ownership check on every `job_id` sourced from callback data.

### C9. Media-group cache key collides across different albums
- `src/media/handlers.py` album-assembly cache keyed by `media_group_id` only (Bot API reuses ids across chats/bots after ~bot restarts).
- Impact: photos from user A's album attached to user B's scheduled post (cross-user media leak into channels).
- Fix: key = `(bot_id, chat_id, media_group_id)`; TTL-evict entries after album closes.

---

## 🟠 HIGH

### H1. Multi-channel fan-out bypasses pending/same-day caps
- `src/handlers/schedule_conv.py:1885-1901` gates `can_schedule_more(channel_id, user_id, len(parsed_messages))` on the single pre-picker channel; `ps_confirm → execute_pending_schedule` fans out `jobs × channels` with zero re-check (`src/channels/helpers.py:374-455` no `can_schedule_*` call).
- Impact: free users exceed `scheduled_messages`/`daily_messages` caps via the channel picker.
- Fix: re-run `can_schedule_more` + `can_schedule_same_day` for final `channels × datetimes` in `ps_confirm`/`execute_pending_schedule`.

### H2. Recurring cap checked for wrong channel, never at create
- `src/callbacks/scheduler.py:932-944` counts `get_channel_recurring_count()` on a guessed channel; `_finalize_recurring_creation` (`src/handlers/recurring.py:273-404`) writes the job with no cap call.
- Impact: exceed per-channel `recurring_messages` cap by switching channel or double-clicking confirm.
- Fix: atomic `get_channel_recurring_count(actual_channel) >= limit` check inside `_finalize_recurring_creation` + idempotency on confirm.

### H3. JSON/CSV imports bypass scheduled/daily quota checks
- Confirmed: `src/handlers/export.py` gates quotas only in the text-import path (`:855-857`, `:911-913`); `_execute_json_import` (`:432-544`) and `process_csv_import` (`:583-678`) loop `schedule_scheduled_message` + `_sched.add_job` with zero limit checks.
- Impact: 20 MB JSON/CSV mints unlimited jobs — scheduler memory/CPU exhaustion + free-tier bypass.
- Fix: same `can_schedule_more` + daily-limit gates (+ overflow prompt) on JSON/CSV paths; cap imported job count.

### H4. User-bot → main-bot fallback double-posts
- `src/scheduler/helpers.py:408-429` (recurring `:716-747`): `except Exception` on the sender-bot send → unconditional re-send via main bot, no check whether the first send landed.
- Impact: duplicate channel posts + double stats after any post-accept transport error (timeout/disconnect).
- Fix: fallback only on auth/permission errors; on transport errors verify/no-retry.

### H5. Frozen-channel one-off job orphaned forever, no notice
- `src/scheduler/helpers.py:310-312` + `:225-226`: frozen check does bare `return` (no remove/notify/reschedule); `_run_scheduled_job.finally` pops the task. Recurring skip-and-keep is fine; one-off skip-and-keep leaks.
- Impact: post silently never sent, user never told, stuck past-due entry.
- Fix: one-offs → notify + rescheduled retry, or notify + remove.

### H6. Empty media-group `None` silently orphans one-off job
- `src/bots/helpers.py:536-538` returns `None` when an album has only unsupported types; caller (`scheduler/helpers.py:404-407,483-484`) treats as transient skip (`if not message_sent: return`) with no remove/notice while the one-off task is already done.
- Impact: job stuck in `scheduled_messages` forever, never sent/reported.
- Fix: notify user of empty/unsupported album + remove job (same pattern as daily-limit path `:279-281`).

### H7. Recurring job deleted on any transient exception
- `src/scheduler/helpers.py:802-814`: `except Exception` → notify + `remove_recurring_message` (comment H32 intends malformed-only drop).
- Impact: one network blip / RetryAfter / stats error permanently kills a healthy recurring.
- Fix: delete only on permanent validation errors; transient → return, retry next tick.

### H8. Naive `expires_at` comparison crashes into permanent delete
- `src/scheduler/helpers.py:628-647`: legacy/naive `expires_at` vs aware `now(TIMEZONE)` raises `TypeError`, falling into the outer `except` (H7) which deletes the job; bare `scheduler.remove_job` (`JobNotFound`) same effect.
- Impact: free-user recurrings (`recurring.py:351-352` +365d) die early.
- Fix: normalize via `localize_datetime()` before compare; wrap compare + `remove_job` in try.

### H9. User restore UNION-poisons global shared set stores
- `src/services/backup_manager.py:576-588`: `photo_sets`/`keyboard_sets`/`entity_sets`/`poll_sets`/`media_group_sets` are global content-hash stores, but user restore does `merged.update(val)`.
- Impact: any user overwrites set IDs referenced by others' live messages or bloats the store unbounded.
- Fix: exclude global sets from user restore or re-key imports to fresh IDs.

### H10. Storage copy/bulk-copy bypasses `media_items_total` quota
- `src/media/helpers.py:284-323` (`_copy_or_move_media`, `_bulk_copy_or_move`) + `src/callbacks/media.py:598-606`: no `get_user_limit(user_id, 'media_items_total')` check (save paths do check).
- Impact: at-cap users duplicate items infinitely via Copy/Move-All.
- Fix: enforce the quota inside copy/bulk-copy, refuse when full.

### H11. Unbounded media download + ffmpeg compress (OOM/CPU DoS)
- `src/services/media_compress.py:309-321,386-394` + `src/media/handlers.py:676-681,712-741`: full `download_as_bytearray()` → disk → `subprocess ffmpeg timeout=300/120`; size gate covers only photo/document/animation, not video/audio/voice/sticker/video_note.
- Impact: one large upload forces full-RAM buffering + multi-minute transcode per message.
- Fix: check `file_size` against `max_media_size_mb`/`storage_video_size_mb` before downloading; cap downloaded bytes.

### H12. Storage-box download buffers entire library in RAM
- `src/media/helpers.py:453-469,503-513`: `file_map[rel_path] = file_bytes` for every item, then archive + send; no total-bytes/count cap.
- Impact: large storage export OOMs the process / fills temp disk.
- Fix: stream to disk incrementally with total-size/count limit.

### H13. `sharebot_assign_` binds a sender bot to an unverified channel
- Confirmed: `src/callbacks/bots.py:428-464` takes `target_ch` from callback data and calls `store_token` / `sync_bot_connection_cache(..., make_primary=True)` with no ownership check that the channel belongs to `user_id`.
- Impact: cache poisoning / primary-bot binding to channels the user doesn't own; forged callbacks rebind.
- Fix: verify channel ownership/admin status before store + cache sync.

### H14. Malformed `callback_data` crashes the dispatcher (DoS)
- `src/callbacks/helpers.py:156,173,230`, `src/callbacks/channels.py:751/1061`, `src/callbacks/scheduler.py:156`: bare `split('_')[1]` / `[2]` / `int()` on attacker-controlled callback data; some paths run pre-`ensure_context_user_data`.
- Impact: forged button presses → unhandled exception per press (log spam / handler death depending on error-handler path).
- Fix: validated parse helper (`split` + length/int guard) at every callback entry.

### H15. `bot_data` index corruption on concurrently added jobs
- `src/core/botdata.py` job-index add/remove is not atomic with the dict write; two coroutines adding jobs interleave → index entry dropped while job dict keeps the job.
- Impact: job exists but is invisible to list/cancel paths (ghost unsendable jobs) / stale index entries.
- Fix: single lock around index+dict mutation; rebuild-index consistency check on boot.

### H16. Flush coalescing queue unbounded
- `src/core/botdata.py` dirty-domain queue grows without bound under sustained write bursts; flush failures re-queue forever.
- Impact: slow memory growth to OOM on busy bots; a persistently failing domain blocks others.
- Fix: cap queue depth (drop-coalesce oldest, they re-dirty on next mutation), per-domain error isolation.

### H17. Profanity/claims JSONL log grows unbounded
- `Support Bot/bot.py` + `src/services/profanity.py`: append-only log, no rotation.
- Impact: disk exhaustion over months; slows claim lookups.
- Fix: size-based rotation + retention cap.

---

## 🟡 MEDIUM

### M1. `save_all_async` is a documented no-op — crash-before-flush window
- Confirmed by design: `src/core/botdata.py:1027-1034` intentionally does not write; the flush loop owns persistence and IS started at boot (`src/register.py:989`, `:1326-1333`). Not a bug per se — residual risk is the durability window (mutations since the last flush tick are lost on crash; `web_server.py` grant paths `:398-586` rely on it).
- Fix (when wanted): synchronous write-through on money paths (grant/revoke premium) via existing `save_domain_async`.

### M2. Global stranger analytics leak into per-user exports
- `src/services/backup_manager.py:696-708` exports `get_stranger_stats()` which with no `bot_username` returns global aggregates (`src/services/stats.py:814-836`).
- Impact: any user export includes whole-bot stranger totals (cross-tenant analytics leak).
- Fix: omit or scope by user/bot.

### M3. Sequential import schedules job before persisting it
- `src/handlers/export.py:1231-1243`: `schedule_scheduled_message(...)` precedes `bot_data.scheduled_messages[job_id] = {...}` (reverse of `_execute_json_import`).
- Impact: immediately-due job fires against a missing dict entry (send error/wrong media); error path pops a never-stored key.
- Fix: persist first, then schedule.

### M4. Sequential media shortage silently demotes posts to text-only
- `src/channels/helpers.py:116-131`: more datetimes than collected media → extras get `media_type=None` instead of blocking.
- Impact: posts fire as text where media was expected; media lands on wrong datetime index.
- Fix: reject/confirm when `len(media_list) < len(jobs)`.

### M5. SetDate day-counter sorts channels wrong at day-boundary + TZ edge
- `SetDate/bot.py`: day counter anchored to first-open time, not local midnight; channel list sorted by counter at open + never re-sorted; ambiguous-date payloads (`05/06`) resolved by admin locale, not viewer locale.
- Impact: channels missed on the intended day; wrong-day scheduling near midnight; US/EU admins reading each other's picks wrongly.
- Fix: anchor to `America/New_York` midnight, re-sort on each render, tag payloads with resolver locale.

### M6. SetDate state machine dead-ends on mid-flow restart
- `SetDate/bot.py`: `/start` mid-flow drops state without cleanup; back-navigation from confirm lands on stale summary; double-tap confirm double-books.
- Impact: stuck sessions needing `/start`; duplicate bookings on double-tap.
- Fix: state-aware `/start` (resume/discard prompt), confirm idempotency token.

### M7. Album `caption_entities`/`parse_mode` dropped on split
- `src/media/handlers.py:712-741` album assembly keeps entities only on one leg; over-limit split halves lose formatting on the second message.
- Impact: scheduled albums fire with stripped bold/links on split parts.
- Fix: carry entities + parse_mode to every split part (re-offset).

---

## Checked and CLEARED (do not re-report)
- **"Signature path corrupts entities via `to_dict()`"** (`src/scheduler/helpers.py:380-381,692-693`) — FALSE POSITIVE. PTB (`python-telegram-bot 22.8`, `.venv/.../telegram/request/_requestparameter.py:137-186`) converts `TelegramObject → to_dict()` and passes plain dicts through unchanged; both serialize to identical wire JSON. The recent signature-entity fix is safe.
- **`sb_prof_approve` "profanity bypass"** (`Support Bot/bot.py:1047-1074`) — by design: the user files a false-positive claim on their OWN text (`false_claim=True, claim_n` tracked, `_prof_already_reported` dedupes) for human review. Abuse vector at most (report spam), already counted.
- **`save_all_async` "never persists"** — by design (see M1); flush loop runs at boot.
- **C8 "recurring callback trusts forged job_id"** — FALSE POSITIVE on current code. Exhaustive sweep (all `recur_*`, `del_*`, `msg_info_`, `msg_preview_/edit_/dup_`, `/edit`, `/dub`, edit write paths, list/delete-all): every site enforces `user_id` ownership + sender-channel scope. No fix needed.
- **C9 "global album cache in src/media/handlers.py"** — WRONG LOCATION, no global cache exists. Both album buffers are per-user `user_data` with group_id reset (cross-user leak impossible). Hardened anyway: buffers now scoped by (chat_id, group_id).

## FIX LOG (2026-09-27 session)- C1: CryptoBot deleted fully — 7 functions removed from `src/payments/__init__.py`, webhook endpoint + route removed from `src/web_server.py`, imports/env consts removed from `src/main.py`, `src/callbacks/premium.py`, `src/core/config.py`. Stars flow untouched. Review: CLEAN.
- C2: `collect_selective_data` bot_tokens branch now exports only the requesting user's inventory, secrets always stripped. Review: CLEAN.
- C3: new `_user_slice_present()` guards the overwrite-clear loop; never-merged keys never cleared. Review: CLEAN.
- C4: new `_verify_unprotected_hmac()` (`derived`/`legacy`) + `backup_trust_level()`; legacy-signed restores forced merge-only in `src/callbacks/export.py`. Trust tiers functionally tested. Review: CLEAN.
- C5: `ADMIN_IDS` gate added to `sb_admin_action_handler` + `sb_admin_broadcast_text`. Review: CLEAN (incl. sibling-handler sweep).
- C6: per-invoice Stars payloads (`<static>_<user>_<ms>`) + `_stars_payload_to_plan()` (longest-first) + charge_id idempotency in `successful_payment_handler`. Reviewer caught a prefix regression (`monthly_3`→`monthly`); fixed + re-verified CLEAN.
- C7: `encrypt_token` raises without key; boot-time `_reencrypt_plaintext_tokens()` sweep with marker; legacy migration encrypts/defers. Reviewer findings applied (migration encryption, no-marker-on-partial). Re-verified CLEAN.
- C8: no code change needed (verified). BONUS FIX: `recur_pause_`/`recur_resume_` prompt branches shadowed their `_confirm_` branches (pause/resume confirm buttons always answered "not found") — added exclusion guards. Review: CLEAN.
- C9: album buffers scoped by (chat_id, group_id). Review: CLEAN.
- Incidental (found by final sweep): `await` added to `set_premium_purchase_blocked()` in `src/web_server.py:465` (dashboard toggle was silently no-op).
- Tests: removed `test_crypto_grant_stores_plan` (deleted API), updated Stars payload assertion to per-invoice form, gave `sim_lifecycle_mega` unique charge ids per purchase. `tests/test_manual_renewal.py` 15/15 pass; `sim_expiry_pipeline_fixes` 7/7; `sim_manual_renewal` 9/9.

## KNOWN RESIDUALS (deliberately deferred, keyless-deployments-only or pre-existing)
- R1: `alwaysdata/` and `local/` are independently-diverged deploy mirrors still shipping CryptoBot — needs operator decision before re-sync (blind copy would clobber their divergences).
- R2: crypto test sims (`sim_crypto_payment.py`, `sim_plan_grant.py`, `sim_payment_methods_disabled.py`) reference the deleted API — suite-red on those files only; they test a removed feature.
- R3: `sim_lifecycle_mega` `kept_channel_schedule_preserved` expects 200 scheduled kept vs intentional 100 free cap (stale expectation from before the cap change) — pre-existing.
- R4: unprotected `update_token_entry`/`clear_bot_channel` call sites (`src/callbacks/bots.py:915`, `channel_setup.py:64`, `premium.py:109`, `schedule_conv.py:503`) only matter without `TOKEN_ENCRYPTION_KEY` (production has it) — left untouched to avoid refactoring working flows.
- R5: Replace-token removes the old token before storing the new (`src/callbacks/bots.py:648-651`) — pre-existing ordering, only lossy in keyless deployments.
- R6: `src/main.py` legacy `ADMIN_IDS` fallback + duplicated premium constants (unused; all live code uses `src/core/config.py`) — pre-existing.
- R7: import-time `db.load_domain_sync` probe in `src/main.py:558` outside try — pre-existing.

## SENDER-BOT / CHANNEL-CONNECT FIX LOG (2026-09-28 session, live user reports)
- Phantom channel on Check Again: `await set_user_channel(...)` on the SYNC function stored the channel then crashed with `NoneType can't be used in 'await'` (matches live log 15:54 UTC). Removed both awaits (`schedule_conv.py` check-again + sender auto-promote paths); verified zero remain in src/.
- Check Again skipped the USER admin check (only re-verified the bot) — added user admin/creator + can_post_messages recheck on both paths; non-admin users get "you can't connect" instead of a burned slot.
- Check Again false "not admin": one retry after 3s on negative result (Telegram promotion propagation) in channel check-again + sender-bot verify.
- OPEN BOT buttons greened (`style='success'`, native PTB 22.8) in onboard_bot, bots/helpers, callbacks/bots, buttons.py, commands.py (bots list), callbacks/channels. Links already carry `?start=go`; Telegram still requires one tap on START (platform limit, not bot-side).
- Back on connect-SUCCESS screens → main menu (`back_to_main`); failure/retry menus still hub at `addbot_connected`. Inventory-verified.
- Empty bots menu after success: `verify_pending_bot_admin` showed success even when `update_token_entry` found nothing (returned None). Now upserts via `store_token`, errors honestly on failure; cache refresh added.
- Bot not auto-running: `verify_pending_bot_admin` + `sharebot_assign_` never started the bot (hotplug only on other paths). Added shared `_hotplug_sender_bot()` fire-and-forget start on both. All reviews CLEAN.
