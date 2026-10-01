# Render deployment

This project is configured for a single Render Web Service. The service exposes the
Telegram webhook and the `/health` endpoint from the same `aiohttp` server.

## Recommended service settings

- **Build command:** `pip install --disable-pip-version-check --no-cache-dir -r requirements.txt`
- **Start command:** `python -u run.py`
- **Health check path:** `/health`
- **Mode:** `BOT_MODE=webhook`
- **Port:** Render's `PORT` value, also set as `WEBHOOK_PORT`
- **Persistence:** attach a persistent disk mounted at `/opt/render/project/src/data`, or configure an external durable backend such as Turso/Postgres.

`render.yaml` contains the non-secret defaults. Copy the secret variables into the
Render dashboard and never commit them.

## Required environment variables

```text
MAIN_BOT_TOKEN=...
BASE_URL=https://your-service.onrender.com
TOKEN_ENCRYPTION_KEY=...
FILE_ENCRYPTION_KEY=...
DEEP_LINK_SECRET=...
ADMIN_IDS=...
ADMIN_DASHBOARD_TOKEN=...
```

The deployment defaults to SQLite because it reduces JSON rewrite churn. SQLite is
safe for this deployment only when the service has one instance and its `data`
directory is persistent. For a service that may move between instances, use Turso or
Postgres instead.

## Resource-saving switches

The launcher keeps all three bots enabled by default. If a bot is not needed, disable
its process to reduce memory and CPU usage:

```text
RUN_SETDATE_BOT=0
RUN_SUPPORT_BOT=0
```

Do not disable SetDate if users depend on the separate scheduling bot. Do not disable
SupportBot if the main bot redirects support and feedback there.

## Bandwidth advice

Hobby includes 5 GB/month before overage. Keep media on Telegram where possible by
reusing Telegram `file_id` values. Avoid using Render as a media proxy, and monitor
large imports, archive downloads, broadcasts, and media compression. The service
should be upgraded or media functionality limited if those operations regularly
approach the monthly allowance.

## Persistent disk warning

A Render disk is not included automatically by the Blueprint. Add one in the Render
service settings and mount it at:

```text
/opt/render/project/src/data
```

The application reads `DATA_DIR`, so the same mount path is used by the main bot,
SetDate, SQLite, logs, backups, and shared session files. Keep a separate encrypted
backup outside Render as well.

## Small-instance operation

The smallest compute instance can run the bot at low traffic, but media compression,
large exports, imports, and broadcasts are CPU/memory intensive. Start with at least
0.5 vCPU and 1 GB RAM when possible. If staying on the smallest instance, consider
disabling unused bot processes and limiting media-heavy features.
