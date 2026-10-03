"""One-off: dump exact built HTML regions that drifted from docs."""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

t = open(os.path.join(REPO, 'website', 'legal', 'terms.html'), encoding='utf-8').read()
p = open(os.path.join(REPO, 'website', 'legal', 'privacy.html'), encoding='utf-8').read()

out = []
out.append('### TERMS billed-p (line ~302)')
i = t.find('<p>Plans are billed in')
out.append(t[i:i + 900])
out.append('### TERMS intro-p count: %d' % t.count(
    '<p>Premium is offered at the prices displayed in the in-app premium menu. Current standard prices are:</p>'))
out.append('### TERMS <th>Price</th> count: %d' % t.count('<th>Price</th>'))
out.append('### TERMS toc old-label count: %d' % t.count('>13. Referral Program</a>'))
out.append('### TERMS toc old-title count: %d' % t.count('title="13. Referral Program"'))
out.append('### TERMS toc old-anchor count: %d' % t.count('#13-referral-program"'))

out.append('### PRIVACY website-region: find ul start')
j = p.find('Our Website is a static site (no user accounts')
# locate enclosing <ul> .. </ul>
us = p.rfind('<ul>', 0, j)
ue = p.find('</ul>', j) + len('</ul>')
out.append('UL region length: %d' % (ue - us))
out.append(p[us:ue][:300] + ' ...TAIL... ' + p[us:ue][-300:])
out.append('### PRIVACY after-ul (next 600 chars)')
out.append(p[ue:ue + 600])
out.append('### PRIVACY children paras')
k = p.find('<p>The Website itself is general-audience')
out.append(p[k:k + 1400])

open(os.path.join(REPO, 'tools', 'regions.txt'), 'w', encoding='utf-8').write('\n'.join(out))
