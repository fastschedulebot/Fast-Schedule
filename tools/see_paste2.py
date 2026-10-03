"""Render recent pastes as ASCII art for context."""
import os
from PIL import Image

d = os.path.expandvars(r'C:\Users\MAX\AppData\Local\Temp\freebuff-desktop-pastes')
for name in ['paste-1790963128046-20520.png', 'paste-1790957805099-20520.png']:
    p = os.path.join(d, name)
    if not os.path.isfile(p):
        print(name, 'missing')
        continue
    im = Image.open(p).convert('RGB')
    print('=' * 100)
    print(name, im.size)
    W, H = 100, 34
    small = im.resize((W, H))
    chars = ' .:-=+*#%@'
    px = small.load()
    for y in range(H):
        print(''.join(chars[min(9, int(sum(px[x, y]) / 3 * 10 / 256))] for x in range(W)))
