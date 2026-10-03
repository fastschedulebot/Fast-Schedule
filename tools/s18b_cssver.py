# s18b: mirror unified-nav CSS to website copy; bump main.css version.
import io

OLD_V = '20261002c2'
NEW_V = '20261002c3'

src = io.open('styles/main.css', encoding='utf-8').read()
i = src.find('Unified navbar')
start = src.rfind('\n/* ----------', 0, i)
endmark = '.nav-unified .nav-group { gap: 8px; }\n}'
end = src.find(endmark, i) + len(endmark)
block = src[start:end]
assert '.nav-unified' in block

dst = io.open('website/styles/main.css', encoding='utf-8').read()
anchor = '.brand { display: flex; align-items: center; gap: 10px; font-weight: 800; margin-right: auto; }'
assert dst.count(anchor) == 1 and 'Unified navbar' not in dst
dst = dst.replace(anchor, anchor + '\n' + block, 1)
io.open('website/styles/main.css', 'w', encoding='utf-8', newline='\n').write(dst)
print('css mirrored')

for p in ['website/_build/build_help.py', 'website/_build/build_blog.py',
          'website/_build/build_static.py', 'website/_build/build_site.py',
          'website/index.html']:
    s = io.open(p, encoding='utf-8').read()
    n = s.count('main.css?v=' + OLD_V)
    assert n >= 1, (p, n)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(
        s.replace('main.css?v=' + OLD_V, 'main.css?v=' + NEW_V))
    print('[ok]', p.split('/')[-1], 'x%d' % n)
print('s18b done')
