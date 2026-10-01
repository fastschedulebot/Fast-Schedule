/* =====================================================================
   Mini AI for help search — pure client-side intent matching.
   No server, no API: a small scoring engine that reads the visitor's
   free-text query and answers "what does the user mean":

     1. tokenizer with stop-word removal + typo tolerance (levenshtein
        against the site's own vocabulary),
     2. synonym/intent expansion (typos like "chanel" → channel,
        "reccuring" → recurring, phrases like "every week" → recurring),
     3. intent classification (schedule / media / payment / error …),
     4. scored ranking over the site's article index,
     5. a human-sounding "interpretation" line: "You mean: how to connect
        your own sender bot".

   Exposed as window.HelpAI = { interpret, scoreAll, expand }.
   ===================================================================== */
(function () {
  'use strict';

  /* ---------- vocabulary + intents ---------- */
  var STOP = { the: 1, a: 1, an: 1, is: 1, are: 1, do: 1, does: 1, did: 1, how: 1, what: 1, why: 1,
    when: 1, where: 1, can: 1, i: 1, my: 1, me: 1, to: 1, of: 1, in: 1, on: 1, for: 1, with: 1,
    and: 1, or: 1, it: 1, its: 1, this: 1, that: 1, you: 1, your: 1, be: 1, been: 1, get: 1,
    got: 1, if: 1, so: 1, but: 1, from: 1, at: 1, as: 1, was: 1, were: 1, will: 1, would: 1,
    should: 1, could: 1, please: 1, help: 1, need: 1, want: 1, there: 1, not: 1, no: 1, yes: 1 };

  /* intent groups: each is a "topic" the site covers, with a plain-language
     label and its synonyms. A query word matching ANY synonym pulls the
     whole group in — that is what makes "pics dont send" find media posts. */
  var INTENTS = [
    { id: 'schedule', label: 'scheduling posts',
      words: ['schedule', 'scheduled', 'scheduling', 'recurring', 'repeat', 'repeating', 'cron',
        'every', 'weekly', 'daily', 'month', 'batch', 'queue', 'queued', 'time', 'date', 'timezone',
        'reccuring', 'reccuring', 'shedule', 'sheduling', 'scheduel', 'repaeat', 'everyweek', 'everyday'] },
    { id: 'media', label: 'photos and media',
      words: ['photo', 'photos', 'pic', 'pics', 'picture', 'image', 'images', 'video', 'videos',
        'album', 'gif', 'media', 'file', 'files', 'document', 'upload', 'storage', 'attach',
        'picures', 'poto', 'vid', 'vids', 'photes'] },
    { id: 'channel', label: 'connecting a channel',
      words: ['channel', 'channels', 'connect', 'connecting', 'admin', 'administrator', 'administsrator',
        'add', 'linked', 'link', 'group', 'supergroup', 'chanel', 'channal', 'connct', 'conect'] },
    { id: 'bot', label: 'sender bots',
      words: ['bot', 'bots', 'sender', 'token', 'own', 'custom', 'brand', 'bott', 'sendr'] },
    { id: 'payment', label: 'premium, billing and refunds',
      words: ['premium', 'pay', 'payment', 'billing', 'buy', 'purchase', 'stars', 'invoice', 'refund',
        'refunds', 'crypto', 'price', 'pricing', 'cost', 'subscription', 'upgrade', 'plan', 'free',
        'money', 'charged', 'renew', 'cancell', 'cancel', 'refound', 'premum', 'subscrition'] },
    { id: 'backup', label: 'backup and export',
      words: ['backup', 'export', 'import', 'restore', 'fsback', 'fspback', 'migrate', 'migration',
        'transfer', 'move', 'copy', 'bakup', 'exprot', 'download', 'data'] },
    { id: 'stats', label: 'statistics',
      words: ['stats', 'statistics', 'views', 'leaderboard', 'report', 'reports', 'analytics',
        'count', 'counter', 'performance', 'statisitcs', 'analitycs'] },
    { id: 'error', label: 'fixing problems',
      words: ['error', 'errors', 'problem', 'problems', 'issue', 'fail', 'fails', 'failed', 'failing',
        'stuck', 'broken', 'notworking', 'doesnt', 'dont', 'wont', 'cannot', 'cant', 'fix',
        'troubleshoot', 'late', 'delay', 'delayed', 'missing', 'skipped', 'disappeared', 'wrong'] },
    { id: 'account', label: 'getting started',
      words: ['start', 'begin', 'setup', 'onboarding', 'account', 'register', 'signup', 'first',
        'begining', 'stat', 'strat'] },
    { id: 'feedback', label: 'contacting support',
      words: ['support', 'contact', 'ticket', 'feedback', 'human', 'ask', 'report'] },
    { id: 'formatting', label: 'formatting and buttons',
      words: ['format', 'formatting', 'bold', 'italic', 'link', 'button', 'buttons', 'inline',
        'markdown', 'html', 'emoji', 'signature', 'footer', 'spoiler'] },
    { id: 'limits', label: 'plan limits',
      words: ['limit', 'limits', 'maximum', 'max', 'howmany', 'quota', 'exceed', 'exceeded', 'cap'] }
  ];

  /* common typos → the correctly spelled intent keyword, so a misspelled
     query still lands on the right topic ("reccuring" → recurring). */
  var TYPOS = {
    reccuring: 'recurring', recuring: 'recurring', recurriing: 'recurring',
    shedule: 'schedule', sheduled: 'scheduled', scheduel: 'schedule', scedule: 'schedule',
    chanel: 'channel', channal: 'channel', channle: 'channel',
    messge: 'message', mesage: 'message', messege: 'message',
    recieve: 'receive', recived: 'received',
    delet: 'delete', delte: 'delete',
    preimum: 'premium', premum: 'premium', peremium: 'premium',
    refound: 'refund', refun: 'refund',
    backp: 'backup', bakup: 'backup',
    statisitcs: 'statistics', statistcs: 'statistics',
    settigns: 'settings', setings: 'settings',
    timezome: 'timezone', timezon: 'timezone',
    erorr: 'error', eror: 'error',
    publsih: 'publish', pulbish: 'publish',
    conected: 'connected', conncet: 'connect',
    evry: 'every', weekli: 'weekly',
    signture: 'signature', signiture: 'signature'
  };

  /* phrase intents: multi-word patterns mapped to a topic ("every week" →
     schedule). Checked before single words. */
  var PHRASES = [
    { re: /every\s*(week|day|month|hour|morning|evening)/, intent: 'schedule', label: 'repeating posts on a schedule' },
    { re: /once\s*a\s*(week|day|month)/, intent: 'schedule', label: 'repeating posts on a schedule' },
    { re: /(not|dont|don'?t|isn'?t|is not|wont|won'?t)\s*(send|sending|post|posting|publish|publishing|work|working|appear)/, intent: 'error', label: 'posts not going out' },
    { re: /(my|the)\s*(photo|pic|image|video)s?\s*(does|do)?n'?t/, intent: 'error', label: 'media posts failing' },
    { re: /how\s*(do|to|can)/, intent: null },   /* "how do I …" is generic, no pull */
    { re: /difference\s*between/, intent: null },
    { re: /(how much|what.*cost|price)/, intent: 'payment', label: 'pricing' },
    { re: /(connect|add)\s*(my|a|the)?\s*(own\s*)?(channel|bot)/, intent: 'channel', label: 'connecting something to the bot' }
  ];

  /* ---------- tokenizer ---------- */
  function tokenize(q) {
    return String(q || '').toLowerCase()
      .replace(/[^a-z0-9\s'-]/g, ' ')
      .split(/\s+/)
      .filter(Boolean);
  }

  /* levenshtein distance, capped — used to pull near-miss words onto the
     right intent ("schedul" matches "schedule"). Small words only fuzz
     against small words so "on" never becomes "own". */
  function lev(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var m = a.length, n = b.length;
    if (!m) return n; if (!n) return m;
    var prev = new Array(n + 1), cur = new Array(n + 1);
    for (var j = 0; j <= n; j++) prev[j] = j;
    for (var i = 1; i <= m; i++) {
      cur[0] = i;
      var best = cur[0];
      for (var k = 1; k <= n; k++) {
        var c = a.charCodeAt(i - 1) === b.charCodeAt(k - 1) ? 0 : 1;
        cur[k] = Math.min(prev[k] + 1, cur[k - 1] + 1, prev[k - 1] + c);
        if (cur[k] < best) best = cur[k];
      }
      if (best > max) return max + 1;   /* early exit */
      for (var t = 0; t <= n; t++) prev[t] = cur[t];
    }
    return prev[n];
  }

  /* expand one raw word into [canonicalWord, intentIds...] */
  function resolveWord(w) {
    if (STOP[w]) return null;
    if (TYPOS[w]) w = TYPOS[w];
    var intents = [];
    for (var i = 0; i < INTENTS.length; i++) {
      var words = INTENTS[i].words;
      for (var j = 0; j < words.length; j++) {
        var t = words[j];
        if (w === t) { intents.push(INTENTS[i]); break; }
        /* prefix match: "schedu" pulls the schedule intent */
        if (t.length >= 5 && w.length >= 4 && t.indexOf(w) === 0) { intents.push(INTENTS[i]); break; }
        /* typo fuzz: distance 1 for ≤6-letter words, 2 for longer */
        var maxD = t.length >= 7 || w.length >= 7 ? 2 : 1;
        if (w.length >= 4 && lev(w, t, maxD) <= maxD) { intents.push(INTENTS[i]); break; }
      }
    }
    return { word: w, intents: intents };
  }

  /* ---------- public API ---------- */

  /* expand(q) → { words, intents, label } — the AI's reading of the query */
  function interpret(q) {
    var toks = tokenize(q);
    var phraseLabel = null;
    var forced = {};
    PHRASES.forEach(function (p) {
      if (p.intent && p.re.test(String(q).toLowerCase())) {
        forced[p.intent] = true;
        if (!phraseLabel) phraseLabel = p.label;
      }
    });

    var words = [], intents = {};
    toks.forEach(function (w) {
      var r = resolveWord(w);
      if (!r) return;
      words.push(r.word);
      r.intents.forEach(function (it) { intents[it.id] = it; });
    });
    Object.keys(forced).forEach(function (id) {
      var it = null;
      for (var i = 0; i < INTENTS.length; i++) if (INTENTS[i].id === id) { it = INTENTS[i]; break; }
      if (it) intents[id] = it;
    });

    var list = Object.keys(intents).map(function (k) { return intents[k]; });
    /* the interpretation line: the strongest intent's label */
    var label = phraseLabel || (list.length ? list[0].label : null);
    return { words: words, intents: list, label: label, raw: String(q || '').trim() };
  }

  /* scoreAll(q, docs) → ranked docs. A doc is { t: title, b: body, c: cat }.
     Scoring = intent fit + word overlap + typo tolerance + phrase bonus. */
  function scoreAll(q, docs) {
    var ex = interpret(q);
    var qLow = String(q || '').toLowerCase().trim();
    var want = {};
    ex.intents.forEach(function (it) { want[it.id] = true; });
    var docIntent = (function () {
      /* docs may carry a precomputed intent id (help center tags each article) */
      return function (d) { return d.intent || d.i || ''; };
    })();

    return docs.map(function (d) {
      var t = String(d.t || '').toLowerCase();
      var body = String(d.b || d.body || '').toLowerCase();
      var s = 0;

      /* exact phrase in title/body is the strongest signal */
      if (qLow.length > 2) {
        if (t.indexOf(qLow) !== -1) s += 140;
        else if (body.indexOf(qLow) !== -1) s += 55;
      }

      /* intent fit: does this doc belong to a topic the query pulled in? */
      var di = docIntent(d);
      if (want[di]) s += 70;

      /* word overlap with typo tolerance */
      var words = t.split(/\s+/);
      ex.words.forEach(function (w) {
        var hit = 0;
        words.forEach(function (x) {
          if (x === w) hit = Math.max(hit, 110);
          else if (x.indexOf(w) === 0 || w.indexOf(x) === 0 && x.length >= 4) hit = Math.max(hit, 55);
          else if (x.indexOf(w) !== -1) hit = Math.max(hit, 30);
          else if (w.length >= 5 && lev(w, x, 1) <= 1) hit = Math.max(hit, 25);
        });
        if (!hit && body.indexOf(w) !== -1) hit = 14;
        if (hit) s += hit; else s -= 30;
      });

      return { doc: d, score: s, ex: ex };
    }).filter(function (x) { return x.score > 0; })
      .sort(function (a, b) { return b.score - a.score; });
  }

  window.HelpAI = { interpret: interpret, scoreAll: scoreAll, tokenize: tokenize, lev: lev };
})();
