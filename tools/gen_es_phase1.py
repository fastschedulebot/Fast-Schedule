"""Generate translations/es.json phase 1: full key coverage, core UI in natural Spanish, rest copied from EN (fallback-safe)."""
import json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
en = json.load(open(ROOT/"translations"/"en.json", encoding="utf-8-sig"))
es = copy.deepcopy(en)
es["flag"] = "ES"
es["name"] = "Espanol"
OV = {
  "welcome_intro": "Bienvenido a Fast Scheduler Bot! Soy tu gestor de canales. Programa publicaciones, recurrentes y estadisticas desde un solo lugar. Usa el menu de abajo para empezar!",
  "welcome_no_channel": "Bienvenido! Conecta tu primer canal para empezar a programar.",
  "welcome_subscribed": "Gracias por suscribirte!",
  "welcome_not_subscribed": "Suscribete a nuestro canal para usar todas las funciones.",
  "about_text": "Acerca de Fast Scheduler Bot Version: {version} Programa y gestiona tus publicaciones con facilidad.",
  "about_bot_info": "Fast Scheduler Bot - @FastSchedulerBot Tu herramienta de gestion de canales. Version: {version}",
  "select_language": "Elige tu idioma:",
  "language_changed": "Idioma cambiado a {lang}.",
  "lang_sync_disable": "Desactivar sincronizacion",
  "lang_sync_enable": "Activar sincronizacion",
  "lang_sync_explainer": "Tu idioma se sincroniza automaticamente con SetDate.",
  "help_center_intro": "Centro de ayuda Elige un tema:",
  "tutorial_welcome": "Bienvenido al tutorial! Te guiare en 3 pasos: conecta tu canal, conecta tu bot y programa tu primer mensaje.",
  "tutorial_connect_channel_prompt": "Paso 1 - Conecta tu canal. Anade @FastSchedulerBot como administrador y enviame @tucanal.",
  "tutorial_channel_connected": "Canal conectado!",
  "tutorial_bot_done": "Tutorial completado! La gestion de {channel} ahora es con tu bot @{bot}. Abre @{bot} y programa tu primer mensaje!",
  "tutorial_complete": "Tutorial completado! Ya puedes programar tus publicaciones.",
  "tutorial_already_configured": "Canal conectado! Este canal ya lo configuro su dueno: Zona horaria: {tz} - Bot: @{bot} - No necesitas anadir otro. Tutorial completo! Abre @{bot} para programar en {channel}.",
  "timezone_prompt_method": "Como quieres poner tu zona horaria?",
  "timezone_pick_title": "Elige tu zona horaria",
  "back_to_menu": "Volver al menu",
  "contact_btn": "Contactar soporte",
  "help_contact_btn": "Contactar @MaximalXP",
}
for k,v in OV.items():
    if k in es and isinstance(es[k], str):
        es[k]=v
def set_nested(d, dotted, val):
    parts=dotted.split(".")
    cur=d
    for p in parts[:-1]:
        cur=cur.get(p,{})
    if parts[-1] in cur and isinstance(cur[parts[-1]], str):
        cur[parts[-1]]=val
set_nested(es,"back.btn","Atras")
set_nested(es,"back.to_menu","Volver al menu")
if isinstance(es.get("action"),dict):
    es["action"]["cancelled"]="Accion cancelada."
    es["action"]["channel_pick_title"]="Elige un canal. Elige uno de tus canales conectados:"
    es["action"]["restricted"]="Esta accion esta restringida."
    es["action"]["restricted_nonadmin"]="Solo los administradores pueden hacerlo."
if isinstance(es.get("add"),dict):
    es["add"]["sender_bot"]="Anadir bot remitente"
    es["add"]["another_bot"]="Anadir otro bot"
    es["add"]["btn"]="Anadir"
out = ROOT/"translations"/"es.json"
out.write_text(json.dumps(es, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote keys={len(es)}")
