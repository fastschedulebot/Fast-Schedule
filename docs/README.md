# Telegram Parser

This repository includes `tg_parser.py` — an async, robust Telegram channel parser with features:

- Concurrent parsing of multiple channels
- Duplicate detection (hash-based) and a `seen_messages.json` DB
- Blocked words and regex filters (skips messages containing them)
- Removal patterns to delete parts of post text before saving
- Multi-format saving: JSON, TXT, CSV (configurable)
- Media downloading with concurrency control and FloodWait handling
- Configurable via `parser_config.json` or environment variables

Getting started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure credentials either in `parser_config.json` or using env vars:

Windows PowerShell example:

```powershell
$env:TELEGRAM_API_ID=30542455
$env:TELEGRAM_API_HASH="cab61bb85328aa3c9de88ba8a779127c"
```

3. Run parser:

```bash
python "tg_parser.py" --config parser_config.json --channels channel1,channel2
```

Or provide a path to a file containing channel identifiers (one per line):

```bash
python "tg_parser.py" --channels channels_list.txt
```

Notes

- This tool reads public channels or those the logged-in account can access. It does not perform scraping that violates Telegram policies. Avoid mass automated actions that emulate abusive behaviour.
- The script only downloads media and saves local copies; it does not delete or modify remote messages.
