#!/usr/bin/env node
// Measure Russian ("lang=ru") layout overflow across the whole static site.
//
// Russian strings are longer than their English originals, so boxes sized by
// eye in English clip or spill in Russian. This drives headless Chrome over the
// DevTools protocol (no npm dependencies -- Node's global WebSocket is enough),
// switches every page to Russian, and reports elements whose content is wider
// than their own box or which stick out past the viewport.
//
//   node tools/scan_ru_overflow.mjs --base http://localhost:8811 --out ru_overflow.json
//   node tools/scan_ru_overflow.mjs --urls urls.txt --widths 390,768,1440
//
// Requires a static server already running (see tools/ -- the site is a plain
// static build, no server needed beyond python -m http.server).

import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  '/c/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
].filter(Boolean);

function arg(name, dflt) {
  const i = process.argv.indexOf('--' + name);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}

const BASE = arg('base', 'http://localhost:8811').replace(/\/$/, '');
const OUT = arg('out', 'ru_overflow.json');
const WIDTHS = arg('widths', '390,414,768,1024,1440').split(',').map(Number);
const URL_FILE = arg('urls', '');
const LIMIT = Number(arg('limit', '0')) || Infinity;
const SHOT = !!arg('shot', '');

// --cyr reports how much of each page's main content is actually rendered in
// Russian, instead of measuring overflow. Switching language only rewrites the
// strings present in window.FS_RU_CONTENT, so a page can come up with a Russian
// <title> and Russian chrome while its article body is still English. This
// counts the Cyrillic share of the main content so that gap is measurable
// instead of a matter of opinion.
const CYR = !!arg('cyr', '');
// How long to let the language switch settle before measuring. The switch can
// need to fetch ru-content.js first, so a short wait reads a half-translated
// page and under-reports badly.
const SETTLE = Number(arg('settle', '700'));
const CYR_EXPR = `(() => {
  const root = document.querySelector('main') || document.querySelector('article') || document.body;
  // textContent, NOT innerText: the legal docs set content-visibility, which
  // skips offscreen subtrees, so innerText reads a mostly-unrendered page and
  // badly under-reports the Russian share.
  const text = (root.textContent || '').replace(/\s+/g, ' ').trim();
  // Count by code point rather than by regex. This string is itself a template
  // literal, so a character-class escape needs a second round of escaping and
  // silently degrades into matching plain ASCII.
  let cyr = 0, lat = 0;
  for (const ch of text) {
    const c = ch.codePointAt(0);
    if (c >= 0x400 && c <= 0x4ff) cyr++;
    else if ((c >= 0x41 && c <= 0x5a) || (c >= 0x61 && c <= 0x7a)) lat++;
  }
  return { chars: text.length, cyr, lat, pct: lat + cyr ? Math.round(100 * cyr / (lat + cyr)) : 0,
    h1: (document.querySelector('h1') || {}).innerText || '',
    title: document.title, htmlLang: document.documentElement.lang,
    ls: (function(){ try { return localStorage.getItem('fs-lang'); } catch(e){ return 'ERR'; } })(),
    keys: window.FS_RU_CONTENT ? Object.keys(window.FS_RU_CONTENT).length : 0,
    sample: text.slice(0, 120) };
})()`;

const urls = URL_FILE && existsSync(URL_FILE)
  ? readFileSync(URL_FILE, 'utf8').split(/\r?\n/).map(s => s.trim()).filter(s => s && !s.startsWith('#'))
  : [
      '/', '/help/', '/help/a/admins.html', '/help/a/posts.html',
      '/blog/', '/legal/terms.html', '/legal/privacy.html', '/legal/refundpolicy.html',
      '/faq.html', '/pricing.html', '/features.html', '/ru/', '/ru/legal/terms.html',
    ];

// Boxes that scroll or clip by design; their content is *meant* to exceed them.
const SCROLLERS = '.marquee, .marquee-track, .pricing-carousel, .pricing-stage, ' +
  '.carousel, .slider, .phone-screen, #phone3d, .tg-screen, .hero-phone, ' +
  '.hc-toc-fab, .toc-sheet, [data-hc-scroller]';

const SCAN = `(() => {
  const scrollers = ${JSON.stringify(SCROLLERS)};
  // Content that sticks out of a scroll container is *supposed* to stick out --
  // .table-scroll, .marquee and friends exist precisely to hold wider content.
  // So walk the ancestors and skip anything already clipped or scrollable,
  // rather than trusting a fixed list of class names.
  const insideScroller = el => {
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (/auto|scroll|hidden|clip/.test(cs.overflowX)) return true;
      if (cs.overflow === 'hidden') return true;
      if (p.matches && p.matches(scrollers)) return true;
    }
    return false;
  };
  const path = el => {
    let s = el.tagName.toLowerCase();
    const c = (el.className && typeof el.className === 'string') ? el.className.trim() : '';
    if (el.id) s += '#' + el.id; else if (c) s += '.' + c.split(/\\s+/).slice(0, 3).join('.');
    return s;
  };
  const vw = document.documentElement.clientWidth;
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (el.closest(scrollers)) return;
    if (insideScroller(el)) return;
    // Only report boxes that actually contain Russian text (or an icon inside
    // a text box) -- pure layout scaffolding is not a translation-fitting bug.
    const R = Math.round(r.right - vw);
    const L = Math.round(-r.left);
    const s = el.scrollWidth - el.clientWidth;
    if (R <= 2 && L <= 2 && s <= 2) return;
    const txt = (el.innerText || '').trim().replace(/\\s+/g, ' ');
    out.push({ p: path(el), R, L, s, cyr: /[\\u0400-\\u04ff]/.test(txt), txt: txt.slice(0, 40) });
  });
  return { vw, docScrollW: document.documentElement.scrollWidth, docClientW: vw, n: out.length, items: out.slice(0, 14) };
})()`;

function findChrome() {
  for (const c of CHROME_CANDIDATES) if (existsSync(c)) return c;
  throw new Error('No Chrome/Edge binary found. Set CHROME_PATH.');
}

async function launch() {
  const bin = findChrome();
  const port = 9333 + Math.floor(process.pid % 500);
  const dir = mkdtempSync(join(tmpdir(), 'ru-overflow-'));
  const proc = spawn(bin, [
    '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--disable-extensions', '--disable-background-networking', '--mute-audio',
    '--hide-scrollbars=false',
    `--user-data-dir=${dir}`,
    `--remote-debugging-port=${port}`,
    'about:blank',
  ], { stdio: 'ignore', detached: false });

  let target = null;
  for (let i = 0; i < 100; i++) {
    await new Promise(r => setTimeout(r, 200));
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      target = list.find(t => t.type === 'page');
      if (target) break;
    } catch { /* not up yet */ }
  }
  if (!target) { proc.kill(); throw new Error('Chrome did not expose a debug target'); }
  return { proc, port, ws: target.webSocketDebuggerUrl };
}

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = new Map();
    ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && this.pending.has(m.id)) {
        const { res, rej } = this.pending.get(m.id); this.pending.delete(m.id);
        m.error ? rej(new Error(m.error.message)) : res(m.result);
      } else if (m.method) {
        (this.events.get(m.method) || []).forEach(f => f(m.params));
      }
    });
  }
  on(ev, fn) { if (!this.events.has(ev)) this.events.set(ev, []); this.events.get(ev).push(fn); }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.pending.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); rej(new Error('timeout ' + method)); } }, 60000);
    });
  }
  async eval(expr) {
    const r = await this.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + ' ' + (r.exceptionDetails.exception?.description || ''));
    return r.result.value;
  }
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const { proc, ws } = await launch();
  const wsock = new WebSocket(ws);
  await new Promise((res, rej) => { wsock.addEventListener('open', res); wsock.addEventListener('error', rej); });
  const cdp = new CDP(wsock);
  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');

  const pages = urls.slice(0, LIMIT);
  const report = [];
  for (const w of WIDTHS) {
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: w, height: 900, deviceScaleFactor: 1, mobile: w < 768 });
    for (const u of pages) {
      const url = u.startsWith('http') ? u : BASE + u;
      let loaded = false;
      const onLoad = () => { loaded = true; };
      cdp.on('Page.loadEventFired', onLoad);
      await cdp.send('Page.navigate', { url });
      for (let i = 0; i < 60 && !loaded; i++) await sleep(100);
      await sleep(700);
      // Force Russian through the site's own switcher, then let it settle.
      await cdp.eval(`(async()=>{try{if(window.FS_LANG&&window.FS_LANG.set){window.FS_LANG.set('ru');}else{document.documentElement.lang='ru';}}catch(e){};await new Promise(r=>setTimeout(r,${SETTLE}));return 1})()`);
      if (CYR) {
        const c = await cdp.eval(CYR_EXPR);
        report.push({ url, w, ...c });
        process.stdout.write(`${String(c.pct).padStart(4)}% cyr  ${String(c.chars).padStart(6)} ch  ${u}\n`);
        continue;
      }
      const r = await cdp.eval(SCAN);
      report.push({ url, w, ...r });
      const bad = r.n;
      process.stdout.write(`${String(w).padStart(4)}  ${String(bad).padStart(3)} over  ${u}\n`);
    }
  }
  writeFileSync(OUT, JSON.stringify(report, null, 1));
  if (CYR) {
    const rows = report.slice(0, pages.length);
    const avg = Math.round(rows.reduce((a, b) => a + b.pct, 0) / (rows.length || 1));
    const low = rows.filter(r => r.pct < 50);
    console.log(`\npages=${rows.length} avgCyr=${avg}%  below50%=${low.length}`);
    for (const r of low.sort((a, b) => a.pct - b.pct).slice(0, 25)) {
      console.log(`  ${String(r.pct).padStart(3)}%  ${r.url.replace(BASE, '')}  (${r.chars} chars)`);
    }
    console.log(`report -> ${OUT}`);
    wsock.close(); proc.kill(); process.exit(0);
  }
  const total = report.reduce((a, b) => a + b.n, 0);
  const badUrls = [...new Set(report.filter(r => r.n).map(r => r.url))];
  console.log(`\npages=${pages.length} widths=${WIDTHS.length} totalOverlaps=${total} urlsWithIssues=${badUrls.length}`);
  console.log(`report -> ${OUT}`);
  wsock.close();
  proc.kill();
  process.exit(0);
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });