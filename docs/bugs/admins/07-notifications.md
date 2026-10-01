# Agent 7/8 — Notification fan-out audit: channel-admin events

Scope: every admin-event notification (added/removed, permission granted/changed/revoked,
ownership transfer initiated/accepted/declined, permission requested/approved/denied,
blocked/unblocked incl. revoke/restore, unblock/restore requested/decided).
Codebase snapshot: `src/callbacks/channel_admins.py` (1235 lines), `src/channels/admins.py`,
`src/admin/handlers.py` (block conv), `src/callbacks/admin/users.py` (block toggle),
`src/core/i18n.py`, `translations/en.json` + `translations/ru.json`.
Method: full read of the dispatcher + notify helpers, EN/RU key-diff scripts, placeholder
cross-checks, live `t()` rendering via `.venv` python, ran sims
`tests/channel_admins/sim_chadm_callbacks.py` (17/17 pass),
`sim_transfer_flow.py` (12/12 pass), `sim_revoke_restore.py` (16/16 pass).
System python has no pytest and a wrong PTB version; sims only run under `.venv`.

## Verdict

**NOT CLEAN — 3 functional bugs (1 high), 1 RU-only raw-key bug, 5 silent gaps, 3 low-severity issues.**
No crash paths, no leaks to non-involved users, no unfilled `{placeholder}` leaks.
Timing is uniformly immediate (in-handler `send_message`); nothing is tick/deferred —
except transfer expiry, which notifies nobody (lazy check on read).

## What works (verified)

- Recipients are exactly the involved party in every push: affected admin for
  perm-change (`channel_admins.py:1080`), removal (`:1095`), transfer offer (`:1117`),
  request results (`:1132`); old owner for accept (`:813`) / decline (`:851`);
  transfer target for cancel (`:1108`); channel owner for new requests (`:1068`).
  No broadcast, no third-party recipients — no leak surface found.
- Guards on inbound decision buttons: stale Yes is rejected unless the request is
  genuinely pending (`:900-911`, M26); final-deny re-checks owner (`:970-977`, H15);
  accept is gated to the named target (`:796`). A replayed/forwarded button grants
  or denies nothing.
- Undeliverable (blocked bot / deleted account) never crashes: every `_notify_*`
  is wrapped in `try/except: pass` (`:1083-1146`), accept/decline/cancel sends likewise.
  The request path even tracks delivery and picks a different receipt
  (`notified` flag, `:1056-1077`). Robust, but see L1.
- All `{placeholder}` kwargs are supplied at every `t()` call site (the naive-regex
  hits on `:1005`, `:1059`, `:1137`, `:1140` are false positives — args contain nested
  `escape_html(...)` parens). No raw `{key}` leaks in any template.
- Global block-via-conversation notifies correctly: `src/admin/handlers.py:1422-1439`
  sends `user_blocked_msg` in the *target's* language, tracks `notification_sent`,
  and mirrors it in the admin receipt (`:1447-1451`).
- Sims pass: request approve/deny, transfer offer/cancel/decline, revoke/restore
  mechanics all deliver to the right fake peer.

## Bugs

### H1 (HIGH) — 13 of 15 permission-label keys missing in EN *and* RU: raw keys in notifications
- File: `translations/en.json`, `translations/ru.json` (absent) ← `src/channels/admins.py:93-114`
  (`PERM_LABEL_KEYS`) → `src/callbacks/channel_admins.py:93-96` (`_perm_label` → `t()` →
  `src/core/i18n.py:160` returns the raw key on miss).
- Only `chadm_perm_schedule` / `chadm_perm_recurring` exist. The other 13 canonical
  perms (`message_list/preview/edit/change/delete/search`, `stats_view`,
  `leaderboard_view`, `data_export/import/backup`, `settings_hide_channel`,
  `settings_change_permissions`) render as e.g. `chadm_perm_message_list`.
- Live-verified: `t('0','chadm_perm_message_list')` → `'chadm_perm_message_list'`.
- Impact: every `_notify_admin_permissions_changed` (`:1080-1092`, lists **all 15** perms)
  shows 13 raw keys; same leak in owner request DM (`:1059`), `chadm_request_granted` /
  `chadm_request_denied` (`:1137/:1140`, "You can now chadm_perm_…"), `chadm_request_intro`,
  `chadm_no_permission`. The existing EN keys (`statistics/leaderboard/export/manage_messages`)
  are legacy names not in `CHANNEL_PERMISSIONS`, so they never render.
- Fix: add the 12 missing `chadm_perm_*` label keys (both languages).

### M1 (MEDIUM) — per-admin "request notifications" mute is dead (wrong record checked)
- File: `src/callbacks/channel_admins.py:1057` vs `:1017-1026`, `:305-315` in `admins.py`.
- The profile toggle writes the **target admin's** `notify_requests` flag, but
  `_submit_request` gates on `get_admin_notify_requests(channel, owner)` — the **owner's**
  own flag, which no UI can ever change (owner profiles hide the toggle, `:445-461`).
  So the flag is always default-True: muting admin X changes nothing, requests from X
  still ping the owner, and the `chadm_request_sent_owner_off` receipt is unreachable.
- Impact: documented feature ("owner can switch off request notifications for a specific
  admin") does nothing. Fix: check the *requester's* flag at `:1057`.

### M2 (MEDIUM) — owner request DM is localized in the requester's language
- File: `src/callbacks/channel_admins.py:1058-1066` (`_submit_request`).
- `t(user_id, 'chadm_owner_request_notify', …)` and the Yes/No button labels use
  `user_id` = the requester, but the message is sent to the owner (`:1069`).
  Every other notifier in the file correctly uses the recipient (`target_uid` at
  `:1086`, `:1098`, `:1111`, `:1120`, `:1137`).
- Impact: owner with a different language gets a foreign-language approval prompt.
  Fix: use `t(owner, …)` for text + buttons.

### M3 (MEDIUM) — `chadm_request_not_pending` missing in RU → raw key to RU owners
- File: `translations/ru.json` (absent; present in EN) ← `channel_admins.py:910`.
- RU owner tapping a stale/already-resolved Yes button sees the literal key instead of
  the "no longer pending" notice. `t()` has no key-missing fallback beyond EN
  (`i18n.py:142-160`). Fix: add the RU string.

### L1 (LOW) — restore is silent: revoked admin is never told they were restored
- File: `src/callbacks/channel_admins.py:512-535` (`chadm_restore_`).
- Removal pushes `_notify_admin_removed` (`:668`); restore only edits the *owner's*
  message (`:530-534`). The restored admin finds out by accident.
- Fix: send a push (e.g. reuse `chadm_restored`-family text) to `target_uid`.

### L2 (LOW) — restore-grant notice reads "You can now manage for channel …"
- File: `channel_admins.py:921/1137` + `PERM_LABEL_KEYS` (no `'manage'` entry).
- `_perm_label(t,'manage')` → `t(target,'manage')` → `en['manage']` is a dict without
  `btn`/`button`, so `_resolve` returns None → raw `'manage'` (`i18n.py:68-100,160`;
  live-verified). Bare English word, uninflected mid-sentence, unlocalized for RU.
- Fix: dedicated label key (e.g. `chadm_perm_manage_restore`) for the `perm='manage'` path.

### L3 (LOW) — transfer expiry notifies nobody; panel-toggle block/unblock never notify
- Transfer: `get_pending_transfer` (`admins.py:704-726`) expires lazily on read; no
  message to owner or target on the 24h timeout. Both sides can wait on a dead request.
- Global block: the panel toggle (`src/callbacks/admin/users.py:438-467`) blocks *and*
  unblocks with zero user notification, unlike the conversation path
  (`handlers.py:1422-1439`) which notifies on block. Unblock never notifies on either path.
- No "unblock requested/decided" flow exists anywhere in the codebase — that scope item
  is N/A (closest analog: `chadm_request_{channel}_manage` restore-request → covered above).

### L4 (LOW) — pushes name the raw channel ID, never the channel title
- All five push helpers (`:1088`, `:1098`, `:1111`, `:1120`, `:1137-1141`) interpolate
  `escape_html(channel)` = numeric `-100…` ID, while list/profile views resolve the title
  via `get_chat` (`:339-343`, `:414-418`). Correct channel, ugly reference.
- Same for `chadm_transfer_done_owner` (`:816` names only the admin, no channel at all —
  ambiguous for multi-channel owners).

### L5 (LOW) — EN/RU transfer-phrase inconsistency; silent-failure observability
- `chadm_transfer_phrase`: EN has **no** placeholders (literal `[channel]`/`[username]`
  the user must retype, `:723-734`); RU interpolates real `{channel}`/`{username}`.
  Two different confirmation experiences per language (plus the EN phrase never names
  the actual channel — phishing-shape).
- All notify `except: pass` blocks log nothing (`:1091`, `:1104`, `:1114`, `:1129`,
  `:1145`; also `:819`, `:856`; `handlers.py:1438`). Skipped-and-invisible: fine for
  robustness, blind for ops. Consider `logger.warning` on send failure.

## Coverage matrix (event → recipients / timing / text / failure)

| Event | Recipient(s) | When | Text names right entity | Failure |
|---|---|---|---|---|
| Permission saved | target admin only (`:1080`) | immediate | channel ✓ / perms ✗ raw keys (H1) | skip silent |
| Admin removed | target only + restore btn (`:1095`) | immediate | channel ✓ | skip silent |
| Admin restored | owner receipt only (`:530`); target ✗ (L1) | immediate | admin ✓ | n/a (edit) |
| Transfer initiated | target only + accept/decline (`:1117`) + owner receipt (`:762`) | immediate | channel ID only (L4) | skip silent |
| Transfer accepted | old owner DM (`:813`) + target receipt (`:821`) | immediate | admin ✓, channel ✗ absent (L4) | skip silent |
| Transfer declined | old owner DM (`:851`) + target receipt (`:858`) | immediate | admin ✓ | skip silent |
| Transfer cancelled | target DM (`:1108`) + owner receipt (`:783`) | immediate | channel ID only (L4) | skip silent |
| Transfer expired | NOBODY (L3) | lazy on read | — | — |
| Permission requested | owner DM + Yes/No (`:1068`); gated by wrong flag (M1), wrong lang (M2), raw perm (H1) | immediate | user ✓ / perm ✗ / channel ✓ | tracked, alt receipt ✓ |
| Permission approved | target DM (`:1137`) + owner receipt (`:938`) | immediate | perm ✗ raw key (H1); `manage` ✗ (L2) | skip silent |
| Permission denied | target DM + optional reply (`:1140`) + owner receipt (`:985`) | immediate | perm ✗ raw key (H1) | skip silent |
| Restore requested/decided | = permission-requested/approved rows with `perm='manage'` | immediate | "manage" (L2) | same |
| Auto-revoke on sync (TG removal / lost post / deleted acct) | NOBODY (silent by design) | on next sync/check | — | n/a |
| New admin synced | NOBODY (silent) | on sync | — | n/a |
| Notify-toggle changed | owner-only re-render, no push | immediate | — | n/a |
| Global block (conv) | blocked user DM + admin receipt (`handlers.py:1422-1451`) | immediate | reason ✓ | tracked ✓ |
| Global block/unblock (panel toggle) | NOBODY (`users.py:438-467`) (L3) | immediate | — | n/a |
| Non-involved users | receive nothing in all paths | — | — | — |

## Notes
- `chadm_transfer_confirm_warning` exists in EN but is referenced nowhere in `src/` (dead key;
  also absent in RU) — trivia, safe to delete or wire up.
- `chadm_awaiting_*` / `chadm_draft` / `chadm_pending_request` look like missing keys in the
  audit script output but are `context.user_data` state keys, not translation keys — not bugs.
- Sync auto-revoke and silent expiry are arguably by design; listed as gaps so owners can decide.
