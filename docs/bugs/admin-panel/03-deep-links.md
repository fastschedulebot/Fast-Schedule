# Deep Links + Deep Link Builder — audit (Agent 3/6)

Scope: `start=` payload handling in `src/handlers/commands.py` (`start()`), the admin-panel
deep-link builder in `src/callbacks/admin/panel.py`, and `sign`/`verify_deep_link` helpers.
Method: code trace + live `parse()` checks via `python -c` (read-only). No `src/` edits made.

Handler references below are to `src/handlers/commands.py` unless stated otherwise.
`parse()` = `src/services/deep_links.py:48`. `build_link()` = `src/services/deep_links.py:93`.
Short-code catalog = `docs/deep_link_ref.json`.

---

## 1. Every `start=` payload the bot handles — WORKING / BROKEN

### 1a. Marketing / premium plan links — WORKING
| Payload | Handler | Verdict + evidence |
|---|---|---|
| `premium_monthly`, `premium_monthly_3`, `premium_monthly_6`, `premium_yearly`, each optionally suffixed `__<source>` (e.g. `premium_yearly__pricing`) | `commands.py:286-301` → `_deep_link_premium()` (`commands.py:100-121`) | **WORKING.** `_code` is split off the `__source` (used only for `tracking.record_visit`), mapped to a plan, and the real payment menu (`build_premium_plan_payment_content`) is sent as a fresh message. Purchase-blocked state is honoured. |
| `pay`, `pay_monthly`, `pay_yearly` (payment-return status screen) | `commands.py:302-306` → `_handle_premium_payment_return()` (`commands.py:124-155`) | **WORKING.** Read-only status screen; never grants Premium (webhook remains the sole grant path — correct). |

### 1b. Referral / attribution links — WORKING (with caveats)
| Payload | Handler | Verdict + evidence |
|---|---|---|
| `from_bot_<secret>` (sender-bot "Open Main Bot" button) | `commands.py:315-338` | **WORKING.** Secret is recomputed per stored bot via `bot_tracking_secret()` (`src/services/tracking.py:31-39`) and matched; visit is recorded, `context.args` cleared, normal start flow continues. Unknown secret still continues to start (graceful). |
| `ref_<CODE>` (user referral) | `commands.py:343-421` | **WORKING.** Referrer looked up, click processed, referrer notified only on success, referee gets a specific human-readable reason on rejection (`_referral_reason_text`, `commands.py:395-409`). Invalid code → `referral_link_invalid` message (no crash). |
| `sb_<BOTUSERNAME>` (sender-bot referral) | `commands.py:427-501` | **WORKING (partial).** Records `sender_bot_referrals` + stats and shows a connect-bot/help/back promo card. It does **not** open the channel or bot itself — acceptable for a referral promo, but note the case-insensitive match (`.lower()`, line 443) is inconsistent with `sc_`/`rc_` exact match (see §3, bug B5). |

### 1c. SetDate import link — WORKING (no expiry)
| Payload | Handler | Verdict + evidence |
|---|---|---|
| `ats_<token>` (SetDate "import to main", `SetDate/bot.py:1021-1023`) | `commands.py:507-722` | **WORKING.** Session loaded via `load_shared_session_async`; `user_id` match enforced (`commands.py:518`); wrong-user/unknown token → `import_link_invalid` + import state cleaned (`commands.py:704-722`). Checkpoint restore (photo modes, storage, selected channel) and the photo-mode picker both function. **Caveat (bug B8):** single-use (token is `pop`ped on load, `src/services/models.py:1319`) but there is **no TTL/expiry** — a token lives until clicked (SetDate itself notes "entries only vanish when the deep link is clicked", `SetDate/bot.py:61,234`). |

### 1d. Sender-bot shortcut links — MOSTLY BROKEN
| Payload | Handler | Verdict + evidence |
|---|---|---|
| `sc_<bot_username>` | `commands.py:728-760` | **BROKEN (partial).** Sets `preferred_channel` then only renders an info card (`sc_deeplink_text` + Single-post / Message-list / Back buttons). The schedule flow itself is **not** opened — the user must tap again. Fails the "link must open/do that menu/action" requirement. |
| `rc_<bot_username>` | `commands.py:766-790` | **BROKEN.** Sets `preferred_channel` then renders text with **only a Back button**. The recurring flow is never opened; this is a dead end, strictly worse than `sc_`. |
| `cal_<bot_username>` | `commands.py:796-816` | **BROKEN.** Stores `preferred_channel`, then `pass` → falls through to the generic main menu. Calendar never opens; the user gets no indication the payload did anything. |
| `lst_<bot_username>` | `commands.py:822-840` | **BROKEN.** Same pattern: stores channel, falls through to main menu. Message list never opens. |
| `srch_<bot_username>` | `commands.py:846-864` | **BROKEN.** Same pattern: stores channel, falls through to main menu. Search never opens. |

### 1e. Generic step links (`parse()` DSL: `o-…`, `p-…`, `c-…`, `m-…`, `--`-joined) — SPLIT
Primary dispatch is `commands.py:870-1007` with `cmd_map` at `commands.py:913-929`.

**WORKING targets** (verified: `parse()` output → `cmd_map` hit → handler awaited at `commands.py:983`):
`schedule`, `schedule_message`, `recurring`, `recurring_message`, `premium`, `help`
(redirects to Support Bot — opens the redirect, arguably working), `stats`, `channel`,
`connect_channel`, `storage`, `search`, `language`, `calendar`, `export`, `import`, `data`,
`list`, `backup`, `delete`, `bots` (`bots_command` exists, `commands.py:2727`), `referral`,
`feedback`, `message_list` (→ `list_command`), `page=<N>` (`commands.py:896-909`),
bare `o` = legacy truncated `o=cch` (Telegram strips `=`, arrives as just `o`;
special-cased at `commands.py:889-891` → `connect_channel_deep_link_command`, which exists at
`commands.py:2148`), `o-cch` / `o=cch` (if `=` ever survived) → same, `menu` → unknown-target
fallback renders main menu (`commands.py:986-1003`) — works **by accident**, not by design.

**BROKEN targets** (parse fine, but no `cmd_map` entry → silently renders generic main menu
with `page` param at best; user asked for X, gets the home screen):
- All `menu/*` catalog entries except the mapped ones: `show_channel` (`shch`),
  `change_channel` (`xch`), `media_storage` (`ms`), `statistics` (`stat`), `search_menu` (`srchm`),
  `calendar_view` (`cv`), `export_menu` (`em`), `import_data` (`id`), `language_menu` (`lm`),
  `premium_menu` (`pm`), `referral_menu` (`refm`), `back_to_main` (`bm`), `feedback_menu` (`fm`),
  `admin_panel` (`ap`), `delete_menu` (`dm`).
- All `premium/*`: `premium_menu_monthly` (`pmm`), `premium_menu_yearly` (`pmy`),
  `premium_cancel` (`pc`), `upgrade_to_premium` (`utp`), `buy_premium_monthly` (`bpm`).
- All `help_topics/*`: `hc, hcb, hcc, hsch, hmt, hrec, hms, hsd, hfmt, hprem, hie, hco`.
- All `admin/*`: `ac, ab, aui, asl, abu, asu, apc, apm, abs, adlb` (including the builder itself).
- `params/*` / `clicks/*` codes used as the *primary* action (they are only honoured as
  secondary steps `rest_params`, `commands.py:954-981`).
- Concrete probe results: `parse('o-stats')` → `('open','stats')` → hit (long-name passthrough);
  `parse('o-stt')` → `('open','stats')` → hit; but e.g. `parse` of `o-pm`, `o-ms`, `o-stat`,
  `o-ap`, `o-hcc` all yield valid steps that miss `cmd_map` → main-menu fallback. **BROKEN.**

### 1f. Sender-bot instance feature keys — WORKING (owner only)
Bare `schedule | recurring | stats | storage | search | export | data | import | feedback |
calendar | list | signature | delete | edit | dub | backup | referral | timezone | premium |
help | language | channel | channels | newchannel | setchannel` on a **sender-bot instance**,
from the owner, auto-opens the feature (`commands.py:193-200` via `_SENDER_BOT_FEATURE_ROUTE`,
`commands.py:62-97`; args cleared so `/edit`/`/dub` behave like menu clicks). Channel admins get
the permission-filtered home; strangers keep the welcome card. **WORKING.**

### 1g. SetDate side (`from_main_<id>`) — WORKING
`SetDate/bot.py:459-467` (`deep_link_start`, wired at `SetDate/bot.py:1761`) captures
`main_user_id` and enters `schedule_start`. **WORKING** (terms-gate interplay exists but the
pending `/start from_main…` text is preserved across the gate, `SetDate/bot.py:1591-1595,1623-1629`).

---

## 2. Deep-link builder (admin panel) — what it builds today

Implementation: `handle_admin_deep_link_builder`, `src/callbacks/admin/panel.py:247-269`
(exposed as `admin_deep_link_builder`, wired at `src/callbacks/admin/main.py:304-305`,
button at `src/keyboards.py:433`).

What it is: a **static** menu of 9 URL buttons, hardcoded payloads, hardcoded English text:
| Button | Emitted payload |
|---|---|
| Open Main Menu | `?start=menu` |
| Open Schedule | `o-sch` |
| Open Recurring | `o-rec` |
| Open Calendar | `o-cal` |
| Open Statistics | `o-stats` |
| Open Referral Menu | `o-ref` |
| Open Premium Menu | `o-prem` |
| Open Help | `o-hp` |
| Open Search | `o-srch` |

Mapping test (builder-output → start-handler), verified with `parse()` in-process:
- `o-sch` → `('open','schedule')` → `schedule_command` ✔
- `o-rec` → `('open','recurring')` → `recurring_command` ✔
- `o-cal` → `('open','calendar')` → `calendar_command` ✔
- `o-stats` → `('open','stats')` → `stats_command` ✔ (long-name passthrough; the documented
  short code is `stt` — works by luck, see bug B4)
- `o-ref` → `('open','referral')` → `referral_command` ✔
- `o-prem` → `('open','premium')` → `premium_command` ✔
- `o-hp` → `('open','help')` → `help_command` ✔
- `o-srch` → `('open','search')` → `search_command` ✔
- `menu` → `('open','menu')` → unknown-target fallback → main menu ✔ (by accident)

So all 9 emitted links resolve **for an ungated user** — but the builder still fails the
complaint ("doesn't really build links; should: choose what to open, and the link must
open/do that menu/action") because:
1. There is **nothing to choose**: no interactive builder, no target picker, no params
   (`page`, `media_type`/`photo_mode`, `click`, `message`), no premium-plan picker
   (`premium_monthly/yearly`), no `connect_channel`, no sender-bot (`sc_/rc_/cal_`) or
   referral (`ref_`) links. It covers ~8 of 60+ catalog targets and none of the
   `menu/*`, `premium/*`, `help_topics/*`, `admin/*` families — and most of those families
   don't resolve anyway (§1e).
2. The links don't reliably *do* the action: `start()` applies the sender-bot gate M38
   (`commands.py:937-952`) — when management lives in a sender bot, `o-sch`/`o-rec`/… on the
   main bot renders a redirect card instead of opening the feature. The builder gives no
   hint of this.
3. It never uses its own infrastructure: `build_link()`, `get_all_targets()` from
   `src/services/deep_links.py` are not called — payloads are hand-typed literals.

---

## 3. Other bugs (severity + impact)

- **B1 (High) — `=`-form deep links break over the wire; docs teach the `=` form.**
  `docs/deep_link_ref.json` documents `o=cal`-style payloads and `build_link()` correctly emits
  the Telegram-safe `-` form (`o-cal`), but Telegram strips `=` in `?start=` payloads, so a
  shared `?start=o=cal` arrives as bare `o` → misrouted to the connect-channel flow
  (`commands.py:889-891`) instead of calendar. Only the single special case bare-`o` is rescued;
  every other `=` link (e.g. `o=sm--mt=sph` from the doc example) is corrupted. Impact: any link
  copied from the docs/website in `=` form opens the wrong flow. Fix: rewrite docs/examples to
  `-` form and consider rejecting/redirecting bare-`o` ambiguity.
- **B2 (High) — `rc_` is a dead end; `sc_` doesn't open anything; `cal_/lst_/srch_` are silent no-ops.**
  `commands.py:728-864`. Four of five sender-bot shortcut prefixes never open their feature
  (details §1d). Impact: "most deep links don't work" — these are exactly the per-bot links
  users tap. Fix: route them through the real commands (like the generic `open` path does) or
  at minimum give `rc_` the same two-button card `sc_` has.
- **B3 (High) — ~40 catalog targets parse but silently show the home screen.**
  `cmd_map` (`commands.py:913-929`) covers ~22 names; the rest of `deep_link_ref.json`
  (all `premium/*`, `help_topics/*`, `admin/*`, most `menu/*`) falls into the unknown-target
  fallback (`commands.py:986-1003`). Impact: misleading — a tapped link appears to "work"
  (bot opens) but never does what was asked. Fix: either implement the missing routes or reply
  with an explicit "unsupported link" message instead of the generic menu.
- **B4 (Medium) — builder emits `o-stats`, catalog says `stt`; works only via passthrough.**
  `src/callbacks/admin/panel.py:258` vs `docs/deep_link_ref.json` (`stats: stt`). `parse()`
  keeps unknown long names verbatim so `('open','stats')` hits `cmd_map` today, but this relies
  on a fallback path, not the catalog. Fragile to any future strict validation. Fix: emit `o-stt`
  (or make the builder use `build_link()` so this class of drift is impossible).
- **B5 (Medium) — inconsistent username matching across `sb_/sc_/rc_/cal_/lst_/srch_`.**
  `sb_` lowercases both sides (`commands.py:443`); `sc_/rc_/cal_/lst_/srch_` use exact `==`
  (`commands.py:740,778,808,834,858`), and on no-match they silently fall through with zero
  feedback. Impact: same link works as `sb_` but silently does nothing as `sc_` if case differs.
  Fix: lowercase everywhere + an explicit "bot not found" reply.
- **B6 (Medium) — builder violates localization rules + not interactive.**
  Hardcoded English strings in `src/callbacks/admin/panel.py:251-252` (RULE 1 / RULE 14 —
  admin texts belong in `translations/admin/en.json`); no choose-what-to-open UI, no params,
  no copy/preview/validate step. Impact: the exact complaint filed. Fix: rebuild as a real
  picker (category → target → params → preview `t.me/…?start=…` + copy button) driven by
  `get_all_targets()`/`build_link()`.
- **B7 (Medium) — `sign/verify_deep_link` exist but are never used; no start payload is authenticated.**
  `src/core/security.py:144-180` implements HMAC-SHA256 signing + optional `:timestamp` expiry
  (default 86400 s), yet the only reference is an unused import in `src/main.py:18-28`
  (`verify_deep_link`, `sanitize_deep_link_param` imported, never called — also confirmed no
  `sign_deep_link` call sites repo-wide in `src/`). `start()` never verifies anything and never
  sanitizes args. Impact: dead security code gives a false sense of protection; referral/attribution
  payloads are forgeable by construction (probably fine for their threat model, but then the
  helpers should be wired or removed). Fix: either route sensitive payloads through
  sign/verify or delete the helpers + unused imports.
- **B8 (Low-Medium) — `from_bot_` secret and `ats_` tokens have no expiry.**
  `bot_tracking_secret()` (`src/services/tracking.py:31-39`) is a deterministic 16-hex-char
  SHA-256 fingerprint — no secret key, no HMAC, valid forever; `ats_` sessions are single-use
  (`pop` on load) but never expire server-side. Impact: low (fingerprint only drives analytics;
  `ats_` still checks `user_id`), but there is no revocation/rotation story. Fix: document as
  accepted risk or add TTL to shared sessions.
- **B9 (Low) — marketing `__source` split runs before all prefix checks and rewrites `args[0]`.**
  `commands.py:286-308`. Any future/current payload legitimately containing `__` loses its suffix
  before `ref_/sb_/ats_/…` matching. No live collision today (none of those prefixes use `__`),
  but the ordering is fragile. Fix: only strip `__source` for the known `premium_*` family.

---

## 4. Sign / verify summary

- `sign_deep_link(payload, secret=DEEP_LINK_SECRET)` / `verify_deep_link(signed, secret,
  max_age_seconds=86400)`: HMAC-SHA256, `payload.hexsig` format, timestamp-expiry enforced only
  if the payload embeds a trailing `:epoch` component (`src/core/security.py:154-180`). Sound
  design, **but zero call sites** — no HMAC-bound links exist in the product, and nothing expires.
- What *is* used instead: (a) `bot_tracking_secret` — keyless truncated SHA-256 fingerprint,
  attribution only; (b) `ats_` shared-session token — random 24-hex (`secrets.token_hex(12)`,
  `SetDate/bot.py:1021`), single-use, `user_id`-bound, no TTL; (c) everything else — unsigned,
  unexpiring plain payloads.
