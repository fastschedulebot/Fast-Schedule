import json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
en = json.load(open(ROOT/"translations"/"es.json", encoding="utf-8-sig"))
es = copy.deepcopy(en)
es["flag"] = "\U0001F1EA\U0001F1F8"
es["name"] = "Espa\u00f1ol"
OV = {
  "welcome_intro": "\U0001F44B <b>\u00a1Bienvenido a Fast Scheduler Bot!</b>\n\nSoy tu gestor personal de canales de Telegram. Programa publicaciones, crea recurrentes y mira estad\u00edsticas \u2014 todo desde un solo lugar.\n\n<b>\U0001F680 Qu\u00e9 puedo hacer:</b>\n\u2022 \U0001F4C5 <b>Programar</b> \u2014 fecha, hora y contenido, yo publico solo.\n\u2022 \U0001F504 <b>Recurrentes</b> \u2014 diarios, semanales, mensuales.\n\u2022 \U0001F4CA <b>Estad\u00edsticas</b> \u2014 vistas, comentarios y reacciones.\n\u2022 \U0001F916 <b>Bots remitentes</b> \u2014 un bot dedicado por canal.\n\u2022 \U0001F310 <b>Multi-idioma</b> \u2014 ingl\u00e9s, ruso, armenio y espa\u00f1ol.\n\n<b>\U0001F446 Usa el men\u00fa de abajo para empezar.</b>",
  "about_text": "\U0001F4CB <b>Acerca de Fast Scheduler Bot</b>\n\nVersi\u00f3n: {version}\n\nPrograma y gestiona tus publicaciones de Telegram con facilidad.",
  "about_bot_info": "\U0001F916 <b>Fast Scheduler Bot \u2014 @FastSchedulerBot</b>\n\nTu herramienta de gesti\u00f3n de canales. Programa, mide y automatiza.\n\nVersi\u00f3n: {version}",
  "tutorial_bot_done": "\U0001F389 <b>\u00a1Tutorial completado!</b>\n\nTodo listo. La gesti\u00f3n de <b>{channel}</b> ahora es con tu bot <b>@{bot}</b>.\n\nAbre @{bot} y programa tu primer mensaje. \U0001F680",
  "tutorial_already_configured": "\u2705 <b>\u00a1Canal conectado!</b>\n\nBuenas noticias \u2014 el due\u00f1o ya lo dej\u00f3 configurado:\n\u2022 \U0001F550 Zona horaria: <b>{tz}</b>\n\u2022 \U0001F916 Bot remitente: <b>@{bot}</b>\n\n\U0001F389 <b>Tutorial completo.</b> Abre @{bot} para programar en {channel}.",
}
for k,v in OV.items():
    if k in es and isinstance(es[k], str):
        es[k]=v
out = ROOT/"translations"/"es.json"
out.write_text(json.dumps(es, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote es.json natural phase1b")
