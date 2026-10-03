"""Show-more button: square corners, docked to the right end of the last row.

- .hc-more: border-radius 999px -> 10px.
- Chips/others (flex-wrap rows): button moves INSIDE the box as the last
  item, pushed right with margin-left:auto, vertically centered.
- Article rows (full-width blocks): button moves inside the box, the box
  becomes a flex column, button aligns to the right end below the rows.
- Toggle handlers find the box via closest() so the moved button keeps
  working; setup stays idempotent across re-runs.
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

BH = 'website/_build/build_help.py'
BB = 'website/_build/build_blog.py'

# ---------- 1. help CSS ----------
rep_once(BH,
    """    .hc-more { display: inline-flex; align-items: center; gap: 8px; margin: 6px 0 0; font: inherit;
      font-size: .88rem; font-weight: 700; color: var(--green-strong); background: var(--surface);
      border: 1px solid var(--border); border-radius: 999px; padding: 9px 18px; cursor: pointer; }""",
    """    .hc-more { display: inline-flex; align-items: center; gap: 8px; margin: 6px 0 0; font: inherit;
      font-size: .88rem; font-weight: 700; color: var(--green-strong); background: var(--surface);
      border: 1px solid var(--border); border-radius: 10px; padding: 9px 18px; cursor: pointer; }
    /* docked to the right end: inside chips/others rows it rides beside the
       last item (vertically centered); inside article lists it right-aligns
       under the rows (the rows are full-width links, so the button gets its
       own right-aligned row). */
    .hc-chips.has-more, .hc-others.has-more { align-items: center; }
    .hc-chips > .hc-more, .hc-others > .hc-more { margin: 0 0 0 auto; align-self: center; flex: none; }
    [data-list].has-more { display: flex; flex-direction: column; }
    [data-list] > .hc-more { align-self: flex-end; margin: 10px 0 0; }""")

# ---------- 2. help setupMore: move button inside box ----------
rep_once(BH,
    """    function setupMore(scopeSel, itemSel, keep) {
      Array.prototype.forEach.call(document.querySelectorAll(scopeSel), function (box) {
        var items = box.querySelectorAll(itemSel);
        var btn = box.nextElementSibling;
        if (items.length > keep && btn && btn.hasAttribute('data-more')) {
          box.classList.add('is-collapsed');
          btn.hidden = false;
        } else if (btn && btn.hasAttribute('data-more')) {
          btn.hidden = true;
        }
      });
    }""",
    """    function setupMore(scopeSel, itemSel, keep) {
      Array.prototype.forEach.call(document.querySelectorAll(scopeSel), function (box) {
        var items = box.querySelectorAll(itemSel);
        var btn = box.querySelector(':scope > [data-more]') || box.nextElementSibling;
        if (items.length > keep && btn && btn.hasAttribute('data-more')) {
          box.classList.add('is-collapsed');
          box.classList.add('has-more');
          if (btn.parentElement !== box) box.appendChild(btn);
          btn.hidden = false;
        } else if (btn && btn.hasAttribute('data-more')) {
          btn.hidden = true;
        }
      });
    }""")

# ---------- 3. help toggle: closest() finds moved button's box ----------
rep_once(BH,
    """      var mb = ev.target.closest('[data-more]');
      if (mb) {
        var box = mb.previousElementSibling;""",
    """      var mb = ev.target.closest('[data-more]');
      if (mb) {
        var box = mb.closest('[data-list],[data-others],[data-chips-more]') || mb.previousElementSibling;""")

# ---------- 4. blog CSS ----------
rep_once(BB,
    """    .hc-more { display: inline-flex; align-items: center; gap: 8px; margin: 12px 0 0; font: inherit;
      font-size: .88rem; font-weight: 700; color: var(--green-strong); background: var(--surface);
      border: 1px solid var(--border); border-radius: 999px; padding: 9px 18px; cursor: pointer; }""",
    """    .hc-more { display: inline-flex; align-items: center; gap: 8px; margin: 12px 0 0; font: inherit;
      font-size: .88rem; font-weight: 700; color: var(--green-strong); background: var(--surface);
      border: 1px solid var(--border); border-radius: 10px; padding: 9px 18px; cursor: pointer; }
    /* docked to the right end of the chips row, beside the last chip */
    .hc-chips.has-more { align-items: center; }
    .hc-chips > .hc-more { margin: 0 0 0 auto; align-self: center; flex: none; }""")

# ---------- 5. blog setup + toggle ----------
rep_once(BB,
    """      document.querySelectorAll('[data-chips-more]').forEach(function (box) {
        var btn = box.nextElementSibling;
        var need = box.querySelectorAll('.hc-chip').length > 3;
        box.classList.toggle('is-collapsed', need);
        if (btn && btn.hasAttribute('data-more')) btn.hidden = !need;
      });""",
    """      document.querySelectorAll('[data-chips-more]').forEach(function (box) {
        var btn = box.querySelector(':scope > [data-more]') || box.nextElementSibling;
        var need = box.querySelectorAll('.hc-chip').length > 3;
        box.classList.toggle('is-collapsed', need);
        if (btn && btn.hasAttribute('data-more')) {
          if (need) { box.classList.add('has-more'); if (btn.parentElement !== box) box.appendChild(btn); }
          btn.hidden = !need;
        }
      });""")
rep_once(BB,
    """      var mb = e.target.closest && e.target.closest('[data-more]');
      if (!mb) return;
      var box = mb.previousElementSibling;""",
    """      var mb = e.target.closest && e.target.closest('[data-more]');
      if (!mb) return;
      var box = (mb.closest && mb.closest('[data-chips-more]')) || mb.previousElementSibling;""")

print('s21 all done')
