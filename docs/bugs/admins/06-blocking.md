# 06 — Channel-admin BLOCKING audit (Agent 6/8)

READ-ONLY audit. No `src/` edits made. Sims run read-only (see §8).

**Verdict: NOT CLEAN — block is a soft RBAC flag with real enforcement gaps.
The worst gap is a block-bypass: the `_recheck_or_deny` self-heal can re-add a
revoked admin with default permissions on their next action (§B1).**
Blocked users' already-scheduled jobs still fire (§B3), connect-after-block
is not refused (§B5), and the "allow requests" toggle edits the wrong record (§B6).

Counts: **12 issues (1 critical, 4 high, 5 medium, 2 low)** + 1 info note.
What works is listed in §7 (real-time denial, sync-resistance, H13/H15/M26 guards — all verified).

Scope covered: block flow → in-flight sessions → scheduled jobs → sender-bot
bindings → blocked-user CONNECT → exact messages → unblock-request gate →
approve/deny → state cleanup → unblock-restore semantics → revoke-while-acting →
cache invalidation.

---

## 1. Architecture under audit (ground truth)

- RBAC store: `bot_data.channel_admins` `{channel: {user: {is_owner, permissions, joined_at, can_post_messages, notify_requests}}}` —
  `src/channels/admins.py:5-8,168-234`.
- Block store: `bot_data.channel_revoked` `{channel: {user: {reason, revoked_at, [revoked_by]}}}` —
  `src/channels/admins.py:272-302`, persisted via `CHANNEL_REVOKED_FILE` (`src/core/config.py:196`, `src/core/botdata.py:65,620-622`).
- Block primitive: `revoke_channel_admin()` = `remove_channel_admin()` + write revoked entry + `save_all()` —
  `src/channels/admins.py:281-291`. Owner-only wrapper `revoke_admin()` adds the owner check —
  `src/channels/admins.py:862-872`.
- UI block path: `chadm_remove_ → chadm_remove_yes_` — `src/callbacks/channel_admins.py:652-693`
  (executes at line 667).
- UI unblock path: `chadm_restore_` — `src/callbacks/channel_admins.py:512-535`.
  Data-layer alternative: `restore_revoked()` — `src/channels/admins.py:1002-1013` (different semantics, see B9/B12).
- Real-time gate: `_recheck_or_deny()` — `src/callbacks/channel_admins.py:123-254`
  (live `get_chat_member` via `recheck_channel_member`, `src/channels/admins.py:350-372`,
  then `has_channel_permission`, `src/channels/admins.py:331-339`).
- Unblock-request flow: `chadm_request_*` chain — `src/callbacks/channel_admins.py:861-1014`,
  submit ` _submit_request()` at 1035-1077, approve/deny at 890-990, notify helpers at 1080-1146.
- Connect flow: `channel_connect_handler()` — `src/handlers/schedule_conv.py:168-714`
  (RBAC touch only at lines 460-466).
- Scheduler send path: `src/scheduler/helpers.py:287-399` (one-off), `:630-749` (recurring).

---

## 2. Block flow trace (owner blocks an admin)

1. Owner opens `chadm_list_` → profile → `chadm_remove_` (confirm) → `chadm_remove_yes_{channel}_{uid}`
   (`src/callbacks/channel_admins.py:652-693`). Guards: owner-only (656-659), no self-remove (660-662),
   no owner-remove (663-666). Correct.
2. Line 667 executes `revoke_channel_admin(channel, target_uid, reason='removed')`.
   Effect is **synchronous dict mutation**: admin record deleted, revoked entry written,
   `bot_data.save_all()` (sync). Next guarded action denies immediately (no cache in the path —
   `has_channel_permission` reads the live dict every call, `src/channels/admins.py:331-339`). So the
   "immediate effect" half works **for guarded entry points only**.
3. Target receives DM `chadm_removed_notify` + `chadm_removed_notify_hint` with a
   `chadm_request_{channel}_manage` restore button (`_notify_admin_removed`, lines 1095-1105). Verified.
4. What does **NOT** happen on block (all verified by reading the three functions above — none touches
   anything beyond the two dicts): no `ConversationHandler.end`, no `context.user_data` purge (neither the
   target's schedule/recurring drafts, `channel_connect_active`, `chadm_awaiting_*`, nor the owner's
   `chadm_draft[channel][target]`), no APScheduler job removal, no `user_channels` removal, no
   `bot_connections` / sender-bot token change, no `refresh_bot_cache_async`, no `user_info_cache`
   invalidation. Details in B2/B3/B4.

---

## 3. Findings

### B1 — CRITICAL — self-heal resurrects a revoked admin with default permissions (block bypass)
- **File:line:** `src/callbacks/channel_admins.py:159-174` (inside `_recheck_or_deny`).
- **Mechanism:** when `rec` is None (which is exactly the post-block state), the "last-resort identity
  fallback" checks `owned = channel in get_user_channels(user_id)` and re-creates the record via
  `ensure_admin_record(channel, user_id, is_owner=(existing_owner is None))`.
- **Why it fires:** revoke never removes the target's `user_channels` entry (see B2), so any revoked admin
  who ever connected the channel themselves still satisfies `owned == True`. `ensure_admin_record` then
  mints a **fresh record with `DEFAULT_ADMIN_PERMISSIONS`** (`src/channels/admins.py:203-234`, defaults at
  74-90: `schedule/message_list/message_edit/stats_view…: True`).
- **Impact:** the owner's block is undone on the target's very next guarded action, and the target may
  actually end up with *more* permissions than before (defaults, not prior custom set). A revoked admin
  whose pre-block `schedule` was False gets `schedule=True` back.
- **Repro (code path, no edit needed):** owner connects `@ch` (owner record + `user_channels[owner]=[@ch]`);
  co-admin connects `@ch` too (`user_channels[co]=[@ch]`, non-owner record); owner executes
  `chadm_remove_yes_@ch_co` (record gone, revoked set); co-admin presses any guarded button
  (e.g. `schedule_message`) → `_recheck_or_deny` finds no rec → `owned` True → record re-created with
  defaults → Telegram live check passes (still TG admin) → `has_channel_permission` passes for default-True
  perms → action proceeds.
- **Note:** existing sims (`tests/channel_admins/sim_*.py`) never set `user_channels`, so they never hit
  this branch. The sims passing does **not** cover this path.
- **Fix direction (for a later agent):** check `is_channel_admin_revoked(channel, user_id)` before the
  self-heal elevation and refuse with the `chadm_no_management` + restore-request screen; and/or remove the
  revoked user's `user_channels` entry at revoke time.

### B2 — HIGH — revoked user keeps `user_channels`; `_owns_channel` still passes → unguarded surfaces stay open
- **File:line:** `src/services/models.py:264-275` (`get_user_channels` reads `bot_data.user_channels`,
  never RBAC); `src/callbacks/channels.py:31-50` (`_owns_channel`: `channel in get_user_channels` → True
  without consulting `channel_admins`/`channel_revoked`); revoke `src/channels/admins.py:281-291` (does not
  touch `user_channels`).
- **Impact:** after a block, `channel_info_{ch}`, `manage_sender_bot_{ch}`, `managed_info_{ch}`,
  `hide_channel_toggle_{ch}`, `reports_{ch}`, `change_channel_`, `disconnect_channel_*` and the
  `show_channel` overview all still treat the blocked user as an owner (`_owns_channel` True at
  `src/callbacks/channels.py:158,208,253,294,322,345,579,630,804,900,1406,1426`). Only the
  `_recheck_or_deny`-guarded actions (schedule/recurring/statistics/leaderboard/export/manage_messages)
  deny. Channel-info page additionally hardcodes `role='Admin', bot_admin='Yes'` (lines 175-183) for a
  revoked user.
- **Evidence:** `channel_info` handler (156-204) gates only on `_owns_channel`; `management_menu`
  (544-574) is sender-bot-identity gated, not RBAC-denied for revoked users (shows a restore-request button
  instead — acceptable — but still renders the menu).

### B3 — HIGH — blocked admin's pending jobs are kept AND still fire (no send-time RBAC check)
- **File:line (kept):** revoke path writes no job handling — `src/channels/admins.py:281-291`,
  `src/callbacks/channel_admins.py:667-669` (no `remove_scheduled_message` / `paused` / delete).
- **File:line (fire):** send workers `src/scheduler/helpers.py:287-399` (one-off) and `:630-749`
  (recurring) check daily/monthly quotas, frozen/expiry, pause-flag — **zero** calls to
  `has_channel_permission` / `is_channel_admin` / `is_channel_admin_revoked` (grep over
  `src/scheduler/` returns no hits).
- **Impact:** "owner blocks an admin" does not pause, delete, or orphan-guard that admin's already
  scheduled/recurring posts for the channel; they post on schedule as if nothing happened. The profile
  counters (`_render_profile`, `src/callbacks/channel_admins.py:421-430`) keep counting them too.
- **Severity rationale:** for a moderation-motivated block (spam/abuse), the single most important effect
  (stop future posts) is missing.

### B4 — HIGH — in-flight sessions/conversations are not killed; mid-scheduling block only bites at the next guarded callback
- **File:line:** same revoke primitives as B3; no `ConversationHandler.END`, no `context.user_data` mutation,
  no `cancel_any_conversation` (contrast connect success path which *does* call it —
  `src/handlers/schedule_conv.py:700`).
- **Impact:** a blocked admin mid-scheduling keeps all draft state (`pending_schedule`, photo sets,
  `channel_connect_active`, `chadm_awaiting_request_msg/reply/phrase`); text-input steps that do not call
  `_recheck_or_deny` can complete. The next *guarded* callback denies correctly (verified: scheduler
  schedule/recurring/manage_messages at `src/callbacks/scheduler.py:541-542,970-971,1054-1055`; export at
  `src/callbacks/export.py:599-600,624-625`; channels statistics/leaderboard at
  `src/callbacks/channels.py:326-327,349-350,1340-1341`; commands export at
  `src/handlers/commands.py:1970-1971,2000-2001,2776-2777`), so revoke-while-acting is *eventually*
  consistent but not atomic, and the UX is "silently continue then deny at confirm".
- **Also stale:** the owner's `chadm_draft[channel][target]` (set at
  `src/callbacks/channel_admins.py:565-571`) survives the removal; a later restore + save could apply a
  pre-block draft.

### B5 — HIGH — blocked user can re-CONNECT the channel; no "you're blocked" refusal
- **File:line:** `src/handlers/schedule_conv.py:168-714` — no reference to `channel_revoked` /
  `is_channel_admin_revoked` anywhere in the 550-line connect handler (verified by grep; the only RBAC
  touch is `ensure_admin_record` + `sync_channel_admins` at 460-466).
- **Behavior:** a revoked-but-still-Telegram-admin user with `can_post_messages` passes all connect gates
  (bot-admin check 301-344, user-admin check 346-405) and receives the normal
  `channel_connected_success` receipt + main menu (632-701), plus a fresh `user_channels` entry
  (`set_user_channel`, `src/services/models.py:289-321`). The `ensure_admin_record` at line 463 briefly
  re-creates the RBAC record, then `sync_channel_admins` (lines 408-412 of `src/channels/admins.py`)
  strips it again because the uid is in `revoked`. Net state: connected in `user_channels`, absent in
  `channel_admins`, present in `channel_revoked` — connected-but-powerless, after being told "success".
- **Exact-message gap:** there is **no** connect-time "you can't, you're blocked" string in either
  translation bundle (grep `blocked` × `chadm` in `translations/en.json` / `ru.json` — zero connect-path
  hits). The user only learns the truth on their *next* action, which renders `chadm_no_management`
  (+ `chadm_request_restore_btn`) via `_recheck_or_deny` lines 176-187 / 216-239.

### B6 — MEDIUM — "allow unblock requests" toggle edits the wrong record; owner's own flag has no UI
- **File:line (gate):** `_submit_request` checks the **owner's** flag —
  `src/callbacks/channel_admins.py:1057`: `if get_admin_notify_requests(channel, owner):`.
- **File:line (toggle):** profile toggles the **target admin's** flag — lines 1024-1025
  (`set_admin_notify_requests(channel, target_uid, not current)`, displayed at 456-461).
- **File:line (no owner UI):** the notify row is rendered only inside the `else` (non-owner) branch —
  lines 445-461 — so the owner's own `notify_requests` (the only one that gates anything) can never be
  changed from the UI; it stays at the `ensure_admin_record` default `True`
  (`src/channels/admins.py:206,227`). The per-admin toggles the owner *can* flip have zero consumers
  (grep: `get_admin_notify_requests` has exactly 3 call sites — the two above plus the gate).
- **Impact:** the "owner setting to allow/disallow unblock requests" from the spec exists in data but is
  miswired: owners cannot disable request DMs; toggling an admin's bell does nothing observable.

### B7 — MEDIUM — approved-path receipt promise is false: pending requests have no owner-side surface
- **File:line:** `get_pending_requests()` defined `src/channels/admins.py:677-687`, imported at
  `src/callbacks/channel_admins.py:53` but **never called** anywhere in `src/` (grep confirms single hit).
  `_render_admins_list` (`src/callbacks/channel_admins.py:291-390`) renders live admins + revoked/restore
  rows but never pending `permission_requests`.
- **Impact:** if the owner DM (`context.bot.send_message(chat_id=int(owner)…`, lines 1068-1073) fails or the
  owner's flag were off, the request is JSON-only. Yet the requester receipt `chadm_request_sent_owner_off`
  (`translations/en.json`) promises *"they will see it when they open the Admins section"* — untrue.
  Owner-side approve/deny buttons (`chadm_request_yes/no_…`, lines 890-990) then only exist in the DM that
  may never have arrived.

### B8 — MEDIUM — 7-day anti-spam only binds *pending* requests; deny/approve → immediate re-request
- **File:line:** `can_request_permission`, `src/channels/admins.py:627-648`: a matching record with
  `pending == False` returns `(True, None)` (lines 639-640); `record_permission_request` (651-674) appends a
  *new* entry for non-pending matches instead of refreshing cooldown.
- **Impact:** docstring + `REQUEST_COOLDOWN_DAYS = 7` (line 148) advertise "one request per permission per
  user per week", but a denied requester can re-fire instantly (each fires another owner DM). Spam/annoyance
  vector against the owner. The `chadm_cooldown` toast (`translations/en.json`) only triggers while a
  request is still pending.

### B9 — MEDIUM — unblock = reset to defaults, not restoration (prior permissions unrecoverable)
- **File:line (no snapshot):** revoked entry stores only `{reason, revoked_at, [revoked_by]}` —
  `src/channels/admins.py:287-289`. Permissions are destroyed with the record (`remove_channel_admin`,
  252-261).
- **File:line (restore paths):** callback `chadm_restore_` re-adds via `sync_channel_admins`
  (`src/callbacks/channel_admins.py:521-529` → `ensure_admin_record` with defaults,
  `src/channels/admins.py:424-426`); data-layer `restore_revoked` explicitly uses defaults
  (`src/channels/admins.py:1010-1012`). The `manage`-restore grant path does the same
  (`src/callbacks/channel_admins.py:919-920`: `permissions=dict(DEFAULT_ADMIN_PERMISSIONS)`).
- **Impact:** any fine-grained pre-block permission set is lost; unblock always yields the default set
  (schedule/recurring/list/preview/edit/search/stats on; change/delete/export/import/backup/leaderboard/
  settings off). If reset-by-design it is undocumented in UI strings (`chadm_restored`,
  `chadm_manage_restored` imply full return).

### B10 — MEDIUM — UI block path drops the `revoked_by` audit field
- **File:line:** live path `src/callbacks/channel_admins.py:667` calls
  `revoke_channel_admin(channel, target_uid, reason='removed')` — no `revoked_by`.
  The owner-aware wrapper `revoke_admin(…, revoked_by=owner_id)` (`src/channels/admins.py:862-872`) is never
  used by the callback layer (grep: zero callers in `src/callbacks/`).
- **Impact:** `channel_revoked` forensics cannot answer "who blocked whom" for every real block; only
  programmatic/test paths record it.

### B11 — LOW — Telegram creator cannot stay blocked (silent self-heal, no UI warning)
- **File:line:** `src/channels/admins.py:402-407` (`sync_channel_admins` pops the creator out of `revoked`,
  plus line 406-407 double-pop) and 431-436 (creator forced to `is_owner`).
- **Impact:** owner pressing Remove on the Telegram creator appears to succeed (`chadm_removed` toast) but
  the next list/connect/sync restores them as Main Owner. No string warns the owner this is a no-op.
  (Arguably correct — Telegram is authoritative — but the UI should say so.)

### B12 — LOW — restore-path divergence + failed-restore clears the barrier
- **File:line:** callback `src/callbacks/channel_admins.py:521` unrevokes *before* `sync_channel_admins`;
  if the target is no longer a Telegram admin, lines 526-529 show `chadm_restore_failed` — but the revoked
  entry is already gone (the sim at `tests/channel_admins/sim_revoke_restore.py:181-188` enshrines this:
  *"failed restore still clears the stale revoked entry"*).
- **Divergence:** `restore_revoked()` (`src/channels/admins.py:1002-1013`) instead unrevokes *and*
  `ensure_admin_record`s unconditionally — works even when Telegram sync would refuse, i.e. opposite
  outcome offline. Two "restore" functions, two contracts; only the callback one is wired to the UI.
- **Impact:** low (arguably self-cleaning), but a reviewer should know the barrier is cleared on failure,
  letting the user re-connect fresh later.

---

## 4. Blocked-user CONNECT attempts (exact behavior + strings)

No connect-time block check exists (§B5). Sequence for a revoked user who is still a Telegram admin with
posting rights: full `channel_connected_success` success UI → silent RBAC strip on the post-connect sync →
next action renders:

> `chadm_no_management`: *"⛔ <b>You no longer have management ability for this channel.</b>\n\nRequest
> the Main Owner to restore it."* (`translations/en.json`)
> with button `chadm_request_restore_btn`: *"🔄 Request management back"* → `chadm_request_{channel}_manage`.

Permission-scoped (non-revoked, flag missing) denial is instead:

> `chadm_no_permission`: *"⛔ <b>You do not have permission to {perm} for this channel.</b>\n\nContact
> the Main Owner to request access."* with `chadm_request_btn`: *"🙋 Request permission from the admin"*.

There is no *"you can't, you're blocked"* string on the connect path in either language bundle.

---

## 5. Unblock-request flow (as built)

1. **Start:** denied screen button → `chadm_request_{channel}_{perm}` (perm or literal `manage` for full
   restoration) → intro (`chadm_request_intro`) → with/without-message branch
   (`src/callbacks/channel_admins.py:992-1014, 864-889`).
2. **Gate:** `can_request_permission` 7-day pending-only check (§B8); owner-already / already-have guards at
   996-999 (`chadm_already_have`); no-owner guard at 1042-1054 (`chadm_no_owner`).
3. **Owner notify:** DM with `chadm_owner_request_notify` (+ optional `chadm_request_message_label`) and
   inline `chadm_btn_yes/no` → `chadm_request_yes/no_{channel}_{uid}_{perm}` — **iff**
   `get_admin_notify_requests(channel, owner)` (§B6); else silent record + `chadm_request_sent_owner_off`
   receipt (§B7).
4. **Approve:** owner-only re-check (896-899) + genuinely-pending guard M26 (900-911,
   `chadm_request_not_pending`); `manage` → Telegram live re-check (914-918, `chadm_target_not_admin` on
   failure) + re-add with **defaults** (§B9) + `chadm_manage_restored`; single perm → live re-check L2
   (924-934, transient-safe via `chadm_verify_failed`) + grant + resolve + `chadm_granted`
   (912-942). Requester DM: `chadm_request_granted` (via `_notify_request_result`, 1132-1146).
5. **Deny:** `chadm_request_no_` → optional owner reply text (`chadm_deny_reply_prompt`, 944-965) →
   `chadm_request_final_no_` (owner re-verified H15, 966-977) → resolve + `chadm_denied` to owner view +
   `chadm_request_denied` (+ `chadm_owner_reply_label`) DM to requester (978-990, 1132-1146).
6. **Cleanup:** `resolve_permission_request` flips `pending=False, status=approved|denied|resolved`
   (`src/channels/admins.py:690-698, 967-999`) — record retained (audit-friendly), but cooldown released (§B8).

---

## 6. Real-time / cache behavior

- **Revoke-while-acting:** the *next guarded callback* denies — `_recheck_or_deny` performs a live
  `get_chat_member` + store read on every invocation, so no cache TTL to wait out. Verified guarded:
  `schedule` / `recurring` / `manage_messages` (`src/callbacks/scheduler.py:541-542,970-971,1054-1055`),
  `export` (`src/callbacks/export.py:599-600,624-625`; `src/handlers/commands.py:1970-2001,2776-2777`),
  `statistics` / `leaderboard` (`src/callbacks/channels.py:326-327,349-350,1340-1341`). Unguarded surfaces
  (§B2) and in-flight text steps (§B4) do not.
- **Cache invalidation:** there is nothing to invalidate on the RBAC read path (direct dict reads in
  `has_channel_permission` / `is_channel_admin` / keyboard `_perm_ok` at `src/keyboards.py:260-264` — all
  live). Conversely nothing *is* invalidated that should be: `user_channels`, `bot_connections`
  (`get_bot_connection_cache`), `user_info_cache` (1h TTL, `src/services/models.py:23-47`), and
  `context.user_data` all survive the block (B1/B2/B4). No `refresh_bot_cache_async` call exists on any
  revoke/restore path (grep confirms).
- **Self-heal hazards (work both ways):** transient API failures never destroy records (H13:
  `src/channels/admins.py:350-366`, `src/callbacks/channel_admins.py:204-226,595-606`) — good; but the same
  self-heal that protects the owner (`_recheck_or_deny:189-201` owner always passes; `sync` preserves owner
  on fetch failure, 386-391) also resurrects revoked users (B1) and the Telegram creator (B11).
- **Sender-bot bindings:** untouched by design? Any channel admin may *use* the channel's sender bot
  (`src/channels/admins.py:41-45`); *managing* bots belongs to the token owner. Revoke changes neither the
  token's `channel_id` (SQLite) nor `bot_connections` nor bot identity maps — so a blocked admin loses the
  UI permission but the underlying bot wiring is (correctly) left alone. No bug here, just note that B3's
  jobs keep a valid send route.

---

## 7. What works (do not regress)

- Immediate effect on the next guarded action (live dict + live Telegram re-check, no stale cache).
- Owner-only enforcement on every `chadm_*` mutation (`chadm_owner_only`), including list/profile/perm
  save/remove/restore/notify-toggle/transfer-cancel.
- Revocation survives re-syncs and restarts (`channel_revoked` + `sync_channel_admins` skip at
  `src/channels/admins.py:408-412`; regression sim passes).
- Transient-failure safety H13 (never revoke on `ok == False`) in `_recheck_or_deny`, perm-save, and sync.
- Stale-request replay guard M26 (`chadm_request_not_pending`) and deny-path owner re-check H15.
- Removed-admin DM with restore button; approve/deny DMs to requester incl. optional owner reply.
- Transfer flow (phrase + 24h TTL + atomic swap + audit log) unaffected.
- Keyboard permission filtering is live (`has_channel_permission` per render) — hiding is consistent even
  if it is not enforcement.
- Sims: `tests/channel_admins/sim_revoke_restore.py` — all 16 checks pass (re-run 2026-09-30, only
  pre-existing cp1252 console-encoding noise worked around with `PYTHONIOENCODING=utf-8`).

---

## 8. Method + read-only checks run

- Read: `src/channels/admins.py` (full, 1026 lines), `src/callbacks/channel_admins.py` (full, 1235 lines),
  `src/callbacks/channels.py` (management/connect regions), `src/handlers/schedule_conv.py:168-714`
  (connect), `src/scheduler/helpers.py:280-399,630-749` (send), `src/services/models.py:23-130,260-330`
  (block/user/channels), `src/keyboards.py:242-300` (filter), `translations/en.json` chadm_* strings.
- Grep (read-only): `revok|permission_request|notify_requests|channel_revoked` across `src/`; `_recheck_or_deny`
  call sites; `refresh_bot_cache|get_bot_connection_cache` (no revoke/restore callers); scheduler RBAC refs
  (none); `get_pending_requests` callers (none besides def/import); `revoked_by` callers.
- Ran (read-only, no code mods): `sim_revoke_restore.py` → 16/16 pass (with `PYTHONIOENCODING=utf-8` to dodge
  a Windows-console `UnicodeEncodeError` in the sim's own `print`, unrelated to bot logic).
- Not run live (no Telegram tokens / no bot runtime); connect/send sequences traced statically.

---

## 9. Suggested fix order (for the implementing agent, not this audit)

1. B1 (+B2 companion): revoked-guard before self-heal elevation; drop `user_channels` entry on revoke.
2. B3: send-time revoked/permission check (skip + notify, keep job paused rather than silently sending).
3. B5: connect-time revoked check with a dedicated "blocked" string.
4. B6/B7: point the notify toggle at the owner's record (or add an owner-level setting) + render pending
   requests in the Admins section so `chadm_request_sent_owner_off` becomes true.
5. B8/B9/B10: enforce cooldown post-resolution (or document); snapshot permissions in revoked entry or
   document reset; pass `revoked_by` from the UI path.
