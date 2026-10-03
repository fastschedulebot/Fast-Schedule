"""Remove the Help row + quick-search popover from the main page settings menu.

The main page keeps its own navbar (with Blog/Help links), so the settings
Help row is redundant. Applies to both index copies.
"""
import io

for p in ('website/index.html', 'index.html'):
    s = io.open(p, encoding='utf-8', newline='').read()
    start = s.find('<span class="site-menu-wrap">')
    assert start != -1, p
    assert s.count('<span class="site-menu-wrap">') == 1, (p, s.count('<span class="site-menu-wrap">'))
    close = s.find('\n          </span>', start)
    assert close != -1, p
    # include the 10-space indent before <span
    assert s[start - 10:start] == '          ', repr(s[start - 10:start])
    removed = s[start:close]
    assert 'id="siteMenu"' in removed and 'site-menu-row' in removed, p
    s = s[:start - 10] + s[close + len('\n          </span>'):]
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('[ok]', p, 'removed %d chars' % len(removed))
