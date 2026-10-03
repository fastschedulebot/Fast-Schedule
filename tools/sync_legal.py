"""One-off sync: built website/legal/*.html had drifted from docs/*.md.

Replaces the few stale blocks (terms section 10 pricing wording, privacy
section 4(m) website inventory, privacy section 12 children paragraph,
dead #13-referral-program TOC anchors) with the current docs render,
preserving version chrome (updated/effective/ver-dd/ver-changes/cards).

Safe to re-run (asserts exact single matches; no-ops when in sync).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_ru_legal import render

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGAL = os.path.join(REPO, 'website', 'legal')


def fresh_block(doc, start, end):
    html = render(os.path.join(REPO, 'docs', doc))
    i = html.find(start)
    assert i >= 0, 'fresh start missing: ' + start[:60]
    j = html.find(end, i) + len(end)
    assert j > i, 'fresh end missing: ' + end[:60]
    return html[i:j]


def sub_once(path, old, new):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    n = html.count(old)
    if n == 0:
        assert new in html, 'neither old nor new in ' + path + ' for ' + old[:70]
        print('already in sync:', os.path.basename(path), '-', old[:60].replace('\n', ' '))
        return
    assert n == 1, '%s: expected 1 match, found %d for %r' % (path, n, old[:70])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html.replace(old, new, 1))
    print('patched:', os.path.basename(path), '-', old[:60].replace('\n', ' '))


terms = os.path.join(LEGAL, 'terms.html')
privacy = os.path.join(LEGAL, 'privacy.html')
refund = os.path.join(LEGAL, 'refundpolicy.html')

# 1. terms section 10: pricing intro paragraph
sub_once(terms,
         '<p>Premium is offered at the prices displayed in the in-app premium menu. Current standard prices are:</p>',
         fresh_block('terms.md', '<p>Premium is offered at the prices',
                     'Current standard prices are:</p>'))
# 2. terms section 10: table header
sub_once(terms, '<th>Price</th>', '<th>Price (USD)</th>')
# 3. terms section 10: billed paragraph
sub_once(terms,
         '<p>Plans are billed in <strong>Telegram Stars</strong> at Telegram\'s Stars-to-currency rate at checkout; the USD figures above are reference equivalents. <strong>The in-bot prices at checkout are authoritative</strong> and override any figure quoted elsewhere. Prices may be adjusted from time to time. Changes apply to new purchases and renewals after reasonable notice. Promotional and introductory pricing may differ.</p>',
         fresh_block('terms.md', '<p>Plans are billed in',
                     'Promotional and introductory pricing may differ.</p>'))
# 4. TOC: dead #13-referral-program anchor + stale label (3 copies in terms)
for path, AnchorOld, AnchorNew in [
        (terms, '#13-referral-program"', '#13-referral-program-beta"'),
        (privacy, 'terms.html#13-referral-program"', 'terms.html#13-referral-program-beta"'),
        (refund, 'terms.html#13-referral-program"', 'terms.html#13-referral-program-beta"')]:
    with open(path, encoding='utf-8') as f:
        html = f.read()
    n = html.count(AnchorOld)
    if n == 0:
        assert AnchorNew in html, 'neither anchor in ' + path
        print('TOC already in sync:', os.path.basename(path))
        continue
    html = html.replace(AnchorOld, AnchorNew)
    n2 = html.count('>13. Referral Program</a>')
    assert n2 >= 1, 'label missing in ' + path
    html = html.replace('>13. Referral Program</a>', '>13. Referral Program (Beta)</a>')
    n3 = html.count('title="13. Referral Program"')
    assert n3 >= 1, 'title missing in ' + path
    html = html.replace('title="13. Referral Program"', 'title="13. Referral Program (Beta)"')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('patched TOC:', os.path.basename(path), 'anchors=%d labels=%d titles=%d' % (n, n2, n3))

# 5. privacy section 4(m): old bullet list -> current paragraphs (+ pipe table)
with open(privacy, encoding='utf-8') as f:
    phtml = f.read()
anchor = 'Our Website is a static site (no user accounts'
us = phtml.rfind('<ul>', 0, phtml.find(anchor))
assert us >= 0
ue = phtml.find('</ul>', us) + len('</ul>')
old_ul = phtml[us:ue]
assert old_ul.count('<li>') >= 5, 'unexpected ul region'
new_region = fresh_block('privacy.md', '<p>Our Website is a static site',
                         'only our own documentation and articles.</p>')
phtml = phtml[:us] + new_region + phtml[ue:]
with open(privacy, 'w', encoding='utf-8') as f:
    f.write(phtml)
print('patched: privacy.html - website inventory list -> paragraphs+table')

# 6. privacy section 12: two paragraphs -> one (matches docs)
sub_once(privacy,
         '<p>The Website itself is general-audience informational content (documentation, guides, legal pages) with no accounts, no age gate, and no data collection from visitors of any age. The 13+ requirement applies to using the Telegram bots (per Telegram\'s own age requirement).</p>\n<p>We do <strong>not</strong> knowingly collect Personal Data from children below the applicable minimum age. If you believe that a child has provided us with Personal Data without the requisite parental or guardian consent, please contact us immediately at fastschedulebot@gmail.com. If we become aware that we have inadvertently collected Personal Data from a child below the applicable minimum age, we will take steps to delete that information promptly.</p>',
         fresh_block('privacy.md', '<p>The Website itself is general-audience',
                     'delete that information promptly.</p>'))

print('sync done')
