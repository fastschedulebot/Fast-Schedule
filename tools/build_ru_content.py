"""Build website/scripts/ru-content.js: EN -> RU sentence dictionary.

Source: translations/en.json + translations/ru.json (same tree the help
center is generated from). Placeholders filled with plan kwargs (same as
the website build), markdown stripped, split into sentences. Only pairs
with equal sentence counts are kept (positional alignment).
"""
import html as H
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

en = json.load(open(os.path.join(REPO_ROOT, 'translations', 'en.json'), encoding='utf-8-sig'))
ru = json.load(open(os.path.join(REPO_ROOT, 'translations', 'ru.json'), encoding='utf-8-sig'))

try:
    from src.core.plans import get_help_kwargs as _g
    KW = _g()
except Exception:
    KW = {}


def flat(d, out, prefix=''):
    if isinstance(d, dict):
        for k, v in d.items():
            flat(v, out, prefix + '/' + k)
    elif isinstance(d, str):
        out[prefix] = d
    return out


def fill(s):
    return re.sub(r'\{(\w+)\}', lambda m: str(KW.get(m.group(1), m.group(0))), s)


def norm(s):
    s = H.unescape(s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', s)
    s = s.replace('*', '').replace('_', '').replace('`', '')
    s = re.sub(r'^#{1,4}\s*', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'([A-Za-z\u00c0-\u024f\u0400-\u04ff])(\d+\.)', r'\1 \2', s)
    s = re.sub(r'([.!?])([A-Z\u0410-\u042f\u0401])', r'\1 \2', s)
    return s


CMD = re.compile(r'https?|t\.me|[@<>]|^/|__')


def main():
    fe = flat(en, {})
    fr = flat(ru, {})
    pairs = {}
    skipped_ph = 0
    for path, es in fe.items():
        rs = fr.get(path)
        if not rs or es == rs:
            continue
        en_n = norm(fill(es))
        ru_n = norm(fill(rs))
        if not en_n or en_n == ru_n:
            continue
        if re.search(r'\{\w+\}', en_n + ru_n):
            skipped_ph += 1
            continue
        if CMD.search(en_n) or '`' in en_n:
            continue
        is_help = path.startswith('/help')
        en_segs = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', en_n) if s.strip()]
        ru_segs = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', ru_n) if s.strip()]
        if len(en_segs) == len(ru_segs) and len(en_segs) > 1:
            for a, b in zip(en_segs, ru_segs):
                if len(a) >= 18 and a != b and not CMD.search(a) and '`' not in a:
                    pairs[a] = b
        else:
            if len(en_n) >= (4 if is_help else 18):
                pairs[en_n] = ru_n
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
    print('pairs:', len(pairs), 'skipped_ph:', skipped_ph, 'bytes:', os.path.getsize(out))


if __name__ == '__main__':
    main()
