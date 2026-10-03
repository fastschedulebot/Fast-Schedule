"""FAQ open-state x: drawn bars instead of a rotated "+" glyph.

A text "+" rotated 45deg renders off-center (broken-looking x). Two
absolutely-positioned bars sharing one center spin together into a clean x.
Covers the help-hub and blog FAQ variants (the article variant swaps +/-
glyphs without rotation and is untouched).
"""
import io

def load(p):
    return io.open(p, encoding='utf-8', newline='').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('[ok]', p)

def rep_once(p, old, new):
    s = load(p)
    assert s.count(old) == 1, (p, s.count(old), old[:80])
    save(p, s.replace(old, new, 1))

NEW_RULES = """    /* drawn plus (two bars, one shared center) instead of a "+" glyph:
       glyphs rotate off-center and the open-state x looks broken. Both
       bars spin together into a clean x. */
    .hc-faq summary { position: relative; padding-right: 28px; }
    .hc-faq summary::before, .hc-faq summary::after {
      content: ""; position: absolute; top: 50%; background: var(--green-strong);
      border-radius: 2px; transition: transform .25s var(--ease-spring, ease);
    }
    .hc-faq summary::before { right: 1px; width: 14px; height: 2px; transform: translateY(-50%); }
    .hc-faq summary::after { right: 7px; width: 2px; height: 14px; transform: translateY(-50%); }
    .hc-faq details[open] summary::before,
    .hc-faq details[open] summary::after { transform: translateY(-50%) rotate(135deg); }"""

# ---------- help hub variant ----------
rep_once('website/_build/build_help.py',
    """    .hc-faq summary::after {
      content: "+"; flex: none; font-size: 1.35rem; font-weight: 500; line-height: 1;
      color: var(--green-strong); transition: transform .25s;
    }
    .hc-faq details[open] summary::after { transform: rotate(45deg); }""",
    NEW_RULES)

# ---------- blog variant ----------
rep_once('website/_build/build_blog.py',
    """    .hc-faq summary::after { content: "+"; font-size: 1.3rem; color: var(--green-strong);
      transition: transform .25s; flex: none; }
    .hc-faq details[open] summary::after { transform: rotate(45deg); }""",
    NEW_RULES)

print('s23 all done')
