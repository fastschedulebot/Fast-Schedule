## Overview

Telegram Bot API 9.6 (April 3, 2026) introduced **Managed Bots** — a feature that lets a "manager bot" create and control child bots on behalf of users. This eliminates the manual BotFather → copy token → paste token setup flow entirely.

**User-facing goal:** During `hermes setup`, the Telegram step becomes "scan a QR code, tap confirm, done." No BotFather, no token copy-paste.

**Client-side PR:** #10589 (hermes-agent changes — QR code, pairing client, setup wizard)

This issue describes the **backend infrastructure** needed to complete the flow.

---

## How Telegram Managed Bots Work

Reference: https://core.telegram.org/bots/features#managed-bots

1. A bot enables "Bot Management Mode" via @BotFather MiniApp → `can_manage_bots` becomes true
2. Users are sent a deep link: `https://t.me/newbot/{manager_bot}/{suggested_username}?name={name}`
3. User opens link → Telegram shows a pre-filled bot creation screen → user taps confirm
4. Manager bot receives a `managed_bot` update (`ManagedBotUpdated` object) with the new bot's info
5. Manager bot calls `getManagedBotToken(user_id)` → gets the child bot's full token
6. Manager bot now has complete control over the child bot via Bot API

**Key API methods:**
- `getManagedBotToken(user_id)` → returns bot token as string
- `replaceManagedBotToken(user_id)` → rotates the token, returns new one
- `ManagedBotUpdated` — update type received when a managed bot is created or its token changes

**Constraints:**
- Bot Management Mode must be enabled via @BotFather MiniApp (one-time)
- The `request_managed_bot` keyboard button only works in **private chats**
- Child bot is owned by the user on Telegram's side; manager bot holds the token

---

## Architecture

```
┌──────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   hermes setup   │     │   Pairing API          │     │  Manager Bot    │
│   (user's CLI)   │     │   (Cloudflare Worker)  │     │  (@HermesSetup) │
└────────┬─────────┘     └──────────┬───────────┘     └────────┬────────┘
         │                          │                           │
    1. POST /pair {nonce}           │                           │
    ─────────────────────>          │                           │
    <── 201 {nonce}                 │                           │
         │                          │                           │
    2. Print QR code with           │                           │
       deep link containing         │                           │
       suggested_username           │                           │
         │                          │                           │
         │          3. User opens link in Telegram,             │
         │             confirms bot creation                    │
         │                          │                           │
         │                          │    4. Telegram sends      │
         │                          │       managed_bot update  │
         │                          │    ──────────────────────>│
         │                          │                           │
         │                          │    5. getManagedBotToken  │
         │                          │    ──────────────────────>│
         │                          │    <── bot token          │
         │                          │                           │
         │    6. PUT /pair/{nonce}   │                           │
         │       {token, username}   │<──────────────────────── │
         │                          │                           │
    7. GET /pair/{nonce}            │                           │
    ─────────────────────>          │                           │
    <── 200 {token}                 │                           │
         │                          │                           │
    8. Save token to .env           │                           │
```

### Nonce ↔ Username Correlation

The CLI generates both a `nonce` and a `suggested_username` (e.g. `hermes_work_a7f3_bot`). It registers the nonce with the pairing API. The deep link encodes the suggested_username.

When the manager bot receives the `managed_bot` update, the `ManagedBotUpdated` object includes the new bot's `User` object (with `username`). The manager bot needs to correlate this username to a registered nonce.

**Two approaches (pick one):**

**Option A: Nonce encoded in username (simplest)**
- CLI generates username as `hermes_{nonce_prefix}_bot` (e.g. `hermes_a7f3b2c1_bot`)
- Manager bot extracts the nonce prefix from the created bot's username
- Pairing API stores `{nonce_prefix: nonce}` mapping
- Pro: No additional state needed between CLI and manager bot
- Con: Username is less customizable

**Option B: Separate lookup table**
- CLI registers `{nonce: suggested_username}` with pairing API
- Manager bot queries pairing API to find nonce by username
- Pro: Username can be anything
- Con: Extra API call

**Recommendation: Option A** — simpler, fewer moving parts, the username suffix is already random.

---

## Component 1: Pairing API (Cloudflare Worker + KV)

A minimal HTTP API that mediates the token exchange between the CLI and the manager bot.

### Deployment
- **Cloudflare Worker** on `setup.hermes-agent.nousresearch.com` (subdomain of existing docs domain)
- **Cloudflare KV** namespace for nonce → token storage with auto-expiration

### Endpoints

#### `POST /pair`
Register a new pairing nonce. Called by the CLI.

```
Request:  { "nonce": "a7f3b2c1d4e5f6a7b8c9d0e1f2a3b4c5" }
Response: 201 { "nonce": "...", "expires_at": "2026-04-15T16:15:00Z" }
```

- Store nonce in KV with 5-minute TTL
- Rate limit: 10 requests per IP per minute (prevent abuse)

#### `PUT /pair/{nonce}`
Store the bot token. Called by the manager bot (authenticated).

```
Headers:  Authorization: Bearer <MANAGER_BOT_SECRET>
Request:  { "token": "123456:ABCdefGHI...", "bot_username": "hermes_a7f3_bot" }
Response: 200 { "ok": true }
```

- Verify the nonce exists in KV (404 if not)
- Verify Authorization header matches the shared secret
- Update KV entry with the token (preserve TTL)

#### `GET /pair/{nonce}`
Poll for the token. Called by the CLI.

```
Response (not ready): 404 { "status": "waiting" }
Response (ready):     200 { "token": "123456:ABCdefGHI...", "bot_username": "hermes_a7f3_bot" }
```

- On successful retrieval, **delete the KV entry** (one-time use)
- The token should only be retrievable once

### Security considerations
- KV entries auto-expire after 5 minutes (prevents stale token accumulation)
- Manager bot authenticates via shared secret on PUT (prevents injection)
- GET deletes the entry on read (one-time retrieval)
- No user authentication on POST/GET (the nonce itself is the secret — 128-bit random)
- Rate limiting on POST prevents nonce flooding
- CORS: restrict to CLI user-agent or disable entirely (CLI uses httpx, not browser)

### Cloudflare Worker implementation (~60 lines)

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // POST /pair — register nonce
    if (request.method === "POST" && path === "/pair") {
      const { nonce } = await request.json();
      if (!nonce || nonce.length !== 32) {
        return Response.json({ error: "invalid nonce" }, { status: 400 });
      }
      await env.PAIRING_KV.put(nonce, JSON.stringify({ status: "waiting" }), {
        expirationTtl: 300, // 5 minutes
      });
      return Response.json({ nonce, expires_in: 300 }, { status: 201 });
    }

    // PUT /pair/:nonce — store token (manager bot only)
    const putMatch = path.match(/^\/pair\/([a-f0-9]{32})$/);
    if (request.method === "PUT" && putMatch) {
      const auth = request.headers.get("Authorization");
      if (auth !== `Bearer ${env.MANAGER_SECRET}`) {
        return Response.json({ error: "unauthorized" }, { status: 401 });
      }
      const nonce = putMatch[1];
      const existing = await env.PAIRING_KV.get(nonce);
      if (!existing) {
        return Response.json({ error: "nonce not found" }, { status: 404 });
      }
      const { token, bot_username } = await request.json();
      await env.PAIRING_KV.put(nonce, JSON.stringify({ token, bot_username }), {
        expirationTtl: 300,
      });
      return Response.json({ ok: true });
    }

    // GET /pair/:nonce — poll for token
    const getMatch = path.match(/^\/pair\/([a-f0-9]{32})$/);
    if (request.method === "GET" && getMatch) {
      const nonce = getMatch[1];
      const data = await env.PAIRING_KV.get(nonce, "json");
      if (!data) {
        return Response.json({ status: "expired" }, { status: 404 });
      }
      if (!data.token) {
        return Response.json({ status: "waiting" }, { status: 404 });
      }
      // One-time retrieval: delete after read
      await env.PAIRING_KV.delete(nonce);
      return Response.json({ token: data.token, bot_username: data.bot_username });
    }

    return Response.json({ error: "not found" }, { status: 404 });
  },
};
```

### KV namespace setup

```bash
wrangler kv:namespace create PAIRING_KV
# Add the ID to wrangler.toml
```

### wrangler.toml

```toml
name = "hermes-pairing"
main = "src/index.js"
compatibility_date = "2026-04-01"

[vars]
MANAGER_SECRET = ""  # Set via wrangler secret put MANAGER_SECRET

[[kv_namespaces]]
binding = "PAIRING_KV"
id = "<from kv:namespace create>"
```

---

## Component 2: Manager Bot (@HermesSetupBot)

A lightweight Python bot that:
1. Listens for `managed_bot` updates
2. Calls `getManagedBotToken` to get the child bot's token
3. Sends the token to the pairing API

### Setup (one-time)
1. Create a bot via @BotFather (or use an existing Nous bot)
2. Open BotFather's MiniApp → enable "Bot Management Mode"
3. Verify: `getMe` should show `can_manage_bots: true`
4. Deploy the bot process

### Implementation (~80 lines)

```python
"""Hermes Managed Bot — Nous-hosted manager bot for automatic Telegram setup."""

import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logger = logging.getLogger(__name__)

MANAGER_TOKEN = os.environ["MANAGER_BOT_TOKEN"]
PAIRING_API_URL = os.environ.get("PAIRING_API_URL", "https://setup.hermes-agent.nousresearch.com")
PAIRING_API_SECRET = os.environ["PAIRING_API_SECRET"]


async def handle_managed_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle managed_bot updates — new bot created by a user."""
    managed = update.managed_bot
    if not managed:
        return

    bot_user = managed.bot
    creator = managed.user
    bot_username = bot_user.username or ""
    bot_id = bot_user.id

    logger.info(f"Managed bot created: @{bot_username} (id={bot_id}) by user {creator.id}")

    # Get the child bot's token
    try:
        token = await context.bot.get_managed_bot_token(user_id=bot_id)
    except Exception as e:
        logger.error(f"Failed to get managed bot token: {e}")
        return

    # Extract nonce from username (hermes_{nonce_prefix}_bot pattern)
    # The CLI generates usernames like hermes_a7f3b2c1_bot
    nonce_prefix = _extract_nonce_from_username(bot_username)
    if not nonce_prefix:
        logger.warning(f"Could not extract nonce from username: {bot_username}")
        # Try to notify the user directly
        try:
            await context.bot.send_message(
                chat_id=creator.id,
                text=f"Your Hermes bot @{bot_username} was created!\n\n"
                     f"Token: `{token}`\n\n"
                     f"Paste this in your hermes setup if it didn't auto-detect.",
                parse_mode="Markdown",
            )
        except Exception:
            pass
        return

    # Look up full nonce from pairing API and store the token
    try:
        # Find the full nonce that starts with this prefix
        resp = httpx.put(
            f"{PAIRING_API_URL}/pair/{nonce_prefix}",
            json={"token": token, "bot_username": bot_username},
            headers={"Authorization": f"Bearer {PAIRING_API_SECRET}"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            logger.info(f"Token stored for nonce {nonce_prefix[:8]}...")
        else:
            logger.warning(f"Pairing API returned {resp.status_code}")
    except Exception as e:
        logger.error(f"Failed to store token in pairing API: {e}")


def _extract_nonce_from_username(username: str) -> str | None:
    """Extract the pairing nonce from a managed bot username.

    Expected format: hermes_{nonce}_bot or hermes_{profile}_{nonce}_bot
    """
    if not username:
        return None
    parts = username.lower().rstrip("_bot").split("_")
    # The nonce is the last segment before _bot
    if len(parts) >= 2 and parts[0] == "hermes":
        return parts[-1]  # Last segment is the random nonce suffix
    return None


def main():
    app = Application.builder().token(MANAGER_TOKEN).build()

    # Register handler for managed_bot updates
    # Note: python-telegram-bot 9.6+ needed for ManagedBotUpdated support
    app.add_handler(
        MessageHandler(filters.StatusUpdate.MANAGED_BOT_CREATED, handle_managed_bot)
    )

    # Also handle the Update.managed_bot field directly
    # (this may need adjustment based on python-telegram-bot's 9.6 implementation)

    logger.info("Hermes Manager Bot started")
    app.run_polling(allowed_updates=["managed_bot", "message"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
```

### Deployment
- **Container:** Single-process Python container
- **Requirements:** `python-telegram-bot>=22.0` (with Bot API 9.6 support), `httpx`
- **Env vars:** `MANAGER_BOT_TOKEN`, `PAIRING_API_URL`, `PAIRING_API_SECRET`
- **Resources:** Minimal — handles maybe a few requests per minute. Smallest available container.
- **Monitoring:** Log to stdout, alert on repeated `getManagedBotToken` failures

---

## Component 3: DNS Configuration

Add a CNAME or A record for `setup.hermes-agent.nousresearch.com` pointing to Cloudflare Workers.

If the domain is already on Cloudflare DNS:
```
setup.hermes-agent.nousresearch.com → Cloudflare Worker route
```

If not, a separate Cloudflare account/zone can host the Worker with a custom domain.

---

## Integration with hermes-agent (PR #10589)

The client-side code in hermes-agent is already built:

- **`hermes_cli/telegram_managed_bot.py`** — QR code rendering, deep link generation, pairing protocol client
- **`hermes_cli/setup.py`** — Setup wizard offers Automatic [1] vs Manual [2] for Telegram
- **Constants** (configurable):
  - `DEFAULT_API_URL = "https://setup.hermes-agent.nousresearch.com"`
  - `DEFAULT_MANAGER_BOT = "HermesSetupBot"`
  - `DEFAULT_POLL_TIMEOUT = 180` (3 minutes)
  - `POLL_INTERVAL = 2` (seconds)

The CLI flow:
1. Generates a 32-char hex nonce
2. Generates a suggested bot username embedding a random suffix
3. Registers the nonce via `POST /pair`
4. Prints a QR code + URL for the deep link
5. Polls `GET /pair/{nonce}` every 2 seconds with an animated spinner
6. On success, saves the token to `.env`
7. Falls back to manual BotFather flow if anything fails

---

## Rate Limits & Scale

- **Telegram:** No documented rate limit on managed bot creation. Each creation requires user confirmation (anti-abuse by design).
- **Cloudflare Worker:** Free tier handles 100k requests/day. At 2 req/sec poll rate × 3 min timeout = ~90 requests per setup. Supports ~1000 concurrent setups before hitting free tier.
- **Manager bot:** Telegram's bot polling has standard rate limits (30 req/sec for getUpdates). Single bot can handle hundreds of concurrent managed bot creations.

**No rate limiting from our side needed initially.** If we see abuse, add IP-based rate limiting on the Worker (10 POST /pair per IP per minute).

---

## Future Enhancements

- **Token rotation CLI command:** `hermes gateway telegram rotate-token` using `replaceManagedBotToken`
- **Multi-profile auto-setup:** Each `hermes -p <name> setup` auto-creates a uniquely-named bot
- **Self-hosted manager bot:** Config option `telegram.manager_bot_token` for users who want to run their own manager bot instead of using the Nous-hosted one
- **Webhook mode:** Switch manager bot from polling to webhook for lower latency in production

---

## Checklist

- [ ] Create `@HermesSetupBot` (or chosen name) via @BotFather
- [ ] Enable Bot Management Mode in BotFather MiniApp
- [ ] Deploy Cloudflare Worker with KV namespace
- [ ] Configure DNS: `setup.hermes-agent.nousresearch.com`
- [ ] Deploy manager bot process
- [ ] Set shared secret between Worker and manager bot
- [ ] Smoke test: run `hermes setup` → Telegram → auto-create bot → verify token arrives
- [ ] Merge client-side PR #10589
