"""Fix f-string single-quote nesting in build_site.py _cta (s20 P6)."""
import io

p = 'website/_build/build_site.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = """    _cta = (f'<a class="btn btn-primary nav-cta has-tip" '
            f'data-tip="Opens the bot in Telegram. The page you came from is recorded for first-time users." '
            f'href="{BOT_DEEP_LINK}?start=start__legal" target="_blank" '
            f'rel="noopener noreferrer">{svg('send')}<span>Open Bot</span>'
            f'<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>')"""
assert s.count(old) == 1, s.count(old)
new = """    _cta = (f'''<a class="btn btn-primary nav-cta has-tip" '''
            f'''data-tip="Opens the bot in Telegram. The page you came from is recorded for first-time users." '''
            f'''href="{BOT_DEEP_LINK}?start=start__legal" target="_blank" '''
            f'''rel="noopener noreferrer">{svg('send')}<span>Open Bot</span>'''
            f'''<kbd class="tab-kbd" aria-hidden="true">B</kbd></a>''')"""
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('cta fixed')
