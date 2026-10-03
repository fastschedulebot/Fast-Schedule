# Admin Broadcast Compose Flow — Investigation Report (Agent 1/6)

Scope: ADMIN BROADCAST COMPOSE FLOW — `src/callbacks/admin/broadcasts.py` + panel entry.
Method: read-only code trace. No `src/` files modified.

## 1. Which flow is actually live (important: there are TWO)

There are two broadcast implementations in the repo, and only ONE is wired to the admin panel:

- **LIVE flow (reachable):** entry `handle_admin_broadcast` in `src/callbacks/admin/panel.py:110-120`
  (prompt `admin_broadcast_prompt`, returns `BROADCAST_MESSAGE`), with send logic `_broadcast_send`
  in `src/admin/handlers.py:61-379` and step handlers split between `src/admin/handlers.py` and
  `src/callbacks/admin/panel.py`. Conversation wiring: `src/register.py:461-516` (`admin_broadcast_conv`).
  Callback dispatch: `src/buttons.py:41-42` (`broadcast_` prefix → `admin_cb`), routed in
  `src/callbacks/admin/main.py:275-293`.
- **DEAD flow (unwired):** the whole compose wizard in `src/callbacks/admin/broadcasts.py:46-440`
  (`handle_broadcast_menu`, `handle_broadcast_new`, `handle_broadcast_history`, `handle_broadcast_info`,
  `handle_broadcast_text_input`, `handle_broadcast_audience`, `handle_broadcast_confirm_send`,
  `handle_broadcast_execute`). **None** of its callback_datas (`broadcast_new`, `broadcast_menu`,
  `broadcast_audience_*`, `broadcast_confirm_send`, `broadcast_schedule`, `broadcast_add_buttons`,
  `broadcast_add_media`, `broadcast_execute`) has a branch in the dispatcher
  `src/callbacks/admin/main.py:210-362` (verified: zero matches), and no functions named
  `handle_broadcast_schedule` / `handle_broadcast_add_buttons` / `handle_broadcast_add_media` exist
  anywhere in `src/` (verified via repo-wide search). So every button it renders
  (`src/callbacks/admin/broadcasts.py:293-296,328`) is a dead end.

## 2. Live-flow step trace (every step)

1. **Panel entry** — `src/callbacks/admin/panel.py:110-120`: `admin_broadcast` → asks for message content,
   returns `BROADCAST_MESSAGE` (`src/core/config.py:131`).
2. **Text/media intake** — `src/admin/handlers.py:407-536` `admin_broadcast_handler`: stores
   `broadcast_text` (`handlers.py:435`, plain `message.text`/`caption`, max 4000 chars) + raw
   `broadcast_entities` (`handlers.py:437`) + media (`photo/video/document/animation/voice/audio/
   video_note/poll`, `handlers.py:445-499`). Then asks ad yes/no (`handlers.py:516-534`).
3. **Ad branch** — `broadcast_ad_yes` → `src/callbacks/admin/panel.py:339-355` (target free/all);
   `broadcast_ad_no` → `src/callbacks/admin/panel.py:358-374` (skip to auto-deletion choice).
4. **Ad target + orderer** — `broadcast_ad_target_free/all` →
   `src/callbacks/admin/panel.py:377-390` → `_show_ad_orderer_prompt` (`panel.py:393-405`) →
   `BROADCAST_AD_ORDERER`; text handled by `broadcast_ad_orderer_handler`
   (`src/admin/handlers.py:738-773`), which appends `[AD tag, orderer]` to the text
   (`handlers.py:752-759`). Skip path: `handle_broadcast_ad_skip_orderer` (`panel.py:408-427`).
   Both land on the auto-deletion prompt keyboard `[broadcast_ask_delete, broadcast_send_now]`.
5. **Auto-delete choice** — `broadcast_ask_delete` → `handle_broadcast_ask_delete`
   (`panel.py:480-491`) → `BROADCAST_DELETION` prompt (`broadcast_autodelete_title`);
   `broadcast_send_now` → `handle_broadcast_send_now` (`panel.py:494-522`): sets
   `broadcast_delete_at = None` (`panel.py:499`) and sends **immediately** via `_broadcast_send`.
6. **Deletion-time input** — `broadcast_delete_time_handler` (`src/admin/handlers.py:674-735`):
   `skip/no/none/never/-` → no deletion (`handlers.py:692-696`); else `_parse_delete_time(text)`
   (`handlers.py:700`; parser at `src/core/helpers.py:1975-1999`); past → reject (`handlers.py:708-712`).
   Then asks recurring yes/no (`handlers.py:725-735`) → `BROADCAST_RECURRING`.
7. **Recurring branch** — `broadcast_recurring_no` → `handle_broadcast_recurring_no`
   (`panel.py:447-474`): **sends immediately**. `broadcast_recurring_yes` →
   `handle_broadcast_recurring_yes` (`panel.py:433-444`) → cron prompt → `BROADCAST_RECURRING_CRON`.
8. **Cron intake** — `broadcast_recurring_cron_handler` (`src/admin/handlers.py:776-856`): strict
   5-field cron validated via `CronTrigger` (`handlers.py:792-803`), stored in
   `bot_data.broadcast_recurring[job_id]` (`handlers.py:824-827`), scheduled via APScheduler
   (`handlers.py:830-843`), job fn `_send_recurring_broadcast_job` (`handlers.py:859-1039`).
   This is **repeat** scheduling (cron), not one-shot scheduling.
9. **Send fan-out** — `_broadcast_send` (`src/admin/handlers.py:61-379`): premium-first ordering
   (`handlers.py:94-98`), entities-based send (`entities=adjusted_entities`, e.g. `handlers.py:310-317`),
   buttons attached if present (`handlers.py:102-128`), per-message deletion entries appended to
   `bot_data.broadcast_deletions` (`handlers.py:321-331`), backed by
   `src/services/periodic.py:487-512` (`periodic_broadcast_deletion`, 60s loop, spawned at
   `src/register.py:1123`). Button-text builder `broadcast_button_text_handler`
   (`handlers.py:542-668`) + `BROADCAST_BUTTONS` state (`src/register.py:478`) exist but are
   **unreachable** (see §4c).
10. **Dead-flow steps (for reference, NOT reachable):** name → message → audience →
    settings (`broadcast_confirm_send`/`broadcast_schedule`/`broadcast_add_buttons`/`broadcast_add_media`,
    `broadcasts.py:282-305`) → confirm (`broadcasts.py:308-338`) → execute (`broadcasts.py:341-440`).

## 3. Complaint verdicts

### (a) "With no auto-deletion it only allows send-now, no scheduling" — VERIFIED TRUE
- Live flow: the no-deletion path is `handle_broadcast_send_now` (`panel.py:494-522`), which calls
  `_broadcast_send` immediately. The deletion path ends in `broadcast_recurring_no`
  (`panel.py:447-474`, immediate send) or `broadcast_recurring_yes` (cron **repeat**, `panel.py:433-444`
  + `handlers.py:776-856`). There is **no one-shot "send at datetime X" step, state, parser, or job**
  anywhere in the live flow.
- Dead flow: does render a Schedule button (`broadcasts.py:294`,
  `callback_data='broadcast_schedule'`) but no handler exists (repo-wide search: zero hits) and
  `handle_broadcast_execute` (`broadcasts.py:341-440`) ignores `scheduled_at` entirely.
  So even the intended scheduling UI cannot function.

### (b) "Auto-deletion doesn't work correctly" — VERIFIED TRUE (multiple defects, infra exists)
Deletion infrastructure exists (`handlers.py:321-331` queue + `periodic.py:487-512` 60s sweeper,
spawned `register.py:1123`), and works for plain text/photo/video/document/animation/audio. Defects:
1. **Prompt/parser mismatch makes the timer almost unusable:** the prompt
   (`translations/admin/en.json:495` `autodelete_title`) advertises `today at 20:00`,
   `tomorrow at 12:00`, `on 25.12.2027`, `in 5 hours`, `in 3 days`, `next hour`, `now` — **none**
   of which `_parse_delete_time` (`src/core/helpers.py:1975-1999`) accepts. It accepts only
   `N m/min/mins/minute/minutes | N h/hr/hrs/hour/hours | N d/day/days` plus `'%Y-%m-%d %H:%M'`
   and `'%Y-%m-%d'`. Following the prompt always yields `broadcast_autodelete_invalid`
   (`translations/admin/en.json:491`) and an input loop (`handlers.py:700-706`).
2. **`video_note` and `poll` follow-up text is never deleted:** both branches send a second
   text message (`handlers.py:282-287` video_note, `handlers.py:303-308` poll) but only the first
   `msg.message_id` is queued for deletion (`handlers.py:321-331`). The text copy lives forever.
3. **Failed deletions are silently dropped with no retry:** `periodic.py:497-505` — on
   `delete_message` exception it does `pass` and the item is still excluded from `to_keep`.
4. **Dead-flow `auto_delete` is ignored:** `broadcasts.py:93-104` collects it, `handle_broadcast_execute`
   (`broadcasts.py:341-440`) never reads it and never touches `broadcast_deletions`.

### (c) "No way to add inline buttons" — VERIFIED TRUE (effectively; code exists but unreachable)
- Send path supports buttons (`handlers.py:102-128` builds `InlineKeyboardMarkup`;
  `broadcast_button_text_handler`, `handlers.py:542-668`, parses `Label | url` / `Label | action:value`).
- BUT: nothing ever shows the button-builder entry prompt (`add_buttons_title` /
  `send_content_title` / `add_url_title` keys in `translations/admin/en.json:485-507` are never sent
  by any code — verified zero send-sites in `src/`). `register.py:464-466,502-504` registers
  `broadcast_add_url` / `broadcast_add_callback` / `broadcast_buttons_done` entry/fallback patterns,
  but `button_handler` (`src/buttons.py:498-789`) has no branch for them; they fall into the
  `broadcast_` prefix → `admin_cb.handle` → `src/callbacks/admin/main.py`, which has **no matching
  elif** and returns `None` (`main.py:362`). Net effect: the buttons do nothing (spinner only) and
  `BROADCAST_BUTTONS` state (`register.py:478`) can never be entered. Same for the dead flow's
  `broadcast_add_buttons` (`broadcasts.py:295`) — no handler exists.
- Only pre-existing `broadcast_buttons` already in `context.user_data` (e.g. from recurring data)
  would be attached; there is no reachable UI to create them.

### (d) "<b> formatting doesn't work" — VERIFIED TRUE (for literal HTML tags in the live flow)
- Live send is **entities-based, not HTML-based**: intake stores raw entities
  (`handlers.py:437`) and sends with `entities=adjusted_entities` and **no** `parse_mode`
  (e.g. `handlers.py:310-317`; media branches use `caption_entities`). Typing literal
  `<b>text</b>` therefore arrives with no bold entity and is delivered as literal
  `<b>text</b>` characters. Only native client-side formatting (select → Bold) survives, because
  that produces real entities. (The prompt `send_content_title` even promises "Text with
  formatting (bold, italic, etc.)" — `translations/admin/en.json:507` — which is misleading for
  typed tags.)
- The dead flow *would* render `<b>` (it sends `text=` + `ParseMode.HTML`, `broadcasts.py:392-396`)
  and its step-2 prompt advertises `<b>Bold</b>` (`translations/admin/en.json:355`), but it is
  unreachable, so admins never get that behavior.
- Related preview hazard (dead flow): confirm preview interpolates raw user text into an HTML
  message (`broadcasts.py:318-325`), so user-typed `<b>`/`<` can break parsing of the preview itself.

### (e) "Time is not understood correctly" — VERIFIED TRUE
- Auto-delete parser `src/core/helpers.py:1975-1999`: only relative `N + unit(m/h/d + aliases)` and
  absolute `%Y-%m-%d %H:%M` / `%Y-%m-%d`. No `today/tomorrow at HH:MM`, no `DD.MM.YYYY`
  (`on 25.12.2027` from the prompt fails), no `in N hours/days` phrasing, no `next hour`, no `now`.
  Every example in the user-facing prompt (`translations/admin/en.json:495`) except none actually
  parses — users following instructions always get the invalid-time error (`handlers.py:700-706`,
  text `translations/admin/en.json:491` which itself only suggests `today at 20:00`-style examples
  that also fail).
- One-shot broadcast scheduling has no parser at all (no such feature). The only other time input,
  recurring cron (`handlers.py:776-803`), correctly requires strict 5-field cron — fine, but
  unrelated to the complaint.

## 4. Where broadcasts are stored / sent from, and whether scheduled broadcasts fire

- **Live immediate sends:** not stored at all — `_broadcast_send` (`handlers.py:61-379`) fans out
  directly and only persists deletion queue entries (`bot_data.broadcast_deletions`, persisted via
  `BROADCAST_DELETIONS_FILE`, `src/core/botdata.py:52,574-575` / `src/main.py:457`). No
  `broadcast_records` table/list exists for the live flow.
- **Dead-flow records:** `bot_data['broadcasts']` list (`broadcasts.py:379-381,412-417`) with
  `sent/sent_count/scheduled_at` fields and `_get_broadcast_status` (`broadcasts.py:37-43`).
  `broadcasts` is **not** a registered `botdata` persisted domain (see `src/core/botdata.py:52,77`),
  so these would be ephemeral even if the flow were wired. Nothing ever sets `scheduled_at`
  (default `None`, `broadcasts.py:101`) and **no job or sweeper reads `bot_data['broadcasts']`** —
  one-shot scheduled broadcasts can never fire.
- **Recurring broadcasts:** `bot_data.broadcast_recurring` dict (`handlers.py:824-827`) + APScheduler
  `CronTrigger` jobs (`handlers.py:830-843`) executed by `_send_recurring_broadcast_job`
  (`handlers.py:859-1039`). These DO fire while the process lives, but `broadcast_recurring` is a
  dynamic attribute, not a persisted domain, and no restore-on-boot exists — **recurring broadcast
  jobs are lost on restart** (see §5.6).

## 5. Other bugs found (severity + impact)

1. **[HIGH] Dead compose wizard ships user-visible buttons with no handlers.** `broadcasts.py:293-296`
   (`broadcast_schedule`, `broadcast_add_buttons`, `broadcast_add_media`) and `:328`
   (`broadcast_execute`); translation keys referenced by the wizard are reported missing
   (`translations/admin/missing_admin.txt`, e.g. `broadcast_status_draft/scheduled/sent`,
   `broadcast_ad_target_free/all`). Impact: if this menu is ever exposed, every core action is a
   no-op; currently it mainly signals an abandoned half-migration confusing future work.
2. **[HIGH] Auto-delete prompt advertises 7 time formats, parser accepts 0 of them.**
   `translations/admin/en.json:495` vs `src/core/helpers.py:1975-1999`. Impact: admins cannot set
   deletion following instructions; repeated `autodelete_invalid` loop; likely the root of
   complaint (b) reports.
3. **[MEDIUM] Voice broadcasts pass `caption_entities` + `parse_mode='HTML'` together**
   (`handlers.py:247-257`). Telegram rejects caption + parse_mode combined → every voice broadcast
   raises and lands in `failed_count` (`handlers.py:347-353`). Impact: voice broadcasts never deliver.
4. **[MEDIUM] `video_note`/`poll` second text message never auto-deleted** (`handlers.py:271-308`
   vs queue `handlers.py:321-331`, single `message_id` stored). Impact: partial deletion leaves orphan
   copies in every recipient chat — looks like "auto-delete doesn't work".
5. **[MEDIUM] Deletion sweeper drops failures without retry** (`periodic.py:497-505`: `except: pass`,
   item still discarded). Impact: transient API errors or missing-delete-rights permanently leak
   messages that should have been retried/reported.
6. **[MEDIUM] Recurring broadcast jobs not persisted / not restored on restart**
   (`handlers.py:824-843`; `broadcast_recurring` not in `botdata` domains, `botdata.py:52,77`;
   no boot-time re-registration found). Impact: all recurring broadcasts silently stop after any
   restart/deploy until recreated.
7. **[MEDIUM] Button-builder callbacks registered but unhandled → silent no-op.**
   `register.py:464-466,502-504` vs dispatcher gap (`buttons.py:498-789`, `main.py:210-362`).
   Impact: complaint (c); if the entry prompt is ever re-added, taps still die silently.
8. **[LOW] Dead-flow execute ignores media/buttons/auto-delete/schedule**
   (`broadcasts.py:341-440`: sends `text=` + `ParseMode.HTML` only, no `reply_markup`, no deletion
   queue, no `scheduled_at` handling). Impact: wiring it up as-is would ship silent feature loss.
9. **[LOW] Dead-flow confirm preview interpolates raw text into HTML** (`broadcasts.py:318-325`).
   Impact: user `<`/`<b>` breaks preview render (`Can't parse entities`).
10. **[LOW] `_get_broadcast_status` `scheduled` branch unreachable** (`broadcasts.py:37-43`;
    `scheduled_at` never set). Impact: dead status text; history misleading if revived.

## 6. Files of record (evidence index)

- Panel entry & routing: `src/callbacks/admin/panel.py:110-120,339-355,358-374,393-427,433-474,480-522`;
  `src/callbacks/admin/main.py:275-293`; `src/buttons.py:41-42,498-789`; `src/register.py:461-516,1123`.
- Send/delete/cron: `src/admin/handlers.py:61-379,407-536,542-668,674-773,776-856,859-1039`;
  `src/services/periodic.py:487-512`; `src/core/helpers.py:1975-1999`.
- Dead wizard: `src/callbacks/admin/broadcasts.py:46-440` (esp. `:282-305,308-338,341-440`).
- States/persistence: `src/core/config.py:131-146`; `src/core/botdata.py:52,77,574-575`;
  `src/main.py:457`.
- Strings: `translations/admin/en.json:485-508` (esp. `:491,495`), `:349-459`;
  `translations/en.json:221-226`; `translations/admin/missing_admin.txt`.
