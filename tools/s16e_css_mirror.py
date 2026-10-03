# s16e: mirror the global font CSS block into website/styles/main.css.
import io

src = io.open('styles/main.css', encoding='utf-8').read()
i = src.find('Global font size')
start = src.rfind('\n/* ----------', 0, i)
endmark = '.hc-fonts button:nth-child(3) { font-size: 1.12rem; }'
end = src.find(endmark, i) + len(endmark)
block = src[start:end]
assert 'html[data-font=' in block

dst = io.open('website/styles/main.css', encoding='utf-8').read()
anchor = '.gp-row:focus-visible, .gp-row[role="switch"]:focus-visible { outline: 2px solid var(--green); outline-offset: 2px; }'
assert dst.count(anchor) == 1 and 'Global font size' not in dst
dst = dst.replace(anchor, anchor + block, 1)
io.open('website/styles/main.css', 'w', encoding='utf-8', newline='\n').write(dst)
print('css mirrored, block len', len(block))
