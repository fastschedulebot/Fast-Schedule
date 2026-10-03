# -*- coding: utf-8 -*-
"""Docs redesign part 1: append the new docs-system CSS to build_help.py.

Run from repo root:  python tools/restyle_help_docs_1css.py
"""
import io

P = 'website/_build/build_help.py'
t = io.open(P, encoding='utf-8').read()

CSS_NEW = r'''
    /* ================= docs redesign: calm professional system ================= */
    .hc-shell { column-gap: 0; }

    /* ---- sidebar as a true docs tree ---- */
    .hc-side { width: 266px; padding: 20px 10px 48px; font-size: .9rem; }
    .hc-side-title { font-size: .78rem; font-weight: 800; letter-spacing: .09em; text-transform: uppercase;
      color: var(--text-dim); padding: 2px 12px 12px; }
    .hc-side-title svg { width: 15px; height: 15px; }
    .hc-nav-item { padding: 7px 10px; font-size: .88rem; font-weight: 650; border-radius: 8px; }
    .hc-nav-item svg { width: 16px; height: 16px; }
    .hc-nav-item.active { background: color-mix(in srgb, var(--green) 13%, transparent); }
    .hc-subnav a { padding: 5px 10px 5px 36px; font-size: .83rem; border-left: 2px solid transparent;
      border-radius: 0 8px 8px 0; margin-left: 10px; }
    .hc-subnav a:hover { border-left-color: color-mix(in srgb, var(--green) 40%, transparent); }
    .hc-subnav a.active { border-left-color: var(--green); background: color-mix(in srgb, var(--green) 9%, transparent); }
    .hc-side-cta { margin: 16px 8px 0; }

    /* ---- content + right rail grid ---- */
    .hc-content { --hc-gut: clamp(20px, 3.5vw, 44px); }
    .hc-doc { display: grid; grid-template-columns: minmax(0, 1fr) 228px; gap: clamp(28px, 4vw, 56px);
      align-items: start; }
    .hc-doc > article { min-width: 0; }
    .hc-rail { position: sticky; top: calc(var(--hc-head) + 28px); max-height: calc(100vh - var(--hc-head) - 56px);
      overflow-y: auto; scrollbar-width: thin; font-size: .83rem; padding-bottom: 24px; }
    .hc-rail-t { font-weight: 800; font-size: .78rem; letter-spacing: .06em; text-transform: uppercase;
      color: var(--text); margin: 4px 0 10px; }
    .hc-rail nav { display: flex; flex-direction: column; gap: 1px; border-left: 2px solid var(--border); }
    .hc-rail a { display: block; padding: 4px 0 4px 14px; margin-left: -2px; border-left: 2px solid transparent;
      color: var(--text-dim); line-height: 1.45; }
    .hc-rail a:hover { color: var(--green-strong); text-decoration: none; }
    .hc-rail a.on { color: var(--green-strong); font-weight: 700; border-left-color: var(--green); }
    .hc-rail .hc-rail-rel { margin-top: 14px; }
    .hc-rail .hc-rail-rel span { display: block; font-weight: 800; font-size: .75rem; letter-spacing: .06em;
      text-transform: uppercase; color: var(--text-dim); margin-bottom: 6px; }
    @media (max-width: 1279px) { .hc-doc { grid-template-columns: minmax(0, 1fr); } .hc-rail { display: none; } }

    /* ---- docs home: compact head + popular + cards ---- */
    .hc-docs-head { padding: clamp(30px, 5vw, 60px) 0 6px; max-width: 860px; }
    .hc-docs-head h1 { margin: 8px 0 10px; font-size: clamp(1.9rem, 4.4vw, 2.7rem); letter-spacing: -.03em;
      line-height: 1.08; font-weight: 800; }
    .hc-docs-head h1 .grad { color: var(--green); }
    .hc-docs-head .hc-sub { margin: 0 0 22px; font-size: 1.02rem; color: var(--text-dim); max-width: 62ch; }
    .hc-docs-head .hc-search { margin-top: 0; max-width: 640px; }
    .hc-pop { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; margin: 20px 0 6px;
      font-size: .87rem; color: var(--text-dim); }
    .hc-pop b { font-weight: 750; color: var(--text); }
    .hc-pop a { color: var(--green-strong); font-weight: 600; padding: 4px 10px; border-radius: 999px;
      border: 1px solid var(--border); background: var(--surface); white-space: nowrap; }
    .hc-pop a:hover { border-color: var(--green); text-decoration: none; }
    .hc-section-h { display: flex; align-items: baseline; gap: 12px; margin: 34px 0 4px; }
    .hc-section-h h2 { margin: 0; font-size: 1.15rem; letter-spacing: -.01em; }
    .hc-section-h span { color: var(--text-dim); font-size: .86rem; }
    .hc-grid { grid-template-columns: repeat(3, 1fr); }
    @media (max-width: 1020px) { .hc-grid { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 640px) { .hc-grid { grid-template-columns: 1fr; } }
    .hc-cat { display: flex; flex-direction: column; gap: 10px; padding: 20px; text-decoration: none; }
    .hc-cat:hover { text-decoration: none; border-color: color-mix(in srgb, var(--green) 45%, var(--border)); }
    .hc-cat-head { display: flex; align-items: center; gap: 12px; }
    .hc-ic { display: inline-flex; align-items: center; justify-content: center; flex: none;
      width: 40px; height: 40px; border-radius: 12px; color: var(--green-strong);
      background: color-mix(in srgb, var(--green) 12%, transparent); }
    .hc-ic svg { width: 20px; height: 20px; }
    .hc-cat-t { display: block; font-weight: 750; font-size: .98rem; color: var(--text); }
    .hc-cat-c { display: block; font-size: .8rem; color: var(--text-dim); font-weight: 600; margin-top: 2px; }
    .hc-cat-go { margin-left: auto; color: var(--text-dim); }
    .hc-cat-go svg { width: 16px; height: 16px; }
    .hc-cat:hover .hc-cat-go { color: var(--green-strong); }
    .hc-cat-prev { border-top: 1px dashed var(--border); padding-top: 10px; }

    /* ---- article page: flat docs typography ---- */
    .hc-art { background: none; border: 0; box-shadow: none; border-radius: 0;
      max-width: 780px; margin: 0; padding: 0; }
    .hc-crumbs { padding: 24px 0 0; font-size: .82rem; }
    .hc-art > h1 { font-size: clamp(1.7rem, 3.4vw, 2.3rem); margin: 12px 0 6px; }
    .hc-art-meta { color: var(--text-dim); font-size: .87rem; margin: 0 0 18px; display: flex; gap: 8px;
      align-items: center; flex-wrap: wrap; }
    .hc-art-meta .dot::before { content: "·"; margin-right: 8px; }
    .hc-body { font-size: 1.0rem; }
    .hc-body p, .hc-body li { line-height: 1.72; }
    .hc-body p { margin: 0 0 14px; }
    .hc-body ul { margin: 0 0 16px; padding-left: 22px; display: flex; flex-direction: column; gap: 7px; }
    .hc-body li::marker { color: var(--green-strong); }
    .hc-body a { text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px;
      text-decoration-color: color-mix(in srgb, var(--green-strong) 55%, transparent); }
    .hc-body a:hover { text-decoration-color: var(--green-strong); }
    .hc-body h2, .hc-body h3 { letter-spacing: -.015em; line-height: 1.3; margin: 30px 0 10px; }
    .hc-body h2 { font-size: 1.28rem; }
    .hc-body h3 { font-size: 1.08rem; }
    .hc-body code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .86em;
      background: var(--surface-2); border: 1px solid var(--border); padding: 1px 6px; border-radius: 6px; }
    .hc-body pre { background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      padding: 14px 16px; overflow-x: auto; font-size: .85rem; line-height: 1.6; }
    .hc-body table { border-collapse: collapse; width: 100%; font-size: .9rem; margin: 0 0 18px; }
    .hc-body th, .hc-body td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
    .hc-body th { background: var(--surface-2); font-weight: 750; }
    .hc-body img { max-width: 100%; border-radius: 12px; border: 1px solid var(--border); }

    /* ---- faq / related / pager / cta ---- */
    .hc-faq { margin-top: 30px; }
    .hc-faq > h2 { font-size: .82rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
    .hc-faq details { border: 1px solid var(--border); border-radius: 12px; padding: 0 16px; margin-bottom: 8px; }
    .hc-faq details[open] { border-color: color-mix(in srgb, var(--green) 40%, var(--border)); }
    .hc-faq summary { padding: 13px 0; font-weight: 700; font-size: .95rem; cursor: pointer; list-style: none; }
    .hc-faq summary::-webkit-details-marker { display: none; }
    .hc-faq summary::after { content: "+"; float: right; color: var(--green-strong); font-weight: 800; }
    .hc-faq details[open] summary::after { content: "–"; }
    .hc-fa { padding: 0 0 16px; color: var(--text); }
    .hc-fa p, .hc-fa li { line-height: 1.7; }
    .hc-related { margin-top: 26px; }
    .hc-related > h2 { font-size: .82rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase;
      color: var(--text-dim); margin: 0 0 10px; }
    .hc-pager { max-width: 780px; margin: 30px 0 0; }
    .hc-pager a { border-radius: 14px; background: var(--surface); }
    .hc-pager small { display: block; font-size: .75rem; font-weight: 800; letter-spacing: .07em;
      text-transform: uppercase; color: var(--text-dim); margin-bottom: 3px; }
    .hc-pager b { font-size: .95rem; }
    .hc-cta { max-width: 780px; border-radius: 16px; margin-top: 26px; }

    /* ---- feedback ---- */
    .hc-fb { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-top: 30px;
      padding: 16px 18px; border: 1px solid var(--border); border-radius: 14px; background: var(--surface); }
    .hc-fb span.q { font-weight: 700; font-size: .93rem; }
    .hc-fb button { font: inherit; font-size: .87rem; font-weight: 700; padding: 7px 18px; border-radius: 999px;
      border: 1px solid var(--border); background: var(--surface-2); color: var(--text); cursor: pointer; }
    .hc-fb button:hover { border-color: var(--green); color: var(--green-strong); }
    .hc-fb button.picked { background: var(--green); border-color: var(--green); color: #fff; }
    .hc-fb .thanks { font-size: .9rem; color: var(--green-strong); font-weight: 650; }

    /* ---- category / list / search ---- */
    .hc-cat-head { display: flex; gap: 14px; align-items: center; margin: 14px 0 4px; }
    .hc-cat-head h1 { margin: 0; font-size: clamp(1.6rem, 3.2vw, 2.1rem); letter-spacing: -.02em; }
    .hc-cat-head p { margin: 4px 0 0; color: var(--text-dim); }
    .hc-intro { max-width: 780px; color: var(--text); }
    .hc-intro p { line-height: 1.7; }
    .hc-list { display: flex; flex-direction: column; gap: 8px; max-width: 860px; }
    .hc-row { display: flex; align-items: center; gap: 12px; padding: 13px 16px; border: 1px solid var(--border);
      border-radius: 12px; background: var(--surface); }
    .hc-row:hover { border-color: color-mix(in srgb, var(--green) 45%, var(--border)); text-decoration: none; }
    .hc-row-t { font-weight: 650; color: var(--text); }
    .hc-row-m { margin-left: auto; flex: none; font-size: .8rem; color: var(--text-dim); font-weight: 650; }
    .hc-others { margin-top: 26px; font-size: .88rem; color: var(--text-dim); display: flex; flex-wrap: wrap; gap: 6px 12px; }
    .hc-others a { font-weight: 600; }

    /* ---- static .doc pages share the type system ---- */
    .doc { font-size: 1.0rem; }
    .doc h1 { letter-spacing: -.025em; line-height: 1.15; }
    .doc p, .doc li { line-height: 1.72; }
    .doc a { text-decoration: underline; text-underline-offset: 3px;
      text-decoration-color: color-mix(in srgb, var(--green-strong) 55%, transparent); }
    .doc-layout { display: grid; grid-template-columns: minmax(0, 1fr) 228px; gap: clamp(28px, 4vw, 56px);
      align-items: start; }
    @media (max-width: 1279px) { .doc-layout { grid-template-columns: minmax(0, 1fr); } .doc-layout .hc-rail { display: none; } }

    @media (max-width: 760px) {
      .hc-side { width: min(320px, 88vw); }
      .hc-doc { grid-template-columns: minmax(0, 1fr); }
      .hc-rail { display: none; }
      .hc-docs-head h1 { font-size: 1.9rem; }
      .hc-pager { grid-template-columns: 1fr; }
      .hc-body pre { font-size: .8rem; }
    }
'''

anchor = "    @media print {"
assert t.count(anchor) == 1
t = t.replace(anchor, CSS_NEW + "\n" + anchor)
io.open(P, 'w', encoding='utf-8').write(t)
print('css appended')
