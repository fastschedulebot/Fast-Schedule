# Permission Model Core — Audit (Agent 1/8)

Scope: `src/channels/admins.py` (1026 lines, read fully) + every user action on a channel vs. its gate.
Method: full code read + grep over `src/` + live read-only `python -c` probes (in-memory only, no `save_all`, no `src/` edits).

## Model reference (verified working)

- Store shape `src/channels/admins.py:5-8,168-234`: `bot_data.channel_admins = {channel_id: {user_id: {'is_owner': bool, 'permissions': {perm: bool}, 'joined_at': str, 'added_at': str(alias), 'can_post_messages': bool, 'notify_requests': bool, 'added_by': str}}}`. Confirmed in `ensure_admin_record` (203-234), `get_channel_admins` (168-184), `get_admin_record` (187-188).
- Canonical keys `src/channels/admins.py:46-62` (15 keys): `schedule, recurring, message_list, message_preview, message_edit, message_change, message_delete, message_search, stats_view, leaderboard_view, data_export, data_import, data_backup, settings_hide_channel, settings_change_permissions`. No `manage_bots` (comment 41-45 explains why) — correct.
- `has_channel_permission` (`331-339`): non-record → `False`; `is_owner` → `True` (unconditional bypass); else `perms.get(perm, False)`. Verified by probe: owner `True`, non-member `False`, all-false co-admin `False` on every canonical perm.
- `is_channel_owner` (`199-200`) / `get_channel_owner` (`191-196`): string-compared scan for `is_owner`. Owner bypass is **correct per spec** (owner implicitly has everything, cf. line 40 + `get_admin_permissions` 318-328 returning all-`True` for owner). Verified: `get_admin_permissions(owner)` all-`True`; non-member `{}`.
- `DEFAULT_ADMIN_PERMISSIONS` (`74-90`): `True` = schedule, recurring, message_list, message_preview, message_edit, message_search, stats_view; `False` = message_change, message_delete, leaderboard_view, data_export, data_import, data_backup, settings_hide_channel, settings_change_permissions. Verified by probe.
- `FEATURE_PERMISSION` (`117-137`) correctly maps UI/feature aliases → canonical perms (e.g. `export→data_export`, `statistics→stats_view`, `msg_list_menu→message_list`). **But nothing at the enforcement points uses it** (see B1).
- `LEGACY_PERM_MAP` (`140-145`) exists for migration only; also unused at enforcement.
- `_recheck_or_deny` (`src/callbacks/channel_admins.py:123-254`) **for the paths that call it** is correctly live, not stale: fresh `get_admin_record` (138) → self-heal `sync_channel_admins` (144) → identity fallback (159-174) → owner fast-path with soft re-sync (189-201) → regular-admin strict live `recheck_channel_member` (204) with `ok`-flag handling: transient (`ok==False`) blocks-but-keeps-record (215-226, H13 correct), genuine negative revokes via `remove_channel_admin` + deny (229-239). `recheck_channel_member` (`admins.py:350-372`) is a live `get_chat_member` per action, never cached; `creator→(True,True,True)` correct. `sync_channel_admins` (`375-454`) only revokes after a successful `get_chat_administrators` (early return 391 on failure) — transient-safe. All verified by reading; not re-tested live against Telegram (no network in audit).
- Co-admin with all-`False` permissions: `has_channel_permission` returns `False` everywhere, yet `is_channel_admin` stays `True` (probe confirmed). I.e. model correctly distinguishes "is admin" from "may do X". Working.
- No permission flags are cached in `context.user_data` (grep for `user_data[` permission keys: none found — only `selected_channel/selected_channels/selected_sender_channel`, flow state, search cache). So there is **no stale user_data flag that keeps granting** on gated paths; the staleness problem is instead (a) `selected_channel` surviving revocation and (b) whole flows that never consult the store at all (see B2/B3).

## Bugs / mismatches

### B1 [High] `_recheck_or_deny` call sites pass legacy/group aliases that can never be granted to co-admins — fail-closed lockout (owners unaffected via bypass)
- Files:lines:
  - `src/callbacks/scheduler.py:1055` passes `'manage_messages'`
  - `src/callbacks/export.py:600,625` + `src/handlers/commands.py:1971,2001,2777` pass `'export'`
  - `src/callbacks/channels.py:327` passes `'statistics'`; `src/callbacks/channels.py:350` passes `'leaderboard'`
  - `src/keyboards.py:251-257` `BUTTON_PERM`: `'msg_list_menu'→'manage_messages'`, `'statistics'→'statistics'`, `'export_menu'→'export'`
- Proof: canonical list has none of `manage_messages/export/statistics/leaderboard` (probe: all `in CANON → False`); `has_channel_permission` does `perms.get(perm, False)` with no alias/group expansion (`admins.py:331-339`); `_recheck_or_deny` forwards `perm` verbatim (`channel_admins.py:241`). Probe with a default-permission co-admin: all four aliases → `False`; owner → `True` (bypass masks it).
- Impact: every co-admin is denied message-list, export/data-hub, stats, leaderboard even with all relevant canonical flags `True`. Availability break of the RBAC feature; security-wise fail-closed (no escalation), but the intended grants don't work. Keyboard filter has the same bug in the same direction (buttons wrongly hidden for permitted co-admins).
- Fix direction: resolve through `FEATURE_PERMISSION`/`LEGACY_PERM_MAP` (or accept a set of perms) at `_recheck_or_deny`/`has_channel_permission`/`keyboards._perm_ok` boundary.

### B2 [High] Main-bot schedule & recurring creation paths never call `_recheck_or_deny` — `schedule`/`recurring` flags unenforced outside sender-bot context
- Files:lines (gates that exist): `src/callbacks/scheduler.py:538-543` (`schedule`, sender-bot only), `965-972` (`recurring`, sender-bot only). Main-bot/hybrid continuation (`scheduler.py:589-644`, `985-1035`), conversation body `src/handlers/schedule_conv.py:1503+` (`selected_channel` from `user_data`, checks only sender-bot routing, quotas, subscriptions — zero RBAC greps in `src/handlers/`), and `src/handlers/recurring.py:129,279,525,752,1272` (same: no RBAC string anywhere in `src/handlers/` except the three `export` gates in `commands.py`).
- Impact: on the main bot a co-admin with `schedule=False` (or `recurring=False`, or removed entirely but still holding `selected_channel` in `user_data`) can walk the conversation and create messages; per-channel quotas still apply but the permission flag does not. Fail-open. (Sender-bot entry is gated, so the hole is main-bot flows + any deep-link that lands there.)
- Fix direction: gate the conversation entry/confirm on `selected_channel` with `_recheck_or_deny(..., 'schedule'/'recurring')`.

### B3 [High] Message list/preview/edit/duplicate/delete, recurring pause/resume/delete, and search have no RBAC check — only creator-ownership (`user_id` match)
- Files:lines:
  - `src/callbacks/user/edit.py:44-63` `_lookup` (ownership + sender-bot channel scope only), used by `preview_callback:90-101`, `edit_callback:104-130`, `duplicate_callback:133-150`, `duplicate_yes:153-176`, `duplicate_no:178-195`, finalizers `_finalize_duplicate:351+`, `_finalize_modify:439+` (limit checks only, no perm check).
  - `src/callbacks/scheduler.py:1046-1089` (`msg_list_menu` main-bot branch: no gate; sender-bot branch gated with the broken `manage_messages` alias), `1091-1145` (`del_`/`del_confirm_`: ownership only), `1147-1166` (`msg_info_`: ownership only), `1172-1238` (recur pause/resume prompt+confirm: ownership only), `1240-1360+` (`list_scheduled/recurring_msgs`: ownership + `channel_filter`, no `message_list/message_preview` check).
  - `src/handlers/search.py:15-78` (`search_handler`/`_execute_search`: `user_id` match only, no `message_search` check), `src/callbacks/premium.py:866-882` (`search_menu` entry: no gate), `129-148` (pagination over `user_data['search_cache']`: no re-check).
- Impact: (1) a co-admin whose `message_edit/message_delete/message_preview/message_list/message_search` was revoked (or never granted) keeps full control of their own jobs; (2) a user removed from admins mid-session keeps acting on pre-existing jobs because nothing re-verifies membership — `selected_channel`/`search_cache`/`last_msg_list_cb` in `user_data` are never invalidated on revocation; (3) conversely `message_list` as a cross-admin visibility perm is meaningless on the main bot since lists are per-creator anyway. Net: the six `message_*` + `message_search` flags are documented but unenforced on these paths. Fail-open for own jobs.
- Fix direction: add `_recheck_or_deny` per job's `channel_id` with the matching canonical perm at each entry (preview→`message_preview`, list→`message_list`, edit/modify→`message_edit`, delete→`message_delete`, change-channel→`message_change`, duplicate→`schedule`+`message_preview` or dedicated rule, search→`message_search`, pause/resume→`recurring`).

### B4 [High] Export picker reads a non-existent permission key `'export'` instead of `'data_export'`
- File:line: `src/callbacks/export.py:215-225` (`admins[...].get('permissions', {}).get('export')`).
- Impact: `rbac_export` is always empty — co-admins with `data_export=True` are never listed as exportable, so channel-scoped export silently drops their channels. Compounds B1 (the `export` alias gates deny them anyway). No escalation (fail-closed), but the grant path is dead code as written.
- Fix direction: `.get('data_export')` (or `has_channel_permission(user_id, ch, 'data_export')`).

### B5 [Medium] Import / backup / media-storage / calendar / stats-dashboard entries have no channel-permission gate
- Files:lines sampled: `src/callbacks/export.py:300+` (`import_data`: channel list via `get_user_channels`, no `data_import` check); backup/export-format handlers under `export.py:648+` and `src/handlers/export.py:646,825` (no `data_backup`/`data_export` per-channel check outside the two B1 gates); `src/callbacks/media.py:49+` (storage is user-level by design — correctly ungated, but then `CHANNEL_PERMISSIONS` has no `media/*` entry while the keyboard/gate lists treat `storage` as a feature: intentional? undocumented); `src/callbacks/scheduler.py:1616+` (`calendar_view`: no `schedule` check); stats dashboard `render_stats_dashboard` reachable without passing through the `sender_bot_stats_` gate depending on entry.
- Impact: `data_import` / `data_backup` flags are unenforced on their flows (fail-open for owners' channels data); media has no channel perm at all so any channel admin with bot access can use shared-media flows — needs a product decision, currently silent.
- Fix direction: gate import→`data_import`, backup→`data_backup`, calendar→`schedule` (or explicit decision), and either document media as user-scoped (working as intended) or add a perm.

### B6 [Low] Owner fast-path skips the live `can_post` enforcement
- File:line: `src/callbacks/channel_admins.py:189-201` returns `True` for `is_owner` even when live `recheck_channel_member` says not-admin/can't-post (only triggers a soft re-sync that deliberately preserves the owner, `admins.py:438-443` + comment).
- Impact: a demoted ex-owner keeps owner powers until the periodic sweep/full sync corrects the store. Matches the stated "never lock the owner out on transient failure" design; genuine Telegram-side owner changes are handled by `sync_channel_admins` creator-wins logic (`431-436`), but a single action in the window still passes. Acceptable if deliberate — record as known trade-off, not a regression.
- Note: `sync_channel_admins:404-407` un-revokes the Telegram creator even if previously `revoke_channel_admin`'d — correct (Telegram is authoritative), and `get_channel_owner` returns the first `is_owner` found, so a double-owner state would resolve to whichever scans first; `accept_ownership_transfer` (755-791) and creator-wins loop prevent persistence, but no invariant asserts single-owner. Low.

## What was verified as working
- Storage shape, defaults, owner-bypass semantics, all-false co-admin denial, non-member denial, `get_admin_permissions` owner/non-member behavior (probes above).
- `_recheck_or_deny` live semantics on the paths that call it (fresh store read + live `get_chat_member` + transient-vs-genuine split + revoke-only-on-genuine). Correct; no cached/stale snapshot at the check itself.
- Revoked-set (`channel_revoked`, `revoke_channel_admin:281-291`, `is_channel_revoked:277-278`) correctly survives `sync_channel_admins` (408-412) except for the Telegram creator (405-407, correct).
- Sender-bot entry gates for schedule/recurring/statistics/leaderboard/export exist and are live (lines cited in B1) — broken only by the alias bug, not by staleness.
- `user_data` carries no permission booleans, so gated paths cannot be fooled by replayed flags; the residual staleness is `selected_channel`/`search_cache`/job-ownership flows that bypass the store (B2/B3).

## Coverage list (actions vs. gate found)
| Action | Gate (CURRENT data?) | Verdict |
|---|---|---|
| schedule create (sender bot) | `_recheck_or_deny 'schedule'` live | OK |
| schedule create (main bot conv) | none | B2 |
| recurring create (sender bot) | `_recheck_or_deny 'recurring'` live | OK |
| recurring create (main bot conv) | none | B2 |
| recurring pause/resume/delete | ownership only | B3 |
| message list | sender-bot: broken alias; main-bot: none | B1+B3 |
| message preview (`msg_preview_`, `msg_info_`) | ownership only | B3 |
| message edit/modify | ownership only | B3 |
| message duplicate | ownership + limits only | B3 |
| message delete (`del_*`) | ownership only | B3 |
| message change-channel | ownership only (finalize) | B3 |
| search entry + execute + pages | none | B3 |
| stats (`sender_bot_stats_`/`stats_main_`) | live but alias `'statistics'` | B1 |
| leaderboard (`lb_*`) | live but alias `'leaderboard'` | B1 |
| export/data-hub/commands | live but alias `'export'` + wrong key | B1+B4 |
| import / backup | none | B5 |
| media/storage | none (user-scoped by design?) | B5 note |
| calendar | none | B5 |
| owner bypass / all-false / removed-mid-session on gated paths | correct live semantics | OK |
