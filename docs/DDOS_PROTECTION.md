# DDoS & Attack Protection — Fast Scheduler

This document describes the layered "shield" protecting the Fast Scheduler
public surfaces: the static website (GitHub Pages) and the bot's HTTP server
(webhooks + admin dashboard on Render / AlwaysData / local).

## Architecture of the shield

```
Internet
  │
  ▼
[ Layer 1: Edge / CDN ]            Cloudflare / platform edge — volumetric
  │                                flood absorption, TLS termination, WAF
  ▼
[ Layer 2: Server middleware ]     src/core/http_shield.py — per-IP rate limit,
  │                                auto-ban, concurrency cap, body caps,
  │                                security headers (aiohttp, first middleware)
  ▼
[ Layer 3: Route guards ]          webhook secret tokens, dashboard bearer auth,
  │                                Origin/CSRF checks, per-action rate limits
  ▼
[ Layer 4: Handlers ]              input caps, entity-escaped output, audit logs
```

## Layer 1 — Edge (recommended, deploy-side)

The in-process shield (layer 2) stops abusive *requests*, but a true
volumetric DDoS must be absorbed before it reaches your server. Put a CDN in
front of each surface:

| Surface | Host | Protection |
|---|---|---|
| Website (`website/`) | GitHub Pages | Cloudflare proxy (orange cloud) or Fastly; GitHub Pages itself is DDoS-resistant. Static pages also carry a CSP (see below). |
| Bot webhooks + dashboard | Render / AlwaysData | Cloudflare in front, or at minimum the platform's built-in DDoS protection. |

When a reverse proxy/CDN is in front of the bot, set:

```env
TRUST_PROXY_HEADERS=1
```

so the shield identifies clients by `X-Forwarded-For` / `X-Real-IP` (set by
your proxy) instead of the socket peer (which would otherwise be the proxy's
IP for everyone). Without a trusted proxy, leave it unset — spoofed headers
must never be able to poison the limiter.

Optional hard allow-list for monitoring probes:

```env
SHIELD_ALLOWLIST=203.0.113.7,198.51.100.22
```

### Cloudflare quick-start for the webhook host
1. Proxy the domain (orange cloud).
2. Security → WAF: enable the managed ruleset.
3. Security → Bots: enable bot fight mode.
4. Rate limiting rule: `/webhook/*` allow generous (Telegram bursts),
   `/api/*` strict (e.g. 60/min/IP) — the app shield backs this up anyway.
5. Cache: website assets cached at the edge; `/api/*` and `/webhook/*` never.

## Layer 2 — In-process shield (`src/core/http_shield.py`)

Runs as the FIRST aiohttp middleware for every request:

1. **Per-IP sliding-window rate limit** — 120 req/min per IP (webhooks get a
   separate, larger budget of 1200/min because Telegram bursts updates).
   Over the limit → `429 Too Many Requests` with `Retry-After`.
2. **Automatic bans** — an IP that trips the limit 3× inside 10 minutes is
   banned (10 min, doubling per repeat offence up to 1 h) → `403 Forbidden`.
3. **Concurrency cap** — max 20 in-flight requests per IP; kills slowloris
   / connection-exhaustion clients.
4. **Body-size caps** — `Content-Length` pre-gate (1 MB default) plus aiohttp
   `client_max_size`, plus per-route 64 KB JSON caps on the dashboard.
5. **Security headers** on every response: `X-Content-Type-Options`,
   `X-Frame-Options: DENY`, `Referrer-Policy`, `COOP`, `CORP`,
   `Permissions-Policy`, API `Content-Security-Policy: default-src 'none'`,
   `Cache-Control: no-store`.
6. **Error middleware** — unhandled exceptions become a terse JSON 500, never
   a traceback page.
7. **/health is exempt** and returns only `{"status": "ok"}` — no version,
   uptime or app-count fingerprinting.

### Env knobs (all optional)

| Variable | Default | Meaning |
|---|---|---|
| `SHIELD_MAX_REQ` | `120` | Max requests per IP per window (non-webhook) |
| `SHIELD_WINDOW` | `60` | Window seconds |
| `SHIELD_WEBHOOK_MAX_REQ` | `1200` | Max requests per IP per window on `/webhook/*` |
| `SHIELD_BAN_THRESHOLD` | `3` | Violations inside the tracking window before a ban |
| `SHIELD_BAN_TRACK_WINDOW` | `600` | Violation tracking window (s) |
| `SHIELD_BAN_SECONDS` | `600` | Base ban duration (s) |
| `SHIELD_BAN_MAX_SECONDS` | `3600` | Ban escalation cap (s) |
| `SHIELD_MAX_CONCURRENT` | `20` | Max in-flight requests per IP |
| `SHIELD_MAX_BODY` | `1048576` | Max request body bytes |
| `SHIELD_ALLOWLIST` | *(empty)* | Comma-separated IPs never limited |
| `TRUST_PROXY_HEADERS` | *(off)* | `1` when behind a trusted reverse proxy |

Tune `SHIELD_MAX_REQ` / `SHIELD_WEBHOOK_MAX_REQ` upward if legitimate traffic
grows; the defaults deliberately shed aggressive clients, not real users.

## Layer 3 — Route guards (already in the code)

- **Webhooks**: path keys derived from the bot token (`m_<sha24>`,
  `sb_<sha16>`) — unguessable; `X-Telegram-Bot-Api-Secret-Token` validated in
  constant time, always on in webhook mode; per-key failure circuit breaker
  sheds hammering on unknown/bad paths; malformed updates never crash the
  dispatcher.
- **Dashboard**: bearer-token auth (`ADMIN_DASHBOARD_TOKEN`, constant-time
  compare), deny-by-default when unset; Origin/CSRF allow-list
  (`ALLOWED_ORIGINS`); per-IP 60 req/min action limiter; every mutating
  endpoint audited.
- **CryptoBot payments**: HMAC signature verification before any state change.

## Layer 4 — Output & input hardening

- Help-center search (website + build generators): strict entity-encoding
  (`& < > " '`), highlighting done by escaping literal text and injecting
  only fixed `<mark>` tags — no HTML stripping, no injection path.
- Static pages ship `Content-Security-Policy` with `base-uri 'self'`,
  `frame-ancestors 'self'`, `upgrade-insecure-requests`,
  `object-src 'none'`, `form-action 'self'`, plus
  `referrer strict-origin-when-cross-origin`.
- All external links use `rel="noopener noreferrer"`.
- Dashboard text caps (500/4000/64-char limits) and validated JSON bodies
  (`isinstance(dict)` checks) on every mutating endpoint.

## Verification

```bash
# Shield unit checks (9 groups)
PYTHONPATH=. python tests/security/sim_http_shield.py

# Full middleware stack over real HTTP (flood → 429 → ban, headers, 413)
PYTHONPATH=. python tests/security/sim_web_shield_integration.py

# All security sims
PYTHONPATH=. python tests/security/run_all.py
```

## Incident playbook

1. Check `/health` — still `ok`? The process is alive; the shield is shedding.
2. Platform logs: grep `[SHIELD]` for ban events and `IP ... banned` lines.
3. Massive volumetric attack → enable "Under Attack" mode at the CDN; the
   origin shield keeps working underneath.
4. A specific abusive IP range → add to the CDN block list (preferred) or a
   deny rule at the platform; the app shield handles the rest.
5. False positives (a shared NAT tripping limits) → raise `SHIELD_MAX_REQ`
   or add the NAT IP to `SHIELD_ALLOWLIST`.
