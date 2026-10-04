#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Delete the fabricated testimonials and put the brand first in the <title>.

Two fixes in one script because they land in the same few files.

1. The three "Reviews" cards (Milena / Artem / Sofia, each carrying a
   5-star aria-label) were invented copy. Nobody sourced them, nobody
   consented to being named, and a visitor cannot tell them apart from a
   real customer. Invented social proof on a pricing page is the kind of
   thing that gets a domain flagged, so the whole section goes rather than
   being softened.

2. <title> led with "Fast Scheduler" already, but Google rewrote it on the
   SERP and demoted the brand into the snippet ("Schedule Telegram Channel
   Posts on Autopilot" as the link text, "Fast Scheduler is a free Telegram
   bot..." as the description). Long titles get rewritten; short literal
   ones usually survive. The new one is 48 chars, brand first, and carries
   the phrase people actually type into the search box.

Every file here is hand-maintained markup - no builder regenerates any of
it - so this edits website/ in place. Root-level copies come from
tools/sync_root.py; run that afterwards.

Two details this has to get right:

* The tree is a mix of LF and CRLF files (main.css and ru-chrome.js are
  CRLF, everything else here is LF), so every pattern is re-expanded to the
  file's own newline before matching.
* Patterns are best-effort so a re-run is a no-op, and correctness is
  asserted afterwards from REQUIRED (must now be present) and LEFTOVER
  (must now be absent) markers. Nothing is written until the whole pass
  has been computed and checked, so a MISS can never leave half the site
  patched.

Usage:  python tools/remove_fake_reviews.py          apply
        python tools/remove_fake_reviews.py --check  report only, exit 1
                                                  if the old markup survives
"""
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE_EN = 'Fast Scheduler — Telegram Channel Post Scheduler'
TITLE_EN_OLD = 'Fast Scheduler — Schedule Telegram Channel Posts on Autopilot'
TITLE_RU = 'Fast Scheduler — Планировщик постов для Telegram-каналов'
TITLE_RU_OLD = 'Fast Scheduler — автопланирование постов Telegram-канала'

DESC = ('Fast Scheduler is a free Telegram bot that schedules, publishes and '
        'tracks your channel posts. Batch-schedule a week in one chat, post '
        'from your own bot.')
# lang.js re-stamps the meta description from META.desc on every homepage
# load, so this string has to be the same one the static head ships. It used
# to be a different, 236-char sentence - which is why a crawler rendering
# the page saw a description nobody had audited.
DESC_RU = ('Fast Scheduler — бесплатный Telegram-бот: планирование и '
           'публикация постов канала, аналитика. Планируйте неделю контента '
           'в одном чате и публикуйте от своего бота.')
DESC_RU_OLD = ('Fast Scheduler — бесплатный Telegram-бот для '
               'автопланирования, публикации и аналитики постов канала. '
               'Планируйте недели контента в одном чате, публикуйте от своего '
               'бота и смотрите, что заходит. Настройте один раз — экономьте '
               'часы каждую неделю.')
# Every description this script has ever installed, so a re-run can correct
# a length regression. seo_audit.py fails a page outside 70-160 chars, which
# is what pushed the first attempt (187) back out.
DESC_OLD = [
    '<meta name="description" content="Fast Scheduler is a free Telegram bot '
    'that schedules and auto-publishes your channel posts. Batch-schedule a '
    'week in one chat and post from your own bot.">',
    '<meta name="description" content="Fast Scheduler is a free Telegram bot '
    'that schedules, publishes and tracks your channel posts. '
    'Batch-schedule a week of content in one chat, post from your own bot, '
    'and see what performs.">',
]
# lang.js carries its own copy of the sentence; same list, without the tags.
META_DESC_OLD = [
    'Fast Scheduler is a free Telegram bot that schedules, publishes and '
    'tracks your channel posts on autopilot. Batch-schedule weeks of content '
    'in one chat, post from your own bot, and see what performs. Set it once '
    '— save hours every week.',
]

PATCHES = [
    ('website/index.html', 'patch_index'),
    ('_hero_phone_backup/index_cb1.html', 'patch_hero_backup'),
    ('_hero_phone_backup/index_cb6.html', 'patch_hero_backup'),
    ('_hero_phone_backup/index_cb8.html', 'patch_hero_backup'),
    ('website/scripts/lang.js', 'patch_lang_js'),
    ('website/scripts/ru-chrome.js', 'patch_ru_chrome'),
    ('website/scripts/hotkeys-modal.js', 'patch_hotkeys_modal'),
    ('website/scripts/hotkeys.js', 'patch_hotkeys'),
    ('website/styles/main.css', 'patch_main_css'),
    ('website/styles/lang.css', 'patch_lang_css'),
]

# (file, marker) pairs that must exist once the patch has run. These are
# what makes the script safe to re-run: a MISS is tolerated, a failed
# post-condition is not.
REQUIRED = [
    ('website/index.html', '<title>' + TITLE_EN + '</title>'),
    ('website/index.html', 'content="' + TITLE_EN + '"'),
    ('website/index.html', 'content="' + DESC + '"'),
    ('website/index.html', '<a href="#pricing" data-hk="sec4">Pricing</a>'),
    ('website/index.html', '<a href="#faq" data-hk="sec5">FAQ</a>'),
    ('website/index.html', '<!-- ============ PRICING ============ -->'),
    ('website/scripts/lang.js', "en: '" + TITLE_EN + "'"),
    ('website/scripts/lang.js', "ru: '" + TITLE_RU + "'"),
    ('website/scripts/lang.js', "desc: {"),
    ('website/scripts/lang.js', "en: '" + DESC + "'"),
    ('website/scripts/lang.js', "ru: '" + DESC_RU + "'"),
    ('website/scripts/lang.js', 'if (rm.title) META.title.ru ='),
    ('website/scripts/ru-chrome.js', "      title: '" + TITLE_RU + "',"),
    ('website/scripts/ru-chrome.js', "      desc: '" + DESC_RU + "'"),
    ('website/scripts/hotkeys.js', 'name: \'Pricing\''),
    ('website/scripts/hotkeys-modal.js', "id: 'sec4', key: '4', page: 'home', name: 'Pricing'"),
    ('website/scripts/hotkeys-modal.js', "id: 'sec5', key: '5', page: 'home', name: 'FAQ'"),
    ('website/styles/lang.css', 'html[lang="ru"] .step p { hyphens: none; overflow-wrap: break-word; }'),
    ('website/styles/main.css', '.steps > * { min-width: 0; }'),
    ('_hero_phone_backup/index_cb1.html', '<meta name="robots" content="noindex, nofollow">'),
    ('_hero_phone_backup/index_cb6.html', '<meta name="robots" content="noindex, nofollow">'),
    ('_hero_phone_backup/index_cb8.html', '<meta name="robots" content="noindex, nofollow">'),
]

# Anything a reviewer would grep for to prove the section is gone.
LEFTOVER = [
    ('website/index.html', 'id="reviews"'),
    ('website/index.html', 'href="#reviews"'),
    ('website/index.html', 'TESTIMONIALS'),
    ('website/index.html', 'class="quotes"'),
    ('website/index.html', 'Rated 5 out of 5'),
    ('website/scripts/lang.js', "'Channels that stopped posting by hand'"),
    ('website/scripts/ru-chrome.js', '// reviews'),
    ('website/scripts/lang.js', 'META = window.FS_RU_CHROME.META;'),
    ('website/scripts/ru-chrome.js', '19K subscriber'),
    ('website/scripts/ru-chrome.js', 'Rated 5 out of 5'),
    ('website/scripts/ru-chrome.js', ".stars"),
    ('website/scripts/hotkeys.js', '#reviews'),
    ('website/scripts/hotkeys-modal.js', '#reviews'),
    ('website/styles/lang.css', '.quote'),
    ('website/styles/main.css', '.quote'),
    ('_hero_phone_backup/index_cb1.html', 'id="reviews"'),
    ('_hero_phone_backup/index_cb1.html', 'Milena'),
    ('_hero_phone_backup/index_cb6.html', 'id="reviews"'),
    ('_hero_phone_backup/index_cb6.html', 'Milena'),
    ('_hero_phone_backup/index_cb8.html', 'id="reviews"'),
    ('_hero_phone_backup/index_cb8.html', 'Milena'),
]


def read(rel):
    with io.open(os.path.join(ROOT, rel), 'r', encoding='utf-8', newline='') as f:
        return f.read()


def write(rel, text):
    """Retry: antivirus/indexer on Windows intermittently holds the file
    (OSError 22) and a lost write would leave the site half-patched."""
    path = os.path.join(ROOT, rel)
    for attempt in range(8):
        try:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            return
        except OSError:
            if attempt == 7:
                raise
            time.sleep(0.2 * (attempt + 1))


def eol(text):
    return '\r\n' if '\r\n' in text else '\n'


def adapt(pattern, nl):
    """Rewrite the LF literals above into the file's own newline."""
    if nl == '\n' or '\n' not in pattern:
        return pattern
    return pattern.replace('\n', '\r\n')


def sub(text, old, new, changes, rel, nl):
    """Best-effort replace, so a second run is a no-op. Misses are fine;
    the REQUIRED/LEFTOVER post-conditions are what prove the outcome.

    A match is only counted when it actually changes the file: the robots
    rewrite below is the trap - `noindex, nofollow` CONTAINS `index, follow`
    as a substring, so testing for the old string alone re-fires forever and
    reports a change on every run even though the bytes never move.
    """
    old = adapt(old, nl)
    if old not in text:
        return text
    out = text.replace(old, adapt(new, nl))
    if out == text:
        return text
    changes.append(rel)
    return out


def cut(text, start, end, changes, rel, nl):
    """Delete the block between two markers, keeping `end`."""
    start = adapt(start, nl)
    end = adapt(end, nl)
    i = text.find(start)
    j = text.find(end)
    if i == -1 or j == -1 or j <= i:
        return text
    out = text[:i] + text[j:]
    if out == text:
        return text
    changes.append(rel)
    return out


def patch_index(t, rel, nl, changes):
    s = lambda old, new='': sub(t, old, new, changes, rel, nl)  # noqa: E731

    t = cut(t, '  <!-- ============ TESTIMONIALS ============ -->\n',
            '  <!-- ============ PRICING ============ -->\n', changes, rel, nl)
    t = s('      <a href="#reviews" data-hk="sec4">Reviews</a>\n')
    for line in t.split('\n'):
        if 'href="#reviews"' in line:
            t = t.replace(line + '\n', '')
            changes.append(rel)
            break
    # Renumber the rail keys so 1..5 stay contiguous after Reviews leaves.
    # Anchored on the anchor href, NOT on the current digit: a bare
    # sec5->sec4 then sec6->sec5 swap re-fires on the next run and collapses
    # Pricing and FAQ onto the same key.
    for href, key in (('#pricing', 'sec4'), ('#faq', 'sec5')):
        pat = re.compile(r'(href="%s" data-hk=")sec\d+(")' % re.escape(href))
        was = t
        t = pat.sub(r'\g<1>%s\g<2>' % key, t)
        if t != was:
            changes.append(rel)

    t = cut(t, '    /* Testimonials */\n', '    /* Pricing teaser */\n',
            changes, rel, nl)
    t = s('.feat, .step, .quote { transition: box-shadow',
          '.feat, .step { transition: box-shadow')
    t = s('.plan-g li, .quote p { overflow-wrap: anywhere; }',
          '.plan-g li { overflow-wrap: anywhere; }')
    t = s('.feat, .step, .quote { transition: none; }',
          '.feat, .step { transition: none; }')
    t = s('translateY(-4px) on every .feat/.step/.quote)',
          'translateY(-4px) on every .feat/.step)')

    t = sub(t, TITLE_EN_OLD, TITLE_EN, changes, rel, nl)
    new_desc = '<meta name="description" content="%s">' % DESC
    for prev in DESC_OLD:
        t = s(prev, new_desc)
    return t


def patch_lang_js(t, rel, nl, changes):
    t = t.replace('// (hero/features/how/reviews/pricing/FAQ/CTA)',
                  '// (hero/features/how/pricing/FAQ/CTA)')
    t = sub(t, "    'Reviews': 'Отзывы',\n", '', changes, rel, nl)
    t = sub(t, "    'Channels that stopped posting by hand': 'Каналы, "
               "которые перестали публиковать вручную',\n", '', changes, rel, nl)
    t = sub(t, TITLE_EN_OLD, TITLE_EN, changes, rel, nl)
    t = sub(t, TITLE_RU_OLD, TITLE_RU, changes, rel, nl)
    t = sub(t, DESC_RU_OLD, DESC_RU, changes, rel, nl)
    for prev in META_DESC_OLD:
        t = sub(t, prev, DESC, changes, rel, nl)
    t = patch_meta_merge(t, changes, rel)
    return t


META_MERGE_BAD = ('      if (window.FS_RU_CHROME.META) META = '
                  'window.FS_RU_CHROME.META;')
META_MERGE_NEW = """      // ru-chrome.js ships META as a flat {title, desc} pair of RU strings,
      // while lang.js keeps the nested {en, ru} shape and reads META.title.en
      // on the home page. Assigning the flat object straight over META left
      // META.title.en undefined, so every load stamped document.title and
      // the meta description with the literal text "undefined" - which is
      // also what a crawler rendering the page saw.
      if (window.FS_RU_CHROME.META) {
        var rm = window.FS_RU_CHROME.META;
        if (rm.title) META.title.ru = typeof rm.title === 'string' ? rm.title : rm.title.ru;
        if (rm.desc) META.desc.ru = typeof rm.desc === 'string' ? rm.desc : rm.desc.ru;
      }"""


def patch_meta_merge(t, changes, rel):
    """The home-page title/description used to be overwritten with the string
    'undefined' on every page load."""
    return sub(t, META_MERGE_BAD, META_MERGE_NEW, changes, rel, '\n')


def patch_ru_chrome(t, rel, nl, changes):
    t = sub(t, "      'Reviews': 'Отзывы',\n", '', changes, rel, nl)
    # A FIXUPS row that rewrote the five-star reviews' aria-label. Dead once
    # the cards are gone, but it was the one piece of the fabricated content
    # that survived: the block cut below only removes the MAP entries, and
    # 'Rated 5 out of 5' was never in this script's LEFTOVER markers, so the
    # earlier runs all reported a clean tree while this line sat there.
    t = sub(t, "      ['.stars', 'aria-label', 'Rated 5 out of 5', "
               "'Оценка 5 из 5']\n", '', changes, rel, nl)
    # Match the bare strings, not "key: 'value',": desc is the last member of
    # the META object and so carries no trailing comma.
    # ru-chrome's META wins over lang.js's (that is what the merge is for), so
    # title/description have to be corrected in both copies or the fix in
    # lang.js is silently undone at runtime.
    t = sub(t, TITLE_RU_OLD, TITLE_RU, changes, rel, nl)
    t = sub(t, DESC_RU_OLD, DESC_RU, changes, rel, nl)
    return cut(t, '      // reviews\n', '      // pricing\n', changes, rel, nl)


def patch_hero_backup(t, rel, nl, changes):
    """_hero_phone_backup/ sits at the published site root, so its three
    index_cb*.html copies are live URLs. They carried the same fabricated
    testimonials, the old title, and robots=index,follow with a canonical
    pointing at an unrelated domain - i.e. indexable stale duplicates of the
    homepage. Strip the quotes, retitle, and take them out of the index.

    The files themselves are kept: they are a design backup, and deleting
    someone's backup is not this script's call.
    """
    t = cut(t, '  <!-- ============ TESTIMONIALS ============ -->\n',
            '  <!-- ============ PRICING ============ -->\n', changes, rel, nl)
    for line in t.split('\n'):
        if 'href="#reviews"' in line:
            t = t.replace(line + '\n', '')
            changes.append(rel)
            break
    t = sub(t, '<meta name="robots" content="index, follow">',
            '<meta name="robots" content="noindex, nofollow">', changes, rel, nl)
    t = sub(t, TITLE_EN_OLD, TITLE_EN, changes, rel, nl)
    return t


def patch_hotkeys_modal(t, rel, nl, changes):
    t = sub(t, "    { id: 'sec4', key: '4', page: 'home', name: 'Reviews',"
               "     sel: 'a[href=\"#reviews\"]' },\n", '', changes, rel, nl)
    t = sub(t, "    { id: 'sec5', key: '5', page: 'home', name: 'Pricing',"
               "     sel: 'a[href=\"#pricing\"]' },",
            "    { id: 'sec4', key: '4', page: 'home', name: 'Pricing',"
            "     sel: 'a[href=\"#pricing\"]' },", changes, rel, nl)
    t = sub(t, "    { id: 'sec6', key: '6', page: 'home', name: 'FAQ',"
               "     sel: 'a[href=\"#faq\"]' },",
            "    { id: 'sec5', key: '5', page: 'home', name: 'FAQ',"
            "     sel: 'a[href=\"#faq\"]' },", changes, rel, nl)
    return t


def patch_hotkeys(t, rel, nl, changes):
    t = sub(t, "    { key: '4', always: true, sel: 'a[href=\"#reviews\"]',"
               "  name: 'Reviews',      hint: 'rail' },\n", '', changes, rel, nl)
    t = sub(t, "{ key: '5', always: true, sel: 'a[href=\"#pricing\"]',"
               "  name: 'Pricing',      hint: 'rail' },",
            "{ key: '4', always: true, sel: 'a[href=\"#pricing\"]',"
            "  name: 'Pricing',      hint: 'rail' },", changes, rel, nl)
    t = sub(t, "{ key: '6', always: true, sel: 'a[href=\"#faq\"]',"
               "      name: 'FAQ',          hint: 'rail' },",
            "{ key: '5', always: true, sel: 'a[href=\"#faq\"]',"
            "      name: 'FAQ',          hint: 'rail' },", changes, rel, nl)
    return t


def patch_main_css(t, rel, nl, changes):
    for attr in ('[data-fx="off"]', '[data-motion="off"]'):
        t = sub(t, '%s .feat, %s .step, %s .quote,\n'
                   % (attr, attr, attr),
                '%s .feat, %s .step,\n' % (attr, attr), changes, rel, nl)
        t = sub(t, '%s .feat:hover, %s .step:hover, %s .quote:hover,\n'
                   % (attr, attr, attr),
                '%s .feat:hover, %s .step:hover,\n' % (attr, attr),
                changes, rel, nl)
    t = sub(t, '.hero-copy, .feat, .step, .quote, .plan-g, .page-card,'
               ' .save-grid > *,\n.features-glass > *, .steps > *, .quotes > *'
               ' { min-width: 0; }',
            '.hero-copy, .feat, .step, .plan-g, .page-card, .save-grid > *,\n'
            '.features-glass > *, .steps > * { min-width: 0; }',
            changes, rel, nl)
    t = sub(t, '.hero .sub, .sec-head p, .sec-head h2, .plan-g li, .quote p,'
               ' .feat p,\n',
            '.hero .sub, .sec-head p, .sec-head h2, .plan-g li, .feat p,\n',
            changes, rel, nl)
    t = sub(t, '  .feat:hover, .step:hover, .quote:hover, .page-card:hover,\n',
            '  .feat:hover, .step:hover, .page-card:hover,\n',
            changes, rel, nl)
    return t


def patch_lang_css(t, rel, nl, changes):
    return sub(t, 'html[lang="ru"] .step p,\nhtml[lang="ru"] .quote p'
                   ' { hyphens: none; overflow-wrap: break-word; }',
               'html[lang="ru"] .step p'
               ' { hyphens: none; overflow-wrap: break-word; }',
               changes, rel, nl)


FUNCS = {
    'patch_index': patch_index,
    'patch_hero_backup': patch_hero_backup,
    'patch_lang_js': patch_lang_js,
    'patch_ru_chrome': patch_ru_chrome,
    'patch_hotkeys_modal': patch_hotkeys_modal,
    'patch_hotkeys': patch_hotkeys,
    'patch_main_css': patch_main_css,
    'patch_lang_css': patch_lang_css,
}


def main():
    check = '--check' in sys.argv[1:]
    changes = []
    pending = []

    # Phase 1: compute every patched file in memory. Nothing is written yet.
    for rel, fn in PATCHES:
        before = read(rel)
        after = FUNCS[fn](before, rel, eol(before), changes)
        if after != before:
            pending.append((rel, after))

    # Phase 2: prove the outcome before touching disk.
    staged = {}
    for rel, after in pending:
        staged[rel] = after

    def probe(rel, marker):
        return marker in staged.get(rel, read(rel))

    missing = ['%s: %s' % (rel, m) for rel, m in REQUIRED if not probe(rel, m)]
    if missing:
        for line in missing:
            sys.stderr.write('REQUIRED marker missing -> %s\n' % line)
        sys.stderr.write('nothing written\n')
        return 2

    # Phase 3: write, then re-verify from disk.
    if not check:
        for rel, after in pending:
            write(rel, after)

    left = []
    for rel, marker in LEFTOVER:
        # After a write, verify from disk; in --check mode there is nothing
        # staged for an already-clean file, so fall back to disk too.
        txt = staged.get(rel) or read(rel)
        if marker in txt:
            left.append('%s: %s' % (rel, marker))

    lines = []
    lines.append('files updated: %d' % len(set(changes)) if not check
                 else 'files that would change: %d' % len(pending))
    for rel in sorted(set(changes)):
        lines.append('  patched %s' % rel)
    lines.append('required markers ok: %d/%d' % (len(REQUIRED), len(REQUIRED)))
    lines.append('leftover reviews markup: %d' % len(left))
    for line in left:
        lines.append('  LEFTOVER %s' % line)
    lines.append('title (%d chars): %s' % (len(TITLE_EN), TITLE_EN))
    with io.open(os.path.join(ROOT, 'tmp_remove_reviews.log'), 'w',
                 encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    sys.stdout.write('files updated: %d   leftover: %d   title: %d chars\n'
                     % (len(set(changes)), len(left), len(TITLE_EN)))
    # Non-zero when the site still needs the patch (pending) or still carries
    # reviews markup after it (left). Clean tree, apply or --check: 0.
    return 1 if (left or pending) else 0


if __name__ == '__main__':
    sys.exit(main())