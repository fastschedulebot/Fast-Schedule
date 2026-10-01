# -*- coding: utf-8 -*-
PATS = [
('How much does advertising cost?','Cuanto cuesta la publicidad?'),
('Can I advertise my Telegram channel here?','Puedo anunciar mi canal aqui?'),
('Is there a self-service ad platform?','Hay plataforma de ads auto?'),
('Can I sponsor a specific broadcast message?','Puedo patrocinar un mensaje?'),
('How do I become an admin of a channel?','Como ser admin de un canal?'),
('What happens if another admin of my channel activates Premium?','Que pasa si otro admin activa Premium?'),
('How do I request a permission I don\'t have?','Como pedir un permiso que no tengo?'),
('Do multiple admins get separate limits?','Los admins tienen limites separados?'),
('How do I export my data?','Como exporto mis datos?'),
('How do I restore a backup?','Como restauro una copia?'),
('Can I set up automatic backups?','Puedo programar copias automaticas?'),
('How do I create a password-protected backup?','Como creo copia con clave?'),
("What's included in a full backup?",'Que trae una copia full?'),
("What's the difference between .fsback and .fspback?",'Diferencia entre .fsback y .fspback?'),
('How do I pay for Premium?','Como pago Premium?'),
('Is the payment auto-renewing?','El pago se renueva solo?'),
('When does my Premium expire?','Cuando vence mi Premium?'),
('Can I cancel Premium?','Puedo cancelar Premium?'),
('Can I get a refund?','Puedo pedir reembolso?'),
('Do I need a sender bot to schedule messages?','Necesito bot remitente para programar?'),
('Can I edit a message after I schedule it?','Puedo editar tras programar?'),
('How many scheduled messages can I store?','Cuantos programados puedo guardar?'),
('How many messages can I send per month?','Cuantos puedo enviar por mes?'),
('Can I schedule the same message to multiple channels?','Puedo programar lo mismo a varios canales?'),
('Can I schedule a poll or quiz?','Puedo programar encuesta o quiz?'),
('What media can I attach to a scheduled message?','Que medios puedo adjuntar?'),
('What time zone is used for my scheduled times?','Que zona se usa para mis horas?'),
('What happens if my Premium expires during a schedule?','Que pasa si Premium vence con programa activo?'),
('How do I see everything I have scheduled?','Como veo todo lo programado?'),
('Can I schedule a forwarded message?','Puedo programar un reenviado?'),
('Can I schedule an album of photos?','Puedo programar un album?'),
('Where are my bot tokens stored?','Donde se guardan mis tokens?'),
('Is my data shared or sold?','Se comparten o venden mis datos?'),
('How do I delete my data?','Como borro mis datos?'),
('How do I delete my account and data?','Como borro mi cuenta y datos?'),
('Can I change my account language or time zone?','Puedo cambiar idioma o zona?'),
('Where do I find my user ID?','Donde veo mi ID?'),
('How is my account created?','Como se crea mi cuenta?'),
('When is the best time to post?','Cual es la mejor hora para postear?'),
('What payment methods are supported?','Que pagos aceptan?'),
('Can I switch plans later?','Puedo cambiar de plan despues?'),
('How do I connect my first channel?','Como conecto mi primer canal?'),
('Can I connect multiple channels?','Puedo conectar varios canales?'),
('How do I set a default channel?','Como pongo canal por defecto?'),
('How do I remove a channel?','Como quito un canal?'),
("What is /cancel used for?",'Para que sirve /cancel?'),
('How do I use a promo code?','Como uso un codigo promo?'),
('Where are the settings?','Donde estan los ajustes?'),
('Can I undo a deletion?','Puedo deshacer un borrado?'),
('Can I duplicate a message?','Puedo duplicar un mensaje?'),
]
def translate_q(s):
  for en_, es_ in PATS:
    if s == en_: return es_
  t = s
  t = t.replace('How do I ','Como ')
  t = t.replace('How do ','Como ')
  t = t.replace('Can I ','Puedo ')
  t = t.replace('What ','Que ')
  t = t.replace('Where ','Donde ')
  t = t.replace('When ','Cuando ')
  t = t.replace('Why ','Por que ')
  t = t.replace('Is ','Es ')
  t = t.replace('Do ','Tienen ')
  t = t.replace('Does ','Hace ')
  t = t.replace('my ','mi ')
  t = t.replace('my','mi')
  return t
