# Ownership Transfer — Audit Report (Agent 3/8)

Scope: full ownership-transfer flow (initiate → phrase → pending → accept/decline/timeout/cancel),
what changes on accept, edge cases, notifications. READ-ONLY audit; no `src/` edits.

Core files:
- `src/channels/admins.py` — `get/create/cancel/accept` pending transfers, `transfer_ownership` wrapper,
  `sync_channel_admins` (creator-wins), TTL = 24h (`TRANSFER_TTL_HOURS`, line 149)
- `src/callbacks/channel_admins.py` — `chadm_makeowner_*`, `chadm_transfer_confirm_*`,
  `chadm_transfer_cancel_*`, `chadm_transfer_accept_*`, `chadm_transfer_decline_*`,
  `chadm_text_handler` (phrase), `_notify_transfer_target/_notify_transfer_cancelled`
- `src/services/periodic.py:677-705` — hourly expired-transfer sweep
- `src/callbacks/channels.py:1096-1100,1175-1180` — owner-disconnect wipes `pending_transfers`
- `src/register.py:769-779` — text-handler wiring

Reference behavior (verified working, in-memory + `tests/channel_admins/sim_transfer_flow.py` 12/12 pass):
- Initiation is owner-only at every step (`chadm_makeowner_`, phrase-match, `chadm_transfer_confirm_`,
  `chadm_transfer_cancel_` all compare presser to `get_channel_owner`; non-owner gets `chadm_owner_only` alert).
- Target must already be a bot-side admin (`chadm_admin_not_found`) AND pass a live
  `recheck_channel_member` (Telegram admin + `can_post_messages`), checked at makeowner, confirm, AND accept.
- Transfer to self blocked at entry (`chadm_makeowner_`, `src/channels/admins.py:850-851`).
- `transfer_ownership()` API wrapper blocks self / non-owner initiator / non-admin stranger (verified `False` for all three).
- Accept/decline verify presser == `transfer.target_id` (`chadm_transfer_not_for_you` otherwise) — third parties can't steal/decline.
- Double-initiation via UI is gated (`chadm_transfer_pending_exists` at makeowner + phrase-match branches).
- Cancel is owner-only, clears pending, edits owner screen to `chadm_transfer_cancelled`, DMs target `chadm_transfer_offer_cancelled`.
- 24h TTL enforced lazily on every read (`get_pending_transfer`) + hourly sweep; expired accept/decline
  yields `chadm_transfer_expired` alert; `accept_transfer`/`decline_transfer` return `False` with no pending.
- Old owner demoted to regular admin WITH all permissions forced `True` (not removed) — matches docstring + owner DM text.
- Notifications use each recipient's own language (`t(old_owner, …)` / `t(target, …)`); offer DM carries working
  accept/decline buttons; audit log entry written on accept (`audit_log['ownership_transfers']`).
- Expiry label on the created screen is rendered in the channel timezone (sim-verified, Asia/Tokyo case).

---

## BUG 1 (HIGH): `sync_channel_admins` creator-wins silently REVERTS every bot-side transfer

- Location: `src/channels/admins.py:431-436`
- Proof (read-only repro, temp script, real functions): `accept_ownership_transfer('@c','2')` → owner `2`;
  one `sync_channel_admins` with Telegram creator still `1` → owner flips back to `1` (`rec1=True rec2=False`).
- Why it always fires: a bot-side transfer never changes the Telegram channel creator, but the sync block
  `record['is_owner'] = (uid == creator_uid)` runs on EVERY successful sync and the old-owner record always
  still exists (accept demotes, never removes). Next trigger — `periodic_admin_sync`, opening the admins list
  (`_render_admins_list` syncs first, `src/callbacks/channel_admins.py:307`), or any owner-action re-check —
  undoes the transfer. The feature is durable only when Telegram ownership was ALREADY moved (in which case the
  sync alone would have done the job anyway).
- Impact: ownership transfer appears to succeed (both parties notified) then silently reverts; new owner loses
  Admins-section access, old owner regains it. Data integrity + trust issue.
- Fix direction (not applied): after a bot-side transfer, either exempt the channel from creator-wins until the
  Telegram creator actually changes, or record a `bot_transferred_at`/`bot_owner_override` flag that creator-wins
  must respect (clear it when `creator_uid == rbac_owner` again).

## BUG 2 (MEDIUM): English transfer phrase template never interpolates — `translations/en.json:5652`

- `en.json:5652`: `"I confirm that I transfer management of [channel] to [username]"` (square brackets).
  Every other transfer string uses `{placeholders}`; `ru.json:164` correctly uses `{channel}`/`{username}`.
- Verified: `t('1','chadm_transfer_phrase', channel='MyChan', username='Bob')` →
  `'I confirm that I transfer management of [channel] to [username]'` (literal brackets).
- Impact: English owners see uninterpolated placeholders and must retype a phrase containing literal
  `[channel]`/`[username]`; confusing, looks broken (ru users unaffected). Functional only via exact copy-paste.
- Fix direction: change to `"I confirm that I transfer management of {channel} to {username}"`.

## BUG 3 (MEDIUM): accept does not re-validate `transfer.owner_id == current owner` → dual-owner corruption

- Location: `src/channels/admins.py:755-791` (`accept_ownership_transfer` demotes `transfer['owner_id']`,
  promotes target, never asserts the stored owner is still the owner).
- Trigger: anything that moves RBAC ownership mid-pending (BUG 1's sync-revert is the ready-made trigger:
  A opens pending→B, sync flips owner to Telegram creator C, B accepts → A demoted (no-op), B promoted
  while C stays owner → TWO `is_owner=True` records; `get_channel_owner` returns whichever iterates first).
- Impact: split-brain owner state; owner-only gates answer to the wrong user nondeterministically.
- Fix direction: in `accept_ownership_transfer`, abort (`ValueError`) unless
  `str(transfer['owner_id']) == str(get_channel_owner(channel_id))`; decline/cancel paths should likewise
  address the CURRENT owner, not the stale `transfer['owner_id']`, when notifying.

## BUG 4 (MEDIUM): accept path destroys a valid pending request on TRANSIENT Telegram failure (H13 violation)

- Location: `src/callbacks/channel_admins.py:799-804`. On `recheck_channel_member` failure it does
  `cancel_pending_transfer(channel)` whether `ok` is True (genuine) or False (transient).
  Every sibling path (perm-save `595-606`, request-grant `927-934`, `_recheck_or_deny` `204-226`) distinguishes
  `ok` and preserves state on transient errors; the inline comment even cites the principle.
- Impact: one network hiccup when the target taps Accept permanently kills the request; owner is NOT notified
  (no DM on this branch) so nobody learns why it vanished. Owner must redo phrase + confirm.
- Fix direction: only `cancel_pending_transfer` when `ok` is True; on `ok == False` answer
  `chadm_verify_failed` and keep pending.

## BUG 5 (MEDIUM): accept reassigns RBAC ONLY — connections, default channel, jobs stay with the old owner

- Location: `src/channels/admins.py:755-791` (only `channel_admins` touched; verified in-memory:
  after accept, `user_channels['1']` unchanged, `user_channels.get('2')` still `None`,
  `get_default_channel('1')` still the channel, `get_default_channel('2')` `None`,
  scheduled/recurring indexes — keyed by creator `user_id` (`src/core/botdata.py:660-669`) — untouched).
- Impact: new owner may not see the channel in their connected-channels list / has no default channel or
  sender-bot binding for it; `_render_profile` stats (`channel_admins.py:421-430`, indexed by creator id)
  show 0 jobs for the new owner while the demoted owner retains visibility/control of jobs they created.
  Per-channel quota/premium are unaffected (shared counters; `get_channel_premium` is any-admin), so this is a
  management-continuity gap, not a quota bypass. If RBAC-only transfer is intentional, it should be documented
  in the transfer UI/audit log; otherwise reassign `user_channels`, default channel, bot binding, and job indexes.
- Note: new owner's stored `permissions` dict is left as-is (limited defaults) — harmless today because
  `has_channel_permission` short-circuits on `is_owner`, but a later demotion would resurrect stale limited flags.

## BUG 6 (LOW-MEDIUM): no blocked-user gate anywhere in the transfer flow

- `is_user_blocked` (`src/services/models.py:50`) is never consulted at makeowner / confirm / accept
  (grep over `src/callbacks/channel_admins.py` transfer handlers: zero hits).
- Impact: a globally bot-blocked user can be offered AND can accept Main Ownership of a channel
  (moderation bypass; offer/accept DMs still deliver since sends swallow exceptions silently).
- Fix direction: deny makeowner/confirm when target `is_user_blocked`, and re-check at accept
  (cancel pending + notify owner if the target was blocked mid-flight).

## BUG 7 (LOW-MEDIUM): `chadm_transfer_confirm_` silently OVERWRITES an existing pending (double-transfer race)

- Location: `src/callbacks/channel_admins.py:741-769` — no `get_pending_transfer` guard before
  `create_pending_transfer` (whose docstring even says "replaces any previous", `admins.py:731`).
  The UI gate only lives in the makeowner/phrase steps, but a second completed phrase flow (different target,
  different device/session sharing one `user_data`… or two phrase flags raced) reaches confirm unblocked.
- Impact: first target's accept/decline buttons die with `chadm_transfer_mismatch`/`chadm_transfer_not_for_you`
  and no explanation; first target is never told they were superseded.
- Fix direction: mirror the makeowner guard in confirm (answer `chadm_transfer_pending_exists` when a live
  pending exists for another target).

## BUG 8 (LOW): expiry is silent on both sides + dead buttons linger

- Expired transfers vanish lazily (`get_pending_transfer`) or in the hourly sweep with zero DMs;
  no `chadm_transfer_expired_notify`-style message exists in either locale.
- The target's offer DM keeps live-looking Accept/Decline buttons that only produce an alert when tapped;
  the admins list (`_render_admins_list`, `channel_admins.py:291-391`) shows no pending-transfer indicator,
  so a forgetful owner discovers the state only by retrying makeowner.
- Impact: UX confusion only; no integrity issue. Consider owner+target expiry notices and a pending line/row
  in the admins list with cancel affordance.

## BUG 9 (LOW): hourly sweep mishandles naive `expires_at` (diverges from the lazy reader)

- `src/services/periodic.py:693-697` compares parsed `expires` directly to aware `now`; a naive stored value
  raises `TypeError`, which escapes the per-channel handling into the outer `except` and aborts that sweep
  iteration (logged, not retried for an hour). `get_pending_transfer` (`admins.py:710-725`) explicitly
  normalizes naive vs aware. Normal creation always writes aware ISO, so this bites only legacy/hand-written
  rows — robustness-only finding.
- Fix direction: replicate the lazy reader's tz normalization in the sweep (and `continue`, never abort the loop).

## BUG 10 (LOW): `confirm` path missing defense-in-depth self-check; misc small gaps

- `chadm_transfer_confirm_{channel}_{own_uid}` invoked directly (replayed/tampered callback) passes the
  owner check (presser IS owner) and the live-admin check (creator always passes) and mints a pending
  transfer to self; accept then becomes a confusing no-op round-trip with real notifications. Re-check
  `target != owner` in confirm (makeowner already does).
- Phrase flag is single-slot per user (`user_data['chadm_awaiting_phrase']`): starting makeowner for channel B
  while channel A's phrase is unsubmitted orphans flow A (its phrase then fails with `chadm_phrase_wrong`).
  Key the flag by channel.
- Makeowner/confirm treat transient live-check failure (`ok=False`) as "target not admin" with no
  `chadm_verify_failed` distinction (perm-save path has one) — fail-closed, so safe, but inconsistent and
  retry-hostile.
- Decline/accept-failure notify the STALE `transfer['owner_id']` rather than the current owner (matters once
  BUG 3's staleness is possible); nothing is audit-logged for decline/cancel/expiry (accept only).

## Edge cases explicitly checked — CLEAN

- Transfer to non-admin stranger: blocked (`chadm_admin_not_found` + live recheck; API wrapper `False`). ✔
- Transfer to self: blocked at entry + API. ✔ (only direct-callback confirm replay, BUG 10, slips through)
- Non-owner initiates/cancels: blocked with alert at every handler; sim asserts non-owner cancel alert. ✔
- Second request while first pending: blocked at makeowner + phrase-match; only the confirm handler lacks the guard (BUG 7).
- Owner cancel: works, both sides informed (sim-verified). Target cannot cancel, only decline — correct.
- Target never responds: bounded 24h state, lazy + swept cleanup, safe expired alerts — silent but bounded (BUG 8).
- Expiry/free-limit interplay: NO interplay by design — transfer consults neither `has_premium`, `get_user_limit`,
  nor premium-expiry; safe because limits are per-channel shared and premium is any-admin channel-scoped.
  A transfer can therefore never grant quota the channel didn't already have, nor strand quota. ✔
- Owner disconnect wipes `pending_transfers` + RBAC (`channels.py:1096-1101,1175-1180`) — no orphaned pending. ✔
- Concurrent accepts serialized under `BOT_DATA_LOCK`; second accept raises `ValueError` → mismatch alert. ✔
- Deleted/deactivated targets: live recheck blocks initiation; accept-time recheck + cancel covers mid-flight departure. ✔
  (Revoked-list targets correctly yield `chadm_admin_not_found` since they have no record.)
- `transfer_ownership()` sync wrapper: owner/self/admin checks all verified `False` on violation. Note it
  create-then-immediately-accepts, so it shares BUG 1 (revert on next sync) and BUG 5 (RBAC-only).

## Test/verification log (read-only)

- `python tests/channel_admins/sim_transfer_flow.py` → 12/12 pass (offer, tz-correct expiry, cancel + target notice, non-owner cancel blocked).
- `pytest tests/ -k transfer` → 3 passed (transfer-flow sim ×2 harnesses + display-normalization receipt test).
- `pytest tests/unit/test_channel_admins_comprehensive.py` → collects 0 (module holds helpers, no `test_*` funcs) — coverage gap, not a code bug.
- In-memory probes (temp `DATA_DIR`, no `src/` writes): self/stranger/non-owner API denials; double-`create_pending_transfer`
  overwrite; cancel-again `False`; accept/decline with no pending `False`; RBAC-only accept (connections/default/jobs untouched);
  sync-revert proof (owner `2` → `1` after one `sync_channel_admins`); en phrase literal-bracket rendering.

Verdict: flow control, gating, and notifications are solid; durability (BUG 1) + accept-time reassignment scope (BUG 5)
+ en phrase text (BUG 2) are the items that matter.
