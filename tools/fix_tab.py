"""Fix legal doc-tab active state (callers pass 'privacy.html', tabs use 'privacy')."""
import io

p = 'website/_build/build_site.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = """    def tab(href, label, doc):
        cls = 'doc-tab active' if doc == current else 'doc-tab'
        return f'<a class="{cls}" href="{href}">{label}</a>'"""
assert s.count(old) == 1, s.count(old)
new = """    def tab(href, label, doc):
        cls = 'doc-tab active' if current in (doc, doc + '.html') else 'doc-tab'
        return f'<a class="{cls}" href="{href}">{label}</a>'"""
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('tab fixed')
