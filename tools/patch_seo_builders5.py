"""Round-5 SEO builder patches (idempotent).

Last two findings from tools/seo_meta.py:

  * Three category landing articles (Sender Bots, Channels, Import) still
    produced 53-69 character snippets: they have no prose and only two or
    three FAQ questions, so even the FAQ-derived text fell short of the 70
    character floor. Leading with the article title clears it.

  * blog/a/news-october-legal-refresh.html and
    blog/a/october-2026-legal-refresh.html covered the same October legal
    rewrite and shipped a byte-identical meta description. Only the shorter
    one is edited here; consolidating the two URLs is a content decision for
    the site owner (see docs/SEO_REPORT.md), and giving one a distinct
    snippet is the safe half of it.

Usage:  python tools/patch_seo_builders5.py [--check]
"""
import io
import os
import sys

BUILD = os.path.join('website', '_build')
EDITS = []


def edit(path, old, new, tag):
    EDITS.append((path, old, new, tag))


edit('build_static.py',
     "            if len(_body) < 70 and n.get('faq'):\n"
     "                # Category landing articles have no prose; the questions\n"
     "                # are the only sentence-like text they have.\n"
     "                _qs = ' '.join(strip_html(f['q']) for f in n['faq'][:4])\n"
     "                _body = (_body + ' ' + _qs).strip()\n",
     "            if len(_body) < 70 and n.get('faq'):\n"
     "                # Category landing articles have no prose; the questions\n"
     "                # are the only sentence-like text they have, and two of\n"
     "                # them are not enough to reach the 70 character floor.\n"
     "                _qs = ' '.join(strip_html(f['q']) for f in n['faq'][:4])\n"
     "                _body = ('%s: %s' % (n['title'], _qs)).strip()\n",
     'FAQ snippet leads with the article title')

edit('blog_articles_k.py',
     "   description='Privacy Policy, Terms and Refund Policy rewritten for clarity in October 2026: "
     "what changed, what stayed the same, and where every past version lives.',\n",
     "   description='Short news post on the October 2026 legal rewrite: what changed in the "
     "Privacy Policy, Terms and Refund Policy, and what did not.',\n",
     'distinct description for news-october-legal-refresh')


def main():
    check_only = '--check' in sys.argv
    ok = True
    for path, old, new, tag in EDITS:
        full = os.path.join(BUILD, path)
        src = io.open(full, encoding='utf-8').read()
        if new in src:
            status = 'ok     '
        elif old in src:
            if check_only:
                print('  %-16s PENDING %s' % (path, tag))
                ok = False
                continue
            if src.count(old) != 1:
                print('  %-16s AMBIGUOUS (%d) %s' % (path, src.count(old), tag))
                ok = False
                continue
            src = src.replace(old, new)
            io.open(full, 'w', encoding='utf-8', newline='\n').write(src)
            status = 'patched '
        else:
            print('  %-16s MISSING  %s' % (path, tag))
            ok = False
            continue
        print('  %-16s %s %s' % (path, status, tag))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())