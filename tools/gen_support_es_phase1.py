"""Support Bot es.json phase 1: full coverage, help titles + core in Spanish, bodies copied EN for now (fallback-safe)."""
import json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
src = ROOT/"Support Bot"/"translations"/"en.json"
en = json.load(open(src, encoding="utf-8-sig"))
es = copy.deepcopy(en)

TITLE_OV = {
 "help.advertising.title": "Publicidad y promoción",
 "help.admins.title": "Administradores",
 "help.admins_limits.title": "Cómo comparten límites los admins",
 "help.admins_permissions.title": "Permisos y solicitudes",
 "help.admins_transfer.title": "Transferencia de propiedad",
 "help.backup.title": "Copia de seguridad",
 "help.bot_add.title": "Añadir un bot remitente",
 "help.bot_fleet.title": "Flota de bots",
 "help.bot_manage.title": "Gestionar bots remitentes",
 "help.bot_permissions.title": "Permisos del bot",
 "help.bot_remove.title": "Eliminar un bot remitente",
 "help.bot_rotate.title": "Rotar token",
 "help.open_in_web": "Abrir en la web",
}
for k,v in TITLE_OV.items():
    if k in es: es[k]=v

# generic support.* core keys if present
for k in list(es.keys()):
    if k.startswith("support."):
        # leave EN body for now except menu
        pass
if "support.main_menu" in es:
    es["support.main_menu"] = "🆘 <b>Soporte</b>\n\nElige una opción:"
if "support.open_main_menu" in es:
    es["support.open_main_menu"] = "Abrir menú principal"

out = ROOT/"Support Bot"/"translations"/"es.json"
out.write_text(json.dumps(es, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote support es keys={len(es)} vs en={len(en)}")
