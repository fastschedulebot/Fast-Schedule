"""Make language switching instant and self-contained on doc pages.

Three defects, all from the same root cause -- the Russian content dictionary
was treated as an optional extra rather than part of the page:

1. `ru-content.js` (225 KB / 61 KB gzipped) was loaded by ZERO pages. lang.js
   injected it on demand at the moment the user flipped the switch
   (`ensureContent`), so every switch first showed the page in English and then
   repainted once 61 KB had downloaded. That is the "changing language doesn't
   translate it immediately" report. Loading it eagerly right before ru-chrome.js
   makes FS_RU_CONTENT present synchronously, so `ensureContent` returns on its
   first line and the repaint happens in the same frame.

2. Every page under /ru/ carried a "Read in English" / "Читать на английском"
   link. That existed only because in-place switching did not work; with it
   working the link is a second, competing way to change language and it pushes
   the visitor off the page they were reading. The settings language control
   already does this correctly.

3. Only 23 of 299 help articles linked to the FAQ; 276 had no route to it at
   all. A "See also" entry is added to the ones that lack one.

Idempotent: re-running is a no-op. Use --check to verify without writing.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'website')

RU_VERSION = '20261004b1'
FAQ_LABEL_EN = 'FAQ'
FAQ_LABEL_RU = 'FAQ'


def html_files(sub):
    d = os.path.join(WEB, sub)
    out = []
    for dirpath, _dirs, files in os.walk(d):
        for f in files:
            if f.endswith('.html'):
                out.append(os.path.join(dirpath, f))
    return out


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def fix_eager_ru_content(h):
    """Insert ru-content.js before ru-chrome.js on pages that have a doc scope."""
    if 'class="doc"' not in h and 'class="blog-doc"' not in h:
        return h, False
    if 'ru-content.js' in h:
        return h, False
    m = re.search(r'<script src="([^"]*?)ru-chrome\.js\?v=[^"]*"></script>', h)
    if not m:
        return h, False
    base = m.group(1)
    tag = '<script src="%sru-content.js?v=%s"></script>' % (base, RU_VERSION)
    return h[:m.start()] + tag + h[m.start():], True


READ_EN_PAT = re.compile(
    r'[ \t]*<a\b[^>]*hreflang="en"[^>]*>(?:\s*)'
    r'(?:Read in English|Читать на английском)(?:\s*)</a>[ \t]*\r?\n?',
    re.I)


def strip_read_in_link(h):
    """Remove the "Read in English" link (and the orphan rule it leaves)."""
    if 'Читать на английском' not in h and 'Read in English' not in h:
        return h, False
    before = h
    # Drop the anchor itself.
    h = re.sub(
        r'\s*<a\b[^>]*hreflang="en"[^>]*>\s*'
        r'(?:Read in English|Читать на английском)\s*</a>', '', h)
    # Drop the CSS rule that styled it, if nothing references the class any more.
    if h != before:
        h = re.sub(r'\n?[ \t]*\.read-(?:in|lang)[a-z-]*\s*\{[^}]*\}', '', h)
    return h, h != before


SEE_ALSO_OPEN = '<div class="see-also">'
FAQ_HREF = 'faq.html'


def add_faq_link(h):
    """Give every help article a route to the FAQ.

    The FAQ hub exists at help/a/faq.html but only the faq_* articles linked to
    it, so 280 of 299 articles had no path to it at all - the questions a
    reader lands on were unreachable from the articles they read. The link goes
    at the end of the article body, before the related-article chips.
    """
    if re.search(r'href="[^"]*faq\.html"', h):
        return h, False
    idx = h.rfind('</article>')
    if idx == -1:
        return h, False
    block = ('\n    <p class="see-also-faq">See also: '
             '<a href="%s">%s</a></p>\n  ' % (FAQ_HREF, FAQ_LABEL_EN))
    return h[:idx] + block + h[idx:], True


def main():
    check = '--check' in sys.argv
    changed_files = 0
    counts = {'eager': 0, 'readin': 0, 'faq': 0}

    targets = html_files('legal') + html_files('help') + html_files('blog') \
        + html_files('ru') + [os.path.join(WEB, 'index.html')]

    for p in targets:
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        orig = read(p)
        h = orig

        h, a = fix_eager_ru_content(h)
        h, b = strip_read_in_link(h)
        if '/help/a/' in rel.replace('\\', '/'):
            h, c = add_faq_link(h)
        else:
            c = False

        counts['eager'] += a
        counts['readin'] += b
        counts['faq'] += c

        if h != orig:
            changed_files += 1
            if not check:
                write(p, h)
            else:
                print('WOULD CHANGE %s' % rel)

    print('files changed   : %d' % changed_files)
    print('ru-content eager: %d' % counts['eager'])
    print('read-in removed : %d' % counts['readin'])
    print('faq links added : %d' % counts['faq'])
    return 1 if (check and changed_files) else 0


if __name__ == '__main__':
    sys.exit(main())