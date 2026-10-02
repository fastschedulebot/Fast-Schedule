# -*- coding: utf-8 -*-
"""Blog articles, part 9 — Fast Scheduler Referral Program (beta).

Same editorial rules as blog_articles*.py: real numbers, real mechanics,
named plainly. This one documents our own referral program: why unlocking
needs verification, how crediting works step by step, and what beta means.
"""

BLOG_ARTICLES_I = []

def _a(i, **kw):
    kw['id'] = i
    BLOG_ARTICLES_I.append(kw)

# ============================================================ GROWTH ======

_a('fast-scheduler-referral-program-beta',
   category='growth',
   title='Fast Scheduler Referral Program (Beta): Earn Premium Days for Invites',
   description='How the Fast Scheduler referral program works: why unlocking needs a connected channel plus one scheduled message, how both sides earn 3 Premium days, limits, and what beta status means for you.',
   date='2026-09-28',
   content=(
       "<p>Fast Scheduler has a referral program, currently in <b>beta</b>: "
       "invite channel owners, and both you and the newcomer earn "
       "<b>3 Premium days</b> for every qualifying referral, up to "
       "<b>15 referees (45 days total)</b>. Your personal link lives in "
       "the bot under <code>/referral</code> or Premium &rarr; Referral "
       "Program. This guide explains the two things that confuse people "
       "most: why the program stays locked until you verify, and exactly "
       "when the days land in your balance.</p>"

       "<h3>Why unlocking requires a channel plus one message</h3>"
       "<p>Open the referral menu on a fresh account and you will see a "
       "lock screen instead of your link: connect your channel and "
       "schedule at least one message first. This is deliberate, and it "
       "is the same bar for everyone. Premium days cost real money "
       "\u2014 every gifted day is server time and Telegram Stars fees "
       "paid out of our pocket. Without a verification step, anyone "
       "could generate dozens of empty accounts in an afternoon and "
       "drain the reward pool, which would force us to kill the program "
       "for honest users too.</p>"
       "<p>Connecting a channel proves you have somewhere real to post; "
       "scheduling a message proves you actually use the bot. Together "
       "they take about two minutes: send your channel link in Step 1 "
       "of the tutorial, then schedule any post \u2014 even a test "
       "message counts. We check anonymous counters only (channels "
       "connected, messages created). We never read message contents, "
       "never ask for documents, and never share anything with third "
       "parties. Verification is about activity, not identity.</p>"

       "<h3>How crediting works, click to days</h3>"
       "<p><b>1) Click.</b> A newcomer opens your link and starts the "
       "bot. The click is recorded instantly, but nothing is granted "
       "yet \u2014 this pending state is what you see in your referral "
       "list before they qualify.</p>"
       "<p><b>2) Verify.</b> The newcomer connects their channel and "
       "schedules their first message, exactly like you did. Until "
       "then, the referral stays pending \u2014 no matter how long ago "
       "they clicked.</p>"
       "<p><b>3) Credit.</b> The moment they qualify, both sides receive "
       "<b>3 Premium days</b> automatically. Yours land in the referral "
       "balance (Available days in <code>/referral</code>). If you "
       "already pay for Premium, earned days wait in the balance until "
       "the paid period ends.</p>"
       "<p><b>4) Activate.</b> On the free plan, activate earned days "
       "from the referral menu and a Premium period starts immediately. "
       "Used days move to the Used counter, so earned, used and "
       "available totals are always visible.</p>"

       "<h3>Rules that protect the program</h3>"
       "<p>The referred user must be genuinely new and must arrive via "
       "your link as their first interaction. One referral per user \u2014 "
       "the same newcomer can never credit you twice. Fake accounts "
       "created to farm days do not qualify, and farmed balances can be "
       "removed. These rules are enforced automatically; disputes go to "
       "<b>@MaximalXP</b>.</p>"

       "<h3>What beta means for you</h3>"
       "<p>Beta status affects polish, never balances. Links, tracking, "
       "crediting and activation are all live, but you may meet rough "
       "edges: a counter that updates with a delay, a list that needs a "
       "reopen to refresh. Earned days are recorded the moment they "
       "qualify and are never lost to a display glitch \u2014 reopen "
       "<code>/referral</code> first if a number looks stale. Reward "
       "sizes and limits can still be tuned during beta; anything you "
       "already earned is honored under the rules that were live when "
       "you earned it. Spotted something odd? Send it via "
       "<code>/feedback</code> with step-by-step text and a screenshot "
       "\u2014 beta reports shape the final version.</p>"),

   faq=[
       {'q': 'Why is my referral menu locked?',
        'a': 'The program unlocks after you connect a channel and '
             'schedule at least one message. This verifies your account '
             'is genuine before you can earn rewards. Both steps take '
             'about two minutes inside the bot tutorial.'},
       {'q': 'When do I get my Premium days for a referral?',
        'a': 'When your referee connects their channel and schedules '
             'their first message. At that moment both of you receive '
             '3 Premium days automatically \u2014 yours appear under '
             'Available days in /referral.'},
       {'q': 'Is there a limit to referral earnings?',
        'a': 'Yes: up to 15 referees, i.e. 45 Premium days total, and '
             'one credit per newcomer. Paid Premium subscribers bank '
             'earned days in their balance until the paid period ends.'},
       {'q': 'Are my earned days safe while the program is in beta?',
        'a': 'Yes. Beta affects polish, not balances: every qualifying '
             'referral is recorded immediately, and earned days are '
             'honored even if reward rules are tuned later. Report '
             'glitches via /feedback.'}])
