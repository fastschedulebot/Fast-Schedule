# Audit 04 — Permission Requests (request → approve/deny)

Scope: non-privileged user requests a channel permission (or management restoration) →
owner approve/deny. Code read-only; sims run read-only. All line refs to current tree.

Flow map (files):

- Entry: `src/callbacks/channel_admins.py:176-254` (`_recheck_or_deny`) renders
  `chadm_request_{channel}_{perm}` / `chadm_request_{channel}_manage` buttons on every
  denial screen. `src/callbacks/channels.py:569-570` adds the same restore entry.
- Start: `channel_admins.py:992-1014` (already-have guard, cooldown check, intro with
  with-message / without-message / cancel).
- Optional message: `channel_admins.py:864-880` sets `chadm_awaiting_request_msg`;
  text consumed by `chadm_text_handler` at `channel_admins.py:1200-1216`
  (60-min freshness, Cancel button beside Send).
- Submit: `_submit_request`, `channel_admins.py:1035-1077` — cooldown re-check,
  owner self-heal sync, `record_permission_request`, owner DM with
  `chadm_request_yes/no_{channel}_{uid}_{perm}` buttons (`1064-1066`), receipt to requester.
- Approve: `channel_admins.py:890-943`. Deny: `channel_admins.py:944-990`
  (two-step: `no_` → optional reply → `final_no_`).
- Result notify: `_notify_request_result`, `channel_admins.py:1132-1146`.
- Store: `src/channels/admins.py:627-698`
  (`can_request_permission` / `record_permission_request` /
  `get_pending_requests` / `resolve_permission_request`).
- Global blocked gate: `src/buttons.py:682-692` (runs before `_PREFIX_DISPATCH`,
  which routes `chadm_` at `src/buttons.py:35`).
- Cleanup sweeps: `src/services/periodic.py:677-705` (transfers only), `:708+`
  (retention: only `user_actions` + `issue_log`).
- Sims: `tests/channel_admins/sim_chadm_callbacks.py` (17 checks pass),
  `tests/channel_admins/sim_rbac.py`, `tests/unit/test_channel_admins_comprehensive.py`.

---

## Bugs / issues

### M1 — No cooldown after resolution: deny → instant re-request loop (MEDIUM)
- Where: `src/channels/admins.py:627-648` (`can_request_permission`).
- Logic: any record with `pending == False` returns `(True, None)` immediately.
  The 7-day check applies ONLY while a request is still `pending`.
- Verified read-only probe: record → resolve → `can_request_permission` returns
  `(True, None)`; stored status is `resolved`.
- Impact: after an owner denies, the requester can re-request the same permission
  instantly, forever (request → deny → request…). Each cycle costs the owner one DM.
  The grant path self-limits via the already-have guard
  (`channel_admins.py:997`), but the deny path has no back-off at all.
- Expected: denied requests should start a cooldown (e.g. reuse the 7-day window
  from resolution time) before the same user+perm may be requested again.

### M2 — Pending requests have no owner-visible inbox; receipt text is false (MEDIUM)
- Where: `get_pending_requests` defined `src/channels/admins.py:677-687` but never
  rendered in any UI (only referenced by tests). `_render_admins_list`
  (`src/callbacks/channel_admins.py:291-390`) lists admins + revoked only; the profile
  page (`393-480`) shows no pending items either.
- Mismatch: when the owner's notify flag is off or the DM send fails, the requester
  gets `chadm_request_sent_owner_off` (`translations/en.json:5684`): "…they will see
  it when they open the Admins section." There is nothing to see there — the request
  is invisible to the owner.
- Impact: requests can sit pending with neither party able to act (owner unaware,
  requester blocked by the 7-day pending cooldown per M3/M4). Combined with M3 this is
  a silent deadlock, not just a cosmetic gap.

### M3 — Pending (and resolved) requests never expire; no cleanup (MEDIUM)
- Where: store `src/channels/admins.py:651-698`; sweeps `src/services/periodic.py:677-714`.
- `periodic_transfer_cleanup` expires `pending_transfers` (24 h TTL) but nothing
  touches `permission_requests`. `periodic_data_retention` purges only `user_actions`
  + `issue_log`. `get_pending_transfer` also expires lazily on read (`admins.py:704-726`);
  `permission_requests` has no TTL, no lazy expiry, no sweep.
- Impact: (a) abandoned pendings (owner never acts, DM lost, owner changed) linger
  forever in `data/channels/permission_requests.json`; (b) the requester stays
  cooldown-blocked for 7 days on a request nobody will ever answer, with no recourse
  (see M4); (c) resolved records accumulate unbounded (minor disk growth, ever-growing
  per-channel lists scanned linearly on every request).
- Expected: TTL + periodic sweep for pendings (with requester + owner notification on
  expiry), and/or pruning of old resolved records.

### M4 — Requester cannot withdraw/cancel their own pending request (MEDIUM/LOW)
- Where: full `chadm_request_*` surface in `src/callbacks/channel_admins.py:17-20`
  has no `chadm_request_cancel/withdraw_*` path; only owner Yes/No resolves.
- Impact: mis-tapped or stale requests can only be cleared by the owner. Requester is
  stuck for the 7-day pending window. Downgraded from High only because the
  already-have/duplicate path prevents list-growth abuse; the deadlock aspect is
  covered by M2/M3, this is the missing affordance.

### M5 — No fan-out cap: one user can force N owner DMs on demand (MEDIUM)
- Where: `_submit_request` (`channel_admins.py:1035-1077`) sends one DM per request
  (`1068-1071`); cooldown is per (user, perm) independently (`admins.py:627-648`).
- Impact: with ~15 distinct permissions, a single user can generate ~15 owner DMs
  back-to-back with no batching, digest, or per-user/per-channel rate cap. Each
  request is legitimate in isolation, so the pending-duplicate suppression does not
  help. Owner-notification toggle is per-admin and defaults on.
- Expected: cap requests per user+channel per day, or batch concurrent pendings into
  one owner message.

### L1 — Owner DM rendered in the requester's language, not the owner's (LOW)
- Where: `src/callbacks/channel_admins.py:1059-1066` — `_submit_request` builds the
  owner notification with `t(user_id, …)` where `user_id` is the REQUESTER, for both
  the message text and the Yes/No button labels.
- Impact: owner whose locale differs from the requester's gets an approve/deny prompt
  (a security-sensitive decision) in a foreign language. Should be `t(owner, …)`.
- Note the result-side notify is correct (`_notify_request_result` uses
  `t(target_uid, …)`).

### L2 — Approve live-check is stricter for `manage` than for single perms (LOW)
- Where: `channel_admins.py:913-918` (`manage` restore requires `is_admin AND can_post`)
  vs `channel_admins.py:927-934` (single perm checks `not is_admin` only; `_can_post`
  is captured but ignored).
- Impact: minor inconsistency — a target who lost `can_post_messages` but is still a
  Telegram admin can be granted a single perm but not `manage` restoration. Either
  rule is defensible, but they should match; the unused `_can_post` suggests the
  `manage`-branch rule was intended for both.

### L3 — Callback approve/deny both store status `resolved`; outcome is lost (LOW)
- Where: `src/channels/admins.py:690-698` (`resolve_permission_request` sets
  `status='resolved'` unconditionally) vs the store helpers `approve_permission` /
  `deny_permission` (`967-999`) which set `'approved'` / `'denied'`.
- Impact: the callback path (the only one actually wired to the buttons) erases the
  grant/deny distinction in persisted data — audits and any future "show past
  decisions" UI cannot tell them apart. `approve_permission` / `deny_permission`
  appear unwired to the UI (dead duplication of the same logic with different
  status strings — pick one).

### L4 — Dead `chadm_pending_request` user_data key set on every request start (LOW)
- Where: set at `channel_admins.py:1004`, never read anywhere (submit reads
  `chadm_awaiting_request_msg`; grep confirms zero readers).
- Impact: harmless leftover state written per request start and never cleared
  (overwritten next time). Clean up to avoid confusing future maintainers.

### L5 — Blocked-user protection is UI-gate only; store + text handler unchecked (LOW)
- What holds: `src/buttons.py:682-692` rejects ALL `chadm_*` callbacks from globally
  blocked users (only language/feedback pass), so a blocked user cannot open the
  request screen or press Yes/No via the normal path. Verified by reading the gate
  order (blocked check precedes `_PREFIX_DISPATCH`).
- Gaps (defense-in-depth, not directly exploitable via stock UI):
  1. Store layer has no blocked check: `can_request_permission`,
     `record_permission_request`, and `request_permission` (`admins.py:913-926`)
     accept blocked user_ids.
  2. `chadm_text_handler` (`channel_admins.py:1153+`, group −6, runs BEFORE the
     buttons dispatcher) has no `is_user_blocked` check — a request-message or
     deny-reply flag planted before the block can still be advanced by text.
  3. A request pending when its author is blocked stays pending AND grantable;
     granting succeeds and writes a permission a blocked user cannot currently use
     (gate still blocks them) — stale grant with no cleanup on block/unblock.
- Expected: mirror the blocked check in `chadm_text_handler` and
  `can_request_permission`, and resolve/withdraw a blocked user's pendings on block.

### I1 — Owner notify toggle has no UI for the owner themself (INFO)
- Where: submit consults `get_admin_notify_requests(channel, owner)`
  (`channel_admins.py:1057`); the profile page only renders the 🔔 toggle for
  non-owner admins (`456-461`; owner branch `445-446` shows "full access", no toggle).
- Impact: the `chadm_request_sent_owner_off` receipt path is nearly unreachable via
  UI (owner flag defaults `True` in `ensure_admin_record`, `admins.py:206-227`, and
  nothing lets the owner flip their own). Either expose the toggle on the owner's own
  record view or drop the flag check for owners. Not a bug in enforcement, just dead
  flexibility that makes M2's receipt path misleading.

---

## What works (verified)

- Entry points: every `_recheck_or_deny` denial renders a working request/restore
  button (`channel_admins.py:176-254`); removed-admin notice offers restore with a
  working button (`1095-1105`).
- Guards at start: owner/already-have short-circuits with alerts (`996-999`);
  pending-duplicate suppression updates the existing record in place instead of
  growing the list (`admins.py:657-664`).
- Double-submit safe: two rapid `send_` taps collapse into one pending record;
  double owner Yes/No on a resolved request yields `chadm_request_not_pending`
  instead of granting (M26 check at `900-911`, H15 owner re-check at `974-977`).
- Owner-only enforcement on `yes_`, `no_`, and `final_no_` (`896-899`, `950-953`,
  `974-977`); non-owner taps get `chadm_owner_only` alerts.
- Live Telegram revalidation before granting on both branches, with transient-failure
  protection (never revokes/resolves on `ok == False`; `913-934`). Matches the H13
  pattern used elsewhere.
- Grant effective immediately: `set_admin_permissions` merges `{perm: True}` then
  `save_all`, `resolve_permission_request`, notify (`935-942`); `manage` restore
  re-adds with defaults (`919-922`). `has_channel_permission` reads the same store.
- Requester notified on BOTH outcomes with correct locale, including the owner's
  optional deny-reply text (`1132-1146`, `983-984`); owner gets requester's optional
  message quoted in the DM (`1059-1063`).
- Deny flow is two-step with optional reply and explicit Skip/final-deny
  (`944-990`); sim confirms both branches resolve the pending record.
- Anti-replay/parse: `_split_channel_perm` handles perms containing underscores
  (H10, `98-108`); channel+uid split via `rpartition` verified by sim on a channel
  name containing `_` (`@my_ch`).
- Stale-input hygiene: 60-min freshness on all three text flags + clearing on
  unrelated callbacks (M27, `111-120`, `498-504`, `1162-1221`).
- Transfer-adjacent paths (out of scope but adjacent): 24 h TTL with lazy + hourly
  sweep expiry, owner-cancel notifies target, accept/decline notify the other party
  (`771-859`, `1108-1129`, `periodic.py:677-705`).
- Sims green: `sim_chadm_callbacks.py` — all 17 checks pass (request → notify →
  grant-parse → deny-prompt → final-deny → cancel buttons → self-heal); `sim_rbac.py`
  cooldown/record/resolve checks pass.

---

## Fix priority

1. M1 (deny cooldown) + M5 (fan-out cap) — one anti-abuse pass over
   `can_request_permission` (add post-resolution cooldown + per-user/channel daily cap).
2. M2 (pending inbox in Admins section) + I1 — render `get_pending_requests` in
   `_render_admins_list`/profile so the "owner off" receipt is true and DMs are not
   the only channel.
3. M3 (TTL/sweep for pendings + prune resolved) + M4 (requester withdraw button).
4. L1–L5, I1 as opportunistic fixes (locale arg, `_can_post` consistency, status
   strings, dead key, blocked checks in text handler + store).
