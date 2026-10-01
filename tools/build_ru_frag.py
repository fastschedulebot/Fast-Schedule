"""Fragment-level RU dictionary for the website language switcher.

Renders every help leaf through the site's own text_to_html() (same
function the build uses) in EN and RU, splits rendered HTML into text
fragments in document order, and pairs them 1:1. This matches what the
pages actually contain (inline <b>/<code> splits, steps, list items),
unlike sentence-level matching.

Merges with tools/ru_blog_extra.json (blog titles/descriptions) and
writes website/scripts/ru-content.js.
"""
import html as H
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, os.path.join(REPO_ROOT, 'website', '_build'))

from build_help import text_to_html, fill_placeholders  # noqa: E402


def flat(d, out, prefix=''):
    if isinstance(d, dict):
        for k, v in d.items():
            flat(v, out, prefix + '/' + k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            flat(v, out, prefix + '/' + str(i))
    elif isinstance(d, str):
        out[prefix] = d
    return out


def frags(html):
    """Text fragments of rendered HTML in document order, normalized."""
    parts = re.split(r'<[^>]+>', html)
    out = []
    for p in parts:
        t = H.unescape(p)
        t = re.sub(r'\s+', ' ', t).strip()
        t = re.sub(r'([A-Za-z\u00c0-\u024f\u0400-\u04ff])(\d+\.)', r'\1 \2', t)
        t = re.sub(r'([.!?])([A-Z\u0410-\u042f\u0401])', r'\1 \2', t)
        if t:
            out.append(t)
    return out


def main():
    en = json.load(open(os.path.join(REPO_ROOT, 'translations', 'en.json'), encoding='utf-8-sig'))
    ru = json.load(open(os.path.join(REPO_ROOT, 'translations', 'ru.json'), encoding='utf-8-sig'))
    fe = flat(en.get('help', {}), {})
    fr = flat(ru.get('help', {}), {})
    pairs = {}
    aligned = 0
    fallback = 0
    for path, es in fe.items():
        rs = fr.get(path)
        if not rs or es == rs:
            continue
        is_faq_a = path.rstrip('/').endswith('/a') and '/faq/' in path
        en_r = text_to_html(fill_placeholders(es))
        ru_r = text_to_html(fill_placeholders(rs))
        ef, rf = frags(en_r), frags(ru_r)
        if ef and len(ef) == len(rf):
            for a, b in zip(ef, rf):
                if a != b and len(a) >= 2:
                    pairs[a] = b
            aligned += 1
        else:
            en_n = re.sub(r'\s+', ' ', H.unescape(es)).strip()
            ru_n = re.sub(r'\s+', ' ', H.unescape(rs)).strip()
            if en_n != ru_n and len(en_n) >= 4 and '{' not in en_n + ru_n:
                pairs[en_n] = ru_n
            fallback += 1
    print('leaves:', len(fe), 'aligned:', aligned, 'fallback:', fallback)
    extra_path = os.path.join(REPO_ROOT, 'tools', 'ru_blog_extra.json')
    if os.path.exists(extra_path):
        extra = json.load(open(extra_path, encoding='utf-8'))
        n0 = len(pairs)
        for section in ('titles', 'descs'):
            for ek, rv in extra.get(section, {}).items():
                if ek and rv and ek != rv and ek not in pairs:
                    pairs[ek] = rv
        print('blog extra:', len(pairs) - n0)
    js = 'window.FS_RU_CONTENT=' + json.dumps(pairs, ensure_ascii=False, separators=(',', ':')) + ';'
    out = os.path.join(REPO_ROOT, 'website', 'scripts', 'ru-content.js')
    open(out, 'w', encoding='utf-8').write(js)
    print('pairs:', len(pairs), 'bytes:', os.path.getsize(out))


if __name__ == '__main__':
    main()
