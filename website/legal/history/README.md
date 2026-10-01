# Legal version history

Each public legal page keeps every published version. By default visitors
see the current version (`../<name>.html`); the version switcher under the
"Last updated" line links to archived snapshots in this directory.

## Files

`<name>-<YYYY-MM-DD>.html` — full snapshot of the page as published on that
date (e.g. `privacy-2026-09-26.html`). Snapshots are `noindex` (they must
not compete with the current version in search) and carry the `archived`
article class (opts out of Russian body translation — archives stay in
their original language).

## Publishing a new version

1. Copy the current `website/legal/<name>.html` to
   `history/<name>-<new-date>.html` **before** editing the current page.
2. Run `py -3 tools/build_legal_history.py` from the repo root — it fixes
   asset/peer links, stamps `noindex`, the archive banner, the switcher,
   and the current `lang.js` version. (For a brand-new date, add it to the
   `VERSIONS` list in the script and update the banner/switcher labels.)
3. Edit the current page, bump its "Last updated" (and "Effective") line.
4. Commit both the snapshot and the updated page together.
