"""Inspect a generated /ru/ page. Writes to a file: the Windows console
cannot print Cyrillic (cp1252), so stdout is not usable for this check."""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'website')
CYR = re.compile(r'[А-Яа-яЁё]')


def main():
    out = []
    p = sys.argv[1] if len(sys.argv) > 1 else 'ru/help/a/admins.html'
    s = io.open(os.path.join(SITE, p), encoding='utf-8').read()
    head = s.split('</head>')[0]
    out.append('file: %s (%d bytes)' % (p, len(s)))
    out.append('html lang : %s' % re.search(r'<html[^>]*\blang="([^"]+)"', s).group(1))
    t = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
    out.append('title(%d)  : %s' % (len(t), t))
    d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    out.append('desc(%d)   : %s' % (len(d.group(1)), d.group(1)))
    out.append('canonical : %s' % re.search(r'rel="canonical" href="(.*?)"', s).group(1))
    for m in re.finditer(r'hreflang="([^"]+)" href="([^"]+)"', head):
        out.append('  alt %-10s -> %s' % (m.group(1), m.group(2)))
    out.append('ld types  : %s' % re.findall(r'"@type": "([^"]+)"', head))
    out.append('h1 count  : %d' % s.count('<h1'))
    m = re.search(r'<article class="doc">(.*?)</article>', s, re.S)
    body = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip() if m else ''
    out.append('body      : %s' % body[:300])
    out.append('cyrillic  : %d chars in body, %d latin letters'
               % (len(CYR.findall(body)), len(re.findall(r'[A-Za-z]', body))))
    io.open(os.path.join(ROOT, '_verify_ru.txt'), 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote _verify_ru.txt')
    return 0


if __name__ == '__main__':
    sys.exit(main())