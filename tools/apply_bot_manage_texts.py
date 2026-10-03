import json

EN = {
    "bot_manage_btn": "⚙ Manage",
    "bot_manage_change_token": "🔑 Change token",
    "bot_manage_replace": "🔁 Replace bot",
    "bot_manage_remove": "🗑 Remove bot",
    "bot_manage_switch": "🔀 Switch channel",
    "bot_manage_swap": "⇄ Swap bots",
    "bot_manage_title": "⚙ <b>Manage @{bot}</b>",
    "bot_manage_channel": "📢 Channel: {channel}",
    "bot_manage_no_channel": "No channel attached",
    "bot_manage_intro": "Choose what to do with this bot:",
    "bot_manage_desc_token": "🔑 <b>Change token</b> — update the token when it was revoked in BotFather. Same bot, nothing else changes.",
    "bot_manage_desc_replace": "🔁 <b>Replace bot</b> — swap this bot for a different one. All data moves over, nothing is lost.",
    "bot_manage_desc_remove": "🗑 <b>Remove bot</b> — detach the bot from its channel.",
    "bot_manage_desc_switch": "🔀 <b>Switch channel</b> — attach the bot to another of your channels. Data is kept, the bot just moves.",
    "bot_manage_desc_swap": "⇄ <b>Swap bots</b> — exchange channels between two of your bots.",
    "bot_chtoken_prompt": "🔑 Send the <b>new token</b> for @{bot} (from BotFather, e.g. after the old one was revoked).\n\nNothing else changes — same bot, same channel, all data kept.",
    "bot_chtoken_mismatch": "❌ That token belongs to @{new}, not @{bot}. Send the token for @{bot}, or go back and use Replace bot instead.",
    "bot_chtoken_done": "✅ Token for @{bot} updated. The bot is back online with the new token.",
    "bot_switch_title": "🔀 <b>Switch @{bot} to another channel</b>\n\nPick the channel. Data is kept — the bot just moves there.",
    "bot_switch_confirm": "Move @{bot} from {old} to {new}?\n\n{occupant}",
    "bot_switch_occupant": "@{other} will be left without a channel (it stays in your bot list).",
    "bot_switch_done": "✅ @{bot} is now attached to {channel}. All data kept.",
    "bot_swap_title": "⇄ <b>Swap channels between bots</b>\n\n@{bot} is on {channel}. Choose the bot to swap with:",
    "bot_swap_no_second": "You need two bots to swap. Connect another bot first — then come back here and the swap will continue.",
    "bot_swap_other_no_channel": "@{other} has no channel yet. Connect it to a channel first, or pick another bot.",
    "bot_swap_confirm": "Swap channels?\n\n@{a} → {ch_b}\n@{b} → {ch_a}\n\nSchedules and settings stay with the channels — only the bots move.",
    "bot_swap_done": "✅ Bots swapped:\n\n@{a} → {ch_a}\n@{b} → {ch_b}",
    "bot_swap_continue": "⇄ Ready to continue the swap for @{bot}? Pick the bot to swap with:",
}

RU = {
    "bot_manage_btn": "⚙ Управление",
    "bot_manage_change_token": "🔑 Сменить токен",
    "bot_manage_replace": "🔁 Заменить бота",
    "bot_manage_remove": "🗑 Убрать бота",
    "bot_manage_switch": "🔀 Сменить канал",
    "bot_manage_swap": "⇄ Поменять ботов",
    "bot_manage_title": "⚙ <b>Управление @{bot}</b>",
    "bot_manage_channel": "📢 Канал: {channel}",
    "bot_manage_no_channel": "Канал не привязан",
    "bot_manage_intro": "Выберите действие с этим ботом:",
    "bot_manage_desc_token": "🔑 <b>Сменить токен</b> — обновите токен, если он был отозван в BotFather. Тот же бот, больше ничего не меняется.",
    "bot_manage_desc_replace": "🔁 <b>Заменить бота</b> — поменяйте этого бота на другого. Все данные переедут, ничего не потеряется.",
    "bot_manage_desc_remove": "🗑 <b>Убрать бота</b> — отвязать бота от его канала.",
    "bot_manage_desc_switch": "🔀 <b>Сменить канал</b> — привяжите бота к другому вашему каналу. Данные сохраняются, бот просто переезжает.",
    "bot_manage_desc_swap": "⇄ <b>Поменять ботов</b> — обменяйте каналы между двумя вашими ботами.",
    "bot_chtoken_prompt": "🔑 Пришлите <b>новый токен</b> для @{bot} (из BotFather, например после отзыва старого).\n\nБольше ничего не меняется — тот же бот, тот же канал, все данные на месте.",
    "bot_chtoken_mismatch": "❌ Этот токен принадлежит @{new}, а не @{bot}. Пришлите токен для @{bot} или вернитесь назад и используйте «Заменить бота».",
    "bot_chtoken_done": "✅ Токен для @{bot} обновлён. Бот снова онлайн с новым токеном.",
    "bot_switch_title": "🔀 <b>Переключить @{bot} на другой канал</b>\n\nВыберите канал. Данные сохраняются — бот просто переезжает туда.",
    "bot_switch_confirm": "Переместить @{bot} с {old} на {new}?\n\n{occupant}",
    "bot_switch_occupant": "@{other} останется без канала (он сохранится в списке ботов).",
    "bot_switch_done": "✅ @{bot} теперь привязан к {channel}. Все данные сохранены.",
    "bot_swap_title": "⇄ <b>Обмен каналами между ботами</b>\n\n@{bot} — на {channel}. Выберите бота для обмена:",
    "bot_swap_no_second": "Для обмена нужны два бота. Подключите ещё одного бота — затем вернитесь сюда, и обмен продолжится.",
    "bot_swap_other_no_channel": "У @{other} пока нет канала. Сначала привяжите его к каналу или выберите другого бота.",
    "bot_swap_confirm": "Поменять каналы местами?\n\n@{a} → {ch_b}\n@{b} → {ch_a}\n\nРасписания и настройки остаются с каналами — переезжают только боты.",
    "bot_swap_done": "✅ Боты поменялись:\n\n@{a} → {ch_a}\n@{b} → {ch_b}",
    "bot_swap_continue": "⇄ Продолжим обмен для @{bot}? Выберите бота для обмена:",
}

ES_PREFIX = "Guia en espanol: resumen arriba, detalle original abajo.\n\n"
ES = {
    "bot_manage_btn": "⚙ Gestionar",
    "bot_manage_change_token": "🔑 Cambiar token",
    "bot_manage_replace": "🔁 Reemplazar bot",
    "bot_manage_remove": "🗑 Eliminar bot",
    "bot_manage_switch": "🔀 Cambiar canal",
    "bot_manage_swap": "⇄ Intercambiar bots",
    "bot_manage_title": "⚙ <b>Gestionar @{bot}</b>",
    "bot_manage_channel": "📢 Canal: {channel}",
    "bot_manage_no_channel": "Sin canal asignado",
    "bot_manage_intro": "Elige qué hacer con este bot:",
    "bot_manage_desc_token": "🔑 <b>Cambiar token</b> — actualiza el token si fue revocado en BotFather. Mismo bot, nada más cambia.",
    "bot_manage_desc_replace": "🔁 <b>Reemplazar bot</b> — cambia este bot por otro. Todos los datos se trasladan, nada se pierde.",
    "bot_manage_desc_remove": "🗑 <b>Eliminar bot</b> — desvincula el bot de su canal.",
    "bot_manage_desc_switch": "🔀 <b>Cambiar canal</b> — vincula el bot a otro de tus canales. Los datos se conservan, el bot solo se muda.",
    "bot_manage_desc_swap": "⇄ <b>Intercambiar bots</b> — intercambia los canales entre dos de tus bots.",
    "bot_chtoken_prompt": "🔑 Envía el <b>nuevo token</b> para @{bot} (desde BotFather, por ejemplo tras revocarlo).\n\nNada más cambia — mismo bot, mismo canal, todos los datos intactos.",
    "bot_chtoken_mismatch": "❌ Ese token pertenece a @{new}, no a @{bot}. Envía el token de @{bot} o vuelve atrás y usa Reemplazar bot.",
    "bot_chtoken_done": "✅ Token de @{bot} actualizado. El bot vuelve a estar en línea con el nuevo token.",
    "bot_switch_title": "🔀 <b>Mover @{bot} a otro canal</b>\n\nElige el canal. Los datos se conservan — el bot solo se muda allí.",
    "bot_switch_confirm": "¿Mover @{bot} de {old} a {new}?\n\n{occupant}",
    "bot_switch_occupant": "@{other} se quedará sin canal (seguirá en tu lista de bots).",
    "bot_switch_done": "✅ @{bot} ahora está vinculado a {channel}. Todos los datos conservados.",
    "bot_swap_title": "⇄ <b>Intercambiar canales entre bots</b>\n\n@{bot} está en {channel}. Elige el bot con el que intercambiar:",
    "bot_swap_no_second": "Necesitas dos bots para intercambiar. Conecta otro bot primero — luego vuelve aquí y el intercambio continuará.",
    "bot_swap_other_no_channel": "@{other} aún no tiene canal. Vincúlalo a un canal primero o elige otro bot.",
    "bot_swap_confirm": "¿Intercambiar canales?\n\n@{a} → {ch_b}\n@{b} → {ch_a}\n\nHorarios y ajustes se quedan con los canales — solo se mueven los bots.",
    "bot_swap_done": "✅ Bots intercambiados:\n\n@{a} → {ch_a}\n@{b} → {ch_b}",
    "bot_swap_continue": "⇄ ¿Seguimos con el intercambio de @{bot}? Elige el bot:",
}
ES = {k: (v if k.endswith("_btn") or k in (
    "bot_manage_change_token", "bot_manage_replace", "bot_manage_remove",
    "bot_manage_switch", "bot_manage_swap") else ES_PREFIX + v)
    for k, v in ES.items()}

for lang, pack in (("en", EN), ("ru", RU), ("es", ES)):
    p = f"translations/{lang}.json"
    d = json.load(open(p, encoding="utf-8"))
    overlap = [k for k in pack if k in json.dumps(d)]
    # flat-key check
    def flat(o):
        out = {}
        def rec(x):
            if isinstance(x, dict):
                for kk, vv in x.items():
                    rec(vv)
            else:
                out[x] = True
        rec(o)
        return out
    have = set()
    def rec(x):
        if isinstance(x, dict):
            for kk, vv in x.items():
                if isinstance(vv, dict):
                    rec(vv)
                else:
                    have.add(kk)
    rec(d)
    dup = [k for k in pack if k in have]
    assert not dup, f"{lang} dup keys: {dup}"
    d.update(pack)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(lang, "added", len(pack))

# verify resolve through i18n
import sys
sys.path.insert(0, ".")
from src.core.i18n import t  # noqa: E402
import inspect
sig = inspect.signature(t)
print("t sig:", sig)
