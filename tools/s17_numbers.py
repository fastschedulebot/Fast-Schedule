# s17: use plain readable <ul>-><ol> conversion in build_site.py.
import io

p = 'website/_build/build_site.py'
s = io.open(p, encoding='utf-8').read()
old = ("        # Legal house style: numbered lists instead of bullet dots.\n"
       "        html = html.replace(chr(60)+chr(117)+chr(108)+chr(62), chr(60)+chr(111)+chr(108)+chr(62))"
       ".replace(chr(60)+chr(47)+chr(117)+chr(108)+chr(62), chr(60)+chr(47)+chr(111)+chr(108)+chr(62))")
assert s.count(old) == 1, s.count(old)
new = ("        # Legal house style: numbered lists instead of bullet dots, so every\n"
       "        # body list (including nested ones) renders as <ol>. TOC <ol>s are\n"
       "        # built separately and are unaffected - this only touches md output.\n"
       "        html = html.replace('<ul>', '<ol>').replace('</ul>', '</ol>')")
io.open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(old, new, 1))
print('cleaned')
