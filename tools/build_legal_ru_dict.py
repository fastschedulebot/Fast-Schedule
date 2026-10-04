"""Build the EN->RU dictionary for the three legal pages.

The Russian legal documents already exist and are complete (95.5% Russian) at
website/ru/legal/. They were not reachable from the English pages, which had no
route to them at all: switching language on /legal/terms.html translated 7.2%
of the page because the content dictionary simply had no legal entries.

Rather than re-translating text that a human already translated, this aligns the
two documents and reuses the existing Russian verbatim.

Safety rule, and the reason this is not just a zip() over the block lists: the
English terms page has 293 blocks and the Russian one has 269, so positional
pairing would silently attach the wrong Russian to the wrong English after the
first divergence - worse than leaving it untranslated. Instead the documents are
split on headings (which match exactly, 32 = 32), and a section is only paired
when its EN and RU block counts are equal. Anything that does not line up is
reported and skipped, never guessed.

Output merges into website/scripts/ru-content.js, whose applyContent() pass 1
matches whole text nodes exactly.

Use --check to report without writing.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'website')
PAGES = ('terms', 'privacy', 'refundpolicy')

BLOCK_RE = re.compile(r'<(h[1-6]|p|li|td|th|summary|dt|dd)\b[^>]*>(.*?)</\1>',
                      re.S)
TAG_RE = re.compile(r'<[^>]+>')


def norm(s):
    s = TAG_RE.sub('', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def sections(path):
    """[(heading_text, [(tag, text), ...]), ...] split on headings."""
    with io.open(path, encoding='utf-8') as f:
        h = f.read()
    m = re.search(r'<article class="doc"[^>]*>(.*?)</article>', h, re.S)
    if not m:
        raise SystemExit('no .doc article in %s' % path)
    body = m.group(1)
    out = []
    cur = ('<preamble>', [])
    for tag, inner in BLOCK_RE.findall(body):
        t = norm(inner)
        if not t:
            continue
        if tag in ('h1', 'h2'):
            out.append(cur)
            cur = (t, [])
        else:
            cur[1].append((tag, t))
    out.append(cur)
    return out


def main():
    check = '--check' in sys.argv
    pairs = {}
    stats = {}
    skipped = []

    for name in PAGES:
        en = sections(os.path.join(WEB, 'legal', '%s.html' % name))
        ru = sections(os.path.join(WEB, 'ru', 'legal', '%s.html' % name))
        if len(en) != len(ru):
            skipped.append('%s: %d EN sections vs %d RU sections'
                           % (name, len(en), len(ru)))
            continue
        matched = mism = 0
        for (eh, eb), (rh, rb) in zip(en, ru):
            if len(eb) != len(rb):
                mism += 1
                skipped.append('%s / %s: %d EN vs %d RU blocks'
                               % (name, eh[:40], len(eb), len(rb)))
                continue
            matched += 1
            for (et, etext), (rt, rtext) in zip(eb, rb):
                if et != rt or etext == rtext:
                    continue
                if re.search(r'[а-яА-Я]', etext):
                    continue  # already Russian, never overwrite
                if etext in pairs and pairs[etext] != rtext:
                    skipped.append('%s: conflicting RU for %r' % (name, etext[:40]))
                    continue
                pairs[etext] = rtext
        stats[name] = (matched, mism)

    out = ['# %-14s %8s %8s' % ('page', 'aligned', 'skipped')]
    for k in PAGES:
        if k in stats:
            out.append('# %-14s %8d %8d' % (k, stats[k][0], stats[k][1]))
    out.append('# new EN->RU pairs: %d' % len(pairs))

    path = os.path.join(WEB, 'scripts', 'ru-content.js')
    with io.open(path, encoding='utf-8') as f:
        src = f.read()
    m = re.search(r'window\.FS_RU_CONTENT=(\{.*\});\s*$', src, re.S)
    if not m:
        raise SystemExit('ru-content.js: unexpected shape')
    data = json.loads(m.group(1))

    before = len(data)
    added = 0
    for k, v in pairs.items():
        if k not in data:
            data[k] = v
            added += 1

    out.append('# ru-content.js entries: %d -> %d (+%d)'
               % (before, len(data), added))
    if skipped:
        out.append('# not aligned (left untranslated, deliberately):')
        for s in skipped[:40]:
            out.append('#   ' + s)

    report = '\n'.join(out)
    with io.open(os.path.join(ROOT, 'legal_dict_report.txt'), 'w',
                 encoding='utf-8') as f:
        f.write(report + '\n')
    print(report.encode('ascii', 'replace').decode('ascii'))

    if check or not added:
        return 0
    merged = 'window.FS_RU_CONTENT=' + json.dumps(
        data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(merged)
    print('ru-content.js rewritten (%d bytes)' % len(merged))
    return 0


if __name__ == '__main__':
    sys.exit(main())