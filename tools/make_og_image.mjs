#!/usr/bin/env node
// Render the social preview card (og:image) to a PNG.
//
// The original og-cover.png was produced by a generator that laid text out
// without measuring it: the subtitle and the t.me handle both ran past the
// right edge of the 1200px canvas, so every link preview clipped the words
// mid-sentence ("...channel posts on auto"). Re-rendering with real font
// metrics in headless Chrome is what fixes that -- the browser measures the
// glyphs, so the text either fits or it visibly does not.
//
// It also lets the card use the site's own webfonts, so the preview matches
// the brand rather than whatever the rendering machine happens to have.
//
//   node tools/make_og_image.mjs                    # -> website/og-cover-v2.png
//   node tools/make_og_image.mjs --check            # report overflow, write nothing
//
// Why a new filename: Telegram, Facebook, Slack and X cache preview images
// aggressively and largely ignore cache-busting headers. Repainting the same
// URL would leave every existing share showing the old clipped card forever.

import { spawn } from 'node:child_process';
import { writeFileSync, readFileSync, existsSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const OUT = join(ROOT, 'website', 'og-cover-v2.png');
const CHECK = process.argv.includes('--check');

const W = 1200, H = 630;
// Anything outside this box can be cropped away by a preview card, so nothing
// important is allowed to reach it. Telegram renders the image around 2:1 and
// crops the sides on narrow cards; 72px absorbs that plus rounding.
const SAFE = 72;

// ---------------------------------------------------------------- template
const b64 = (p) => readFileSync(p).toString('base64');
const inter = b64(join(ROOT, 'website', 'fonts', 'inter-latin.woff2'));
const grotesk = b64(join(ROOT, 'website', 'fonts', 'space-grotesk-latin.woff2'));

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>
  @font-face{font-family:'Space Grotesk';src:url(data:font/woff2;base64,${grotesk}) format('woff2');font-weight:400 700;}
  @font-face{font-family:'Inter';src:url(data:font/woff2;base64,${inter}) format('woff2');font-weight:400 700;}
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:${W}px;height:${H}px;overflow:hidden;background:#080c0a}
  /* Centred, not left-aligned. A link preview crops the image to whatever
     shape the app renders, always centred, so anything pinned to an edge is
     the first thing to go. A centred stack keeps every line inside the narrow
     central band that even a 1:1 crop leaves. */
  body{
    font-family:'Inter',system-ui,sans-serif;color:#fff;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;position:relative;padding:56px 60px;
    background-image:
      radial-gradient(820px 520px at 50% 112%, rgba(34,197,94,.30), transparent 62%),
      radial-gradient(700px 430px at 12% -14%, rgba(22,163,74,.24), transparent 62%),
      radial-gradient(700px 430px at 88% -14%, rgba(22,163,74,.24), transparent 62%);
  }
  body::after{content:'';position:absolute;inset:26px;border:1px solid rgba(255,255,255,.10);border-radius:26px;pointer-events:none}
  .mark{width:112px;height:112px;border-radius:28px;margin-bottom:26px;
    background:linear-gradient(145deg,#34d399,#15803d);
    display:grid;place-items:center;box-shadow:0 16px 40px rgba(22,163,74,.34)}
  .mark svg{width:60px;height:60px}
  h1{font-family:'Space Grotesk','Inter',sans-serif;font-weight:700;
    font-size:78px;line-height:1.02;letter-spacing:-.032em}
  /* 28px on one line measures ~570px, so the subtitle still clears the band a
     square crop leaves (x 285..915) without orphaning "autopilot" on its own
     row. It wraps rather than running out of frame if the font ever differs. */
  .sub{margin-top:14px;font-size:28px;line-height:1.3;font-weight:550;color:#7fe3a8;
    letter-spacing:-.008em;max-width:640px}
  .pills{margin-top:26px;display:flex;gap:10px;justify-content:center;flex-wrap:nowrap}
  .pill{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;
    background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.13);
    font-size:19px;font-weight:600;color:#e8fff1;white-space:nowrap}
  .pill svg{width:17px;height:17px;flex:none;color:#4ade80}
  .handle{margin-top:22px;font-size:21px;font-weight:600;color:rgba(255,255,255,.5)}
</style></head><body>
  <div class="mark"><svg viewBox="0 0 24 24" fill="none" stroke="#06210f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>
    <line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div>
  <h1>Fast Scheduler</h1>
  <div class="sub">Schedule Telegram channel posts on autopilot</div>
  <div class="pills">
    <span class="pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h8l-1 8 10-12h-8z"/></svg>Batch scheduling</span>
    <span class="pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/></svg>Your own bot</span>
    <span class="pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Free to start</span>
  </div>
  <div class="handle">t.me/FastSchedulerBot</div>
</body></html>`;

// ------------------------------------------------------------------- cdp
const CHROME = [
  process.env.CHROME_PATH,
  '/c/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium',
].filter(Boolean).find(p => existsSync(p));

function arg(n, d) { const i = process.argv.indexOf('--' + n); return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : d; }

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.p = new Map();
    ws.addEventListener('message', e => { const m = JSON.parse(e.data);
      if (m.id && this.p.has(m.id)) { const { res, rej } = this.p.get(m.id); this.p.delete(m.id);
        m.error ? rej(new Error(m.error.message)) : res(m.result); } }); }
  send(method, params = {}) { const id = ++this.id;
    return new Promise((res, rej) => { this.p.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => { if (this.p.has(id)) { this.p.delete(id); rej(new Error('timeout ' + method)); } }, 60000); }); }
  async eval(e) { const r = await this.send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text); return r.result.value; }
}

(async () => {
  if (!CHROME) throw new Error('No Chrome/Edge found. Set CHROME_PATH.');
  const port = 9700 + (process.pid % 200);
  const dir = mkdtempSync(join(tmpdir(), 'og-'));
  const proc = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars',
    `--user-data-dir=${dir}`, `--remote-debugging-port=${port}`, 'about:blank'], { stdio: 'ignore' });
  let target = null;
  for (let i = 0; i < 100; i++) {
    await new Promise(r => setTimeout(r, 200));
    try { const l = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      target = l.find(t => t.type === 'page'); if (target) break; } catch {}
  }
  if (!target) { proc.kill(); throw new Error('Chrome did not start'); }

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
  const cdp = new CDP(ws);
  await cdp.send('Page.enable'); await cdp.send('Runtime.enable');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });

  await cdp.send('Page.navigate', { url: 'about:blank' });
  await new Promise(r => setTimeout(r, 400));
  await cdp.eval(`document.open();document.write(${JSON.stringify(html)});document.close();`);
  await new Promise(r => setTimeout(r, 1200)); // let the webfonts settle

  // Guard: refuse to write if anything reaches the safe area. This is the check
  // the original generator was missing.
  const over = await cdp.eval(`(() => {
    const bad = [];
    document.querySelectorAll('h1,.sub,.pill,.handle,.mark').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.left < ${SAFE} || r.right > ${W - SAFE} || r.top < ${SAFE} || r.bottom > ${H - SAFE})
        bad.push({ el: el.className || el.tagName, l: Math.round(r.left), r: Math.round(r.right), t: Math.round(r.top), b: Math.round(r.bottom) });
      if (el.scrollWidth > el.clientWidth + 1) bad.push({ el: (el.className||el.tagName)+' clipped', s: el.scrollWidth, c: el.clientWidth });
    });
    return bad;
  })()`);
  if (over.length) {
    console.error('ABORT: content outside the safe area — not writing the PNG:');
    console.error(JSON.stringify(over, null, 1));
    ws.close(); proc.kill(); process.exit(1);
  }
  console.log('safe-area check passed (nothing within %dpx of the edge)', SAFE);

  // Second guard, and the one that actually matches the bug being fixed: does
  // every line survive the crop a preview card applies? object-fit:cover scales
  // by max(boxW/imgW, boxH/imgH) and centre-crops the excess, so a box narrower
  // than 1200x630 loses pixels from BOTH sides.
  const crops = await cdp.eval(`(() => {
    const W=${W},H=${H};
    const ratios=[['Telegram link card',475,285],['Facebook 1.91:1',1200,630],['Slack 1.5:1',600,400],['square',600,600]];
    const els=[...document.querySelectorAll('h1,.sub,.pill,.handle,.mark')];
    const out=[];
    for (const [name,bw,bh] of ratios) {
      const s=Math.max(bw/W,bh/H);
      const visW=bw/s;                       // visible width in image px
      const x0=(W-visW)/2, x1=x0+visW;       // visible horizontal band
      const clipped=els.filter(el=>{const r=el.getBoundingClientRect(); return r.left < x0 || r.right > x1;})
                       .map(el=>({el:el.className||el.tagName,l:Math.round(el.getBoundingClientRect().left),r:Math.round(el.getBoundingClientRect().right)}));
      out.push({name, visible: Math.round(x0) + '..' + Math.round(x1), clipped});
    }
    return out;
  })()`);
  console.log('\ncrop survival (object-fit:cover, centred):');
  for (const c of crops) {
    const tag = c.clipped.length ? 'CLIPPED ' + c.clipped.map(x => x.el).join(', ') : 'all text visible';
    console.log(`  ${c.name.padEnd(20)} visible x ${c.visible.padEnd(11)} ${tag}`);
  }

  if (CHECK) { console.log('--check: nothing written.'); ws.close(); proc.kill(); process.exit(0); }

  const shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  writeFileSync(OUT, Buffer.from(shot.data, 'base64'));
  console.log(`wrote ${OUT} (${W}x${H})`);
  ws.close(); proc.kill(); process.exit(0);
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });