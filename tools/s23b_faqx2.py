"""Article FAQ variant: same drawn-bars treatment (line-based, no escapes)."""
import io

p = 'website/_build/build_help.py'
lines = io.open(p, encoding='utf-8', newline='').read().split('\n')
a = next(i for i, l in enumerate(lines) if 'summary::after { content: "+"; float: right;' in l)
assert lines[a + 1].strip().startswith('.hc-faq details[open] summary::after { content:'), lines[a + 1]
new_block = """    .hc-faq summary { position: relative; padding-right: 28px; }
    .hc-faq summary::before, .hc-faq summary::after {
      content: ""; position: absolute; top: 50%; background: var(--green-strong);
      border-radius: 2px; transition: transform .25s var(--ease-spring, ease);
    }
    .hc-faq summary::before { right: 1px; width: 14px; height: 2px; transform: translateY(-50%); }
    .hc-faq summary::after { right: 7px; width: 2px; height: 14px; transform: translateY(-50%); }
    .hc-faq details[open] summary::before,
    .hc-faq details[open] summary::after { transform: translateY(-50%) rotate(135deg); }"""
lines[a:a + 2] = new_block.split('\n')
io.open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('[ok]', p)
