"""Round-4 SEO builder patches (idempotent).

Round 3 cleared every title-length violation (35 -> 0) and cut duplicate
titles to one pair. Two things were left, both real content problems rather
than tooling problems:

  * help/a/<category-id>.html IS the category's landing article (backup,
    import, premium, channels, language, referral, timezone, bots,
    media_storage, start). Its body is empty -- everything lives in the FAQ
    block -- so the build fell back to the bare title and the SERP snippet
    read "Backup". Two effects: a 6-character snippet, and a title that
    collided with the real guide of the same name (help/a/start.html vs
    help/a/getting_started.html, both "Getting Started").

  * Those pages have no prose at all, only FAQ entries. The description has
    to be built from the questions.

Usage:  python tools/patch_seo_builders4.py [--check]
"""
import io
import os
import sys

BUILD = os.path.join('website', '_build')
EDITS = []


def edit(path, old, new, tag):
    EDITS.append((path, old, new, tag))


edit('build_static.py',
     "    _base_titles = {}\n"
     "    for _n in uniq_articles:\n"
     "        _base_titles[_n['id']] = '%s \\u2014 Fast Scheduler Help' % _n['title']\n",
     "    _base_titles = {}\n"
     "    for _n in uniq_articles:\n"
     "        _cat = by_id.get(_n.get('c'), {})\n"
     "        if _cat.get('id') and _n['id'] == _cat.get('id'):\n"
     "            # The category's own landing article: help/a/backup.html sits\n"
     "            # beside help/c/backup.html. It carries no prose, only FAQ, and\n"
     "            # its title collided with the real guide of the same name\n"
     "            # (start.html vs getting_started.html, both \"Getting Started\").\n"
     "            # Name it for what it actually is.\n"
     "            _base_titles[_n['id']] = '%s Overview \\u2014 Fast Scheduler Help' % _n['title']\n"
     "        else:\n"
     "            _base_titles[_n['id']] = '%s \\u2014 Fast Scheduler Help' % _n['title']\n",
     'category landing articles titled "Overview"')

edit('build_static.py',
     "        _dsrc = (n.get('description') or '').strip()\n"
     "        if len(_dsrc) < 70:\n"
     "            _dsrc = strip_html(n['content']) or _dsrc or n['title']\n",
     "        _dsrc = (n.get('description') or '').strip()\n"
     "        if len(_dsrc) < 70:\n"
     "            _body = strip_html(n['content'])\n"
     "            if len(_body) < 70 and n.get('faq'):\n"
     "                # Category landing articles have no prose; the questions\n"
     "                # are the only sentence-like text they have.\n"
     "                _qs = ' '.join(strip_html(f['q']) for f in n['faq'][:4])\n"
     "                _body = (_body + ' ' + _qs).strip()\n"
     "            _dsrc = _body or _dsrc or n['title']\n",
     'FAQ-derived descriptions')


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
                print('  %-14s PENDING %s' % (path, tag))
                ok = False
                continue
            if src.count(old) != 1:
                print('  %-14s AMBIGUOUS (%d) %s' % (path, src.count(old), tag))
                ok = False
                continue
            src = src.replace(old, new)
            io.open(full, 'w', encoding='utf-8', newline='\n').write(src)
            status = 'patched '
        else:
            print('  %-14s MISSING  %s' % (path, tag))
            ok = False
            continue
        print('  %-14s %s %s' % (path, status, tag))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())