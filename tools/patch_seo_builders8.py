"""Round-8 SEO patch (idempotent).

build_static.py disambiguates article page titles that repeat across
categories ("Signature" exists as both channel_signature and
glossary_signature), but the crawlable index in build_help.py rendered the
raw article title, so two rows in the index column still read "Signature"
while linking to different pages. The index now labels a repeated title with
its category, matching what the destination page's own title already says.

Usage:  python tools/patch_seo_builders8.py [--check]
"""
import io
import os
import sys

BUILD = os.path.join('website', '_build')
OLD = ("    _idx_groups = []\n"
       "    for g in groups:\n"
       "        _cid, _ctitle = g['cat']['id'], g['cat']['title']\n"
       "        _entries = ([g['cat']] if art_eligible(g['cat']) else []) + \\\n"
       "                   [k for k in g['kids'] if art_eligible(k)]\n"
       "        if not _entries:\n"
       "            continue\n")
NEW = ("    _idx_titles = {}\n"
       "    for g in groups:\n"
       "        for k in ([g['cat']] if art_eligible(g['cat']) else []) + \\\n"
       "                  [x for x in g['kids'] if art_eligible(x)]:\n"
       "            _idx_titles[k['title']] = _idx_titles.get(k['title'], 0) + 1\n"
       "    _idx_groups = []\n"
       "    for g in groups:\n"
       "        _cid, _ctitle = g['cat']['id'], g['cat']['title']\n"
       "        _entries = ([g['cat']] if art_eligible(g['cat']) else []) + \\\n"
       "                   [k for k in g['kids'] if art_eligible(k)]\n"
       "        if not _entries:\n"
       "            continue\n")

OLD2 = ("        _items = ''.join(\n"
        "            '<li><a href=\"help/a/%s.html\">%s</a></li>'\n"
        "            % (esc(k['id']),\n"
        "               esc(k['title'] + (' Overview' if k['id'] == _cid else '')))\n"
        "            for k in _entries)\n")
NEW2 = ("        def _idx_label(k):\n"
        "            if k['id'] == _cid:\n"
        "                return k['title'] + ' Overview'\n"
        "            if _idx_titles.get(k['title'], 0) > 1 and \\\n"
        "                    _ctitle.lower() != k['title'].lower():\n"
        "                return '%s (%s)' % (k['title'], _ctitle)\n"
        "            return k['title']\n"
        "        _items = ''.join(\n"
        "            '<li><a href=\"help/a/%s.html\">%s</a></li>'\n"
        "            % (esc(k['id']), esc(_idx_label(k)))\n"
        "            for k in _entries)\n")

EDITS = [('build_help.py', OLD, NEW, 'count repeated index titles'),
         ('build_help.py', OLD2, NEW2, 'index labels repeated titles with their category')]


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