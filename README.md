# Fast Scheduler Website

This folder contains the static website published with GitHub Pages.

## Pages

- `index.html` — minimal landing page with the bot name, Telegram link, and legal-document links.
- `legal/privacy.html` — Privacy Policy.
- `legal/terms.html` — Terms of Service.
- `legal/refundpolicy.html` — Refund Policy.

The landing page currently opens:

```text
https://t.me/FastSchedulerBot
```

The legal links use relative paths, so they work when this complete folder is published as one website.

## Shared website files

- `styles/main.css` — shared stylesheet for the legal pages.
- `scripts/` — scripts used by the legal pages.
- `_build/build_site.py` — generator that builds the legal HTML pages from the Markdown sources in `../docs/`.

## Regenerating legal pages

From the repository root, run:

```bash
python website/_build/build_site.py
```

This regenerates:

```text
website/legal/privacy.html
website/legal/terms.html
website/legal/refundpolicy.html
```

It also updates the generated website configuration used by the legal pages.

## GitHub Pages

Publish the `website/` folder as the GitHub Pages source, or copy its contents to the selected Pages branch/folder while preserving this structure:

```text
website/
├── index.html
├── README.md
├── legal/
│   ├── privacy.html
│   ├── terms.html
│   └── refundpolicy.html
├── scripts/
├── styles/
│   └── main.css
└── _build/
```

For GitHub Pages, the public landing page will normally be available at:

```text
https://<github-user-or-organization>.github.io/<repository-name>/
```

The exact URL depends on the GitHub account, repository name, and Pages settings. If a custom domain is configured, use that domain instead.

Do not publish secret files, `.env` files, databases, logs, virtual environments, or local runtime data with this static website.
