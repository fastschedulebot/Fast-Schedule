"""Round-3 SEO builder patches (idempotent).

Round 2 fixed the crawl graph (327 orphans -> 0) and SERP-length clamping.
What is left, measured by tools/seo_meta.py:

  * 35 help articles still had titles under 30 chars ("Cloud — Fast Scheduler
    Help" is 27). Short titles waste result space and, worse, seven pairs
    collided outright ("Export" exists both as help/a/export.html and as the
    glossary entry help/a/glossary_export.html), which is how a searcher ends
    up on the wrong page.
  * 11 help articles inherited a 6-13 character meta description because the
    category articles carry no `description` field, so the build fell back to
    the bare title. SERP snippet reads "Backup".
  * 17 help articles reused their category hub's description verbatim.
  * help.html and index.html still emitted raw, un-clamped descriptions
    (163 and 236 chars) because those heads are built outside page_head().

Usage:  python tools/patch_seo_builders3.py [--check]
"""
import io
import os
import sys

BUILD = os.path.join('website', '_build')
EDITS = []


def edit(path, old, new, tag):
    EDITS.append((path, old, new, tag))


# ----------------------------------------------------- build_static.py ----
edit('build_static.py',
     "    # ---------------------------------------------------------- articles --\n"
     "    for n in uniq_articles:\n",
     '''    # Title disambiguation. "<Article> — Fast Scheduler Help" is too short for
    # a one-word article ("Cloud" -> 27 chars) and collides whenever two
    # articles share a title across categories (Export vs the Glossary entry
    # Export, Premium vs glossary_premium, Getting Started vs start, ...).
    # Qualify exactly those with their category so every title stays unique
    # and lands in the 30-65 char band search results actually show.
    _base_titles = {}
    for _n in uniq_articles:
        _base_titles[_n['id']] = '%s \\u2014 Fast Scheduler Help' % _n['title']
    _counts = {}
    for _t in _base_titles.values():
        _counts[_t] = _counts.get(_t, 0) + 1
    page_title = {}
    for _n in uniq_articles:
        _t = _base_titles[_n['id']]
        _cat = by_id.get(_n.get('c'), {})
        _ct = _cat.get('title', '')
        if len(_t) < 30 or _counts[_t] > 1:
            _alt = '%s: %s \\u2014 Fast Scheduler Help' % (_n['title'], _ct) if _ct else _t
            if _alt not in _counts:
                _t = _alt
            else:
                _t = '%s \\u2014 %s | Fast Scheduler' % (_n['title'], _ct)
        page_title[_n['id']] = _t

    # ---------------------------------------------------------- articles --
    for n in uniq_articles:
''',
     'unique, full-length help article titles')

edit('build_static.py',
     "        head = page_head(n['title'] + ' — Fast Scheduler Help', desc, canonical,\n",
     "        head = page_head(page_title[aid], desc, canonical,\n",
     'use page_title')

edit('build_static.py',
     "        desc = bh.smart_desc(\n"
     "            n.get('description') or strip_html(n['content']) or n['title'])\n"
     "        canonical = f'{SITE}/help/a/{aid}.html'\n",
     '''        # Category articles ship no `description` field, so the old build
        # fell back to the bare title ("Backup" as a 6-character snippet).
        _dsrc = (n.get('description') or '').strip()
        if len(_dsrc) < 70:
            _dsrc = strip_html(n['content']) or _dsrc or n['title']
        desc = bh.smart_desc(_dsrc)
        canonical = f'{SITE}/help/a/{aid}.html'
''',
     'article description never falls back to a bare title')

edit('build_static.py',
     "        desc = bh.smart_desc(\n"
     "            intro or f'{ctitle} — guides and answers in the Fast Scheduler help center.')\n",
     "        # Lead with the category so the hub's snippet never repeats the\n"
     "        # lead article's verbatim (17 pairs were byte-identical).\n"
     "        desc = bh.smart_desc(\n"
     "            f'{ctitle}: {len(entries)} guides in the Fast Scheduler help center. '\n"
     "            f'{intro or \"guides and answers for \" + ctitle.lower()}')\n",
     'category hub description is distinct')

# ------------------------------------------------------- build_help.py ----
# help.html writes its own <head> (it is not built through page_head()), so
# its title/description were never clamped and shipped at 163 characters.
edit('build_help.py',
     '  <title>Help Center — Fast Scheduler for Telegram</title>\n'
     '  <meta name="description" content="Searchable help center for Fast Scheduler: '
     'scheduling, recurring posts, sender bots, channels, statistics, premium and payments. '
     '{len(article_order)} answers, instantly searchable.">\n',
     '  <title>{fit_title("Help Center — Fast Scheduler for Telegram")}</title>\n'
     '  <meta name="description" content="{esc(smart_desc("Searchable help center for '
     'Fast Scheduler: scheduling, recurring posts, sender bots, channels, statistics, '
     'premium and payments. %d answers, instantly searchable." % len(article_order)))}">\n',
     'help.html title/desc clamped')

# smart_desc must be able to reach the 70-char floor before giving up.
edit('build_help.py',
     "    return best or _cut_words(t, limit)\n",
     '''    if best and len(best) < floor:
        # Still thin. Keep appending whole sentences (FAQ ledes are often two
        # short sentences) until the snippet has some weight in the SERP.
        for m in re.finditer(r'[.!?](?=\\s|$)', t[len(best):]):
            if len(best) + m.end() <= limit:
                best = t[:len(best) + m.end()]
            else:
                break
    return best or _cut_words(t, limit)
''',
     'smart_desc extends to the 70-char floor')

# NOTE: website/index.html is hand-maintained (no builder writes it), so its
# over-long description is edited directly, not from here.


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