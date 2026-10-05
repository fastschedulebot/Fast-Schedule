"""Compare repo-root web tree vs website/ tree (names + sizes only)."""
import os

SKIP_DIRS = {'_build', '__pycache__'}
ROOT_WEB = ['index.html', 'help.html', '404.html', 'robots.txt', 'sitemap.xml',
            'llms.txt', 'llms-full.txt', 'blog', 'help', 'legal', 'ru', 'scripts',
            'styles', 'fonts', 'apple-touch-icon.png', 'og-cover-v2.png',
            'brand-logo.png', 'brand-logo-128.png', 'brand-logo-64.png',
            'icon-96.png', 'icon-48.png', 'favicon-32.png', 'favicon-16.png',
            'storage_state.json', '_headers',
            '5817133906fc4ab78b0f19ca52bf8f58.txt']


def snap(base):
    out = {}
    for top in ROOT_WEB:
        p = os.path.join(base, top)
        if os.path.isfile(p):
            out[top] = os.path.getsize(p)
        elif os.path.isdir(p):
            for dp, dn, fn in os.walk(p):
                dn[:] = [d for d in dn if d not in SKIP_DIRS]
                for f in fn:
                    fp = os.path.join(dp, f)
                    out[os.path.relpath(fp, base)] = os.path.getsize(fp)
        else:
            out[top] = None
    return out


a = snap('.')
b = snap('website')
keys = sorted(set(a) | set(b))
only_a, only_b, diff, same = [], [], [], 0
for k in keys:
    va, vb = a.get(k, 'ABSENT'), b.get(k, 'ABSENT')
    if k not in b or b[k] is None and k not in a:
        pass
    if va == 'ABSENT' or (k in a and a[k] is None):
        only_b.append(k)
    elif vb == 'ABSENT' or (k in b and b[k] is None):
        only_a.append(k)
    elif va != vb:
        diff.append(k)
    else:
        same += 1
print('identical: %d  different: %d' % (same, len(diff)))
print('--- only in root (%d):' % len(only_a))
print('\n'.join('  ' + x for x in only_a[:30]))
print('--- only in website (%d):' % len(only_b))
print('\n'.join('  ' + x for x in only_b[:30]))
print('--- different, largest first:')
import heapq
rows = []
for k in diff:
    rows.append((abs(a[k] - b[k]), k, a[k], b[k]))
for _, k, va, vb in heapq.nlargest(30, rows):
    print('  %s root=%d web=%d' % (k, va, vb))
