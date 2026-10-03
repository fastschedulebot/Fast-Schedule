"""Keep the unified navbar's right Open Bot CTA visible on phones.

Two pre-existing generic rules hide every .nav-cta on small screens
(designed for old article headers). The unified navbar must keep one
compact CTA on the right, like the spec screenshot.
"""
import io

ANCHOR = '@media (max-width: 640px) { .nav-unified .nav-left .nav-cta { display: none; } }'
ADD = (ANCHOR + '\n'
       '@media (max-width: 760px) {\n'
       '  .nav-unified .nav-right .nav-cta { display: inline-flex; padding: 8px 12px; font-size: .82rem; }\n'
       '  .nav-unified .nav-right .nav-cta kbd { display: none; }\n'
       '}')
for p in ('website/styles/main.css', 'styles/main.css'):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(ANCHOR) == 1, (p, s.count(ANCHOR))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(ANCHOR, ADD, 1))
    print('[ok]', p)
