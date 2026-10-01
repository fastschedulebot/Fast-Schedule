# Agent 2/8 — Permission Change Flows (grant / revoke / toggle by owner)

Scope: owner opens an admin profile → toggles a permission → what is written, where,
immediacy (every cache), toggle-all/preset roles, demote-self / last-admin / non-existent
admin, target notification (grant AND revoke), audit trail.
Read-only audit; no `src/` edits. Probes were run via `bash` (`python -c`, pytest) only.

Core files:

- `src/callbacks/channel_admins.py` — UI flow (profile, draft toggle, save, remove, requests)
- `src/channels/admins.py` — RBAC store + `has_channel_permission` + `sync_channel_admins`
- `src/keyboards.py:242-299` — sender-bot main-menu permission filtering
- `src/core/botdata.py:1015-1034` — `save_all()` persistence semantics
- `src/services/models.py:1016-1070` — `BOT_IDENTITY_MAP` (orthogonal to RBAC)
- `src/admin/helpers.py:630-643` — global audit-log reader
- `translations/en.json` (`chadm_*`) — notify/diff strings

Test runs (read-only, no code changes):

- `pytest tests/unit/test_channel_admins_comprehensive.py` (with `-o python_classes=Test*`,
  required because `pytest.ini` sets `python_classes` empty so default collection finds 0):
  **50 passed**.
- `pytest tests/unit/test_callbacks_channel_admins.py`: **15 passed**.
- Live probes confirmed: legacy-perm gate always `False`, `_split_channel_perm` returns
  `(None, None)` for all 4 legacy perms, `set_admin_notify_requests` creates a ghost admin
  record for an unknown uid.

---

## 1. UI flow as built (what works)

1. Owner → `chadm_list_{channel}` → `_render_admins_list`
   (`src/callbacks/channel_admins.py:291-390`). Live `sync_channel_admins` first,
   owner-only gate (`chadm_owner_only` alert otherwise). Self-heals ownerless channels.
2. Tap admin → `chadm_profile_{channel}_{uid}` → `_render_profile` (`:393-480`): stats,
   15 individual permission toggle buttons (`chadm_perm_{channel}_{uid}_{perm}`), a
   notify toggle, back, make-owner + remove (hidden for the owner record itself).
3. Tap a permission → `chadm_perm_…` (`:546-572`): flips **one** flag in a **draft** kept in
   the *owner's* `context.user_data['chadm_draft'][channel][uid]`. Nothing is written to
   the store yet. Draft-aware profile shows unsaved banner + Save/Discard + guarded Back
   (`chadm_perm_leave_`, `:637-649`). Multi-toggle accumulation works (draft built from
   previous draft, not from stored perms — the comment at `:563-564` notes this was a fix).
4. Save → `chadm_perm_save_…` (`:575-625`): owner re-checked, draft popped, target
   re-validated live via `recheck_channel_member`, then
   `set_admin_permissions(channel, target, draft)` (`src/channels/admins.py:237-245`) =
   `ensure_admin_record` + merge + `bot_data.save_all()`. Owner sees a diff summary
   (`chadm_saved_title` + per-perm ON/OFF lines, `:610-622`), target is notified
   (`_notify_admin_permissions_changed`, `:1080-1092`).
5. Discard → `chadm_perm_cancel_…` (`:628-634`): drops draft, re-renders stored profile.
6. Remove → `chadm_remove_…` → strong confirm → `chadm_remove_yes_…` (`:652-693`):
   `revoke_channel_admin(channel, target, reason='removed')` + `_notify_admin_removed`.
   Restore via `chadm_restore_…` (`:512-535`): unrevoke + resync; fails cleanly with
   `chadm_restore_failed` if the user is no longer a Telegram admin.
7. Request path (admin asks, owner grants/denies): `chadm_request_*` (`:862-1014`),
   grant writes via `set_admin_permissions` + `resolve_permission_request`, deny resolves
   + notifies with optional reply. Stale/replayed buttons are rejected (`chadm_request_not_pending`,
   `:909-911`; owner re-check on `final_no_`, `:966-977`). Good.
8. Owner self-protection in UI: toggle owner → `chadm_cannot_edit_owner` (`:560-562`);
   remove self → `chadm_cannot_remove_self` (`:660-662`, `:682-684`); remove owner →
   `chadm_cannot_remove_owner` (`:664-666`); make-owner to self → `chadm_already_owner`
   (`:703-705`); non-existent target on profile/toggle/remove/makeowner →
   `chadm_admin_not_found` (`:406-409`, `:559-562`, `:706-709`). API layer mirrors this
   (`update_admin_permissions` refuses owner target, `remove_admin` refuses owner target,
   `transfer_ownership` refuses self-transfer and non-admin target —
   `src/channels/admins.py:817-860`). Good.

---

## 2. Where it is written

Single source of truth: `bot_data.channel_admins[channel_id][user_id]` =
`{is_owner, permissions: {15 canonical perms}, joined_at/added_at, can_post_messages,
notify_requests, added_by?}`. Revocation bar list: `bot_data.channel_revoked[channel_id][uid]`.
Permission-request inbox: `bot_data.permission_requests[channel_id]` (list of records).
Pending ownership: `bot_data.pending_transfers[channel_id]`.
All writes go through `ensure_admin_record` / `set_admin_permissions` /
`revoke_channel_admin` / `remove_channel_admin` and end in `bot_data.save_all()`.

No toggle-all / preset roles exist. `_render_profile` (`:444-461`) renders exactly the 15
canonical toggles one-by-one plus the notify toggle. There is no select-all, deselect-all,
"editor / viewer / moderator" preset, or group-toggle (the `PERM_GROUPS` dict in
`src/channels/admins.py:65-70` is UI-group metadata only and is never wired to any
callback). Impact: owner managing many admins must tap up to 15 times per admin. Severity: low
(missing convenience, not a correctness bug).

---

## 3. Immediacy — does it take effect immediately?

**Yes for the running process; durability is deferred (by design).** Findings per cache:

- `bot_data.channel_admins` (the only store `has_channel_permission` /
  `get_admin_permissions` read, `src/channels/admins.py:318-339`): mutated **in place**,
  so the very next gate check sees the new value. No restart / re-login / expiry needed.
  Verified: `set_admin_permissions` writes the live dict before `save_all()`.
- `context.user_data`: the *draft* is the only `user_data` involved, and it is
  owner-scoped staging, not an enforcement cache. Toggles are NOT effective until Save
  (by design — unsaved banner says so). One wart: Save/Cancel pop the **entire**
  `chadm_draft` dict (`:584`, `:631`), so drafts for *other* channels/targets staged in
  the same session are silently discarded (see §7, minor).
- `bot_connection_cache` (`bot_data.user_settings[uid]['bot_connections']`,
  `src/services/models.py:387-438`): orthogonal — it caches sender-bot↔channel linkage,
  never RBAC flags. Permission changes neither read nor invalidate it, and do not need to.
- `BOT_IDENTITY_MAP` (`src/services/models.py:1016-1070`): token→sender-bot identity,
  built at startup, unrelated to channel-admin rights. Unaffected (correctly).
- In-memory dicts elsewhere: `user_info_cache` / `user_bot_info` hold display info only.
- Disk: `save_all()` (`src/core/botdata.py:1015-1025`) is a **no-op while the background
  flush loop is running** — durability rides the timed flush, not the handler call. So a
  crash in the flush window loses the change from disk, but in-memory enforcement is
  already immediate. After restart the last flushed state loads. This matches the
  write-budget architecture; not a bug, but operators should know a hard kill within the
  flush interval can roll back the most recent permission edit.
- Clobber risk: `_render_admins_list` and several entries call `sync_channel_admins`,
  which **preserves** existing permission dicts (only touches `can_post_messages` /
  `is_owner`, pops users genuinely absent from Telegram). A just-saved permission set
  survives a sync. Genuine Telegram-side removal does wipe the bot-side record (intended),
  except the revoked-bar keeps owner-removed users out permanently (intended).

---

## 4. BUGS

### B1 (CRITICAL) — Enforcement gates use legacy permission keys that can never match
`src/keyboards.py:251-257`, `src/callbacks/scheduler.py:1055`,
`src/callbacks/channels.py:327,350`, `src/handlers/commands.py:1971,2001,2777`,
`src/callbacks/export.py:600,625` pass `'manage_messages'`, `'statistics'`,
`'leaderboard'`, `'export'` to `_recheck_or_deny` → `has_channel_permission`
(`src/channels/admins.py:331-339`), which does a literal
`perms.get(perm, False)` against records that only ever store the 15 canonical keys
(`schedule`, `message_list`, …, `stats_view`, …, `data_export`, …).
`LEGACY_PERM_MAP` / `FEATURE_PERMISSION` (`src/channels/admins.py:117-145`) are **defined
but never referenced anywhere** (grep: only definition site). Live probe on a fully
permissioned admin: canonical `schedule` → `True`; `statistics` / `export` /
`manage_messages` / `leaderboard` → all `False`.
Impact: **every non-owner admin is denied** message-list (`manage_messages`), statistics,
leaderboard, and export regardless of granted rights; sender-bot main menu
(`keyboards.py:295-297`) hides those buttons for all non-owners. Owner unaffected
(short-circuits `True`), which is why this likely went unnoticed.
Severity: critical. Fix direction (no code changed here): expand legacy keys via
`LEGACY_PERM_MAP` inside `has_channel_permission`/`get_admin_permissions`, or migrate
callers to canonical keys.

### B2 (CRITICAL) — Permission-request flow is unparseable for those same legacy perms
`_split_channel_perm` (`src/callbacks/channel_admins.py:98-108`) only matches suffixes in
`('manage', *CHANNEL_PERMISSIONS)` — `statistics`, `leaderboard`, `export`,
`manage_messages` never match, so it returns `(None, None)` and every
`chadm_request_*` / `chadm_request_yes_*` / `chadm_request_no_*` / `final_no_*` handler
hits `if not channel or not perm: return` and **silently drops** the callback.
Probe: `_split_channel_perm('@ch_statistics' / '@ch_export' / '@ch_manage_messages' /
'@ch_leaderboard')` → `(None, None)`; `'@ch_schedule'` → `('@ch', 'schedule')`.
Impact: an admin denied by B1 taps "Request permission" and nothing happens (no error);
if a request record somehow exists, the owner's Yes/No buttons also silently no-op while
the request stays `pending`, and the 7-day cooldown (`can_request_permission`) blocks
retry — a stuck request. Severity: critical (compounds B1: denied AND cannot ask).

### B3 (MEDIUM) — `chadm_notify_toggle` creates a ghost admin for a non-existent uid
`handle:chadm_notify_toggle_` (`src/callbacks/channel_admins.py:1017-1026`) parses ids and
calls `get_admin_notify_requests` / `set_admin_notify_requests` with **no existence check**;
`set_admin_notify_requests` → `ensure_admin_record` (`src/channels/admins.py:305-308` →
`:203-234`) **creates** a full default-permissions record. Probe: unknown `ghost9` went
from `None` to a complete admin dict with `is_channel_admin → True`.
Impact: crafting/replaying a notify-toggle callback for an arbitrary uid mints a real
channel-admin record (default perms: schedule/recurring/list/preview/search/stats ON).
Severity: medium (requires owner to press it, but owner can be social-engineered with a
forwarded button; and it corrupts the admins list). Fix direction: `get_admin_record`
guard + `chadm_admin_not_found`, mirroring the toggle path.

### B4 (MEDIUM) — No audit trail for permission changes; ownership log would crash the audit viewer
Only ownership acceptance appends anything, to
`bot_data.audit_log['ownership_transfers']` as a **list**
(`src/callbacks/channel_admins.py:825-837`). Permission saves, removals/restores, notify
toggles, and request grants/denies log **nothing**. Worse, the global viewer
`collect_audit_log` (`src/admin/helpers.py:630-643`) iterates `audit_log.items()` expecting
`{entry_id: {admin_id, action, details, timestamp}}` and calls `rec.get(...)` — a list
value raises `AttributeError` (reproduced: `'list' object has no attribute 'get'`).
Impact: (a) no accountability for who granted/revoked what, when; (b) the **first**
ownership transfer arms a crash the next time anyone opens the global audit log.
Severity: medium. Fix direction: log perm events in the entry-dict shape the viewer
expects (or make the viewer tolerant), and never store a bare list under `audit_log`.

### B5 (LOW) — `revoke_channel_admin` called without `revoked_by` on the remove path
`src/callbacks/channel_admins.py:667`: `revoke_channel_admin(channel, target, reason='removed')`
omits `revoked_by`, although the API records it (`src/channels/admins.py:281-291`,
`revoke_admin` passes it at `:871`). Impact: revoked entries from UI removal lack the
`revoked_by` attribution the schema supports. Severity: low.

### B6 (LOW) — Save/Cancel discard drafts for all channels/targets, not just the current one
`chadm_draft` is keyed `[channel][uid]` (`:569-571`) but both save (`:584`) and cancel
(`:631`) `pop('chadm_draft')` wholesale. Impact: staging edits for admin A, then saving
admin B, silently throws away A's unsaved work (no warning; the leave-guard only covers
navigation, not cross-profile saves). Severity: low.

### B7 (INFO) — Notification content gaps (grant AND revoke both fire, but content is weak)
Both directions DO notify, awaited right after the write:
grant/save → `_notify_admin_permissions_changed` (`:624`, `:1080-1092`);
remove → `_notify_admin_removed` (`:668`, `:1095-1105`);
request grant/deny → `_notify_request_result` (`:921-937`, `:983-984`, `:1132-1146`).
Timeliness is correct (after persist, before returning). Content issues:
(a) grant notice sends the **full 15-permission dump**, not the diff the owner saw —
target cannot tell what actually changed;
(b) neither notice names **who** changed it (revoke text says only "by the Main Owner",
grant text names nobody; no owner id/username);
(c) `channel` is the **raw channel id** (`escape_html(channel)`), not the human title
the profile page resolves via `get_chat` (`:414-418`) — confusing for `@`-less numeric ids;
(d) grant notices render in the **target's** language (correct) but the permission labels
use `_perm_label(target_uid, …)` while state words use `t(target_uid, …)` — consistent,
fine; (e) all notifies swallow send failures silently (`except: pass`) — a target that
blocked the bot never gets the memo and the owner is never told delivery failed;
(f) **silent revocations**: auto-sync reaps (`sync_channel_admins` pop loop,
`src/channels/admins.py:444-446`), deleted-account sweeps (`:321`, `:313-336`), and the
save-path `chadm_target_left` branch (`:596-603`) remove rights with **no notice at all**.
Severity: low (info-level, except (f) which can surprise removed admins).

### B8 (INFO) — Dead code + last-admin semantics
- `src/callbacks/channel_admins.py:604-606`: second `return` after `return await
  _render_profile(...)` is unreachable.
- "Removing the last admin": there is **no** last-admin guard beyond owner protection —
  `remove_admin`/`revoke` freely remove the sole non-owner admin (the unit test named
  `test_remove_last_admin_fails` actually only asserts a non-owner cannot remove the
  owner, not a last-admin rule). Owner-only channel afterwards is a valid state, so this
  is documented as intended, not a bug — but the test name overpromises.
- Demoting self: impossible via UI/API (all paths block), ownership can only move via the
  phrase + 24h-accept transfer. Non-existent admin edits are rejected everywhere except B3.
  Severity: info.

---

## 5. What works (do not regress)

- Draft-then-save with diff summary; multi-toggle accumulation; unsaved-changes guard.
- Owner-only gating on every mutation entry (list/profile/toggle/save/remove/transfer/
  request-resolve/notify-toggle), re-checked at save time (TOCTOU-safe against ownership
  change between open and save).
- Target re-validation with `recheck_channel_member` before save/grant; transient API
  failures block-but-preserve instead of destroying records (H13 handling).
- Revoked-bar survives auto-sync (owner removals are not silently re-added); Telegram
  creator override; deleted-account sweep.
- Request anti-spam (weekly cooldown), stale-button rejection, deny-with-reply, restore path.
- Immediate in-memory effect; no stale RBAC caches (`bot_connection_cache` /
  `BOT_IDENTITY_MAP` correctly untouched).
- 50 + 15 existing unit tests pass (with the `python_classes` override noted above).

## 6. Coverage statement

Traced profile→toggle→save→store→gate→notify→(non-)audit end to end, checked all four
caches named in scope, confirmed no toggle-all/role presets, exercised owner-self /
last-admin / ghost-admin edges, verified both notify directions and their exact strings,
and confirmed the audit gap. The two critical findings (B1, B2) were reproduced with
read-only probes; everything else is cited to exact file:line above.
