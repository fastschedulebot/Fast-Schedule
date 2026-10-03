"""Render the pasted screenshot as ASCII art + color summary."""
import os
from PIL import Image

d = os.path.expandvars(r'C:\Users\MAX\AppData\Local\Temp\freebuff-desktop-pastes')
print('dir exists:', os.path.isdir(d))
if os.path.isdir(d):
    print(sorted(os.listdir(d))[-5:])

p = os.path.join(d, 'paste-1790963312354-20520.png')
print('file exists:', os.path.isfile(p))
im = Image.open(p).convert('RGB')
print('size:', im.size)
W, H = 100, 50
small = im.resize((W, H))
chars = ' .:-=+*#%@'
px = small.load()
for y in range(H):
    print(''.join(chars[min(9, int(sum(px[x, y]) / 3 * 10 / 256))] for x in range(W)))
