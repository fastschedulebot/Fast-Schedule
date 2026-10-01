# -*- coding: utf-8 -*-
MAP2 = [
('Activate Days','Activar días'),
('Hide channel from strangers','Ocultar canal a extraños'),
('Show channel to strangers','Mostrar canal a extraños'),
('Bot must be an administrator in the channel.','El bot debe ser admin del canal.'),
('Bot was blocked by the user.','El bot fue bloqueado por el usuario.'),
('Bot was removed from the group/channel.','El bot fue quitado del grupo/canal.'),
('No channel','Sin canal'),
('Bot connected','Bot conectado'),
('Your bots','Tus bots'),
('Add callback button','Añadir botón callback'),
('Broadcasting to all users...','Transmitiendo a todos...'),
('Cache cleared.','Caché borrada.'),
('Admin cache cleared.','Caché admin borrada.'),
('Calendar','Calendario'),
('View Day','Ver día'),
('Today','Hoy'),
('Select a day to see scheduled messages.','Elige un día para ver programados.'),
('No messages on this day.','Sin mensajes este día.'),
('No other channels available.','Sin otros canales.'),
('Select a channel to view:','Elige un canal:'),
('Week','Semana'),
('Month','Mes'),
('Sent','Enviado'),
('Failed','Falló'),
('No longer needed','Ya no lo necesito'),
('Technical issues','Problemas técnicos'),
('Other reason','Otra razón'),
("Please describe why you're cancelling:",'Describe por qué cancelas:'),
('Bots (','Bots ('),
('user(s)','usuario(s)'),
('Callback button:','Botón callback:'),
('Build:','Build:'),
('Yearly —','Anual —'),
('Yearly','Anual'),
('Calendar','Calendario'),
('View Day','Ver día'),
]
def tr2(s):
    t = s
    for en_, es_ in MAP2:
        t = t.replace(en_, es_)
    return t
