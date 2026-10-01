# 05 — Per-Admin Stats (Admin Profile Statistics) — Audit Report

**Scope:** Agent 5/8 — PER-ADMIN STATS. Admin profile/stats view: scheduled/recurring
counts per admin per channel, sent counts, stranger attribution. Staleness,
performance, empty states, deleted-channel handling, timezone, privacy.

**Verdict: NOT CLEAN — 6 issues (1 high, 3 medium, 2 low) + 2 coverage gaps.**
Functionally the profile counts the right *shape* of data and privacy is
fail-closed, but one permission-key bug denies all non-owner stats access, one
type bug undercounts jobs, sent/stranger numbers are missing or misattributed,
and channel-id normalization is inconsistent.

**Method:** read-only code inspection + read-only `bash` sims (no `src/` edits).
Two sims executed:
- `has_channel_permission('111','@ch1','statistics') == False` while
  `'stats_view' == True` (default perms) — confirms Bug 1.
- `add_scheduled_message` with `user_id=222` (int) vs `'222'` (str) creates two
  index keys; `get_user_scheduled_ids('222')` returns only the str one —
  confirms Bug 2.

---

## 1. Where the view lives and what each number is

**Profile view:** `src/callbacks/channel_admins.py:393-480` (`_render_profile`).
Entry: `chadm_profile_{channel}_{uid}` → `handle` at
`src/callbacks/channel_admins.py:538-543` → `_render_profile`.

Numbers shown (and ONLY these two):
- `sched_count` — `src/callbacks/channel_admins.py:421-425`:
  ```python
  sum(1 for jid in bot_data.get_user_scheduled_ids(target_uid)
      for m in [bot_data.scheduled_messages.get(jid) or {}]
      if m.get('channel_id') == channel)
  ```
  = pending (not-yet-sent) scheduled messages authored by `target_uid` for
  exactly this `channel`.
- `rec_count` — `src/callbacks/channel_admins.py:426-430`: same over
  `bot_data.recurring_messages` = active recurring messages by that admin for
  this channel.
- Labels: `chadm_stat_scheduled` / `chadm_stat_recurring`
  (`translations/en.json`), header `chadm_stats_header` ("Statistics (this
  channel)").

**There is no sent-count and no stranger-attribution number on this profile.**
The task scope asks to verify them; they simply are not rendered here (see
Gap A / Gap B). Related but separate surfaces:
- Personal overview: `src/statistics_manager.py:390-446` (`build_stats_overview`:
  scheduled/recurring via full-scan `j.get('user_id') == user_id`, sent/created
  via `bot_data.user_stats`).
- Per-channel engagement: `src/statistics_manager.py:489-563`
  (`render_channel_stats` → `get_channel_stats(user_id, channel_id)` in
  `src/services/stats.py:691-731` + channel-wide `get_top_reactions` in
  `src/services/stats.py:489-502`).
- Channel counters shared by all admins: `get_channel_pending_scheduled_count`
  (`src/channels/admins.py:486-495`), `get_channel_recurring_count`
  (`src/channels/admins.py:550-555`), monthly/daily sent
  (`src/channels/admins.py:515-547`).

---

## 2. Bugs

### Bug 1 (HIGH) — Stats/leaderboard RBAC gate uses legacy permission keys that can never pass
- **File:line:** `src/callbacks/channels.py:327` (`'statistics'`), `:350`
  (`'leaderboard'`); gate impl `src/callbacks/channel_admins.py:123-254`
  (`_recheck_or_deny`); permission store `src/channels/admins.py:46-62`
  (`CHANNEL_PERMISSIONS` contains `stats_view` / `leaderboard_view`, NOT
  `statistics` / `leaderboard`); check `src/channels/admins.py:331-339`
  (`has_channel_permission` looks up `perms.get(perm)` → legacy key always
  `False`).
- **What happens:** any non-owner admin — even with `stats_view: True` and
  `leaderboard_view: True` — is denied `sender_bot_stats_*` / `lb_*` and shown
  the no-permission screen. Owner always passes (owner early-return at
  `channel_admins.py:189-201`), so the bug is invisible to owners/testers
  acting as owner.
- **Verified:** sim with default perms → `stats_view=True`, `statistics=False`,
  `leaderboard=False`, `leaderboard_view=False` (defaults have
  `leaderboard_view=False`, so leaderboard denial is doubly guaranteed).
- **Impact:** per-admin stats/leaderboard feature is owner-only in practice;
  granted `stats_view` permission does nothing. Privacy-safe (fail-closed) but
  functionally broken.
- **Fix hint (not applied):** pass `'stats_view'` / `'leaderboard_view'` (or
  resolve via `FEATURE_PERMISSION`, `src/channels/admins.py:117-137`, which
  already maps `'statistics'→'stats_view'`, `'lb'→'leaderboard_view'`, but the
  gate never consults it).

### Bug 2 (MEDIUM) — `int` vs `str` `user_id` splits the reverse index → profile undercounts
- **File:line:** index build `src/core/botdata.py:655-672`, add/remove
  `src/core/botdata.py:680-716` store `msg.get('user_id')` verbatim as the dict
  key; lookup `get_user_scheduled_ids(target_uid)` / `get_user_recurring_ids`
  (`:668-672`) with `target_uid: str` (`src/callbacks/channel_admins.py:410,
  422, 427`).
- **What happens:** writers store mixed types — e.g. `channels/helpers.py:439`
  `'user_id': user_id`, `handlers/recurring.py:395`, `handlers/export.py:467,
  514, 676, 1092, 1280` pass whatever caller type (`int` from
  `effective_user.id` in some flows, `str` in others). `_build_indices` then
  holds e.g. `{222: [...], '222': [...]}` as **two** keys.
- **Verified:** sim inserting `j1` with int `222` and `j2` with str `'222'` →
  `get_user_scheduled_ids('222') == ['j2']` only. Profile (always `str`) misses
  every int-stored job → shows a smaller number than the admin actually has.
- **Impact:** per-admin scheduled/recurring counts are wrong (always
  undercount, never overcount) whenever any job for that admin was stored as
  int. Multi-admin attribution is otherwise correct in shape (jobs stay under
  their author), but the totals can't be trusted until keys are normalized
  (e.g. `str(uid)` at index write + lookup).
- **Severity:** medium (data-correctness, silent).

### Bug 3 (MEDIUM) — Profile channel comparison not normalized; username-migrated channels miscount
- **File:line:** `src/callbacks/channel_admins.py:424, 429`
  (`m.get('channel_id') == channel`, no `str()`/lowercasing) vs channel-wide
  helper `src/channels/admins.py:492-495` which does
  `str(m.get('channel_id')) == str(channel_id)`, and stats layer
  `_normalize_channel_id` (`src/services/stats.py:32-64`, `@username`
  lowercase mapping).
- **What happens:** after the numeric→`@username` migration, jobs stored under
  the old numeric id don't match a profile opened with the `@username` form
  (or differ by case/`@` prefix) → count 0 or partial. Same latent issue in
  `get_channel_recurring_count` (`src/channels/admins.py:550-555`,
  `m.get('channel_id') == channel_id` without `str()`).
- **Impact:** per-admin counts silently drop to 0/partial for migrated or
  case-variant channel ids. Low frequency but total miscount when hit.
- **Severity:** medium-low → rated medium (silent wrong number).

### Bug 4 (MEDIUM) — Sent-stats attribution is per-(user, channel) but reactions/leaderboard are channel-wide; mixed in one view
- **File:line:** `src/services/stats.py:691-731` (`get_channel_stats` filters
  `WHERE user_id = ? AND channel_id = ?`); `src/services/stats.py:489-502`
  (`get_top_reactions(channel_id)` — **no** user filter);
  `src/statistics_manager.py:325-338` (`build_single_channel_stats` combines
  personal `stats` + channel-wide `reactions`); `render_channel_stats`
  `:507-512` same mix.
- **What happens:** in a multi-admin channel, admin A opening channel stats
  sees `total_messages` = only A's sends (correct per-author attribution, but
  easily misread as the channel total), while "top reactions" aggregates every
  admin's posts. The two numbers on the same screen answer different questions
  ("mine" vs "everyone's") with no label distinguishing them.
- **Impact:** misleading; co-admin contributions invisible in totals, visible
  in reactions. Either scope (mine vs channel) is defensible, but mixing them
  unlabeled is a correctness/UX bug.
- **Note:** SQLite `TEXT` affinity likely coerces int `user_id` inserts to text,
  so the SQL side is less exposed to Bug 2 than the in-memory index — but
  `record_sent_message` (`stats.py:208-222`) still doesn't `str()` explicitly,
  so don't rely on affinity.

### Bug 5 (LOW) — Profile shows pending/recurring only; sent history for that admin+channel unreachable from profile
- **File:line:** omission in `src/callbacks/channel_admins.py:432-443` (only two
  `•` lines); per-admin+channel sent query exists
  (`get_sent_messages(user_id, channel_id)` at `src/services/stats.py:368-394`,
  `get_message_stats` at `:1043-1062`) but is never called from the profile.
- **Impact:** owner auditing "what did admin X actually deliver to channel Y"
  gets pending + recurring but not delivered count. Informational gap, not a
  wrong number.

### Bug 6 (LOW) — Stale numbers for deleted/disconnected channels; deleted-admin jobs orphaned from UI
- **File:line:** profile title fetch `src/callbacks/channel_admins.py:414-418`
  falls back to raw id on `get_chat` failure and still renders counts; no
  "channel deleted/disconnected" warning; no filtering of jobs whose channel is
  gone. Deleted-user auto-revoke in list view `:313-336` + `revoke_channel_admin
  (... reason='deleted')`; profile of a revoked/missing record answers
  `chadm_admin_not_found` (`:406-409`).
- **Impact:** counts for a dead channel look live; jobs of a removed admin
  remain in `scheduled/recurring_messages` (correct — don't delete user data)
  but no UI path reaches them (only owner-visible profile, and the record is
  gone). Minor; no crash observed.

---

## 3. Stranger attribution (Gap B — missing, not miscomputed)

- Recording: `src/handlers/commands.py:219-231` (`record_stranger_visit` with
  `bot_username` + `channel_id`, but `channel_id=None` when the channel is
  hidden for privacy — attribution deliberately dropped there).
- `stranger_conversions` table has **no** `channel_id` column at all
  (`src/services/stats.py:141-148`); `record_stranger_conversion` (`:799-811`)
  stores only `bot_username`.
- Reads: `get_stranger_stats(bot_username?)` (`:814-839`) aggregates by bot
  only. Nothing maps bot→admin (`bot_tracking_secret(owner, channel, uname)` in
  `src/services/tracking.py:31-39` can recompute the triple, but no stats query
  uses it per admin).
- **Result:** no per-admin stranger numbers exist anywhere (neither profile nor
  sender-bot stats UI). A multi-admin channel cannot tell which admin's content
  drew the strangers; hidden-channel visits are unattributable by design. This
  is a scope gap, not a wrong-number bug. Privacy side is correct (hidden
  channel leaks nothing — `commands.py:225`).

---

## 4. Non-bug verification (what works)

- **Privacy / access control — PASS (fail-closed).** List
  (`channel_admins.py:304-306`) and profile (`:403-405`) both require
  `str(owner) == user_id`; every other `chadm_*` branch re-checks owner
  (`:518, 556, 581, 657, 700, 745, 897, 951, 975, 1021`). Non-admin and
  regular-admin viewers get `chadm_owner_only` alert, no data leaked.
  Consequence worth noting: a **regular admin cannot view even their own**
  profile stats — only the owner can. Admin A can never see admin B's numbers
  except via the owner. That matches "owner manages admins" design but means
  non-owners have zero self-stats for their channel work.
- **Callback channel parsing with underscores — PASS.** `rest.rpartition('_')`
  (`:514, 540, 552, ...`) splits at the LAST underscore, so `@my_channel` +
  `_` + uid resolves correctly.
- **Staleness — PASS (live).** Both counts computed fresh per render; no cache,
  no TTL. `sync_channel_admins` runs before list/profile reads, so revoked
  Telegram admins don't linger.
- **Performance — OK.** Profile is O(jobs-of-this-admin), not a full
  `scheduled_messages` scan (index lookup + per-job dict get). One `get_chat`
  for the title. List view is heavier (`sync_channel_admins` + N×`get_chat`
  via `asyncio.gather`, `:307-334`) but bounded by admin count; acceptable.
- **Empty states — PASS (no crash).** Zero counts render as `…: 0` (keys
  `chadm_stat_scheduled/recurring` require `{count}`, always supplied).
  Missing record → `chadm_admin_not_found` alert. Empty admin list →
  `chadm_no_admins`. Deleted accounts → auto-revoked + `chadm_deleted_removed`
  line; revoked section with restore buttons.
- **Timezone — N/A (correct).** Profile renders no dates/times, so no tz bug
  possible. The only date nearby (transfer expiry `:756-761`) uses
  `get_channel_timezone` with ISO-fallback — fine.
- **Attribution shape — PASS.** When types/normalization align, jobs are keyed
  by author `user_id` at creation in all paths checked, and the profile filters
  by `(author, channel)` — the right predicate for "per admin per channel".
  No evidence of cross-admin leakage (A's jobs never counted under B).

---

## 5. Coverage checklist

| Ask | Result |
|---|---|
| What query/sum produces scheduled count | `channel_admins.py:421-425` — index ids + `channel_id ==` filter (live, per render) |
| What query/sum produces recurring count | `channel_admins.py:426-430` — same over recurring |
| Sent counts per admin per channel | NOT on profile (Bug 5); personal totals exist in `get_channel_stats` / `build_stats_overview`, channel-wide counters in `channels/admins.py` |
| Stranger attribution per admin | DOES NOT EXIST (Gap B); visits keyed by bot, conversions lack channel, hidden visits `None` |
| Multi-admin correctness | Shape right, numbers wrong when Bug 2/3 hit; sent totals personal while reactions channel-wide (Bug 4) |
| Staleness | Live — fresh |
| Performance | Profile O(admin jobs); list O(admins) API calls — fine |
| Empty states | OK |
| Deleted channels/users | Counts shown without warning (Bug 6); deleted users auto-revoked, their jobs UI-orphaned |
| Timezone | No dates on profile — N/A |
| Can admin A see admin B's stats | No (owner-only) — PASS |
| Can non-admin view profile | No — PASS |
| Regular admin viewing own stats | Denied too (owner-only) — by design, noted |

## 6. Suggested fixes (for the implementing agent, not applied here)

1. Gate on real keys: `'stats_view'` / `'leaderboard_view'` in `callbacks/channels.py:327, 350`
   (or map through `FEATURE_PERMISSION`).
2. Normalize index keys: `str(uid)` in `_build_indices` / `add_*` / `get_user_*_ids`
   (`core/botdata.py:655-716`), and `str()` both sides of channel comparisons in
   `callbacks/channel_admins.py:424,429` + `channels/admins.py:550-555`.
3. Label or split sent-stats scope (mine vs channel) in `statistics_manager.py`
   (`build_single_channel_stats`, `render_channel_stats`).
4. Add delivered-count line to `_render_profile` via `get_message_stats` /
   `get_sent_messages(user_id, channel_id)`; add per-admin stranger view or
   explicitly document it as out of scope (hidden-channel visits must stay
   `None`).
