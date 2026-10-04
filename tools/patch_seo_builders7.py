"""Round-7 SEO patch (idempotent).

Round 1 gave help articles a stable first-seen date, but 328 of 404 sitemap
entries still carried `BUILD_DATE`: the home page, help.html, all 24 category
hubs and the three legal documents were re-dated on every single rebuild.
Google's guidance is explicit that a lastmod which is always "today" is worse
than no lastmod at all, because crawlers stop trusting it and stop scheduling
revisits on the dates you actually care about.

Same first-seen registry as the help articles, so the sitemap now only moves
when the page genuinely changes.

Usage:  python tools/patch_seo_builders7.py [--check]
"""
import io
import os
import sys

BUILD = os.path.join('website', '_build')
EDITS = []


def edit(path, old, new, tag):
    EDITS.append((path, old, new, tag))


edit('build_static.py',
     "            'url': canonical, 'dateModified': BUILD_DATE,\n",
     "            'url': canonical, 'dateModified': publish_date('hub', cid),\n",
     'category hub dateModified is stable')

edit('build_static.py',
     "    urls = [(SITE + '/', '1.0', BUILD_DATE), (SITE + '/help.html', '0.9', BUILD_DATE)]\n",
     "    urls = [(SITE + '/', '1.0', publish_date('site', 'home')),\n"
     "            (SITE + '/help.html', '0.9', publish_date('site', 'help'))]\n",
     'home + help lastmod are stable')

edit('build_static.py',
     "    urls += [(f'{SITE}/help/c/{cid}.html', '0.7', BUILD_DATE) for cid, _, _ in cat_urls]\n",
     "    urls += [(f'{SITE}/help/c/{cid}.html', '0.7', publish_date('hub', cid))\n"
     "             for cid, _, _ in cat_urls]\n",
     'category hub lastmod is stable')

edit('build_static.py',
     "    urls += [(SITE + '/legal/privacy.html', '0.4', BUILD_DATE),\n"
     "             (SITE + '/legal/terms.html', '0.4', BUILD_DATE),\n"
     "             (SITE + '/legal/refundpolicy.html', '0.4', BUILD_DATE)]\n",
     "    for _slug in ('privacy', 'terms', 'refundpolicy'):\n"
     "        urls.append((SITE + '/legal/%s.html' % _slug, '0.4',\n"
     "                     publish_date('legal', _slug)))\n",
     'legal lastmod is stable')

edit('build_static.py',
     "    d.setdefault('help', {})\n",
     "    d.setdefault('help', {})\n    d.setdefault('hub', {})\n"
     "    d.setdefault('legal', {})\n    d.setdefault('site', {})\n",
     'registry has slots for hub/legal/site')


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