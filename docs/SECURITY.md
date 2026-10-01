# Security Hardening Report

## Overview

This document describes the security measures implemented in the Fast Scheduler & SetDate Telegram bot. The goal is to protect sensitive data (bot tokens, user information, premium status) even if an attacker gains access to the server.

---

## 1. Bot Token Encryption (CRITICAL)

**Before:** Bot tokens were stored in **plaintext** in `src/token_manager.json`.

**After:** All bot tokens are encrypted using **AES-256-GCM** before being written to disk.

### How it works:
- **Encryption key** (`TOKEN_ENCRYPTION_KEY`) is stored in `.env`, **never** in code.
- Key is a base64-encoded 256-bit (32-byte) random value, generated automatically on first run by `run.py`.
- Each token gets a unique 12-byte random IV (initialization vector).
- AES-256-GCM provides authenticated encryption (integrity + confidentiality).
- Tokens are decrypted **in memory only** when read from the database.
- Plaintext tokens are **never** written back to disk.

### Key Rotation:
To rotate the encryption key:
1. Decrypt all tokens using the old key (via `decrypt_tokens.py --key OLD_KEY --output decrypted.json`)
2. Update `TOKEN_ENCRYPTION_KEY` in `.env` with the new key
3. Delete `src/token_manager.json` (the bot will re-encrypt tokens as users reconnect them)

---

## 2. Token File Protection

**Before:** `token_manager.json` had default filesystem permissions (world-readable on some systems).

**After:**
- `run.py` sets **0600** permissions (owner read/write only) on `.env`, `token_manager.json`, and all data files.
- Data directories get **0700** permissions.
- On Windows, these permissions are advisory (NTFS ACLs); on Linux/macOS, they are enforced by the kernel.

---

## 3. Admin Decryption Tool

**File:** `decrypt_tokens.py`

A standalone script that allows the bot creator to decrypt and view the token database.

### Usage:
```bash
# Read key from .env (default)
python decrypt_tokens.py

# Specify a different .env file
python decrypt_tokens.py --env /path/to/.env

# Provide key directly
python decrypt_tokens.py --key YOUR_BASE64_KEY

# Write to file instead of stdout
python decrypt_tokens.py -o decrypted.json

# Pretty-print
python decrypt_tokens.py --pretty
```

### Security:
- Does NOT require the bot to be running.
- Can only decrypt tokens on the machine where the `.env` file (with `TOKEN_ENCRYPTION_KEY`) is accessible.
- The key is kept in memory only; it is never written to a file by this script.

---

## 4. Admin Password Authentication

**New Setting:** `ADMIN_PASSWORD` in `.env`

If set, sensitive admin operations (granting premium, broadcasting, etc.) require both:
1. Telegram user ID in `ADMIN_IDS` list
2. The correct `ADMIN_PASSWORD` value

If `ADMIN_PASSWORD` is left empty, only the Telegram user ID check is performed (backward-compatible).

---

## 5. Rate Limiting

**Before:** Only daily message send limit existed.

**After:** Action-specific rate limiting has been added:
- **Storage creation**: max 3 times per minute
- More actions can be rate-limited by calling `check_action_rate_limit(user_id, action_name, max_per_minute)`

Rate limits are in-memory (reset on bot restart) and per-user.

---

## 6. Error Handling

**Before:** Full stack traces could potentially be exposed to users.

**After:**
- The `global_error_handler` sends a generic error message to the user: *"An internal error occurred. The admin has been notified."* — never exposing stack traces.
- Full error details (including stack traces) are logged to the admin issue log and sent to admin via Telegram.
- The error type (e.g., `BadRequest`, `TimedOut`) is included in the user-facing message for basic context.

---

## 7. Secure Logging

**Before:** Tokens could potentially appear in debug logs.

**After:**
- `redact_token()` function replaces all but first 4 and last 4 characters of tokens with `...`.
- Token manager now uses `redact_token()` when logging token-related events.
- Sensitive actions (token storage, removal, subscription changes) are explicitly logged with user ID.
- Never log plaintext tokens.
- Logs are stored in `data/logs/bot_debug.log` with rotation (2 MB, 2 backups).

---

## 8. Deep Link Security

**New Setting:** `DEEP_LINK_SECRET` in `.env`

Deep links (`/start=...`) can now be signed with an HMAC-SHA256 signature to prevent tampering.

### Functions:
- `sign_deep_link(payload)` — appends `.sig` to payload
- `verify_deep_link(signed)` — verifies signature, returns payload if valid, `None` if tampered
- `sanitize_deep_link_param(param)` — strips non-alphanumeric characters

Deep link validation is available but not yet enforced on all deep link paths (requires per-path integration).

---

## 9. Input Validation

**Added:**
- `validate_bot_token(token)` — regex validation for token format (`123456:ABCdef...`)
- `sanitize_deep_link_param(param)` — strips dangerous characters from deep link parameters

The `onboard_bot.py` already validates tokens via Telegram's `get_me()` API before storing.

---

## 10. Dependency Security

**Required libraries** (all already in `requirements.txt`):
- `cryptography>=41.0.0` — provides AES-256-GCM encryption
- `python-dotenv>=1.0.0` — loads `.env` configuration
- `python-telegram-bot[job-queue]>=22.7` — Telegram Bot API framework (all requests use HTTPS by default)

**Recommended audit tools** (not yet in requirements):
```bash
pip install pip-audit
pip-audit  # check for known vulnerabilities
```

---

## 11. Auto-Generated Keys

On first run, `run.py` automatically:
1. Generates a `TOKEN_ENCRYPTION_KEY` (256-bit random, base64-encoded)
2. Generates a `DEEP_LINK_SECRET` (64-char hex)
3. Writes both to `.env`
4. Sets restrictive file permissions (0600 on sensitive files)
5. Migrates any existing plaintext tokens to encrypted format

---

## 12. New Files Created

| File | Purpose |
|------|---------|
| `src/security.py` | Encryption, signing, rate limiting, validation utilities |
| `decrypt_tokens.py` | Admin tool to decrypt and view token database |
| `.env.example` | Template for `.env` (documentation, no real secrets) |
| `SECURITY.md` | This documentation file |

---

## 13. Files Modified

| File | Changes |
|------|---------|
| `src/token_manager.py` | Added encryption/decryption of token field on save/load; added `check_token_validity()`; added redacted logging |
| `src/main.py` | Added security module imports; added rate limiting to storage creation; improved error handler (no stack traces to users) |
| `run.py` | Added `init_security()` and `migrate_tokens_to_encrypted()` auto-generation and migration |
| `.env` | Added `TOKEN_ENCRYPTION_KEY`, `DEEP_LINK_SECRET`, `ADMIN_PASSWORD` placeholders |

---

## 14. Remaining Recommendations (Future Work)

1. **Token Health Checks**: Schedule periodic `check_token_validity()` calls to detect revoked tokens and notify users.
2. **Full Deep Link Signing**: Enforce `verify_deep_link()` on all incoming deep link paths.
3. **Admin 2FA**: Add Telegram confirmation code as second factor for admin login.
4. **Database Encryption at Rest**: Encrypt the entire `data/` directory using e.g. SQLCipher or eCryptfs.
5. **Fail2Ban**: Configure fail2ban for webhook endpoints.
6. **Regular Audits**: Run `pip-audit` and `bandit` regularly.
7. **Webhook Firewall**: Restrict webhook endpoints to known IPs (Telegram, CryptoBot).
