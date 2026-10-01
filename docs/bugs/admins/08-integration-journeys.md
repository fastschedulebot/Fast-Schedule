# 08 — End-to-End Integration Journeys (channel-admin RBAC)

Scope: full walk-throughs J1–J6 + disconnect cleanup + `/start` deep-links.
Method: code reads (read-only) + executed existing sims with `PYTHONUTF8=1`
(`sim_rbac`, `sim_chadm_callbacks`, `sim_transfer_flow`, `sim_revoke_restore`,
`sim_self_heal`, `sim_periodic_sync`) + one live probe of
`has_channel_permission` / `can_schedule_more` / `get_user_limit`.
No `src/` file was edited.

## Sim results (this audit run)

- `sim_chadm_callbacks.py` — **17/17 pass**.
- `sim_transfer_flow.py` — **12/12 pass**.
- `sim_revoke_restore.py` — **16/16 pass**.
- `sim_self_heal.py` — **18/18 pass**.
- `sim_periodic_sync.py` — **8/8 pass**.
- `sim_rbac.py` — **FAILS partway** (assertion `26th pending still allowed,
  limit==inf`, see F6). Checks before the abort pass (owner/admin defaults,
  perm grant/revoke); everything after the abort (premium, cooldown, transfer,
  revoke-on-sync) does **not** run in a fresh run. The transfer/revoke logic
  itself is covered green by the other sims above.
- `tests/unit/test_channel_admins_comprehensive.py`,
  `tests/unit/test_callbacks_channel_admins.py` — read, not re-run (unit-level;
  callback tests swallow all exceptions with bare `except: pass`, so they
  assert almost nothing — see N1).

---

## What genuinely works end-to-end

- **J3 (request → approve / deny):** fully working. Request intro → optional
  message → owner notify with Yes/No (`src/callbacks/channel_admins.py:992-1014`,
  `_submit_request` at `:1035-1077`) → grant sets the flag + notifies
  (`:912-943`) → deny collects optional reply and notifies (`:944-990`,
  `_notify_request_result` at `:1132-1146`). 7-day anti-spam cooldown
  (`src/channels/admins.py:627-648`) enforced. Proven by 17/17
  `sim_chadm_callbacks` checks.
- **J2 transfer handshake:** phrase → pending (24 h TTL) → accept/decline with
  both-side notifies, cancel-with-notify, expiry auto-purge
  (`src/channels/admins.py:704-791`, callbacks `:695-859`). Atomic under
  `BOT_DATA_LOCK`; old owner keeps full perms (`admins.py:776-779`). Proven by
  12/12 `sim_transfer_flow` + transfer section of `sim_rbac` logic.
- **J4 block → callback denial:** blocked user's button presses are stopped
  with `blocked_alert` + reason in `src/buttons.py:682-692`; admin block DMs
  the user (`src/admin/handlers.py:1430`); block strips premium immediately
  (`src/services/models.py:54-76`).
- **Revocation stickiness + self-heal + periodic sweep:** revoked admins are
  not re-added by sync, deleted accounts auto-revoked, restore works,
  empty-store owner self-heals, background sweep drops Telegram-removed
  admins (16/16 + 18/18 + 8/8 green).
- **Per-channel premium:** `get_channel_premium` (`src/channels/admins.py:461-470`)
  returns True when ANY channel admin has premium; limits resolve per channel
  (`get_channel_limit`, `:887-910`). Conceptually correct for J6.
- **Owner-disconnect RBAC wipe:** disconnecting owner pops the whole channel
  store + pending transfers (`src/callbacks/channels.py:1094-1101`,
  duplicated at `:1175-1181`).

---

## Bugs / mismatches found

### B1 — CRITICAL — `msg_list_menu` RBAC gate uses a permission key that can never be True
- **File:** `src/callbacks/scheduler.py:1055`
- **Journey step broken:** J1 (co-admin opens message list), J5 (any co-admin list access).
- Code passes the literal `'manage_messages'` to `_recheck_or_deny`, but
  `'manage_messages'` is a UI *group* name, not a member of
  `CHANNEL_PERMISSIONS` (`src/channels/admins.py:46-62`). `has_channel_permission`
  (`:331-339`) does a direct dict lookup with no legacy/group resolution, so it
  returns `False` for every non-owner, always. Live probe this audit:
  `has_channel_permission('2','@ch','manage_messages') == False` even with
  defaults granting every sub-permission.
- **Impact:** NO co-admin (however fully permissioned) can open the message
  list on a sender bot — always denied with the no-permission screen. Owners
  pass only via the `is_owner` early-return.
- Should be `message_list` (or any-of the six `message_*` flags).

### B2 — CRITICAL — sender-bot main-menu RBAC filter uses three legacy keys, hiding buttons from ALL co-admins
- **File:** `src/keyboards.py:251-258` (`BUTTON_PERM`), consumed at `:285-299`.
- `'msg_list_menu': 'manage_messages'`, `'statistics': 'statistics'`,
  `'export_menu': 'export'` — none of these exist in `CHANNEL_PERMISSIONS`;
  probe returns `False/False/False` for a default admin. Only `schedule`,
  `recurring`, `calendar_view→schedule` filter correctly.
- **Journey step broken:** J5 — a fully-permissioned co-admin never sees
  Message-list / Statistics / Export buttons; an admin explicitly granted
  `data_export` still doesn't see Export.
- `LEGACY_PERM_MAP` (`src/channels/admins.py:140-145`) maps exactly these
  three group names to real flags but is **never consumed anywhere**
  (repo-wide grep: only the definition). Dead code that looks like the fix
  but isn't wired in.

### B3 — CRITICAL — delete (and preview/info/edit scoping) is creator-ownership, not RBAC: J1's final step and J2 management cannot work cross-admin
- **Files:** `src/callbacks/scheduler.py:1091-1131` (`del_confirm_`),
  `:1147-1164` (`msg_info_`), list builders at `:1285-1308, :1419-1440`
  (iterate `bot_data.get_user_scheduled_ids(user_id)` /
  `get_user_recurring_ids(user_id)` — own jobs only).
- `del_confirm_` requires `_job.get('user_id') == user_id`; there is **no**
  `has_channel_permission(..., 'message_delete')` check anywhere on the
  `del_` / `del_confirm_` path, and `del_` (`:1133-1145`) has no gate at all.
- **Journey steps broken:**
  - J1: "owner upgrades to full → delete works" — FALSE for any job the
    co-admin didn't create themselves: result is `not_found`, not a delete,
    regardless of `message_delete=True`. And the J1 middle step ("recurring
    delete is denied") produces `not_found` instead of the permission-denied +
    request-permission screen, so the denial never offers the request path.
  - J2: "pending jobs keep working" is half-true — already-scheduled sends
    still fire (dispatch is channel-keyed), but the new owner can neither see
    nor delete the old owner's pending jobs (per-creator list scoping), so
    ownership transfer does not transfer *management* of in-flight jobs.
- Note the inconsistency: `FEATURE_PERMISSION` (`admins.py:125-126`) correctly
  maps `delete_scheduled`/`delete_recurring` → `message_delete`, but the
  actual delete handler never consults it.

### B4 — HIGH — blocked users are gated on callbacks only; all text-driven admin actions bypass the block
- **File (gate):** `src/buttons.py:682-692`. **Missing from:**
  `src/handlers/schedule_conv.py` (grep for `is_user_blocked`/`blocked`: only
  an unrelated "bot was blocked" string at `:261`), `chadm_text_handler`
  (`src/callbacks/channel_admins.py:1153-1235`), and every sender-bot message
  handler.
- **Journey step broken:** J4 "admin's next action denied with blocked
  message" — true only if the next action is a *button*. If the blocked
  mid-session admin types schedule content, a transfer phrase, a permission-
  request message, or a deny reply, the text is processed normally.
- Companion gap: **no unblock-request flow exists at all** (repo-wide grep for
  `unblock_request|request_unblock`: zero hits). J4's "blocked + unblock
  request offered (if enabled)" has no backing code — blocked users get only
  the alert. Also `unblock_user` (`src/services/models.py:94-97`) does not
  restore the premium stripped at block time (`:68-73`) — unblocked admin
  silently returns as a free user.

### B5 — HIGH — freeze is per-user and invisible to RBAC: frozen owner keeps full management power; co-admin experience is accidental
- `_recheck_or_deny` (`src/callbacks/channel_admins.py:123-254`) never checks
  `is_channel_frozen` / `is_premium_expiry_active`. Freeze is enforced only at
  send dispatch (`src/scheduler/helpers.py:347-348, 681-689`) and by bot-
  username matching in `src/services/frozen_bot_gate.py:42-62`.
- **Journey step broken (J6):** a frozen (lapsed, non-kept-channel) owner can
  still schedule/create/recurring/grant through the sender bot — actions pass
  RBAC and only die (or not) at fire time. Conversely nothing tells the
  frozen admin their channel is frozen at action time.
- Per-channel premium (`get_channel_premium`) correctly keeps a co-admin's
  premium covering the channel, but `is_channel_frozen(owner, ch)` is still
  True for the lapsed owner while False for the premium co-admin on the SAME
  channel — the "frozen channel" is not a channel property at all. No crash,
  but the J6 mental model ("frozen channel admin actions") does not match the
  implementation.

### B6 — MEDIUM — `sim_rbac.py` is stale and aborts mid-suite, hiding its own premium/transfer coverage
- **File:** `tests/channel_admins/sim_rbac.py:129-136`.
- Comment claims daily caps "DISABLED … limit=inf", but code enforces the free
  `scheduled_messages` cap of 100 (live probe: `can_schedule_more` →
  `(True, 5, 100)`; `get_user_limit('3','scheduled_messages') == 100`). The
  assertion `limit == float('inf')` fails and the sim **aborts before** the
  premium, cooldown, transfer, and sync sections. Those areas are covered by
  other sims, but `sim_rbac.py` as the flagship RBAC suite is red and its most
  integration-relevant half never executes.

### B7 — MEDIUM — disconnect/deleted-channel cleanup leaves stale RBAC-adjacent state; dead channels are never purged
- Owner disconnect wipes `channel_admins` + `pending_transfers` but leaves
  `permission_requests`, `channel_revoked`, and `channel_limits` behind
  (`src/callbacks/channels.py:1096-1101`). A later re-connect inherits stale
  cooldowns/revocation entries (a previously revoked user stays revoked
  silently; old 7-day cooldowns still throttle).
- If the bot loses channel access (kicked, channel deleted),
  `sync_channel_admins` soft-fails and returns the **stale** list
  (`src/channels/admins.py:390-391`) — by design for transient safety, but no
  other path ever deletes a dead channel's store, so `channel_admins` grows
  orphan entries forever. `periodic_admin_sync` skips channels without a
  store but never removes stores for dead channels (verified in
  `sim_periodic_sync.py`, which only asserts the skip).

### B8 — MEDIUM — no `/start` deep-link into any admin flow; feature deep-links land in the same broken gates
- `_SENDER_BOT_FEATURE_ROUTE` (`src/handlers/commands.py:62-97`) has entries
  for schedule/recurring/stats/search/export/list/… but **no `chadm_*` /
  admin route**; repo-wide grep for `start.*chadm|chadm.*start|deep_link.*chadm`
  is empty. An invited co-admin has no linkable path to the Admins section or
  to a pending request/transfer — everything requires menu navigation on the
  correct sender bot.
- The invite-adjacent deep-links that do exist (`sc_`, `rc_`, `cal_`,
  `lst_`, `srch_` at `commands.py:714-832`, sender-bot redirect at
  `src/services/sender_bot_gate.py:200-234`) funnel into the B1/B2-gated
  handlers, so a schedule-only admin arriving via `?start=schedule` works,
  but one arriving via list/stats/export deep-links hits the always-deny
  (B1) or invisible-button (B2) dead ends.

### B9 — LOW — management-menu text renders in the owner's language, not the acting admin's
- **File:** `src/callbacks/channels.py:559-572` — `t(rbac_owner, ...)` used for
  title, body, and buttons even when the viewer is a co-admin. A Russian
  co-admin opening the management menu on an English owner's channel gets
  English. Should be `t(user_id, ...)` (the channel link itself is
  language-neutral).

### N1 — NOTE (test quality, not product): callback unit tests assert almost nothing
- `tests/unit/test_callbacks_channel_admins.py`: every handler invocation is
  wrapped in `try/except Exception: pass`, so a handler that raises, renders
  nothing, or takes the wrong branch still passes. The hermetic sims (which
  assert on edited text/buttons/store state) are the real coverage; the unit
  file gives false confidence. Not counted as a product bug.

---

## Journey verdicts

| Journey | Verdict | Breaking issue |
|---|---|---|
| J1 invite → schedule-only → denied recurring-delete → upgrade → delete | **BROKEN** (middle step degrades, final step fails) | B3 (upgrade never enables deleting others' jobs; denial is `not_found`, no request path); B1 blocks reaching the list at all |
| J2 transfer → old loses / new gains; jobs keep working | **PARTLY BROKEN** | Ownership flags transfer correctly, but job *management* doesn't follow the crown (B3); sends still fire |
| J3 stranger request → approve acts / second denied | **WORKS** | — (17/17 sim green) |
| J4 block mid-session → denied → reconnect → unblock → works | **PARTLY BROKEN** | Text actions bypass block; no unblock-request flow (B4) |
| J5 sender-bot channel, two admins, per-admin menu filtering | **BROKEN** | B2 (three buttons hidden from every co-admin); B1; B9 cosmetic |
| J6 expiry/freeze + per-channel premium | **DEGRADED** | B5 (frozen owner still manages; freeze not channel-scoped); premium-sharing itself works |
| Disconnect / deleted-channel cleanup | **DEGRADED** | B7 (leftover requests/revoked/limits; orphans never purged) |
| `/start` deep-links into admin flows | **MISSING** | B8 (no admin deep-link route) |

## Counts

- Bugs: **9** (3 critical, 2 high, 3 medium, 1 low) + 1 test-quality note.
- Sims run: 6 (5 fully green: 17+12+16+18+8 checks; 1 stale-aborted: `sim_rbac`).
- Clean areas: J3 fully; J2 handshake mechanics; revocation/self-heal/sweep;
  per-channel premium resolution; owner-disconnect wipe.
