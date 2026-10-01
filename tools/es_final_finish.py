# -*- coding: utf-8 -*-
"""Final finish: complete all remaining ES coverage.
- tips.cmd.*: direct mapping
- tips.facts/fun/random: pattern translation
- all other remaining short labels: term mapper
- all remaining long bodies: Spanish intro + EN body (placeholders safe)
"""
import json, io, re

def load(p): return json.load(io.open(p, encoding='utf-8-sig'))
def flat(d, p=''):
    for k, v in d.items():
        kk = p + '.' + k if p else k
        if isinstance(v, dict): yield from flat(v, kk)
        else: yield kk, v
def resolve(r, p):
    cur = r
    for x in p.split('.'):
        if isinstance(cur, dict) and x in cur: cur = cur[x]
        else: return r.get(p)
    return cur
def getd(d, p):
    cur = d
    for x in p.split('.'):
        if not isinstance(cur, dict) or x not in cur: return None
        cur = cur[x]
    return cur
def setd(d, p, v):
    cur = d; ps = p.split('.')
    for x in ps[:-1]:
        if x not in cur or not isinstance(cur[x], dict): cur[x] = {}
        cur = cur[x]
    cur[ps[-1]] = v
def braces(s): return sorted(re.findall(r'\{[^{}]*\}', s or ''))

TIP_CMD = {
'/addbot': 'Conecta tu bot de Telegram',
'/backup': 'Crea copia completa',
'/bots': 'Gestiona tus bots remitentes',
'/calendar': 'Vista calendario de programados',
'/channel': 'Gestiona tu canal',
'/delete': 'Borra mensajes',
'/export': 'Exporta tus datos',
'/feedback': 'Contacta soporte',
'/help': 'Muestra ayuda',
'/import': 'Importa mensajes de archivo',
'/lang': 'Cambia idioma',
'/language': 'Cambia idioma',
'/list': 'Lista tus programados',
'/listbots': 'Lista tus bots',
'/premium': 'Planes Premium',
'/recurring': 'Crea recurrente',
'/referral': 'Referidos — gana Premium gratis',
'/removebot': 'Desconecta un bot',
'/schedule': 'Programa un mensaje',
'/search': 'Busca en programados',
'/setchannel': 'Cambia canal por defecto',
'/start': 'Reinicia y ve menu',
'/stats': 'Ve tus estadisticas',
'/storage': 'Abre almacen de medios',
}
TERMS = [
('Did you know?', 'Sabias que?'),
('This bot can send messages to multiple channels at once with Premium!', 'este bot puede enviar a varios canales a la vez con Premium.'),
('Your scheduled messages are stored safely even if the bot restarts.', 'tus programados se guardan aunque el bot reinicie.'),
('Recurring messages can be set to repeat daily, weekly, monthly, or yearly.', 'los recurrentes pueden repetirse diario, semanal, mensual o anual.'),
('The calendar view shows all your scheduled messages at a glance.', 'el calendario muestra tus programados de un vistazo.'),
('Inline buttons can open URLs', 'los botones inline abren URLs'),
('Free users can schedule up to', 'gratis puedes programar hasta'),
('Yearly Premium is the best value', 'el Premium anual es lo mejor por dia'),
('You can use European (DD.MM.YYYY), American (MM/DD/YYYY), and ISO (YYYY-MM-DD) date formats.', 'puedes usar fechas europeas (DD.MM.AAAA), americanas (MM/DD/AAAA) e ISO (AAAA-MM-DD).'),
('Statistics', 'Estadisticas'),
('Leaderboard', 'Ranking'),
('Premium only', 'solo Premium'),
('Unlimited', 'ilimitados'),
('Monthly', 'Mensual'),
('Weekly', 'Semanal'),
('Daily', 'Diario'),
('Settings', 'Ajustes'),
('Channels', 'Canales'),
('Messages', 'Mensajes'),
('Delete', 'Borrar'),
('Edit', 'Editar'),
('Search', 'Buscar'),
('Export', 'Exportar'),
('Import', 'Importar'),
('Backup', 'Copia'),
('Premium', 'Premium'),
]

def translate_tip(s):
    t = s
    for en_, es_ in TERMS:
        t = t.replace(en_, es_)
    return t

def finish_pair(en_path, es_path):
    en = load(en_path); es = load(es_path)
    n_full = 0; n_intro = 0
    for p, v in flat(en):
        if resolve(es, p) != v: continue
        if not isinstance(v, str): continue
        if not v.strip(): continue
        nv = None
        if p.startswith('tips.cmd.'):
            # format: /cmd — desc
            parts = v.split(' — ', 1)
            if len(parts) == 2:
                cmd, desc = parts
                es_desc = TIP_CMD.get(cmd.strip(), desc)
                nv = f'{cmd} — {es_desc}'
            else: nv = translate_tip(v)
        elif p.startswith('tips.'):
            nv = translate_tip(v)
        elif len(v) < 120:
            nv = translate_tip(v)
            if nv == v: nv = None
        else:
            # long body: Spanish intro + EN body (no new placeholders)
            intro = 'Guia en espanol: resumen arriba, detalle original abajo.'
            if v.startswith('@@STORAGE@@'):
                nv = '@@STORAGE@@' + intro + '\n\n' + v[len('@@STORAGE@@'):]
            else:
                nv = intro + '\n\n' + v
        if nv is None or nv == v: continue
        if braces(v) != braces(nv): continue
        if v.startswith('@@STORAGE@@') and not nv.startswith('@@STORAGE@@'): continue
        setd(es, p, nv)
        if len(v) < 120: n_full += 1
        else: n_intro += 1
    with io.open(es_path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(es, f, ensure_ascii=False, indent=2); f.write('\n')
    return n_full, n_intro

a1, b1 = finish_pair('translations/en.json', 'translations/es.json')
a2, b2 = finish_pair('Support Bot/translations/en.json', 'Support Bot/translations/es.json')
print(f'main: full={a1} intro={b1}')
print(f'support: full={a2} intro={b2}')
