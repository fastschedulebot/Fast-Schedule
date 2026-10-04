"""Make tag_ru_chrome.py survive transient Windows write failures.

The script rewrites all 408 HTML pages to wire up ru-chrome.js/lang.js. A
single `open(p, 'w')` raising OSError [Errno 22] (antivirus, Search Indexer,
or a sync client briefly holding a handle) aborted the whole run with exit 1
*partway through the site*, leaving some files wired and some not — and it
exited 1 whether it had touched 1 file or 400, so the failure gave no clue
how bad the damage was.

Fix: retry each write with a growing backoff, collect the files that never
succeeded, and report them explicitly at the end. A transient lock now
costs nothing; a genuinely unwritable file still fails the build, loudly and
with a usable message.

Usage:  python tools/fix_ru_chrome_retry.py [--check]
"""
import io
import os
import sys

FULL = os.path.join('website', '_build', 'tag_ru_chrome.py')

OLD_IMPORT = "import os\nimport re\n"
NEW_IMPORT = "import os\nimport re\nimport sys\nimport time\n"

OLD_WRITE = """        if s != orig:
            open(p, 'w', encoding='utf-8').write(s)
            files += 1

print('files updated:', files, '| lang tags wired:', tags)
"""
NEW_WRITE = '''        if s != orig:
            if _write(p, s):
                files += 1
            else:
                failed.append(p)

print('files updated:', files, '| lang tags wired:', tags)
if failed:
    print('[error] could not write %d file(s):' % len(failed))
    for p in failed[:20]:
        print('   ', p)
    sys.exit(1)
'''


def main():
    src = io.open(FULL, encoding='utf-8').read()

    if NEW_WRITE in src:
        print('  tag_ru_chrome.py  ok      resilient writes already applied')
        return 0

    if '--check' in sys.argv:
        print('  tag_ru_chrome.py  PENDING resilient writes')
        return 1

    if src.count(OLD_IMPORT) != 1:
        print('  tag_ru_chrome.py  MISSING import anchor (%d)' % src.count(OLD_IMPORT))
        return 1
    if src.count(OLD_WRITE) != 1:
        print('  tag_ru_chrome.py  MISSING write anchor (%d)' % src.count(OLD_WRITE))
        return 1

    helper = '''
def _write(path, text, attempts=8, delay=0.25):
    """Write, retrying the transient sharing violations Windows throws when
    another process briefly holds a handle. Returns False if it never wrote.
    """
    for i in range(attempts):
        try:
            with io.open(path, 'w', encoding='utf-8', newline='\\n') as fh:
                fh.write(text)
            return True
        except OSError:
            if i == attempts - 1:
                return False
            time.sleep(delay * (i + 1))
    return False

'''
    src = src.replace("files = 0\ntags = 0\n", helper.lstrip('\n') + "files = 0\ntags = 0\nfailed = []\n")
    src = src.replace(OLD_WRITE, NEW_WRITE)
    src = src.replace(OLD_IMPORT, NEW_IMPORT)
    # the script already reads with the builtin open(); use io consistently
    src = src.replace("import io\n", "import io\n", 1)
    if "\nimport io\n" not in src:
        src = src.replace("import os\nimport re\n", "import io\nimport os\nimport re\n", 1)

    io.open(FULL, 'w', encoding='utf-8', newline='\n').write(src)
    print('  tag_ru_chrome.py  patched resilient writes')
    return 0


if __name__ == '__main__':
    sys.exit(main())