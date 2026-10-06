#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Part 4: full RU help-hub assembly (surgery + transform + head)."""

import io
import os
import re

from build_ru_pages import SITE, BASE, transform, set_head, fix_asset_paths
from build_ru_pages2 import rebuild_hub_ld, inject_alts, _write
from build_ru_pages3 import merged_map, apply_surgery


def build_help_hub_full(MAP, patch, en_data, audit_only=False):
    src = os.path.join(SITE, 'help.html')
    html = io.open(src, encoding='utf-8').read()
    html, stats = apply_surgery(html, patch, en_data)
    html = rebuild_hub_ld(html, patch)
    html, unmapped = transform(html, merged_map(MAP))
    m = re.search(r'scripts/help-data\.js\?v=([^"]+)', html)
    ver = m.group(1) if m else '20261005a1'
    html = html.replace('scripts/help-data.js?v=' + ver,
                        'scripts/help-data-ru.js?v=' + ver)
    html = fix_asset_paths(html)
    from build_ru_pages2 import HUB_TITLE_RU, HUB_DESC_RU
    html = set_head(html, HUB_TITLE_RU, HUB_DESC_RU,
                    BASE + '/ru/help.html', BASE + '/help.html')
    if audit_only:
        return None, unmapped, stats
    out = os.path.join(SITE, 'ru', 'help.html')
    _write(out, html)
    inject_alts(src, BASE + '/ru/help.html', BASE + '/help.html')
    return out, unmapped, stats
