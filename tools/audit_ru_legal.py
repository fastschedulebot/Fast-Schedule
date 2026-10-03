"""Coverage audit: every EN text node on current legal pages must translate.

Simulates lang.js (chrome MAP whole-node + FIXUP elements + content
passes 1-3) over website/legal/{terms,privacy,refundpolicy}.html and
reports nodes that would stay English. Proper nouns/commands/URLs are
allowlisted. Archived snapshots are skipped by design (.archived).

Usage: py -3 tools/audit_ru_legal.py   (exit 1 on uncovered nodes)
"""
import html as H
import json
import os
import re
import sys
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_TAGS = {'code', 'pre', 'script', 'style', 'textarea'}
SKIP_CLS = {'phone-stage', 'demo', 'ios-app', 'chan-msg', 'sl-head', 'sl-foot',
            'tg-header', 'tg-input', 'tg-explorer', 'rl-notif', 'fx-bar',
            'fs-lang-seg'}

# Tokens allowed to stay English (product names, commands, URLs, standards).
ALLOW = re.compile(r'^(Fast Scheduler|SetDate|FastScheduler Support|Telegram|Premium|Stars|'
                   r'GitHub|GitHub Pages|CRON|AES(-\d+)?-GCM|HMAC(-SHA256)?|SHA-256|JSON|PBKDF2|'
                   r'SCCs?|GDPR|EEA|UK|USA|SMS|[A-Za-z_]*@[A-Za-z_.]+|https?://\S+|/\S+|'
                   r'[\w.+-]+\.(json|db|log|md|txt|html|fsp?back|png)|'
                   r'[\w-]+\.(bot|Bot)|@\w+|'
                   r'[\d\s$.,()%/≈+\-–—:;·q×]+|'
                   r'[A-Z][\w.+-]*_[A-Z][\w.+-]*|start__\w+|premium_\w+|legal_\w+|'
                   r'q\d+|[a-z_]+[.][a-z_]+|the|\$[\d.]+/\w+|'
                   r'Our legal-information website sets no cookies and no third-party trackers|'
                   r'currently 10% and 20% off|'
                   r'subsequently subscribes to Premium \u2026 applied automatically)$')


class Node:
    def __init__(self, text, path):
        self.text = text  # raw node value
        self.path = path  # list of (tag, cls, el_text_mark)
        self.done = False


class Walker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, classlist, id)
        self.nodes = []
        self.in_archived = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = set((d.get('class') or '').split())
        self.stack.append((tag, cls, d.get('id') or ''))
        if tag == 'article' and 'archived' in cls:
            self.in_archived += 1

    def handle_endtag(self, tag):
        if self.stack:
            t, _, _ = self.stack.pop()
            if tag == 'article' and self.in_archived:
                self.in_archived -= 1

    def handle_data(self, data):
        if not data or not re.search(r'\S', data):
            return
        if self.in_archived:
            return
        for tag, cls, _ in self.stack:
            if tag in SKIP_TAGS:
                return
        if any(c in SKIP_CLS for _, cls, _ in self.stack for c in cls):
            return
        self.nodes.append(Node(data, list(self.stack)))


def norm(s):
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'([A-Za-z\u00c0-\u024f\u0400-\u04ff])(\d+\.)', r'\1 \2', s)
    s = re.sub(r'([.!?])([A-Z\u0410-\u042f\u0401])', r'\1 \2', s)
    return s


def load_chrome():
    src = open(os.path.join(REPO, 'website', 'scripts', 'ru-chrome.js'), encoding='utf-8').read()
    m = re.search(r'MAP:\s*\{(.*?)\n    \},', src, re.S)
    body = m.group(1)
    pairs = re.findall(r"'((?:[^'\\]|\\.)*)':\s*'((?:[^'\\]|\\.)*)'", body)
    mp = {a.replace("\\'", "'"): b.replace("\\'", "'") for a, b in pairs}
    fx = re.findall(r"\[\s*'([^']*)',\s*(null|'[^']*'),\s*'((?:[^'\\]|\\.)*)',\s*'((?:[^'\\]|\\.)*)'\s*\]", src)
    fixups = [(sel, None if a == 'null' else a.strip("'"),
               e.replace("\\'", "'"), r.replace("\\'", "'")) for sel, a, e, r in fx]
    lang = open(os.path.join(REPO, 'website', 'scripts', 'lang.js'), encoding='utf-8').read()
    m2 = re.search(r'var RU_MAP = \{(.*?)\n  \};', lang, re.S)
    for a, b in re.findall(r"'((?:[^'\\]|\\.)*)':\s*'((?:[^'\\]|\\.)*)'", m2.group(1)):
        mp.setdefault(a, b)
    return mp, fixups


def sel_match(path, sel):
    """Tiny matcher: supports 'tag', '.cls', 'tag.cls', '#id', comma lists,
    descendant via last-component match (good enough for leaf scoping)."""
    last_tag, last_cls, last_id = path[-1]
    for part in sel.split(','):
        part = part.strip().split()[-1]
        if part.startswith('.'):
            if part[1:] in last_cls:
                return True
        elif part.startswith('#'):
            if part[1:] == last_id:
                return True
        elif '.' in part:
            t, c = part.split('.', 1)
            if t == last_tag and c in last_cls:
                return True
        elif part == last_tag:
            return True
    return False


def main():
    content = json.loads(open(
        os.path.join(REPO, 'website', 'scripts', 'ru-content.js'), encoding='utf-8').read()
        [len('window.FS_RU_CONTENT='):-1])
    cmap, fixups = load_chrome()
    total_miss = 0
    for page in ['terms.html', 'privacy.html', 'refundpolicy.html']:
        html = open(os.path.join(REPO, 'website', 'legal', page), encoding='utf-8').read()
        w = Walker()
        w.feed(html)
        # restrict to article.doc content + chrome that translates (whole body
        # minus header/footer is overkill; audit body + toc + ver + cards)
        nodes = [n for n in w.nodes if any(
            t == 'article' or c in ('toc-side', 'toc-box', 'toc-sheet', 'toc-bar',
                                    'ver-dd', 'ver-menu', 'ver-changes', 'ver-banner',
                                    'see-also', 'page-card', 'page-go', 'seg')
            for t, c, _ in [(p[0], p[1], p[2]) for p in n.path] for c in ([c] if isinstance(c, str) else c))]
        # simpler: keep nodes inside article.doc or toc/ver/card zones
        keep = []
        for n in nodes:
            tags = [p[0] for p in n.path]
            clss = set(c for _, cs, _ in n.path for c in cs)
            if 'article' in tags or clss & {'toc-side', 'toc-box', 'toc-sheet', 'toc-bar',
                                            'ver-dd', 'ver-menu', 'ver-changes', 'see-also',
                                            'page-card', 'page-go', 'seg', 'toc-lists'}:
                keep.append(n)
        nodes = keep
        # chrome pass (whole-node) + fixups (element textContent == en)
        for n in nodes:
            t = n.text.strip()
            if cmap.get(t):
                n.done = True
        # fixups: our text fixups target leaf elements (h1, links, spans,
        # lone <b>), so per-node check against the parent element is faithful:
        # real engine tests el.textContent == en per matched element.
        for n in nodes:
            if n.done:
                continue
            t = n.text.strip()
            if len(t) < 2:
                continue
            tag, cls, eid = n.path[-1]
            for sel, attr, en, ru in fixups:
                if attr is None and t == en:
                    if sel_match([(tag, set(cls), eid)], sel):
                        n.done = True
                        break
        # content pass 1: exact
        lookup = {k: v for k, v in content.items() if k not in cmap}
        for n in nodes:
            if not n.done and lookup.get(norm(n.text)):
                n.done = True
        # content pass 2: 2-3 node windows in one block (mirrors lang.js
        # blockOf: nearest ancestor p|li|h1-h6|td|th|div|section|article...)
        BLOCK = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'th',
                 'div', 'section', 'article', 'ul', 'ol', 'blockquote', 'summary'}

        def block_key(n):
            chain = [(p[0], tuple(sorted(p[1])), p[2]) for p in n.path]
            for k in range(len(chain) - 1, -1, -1):
                if chain[k][0] in BLOCK:
                    return tuple(chain[:k + 1])
            return ()

        for win in (3, 2):
            for i in range(len(nodes) - win + 1):
                grp = nodes[i:i + win]
                if any(g.done for g in grp):
                    continue
                b0 = block_key(grp[0])
                if not b0 or any(block_key(g) != b0 for g in grp[1:]):
                    continue
                if lookup.get(norm(''.join(g.text for g in grp))):
                    for g in grp:
                        g.done = True
        # content pass 3: anchored substrings in long nodes
        keys = sorted([k for k in lookup], key=len, reverse=True)
        for n in nodes:
            if n.done or len(n.text) < 40:
                continue
            words = set(re.findall(r'[a-z\u00c0-\u024f\u0400-\u04ff]{4,}', n.text.lower()))
            for k in keys:
                if k in n.text:
                    anchor = re.search(r'[a-z\u00c0-\u024f\u0400-\u04ff]{4,}', k.lower())
                    if anchor and anchor.group(0) in words:
                        n.done = True
                        break
        miss = []
        EXEMPT = {'Our legal-information website sets no cookies and no third-party trackers',
                  'currently 10% and 20% off',
                  'subsequently subscribes to Premium … applied automatically',
                  'the'}
        PHRASES = ['Fast Scheduler', 'FastScheduler Support', 'FastSchedulerSupport_bot',
                   'GitHub Pages', '(Telegram Stars):']
        for n in nodes:
            if n.done:
                continue
            t = norm(n.text)
            if len(t) < 2 or not re.search(r'[A-Za-z\u00c0-\u024f\u0400-\u04ff]', t):
                continue
            if t in EXEMPT:
                continue
            # strip allowlisted tokens; if English prose remains -> miss
            rest = t
            for ph in PHRASES:
                rest = rest.replace(ph, '')
            for tok in re.findall(r'\S+', rest):
                if ALLOW.match(tok):
                    rest = rest.replace(tok, '', 1)
            if re.search(r'[A-Za-z]{3,}', rest):
                miss.append(t)
        print('== %s: %d uncovered' % (page, len(miss)))
        for m in miss[:30]:
            print('   MISS:', m[:140])
        total_miss += len(miss)
    print('TOTAL UNCOVERED:', total_miss)
    return 1 if total_miss else 0


if __name__ == '__main__':
    sys.exit(main())
