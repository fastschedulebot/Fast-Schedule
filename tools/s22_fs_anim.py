"""Fullscreen focus mode: hiding chrome animates instead of snapping.

- Navbar slides up (same transform + negative-margin trick as scroll-hide,
  so content glides up; base transition already exists in main.css).
- Floating bits (progress, fab, rail, side-reveal) fade (+rise).
- In-flow blocks (footer, cta, pager, rail, sidebar) fade, then release
  space via display allow-discrete (older browsers: instant, as before).
- Sidebar reuses its margin-collapse slide on desktop; the shell stays
  flex in fs so the collapse glides instead of jumping.
- Motion-off needs no gating: the global kill (transition-duration .001s)
  makes all of this instant when Animations are disabled.
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

# ---------- 1. replace the instant-hide block ----------
rep_once(BH,
    """    html.hc-fs header.site, html.hc-fs footer.site, html.hc-fs .hc-side, html.hc-fs .hc-side-reveal,
    html.hc-fs .hc-rail, html.hc-fs .hc-fab, html.hc-fs .hc-progress, html.hc-fs .hc-hsearch,
    html.hc-fs .hc-cta, html.hc-fs .hc-pager { display: none !important; }
    html.hc-fs .hc-shell { display: block; }""",
    """    /* ---- fullscreen focus mode: chrome hides WITH animation ----
       The navbar slides up (same transform + negative-margin trick as
       scroll-hide, so the article glides up to fill the space); floating
       bits fade; in-flow blocks fade, then release space via display
       allow-discrete (older browsers fall back to the old instant hide).
       The search field lives inside the header, so it rides along. The
       shell stays flex so the collapsing sidebar glides (as when the
       sidebar is closed normally) instead of jumping. */
    html.hc-fs header.site { transform: translateY(-100%); margin-bottom: calc(-1 * var(--nav-h, 65px)); }
    html.hc-fs .hc-progress, html.hc-fs .hc-fab, html.hc-fs .hc-rail, html.hc-fs .hc-side-reveal {
      opacity: 0; visibility: hidden; pointer-events: none;
      transition: opacity .3s var(--ease-apple), transform .35s var(--ease-apple), visibility 0s .4s; }
    html.hc-fs .hc-fab, html.hc-fs .hc-rail, html.hc-fs .hc-side-reveal { transform: translateY(10px); }
    html.hc-fs footer.site, html.hc-fs .hc-cta, html.hc-fs .hc-pager, html.hc-fs .hc-rail {
      display: none; opacity: 0; visibility: hidden;
      transition: opacity .3s var(--ease-apple), display 0s .35s allow-discrete, visibility 0s .35s; }
    html.hc-fs .hc-side { display: none; opacity: 0; visibility: hidden; pointer-events: none;
      transition: opacity .3s var(--ease-apple), display 0s .45s allow-discrete, visibility 0s .45s; }
    @media (min-width: 1021px) {
      html.hc-fs .hc-side { margin-left: -284px; }
    }""")

# ---------- 2. base transitions so the way BACK also glides ----------
rep_once(BH,
    """    .hc-progress {
      position: fixed; top: var(--hc-head); left: 0; height: 3px; width: 0;
      background: var(--green);
      z-index: 60; border-radius: 0 3px 3px 0; pointer-events: none;
      transition: top .32s var(--ease-apple, ease);
    }""",
    """    .hc-progress {
      position: fixed; top: var(--hc-head); left: 0; height: 3px; width: 0;
      background: var(--green);
      z-index: 60; border-radius: 0 3px 3px 0; pointer-events: none;
      transition: top .32s var(--ease-apple, ease), opacity .3s, visibility 0s;
    }""")
rep_once(BH,
    """      box-shadow: 0 10px 26px color-mix(in srgb, var(--green) 45%, transparent);
      transition: background .18s, box-shadow .22s, color .18s;
    }""",
    """      box-shadow: 0 10px 26px color-mix(in srgb, var(--green) 45%, transparent);
      transition: background .18s, box-shadow .22s, color .18s, opacity .3s, visibility 0s,
        transform .35s var(--ease-apple);
    }""")
rep_once(BH,
    """      background: var(--surface);
      border: 1px solid var(--border); cursor: pointer;
      box-shadow: var(--shadow-sm); transition: border-color .2s, color .2s;
    }""",
    """      background: var(--surface);
      border: 1px solid var(--border); cursor: pointer;
      box-shadow: var(--shadow-sm); transition: border-color .2s, color .2s, opacity .3s,
        visibility 0s, transform .35s var(--ease-apple);
    }""")

# ---------- 3. base transitions for cta/pager/rail (no existing ones to clash) ----------
rep_once(BH,
    "    /* ---- fullscreen focus mode: chrome hides WITH animation ----",
    "    /* in-flow fade blocks: the way back in glides too */\n"
    "    .hc-cta, .hc-pager, .hc-rail {\n"
    "      transition: opacity .3s var(--ease-apple), display .3s allow-discrete, visibility 0s; }\n"
    "    /* ---- fullscreen focus mode: chrome hides WITH animation ----")

print('s22 all done')
