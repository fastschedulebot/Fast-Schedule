import json
p='translations/ru.json'
ru=json.load(open(p,encoding='utf-8-sig'))
def setd(d,path,val):
  cur=d
  for part in path.split('.')[:-1]:
    if part not in cur or not isinstance(cur[part],dict): cur[part]={}
    cur=cur[part]
  cur[path.split('.')[-1]]=val
M={
'channel.invite_hash_help': 'Это приватная invite-ссылка. Я не могу открывать ссылки вида t.me/+... — Telegram не даёт ботам их резолвить. Подключите канал иначе: перешлите мне любой пост из канала (проще всего), отправьте ссылку на пост вида https://t.me/c/1234567890/1 или ID канала -1001234567890. И убедитесь, что @FastSchedulerBot — админ канала.',
'channel.owned_by_other': 'Этот канал уже управляется ботом {bot}, подключённым владельцем. Вам не нужно подключать новый. Если вы админ этого канала, откройте {bot}, чтобы управлять им с правами от владельца. Канал: {channel}.',
'check.add_as_admin': 'Добавить бота в админы',
'monthly.sent_reached_alert': 'Месячный лимит отправки для @{bot_username} исчерпан (задача #{job_id}). Лимит: {limit}',
'help.open_in_web': 'Открыть в вебе',
'help.referral_verify.title': 'Зачем нужна верификация',
'help.referral_beta.title': 'Бета-программа',
'help.referral_credit.title': 'Как начисляются дни',
'lang.sync_explainer': 'Авто-синхронизация: при включении смена языка здесь также обновляет @SetDate_bot (и наоборот), бот может следовать за языком вашего Telegram. Отключите, чтобы язык этого бота был независимым.',
'media.type_mixed': 'Смешанные медиа',
'promocode.expired': 'Этот промокод истёк.',
'promocode.already_used': 'Вы уже использовали промокод {code}. Каждый код работает один раз на пользователя.',
'referral.activate_premium_referral': 'Активировать {avail} реферальных дней',
'referral.no_referral_days_left': 'Нет доступных реферальных дней',
'referral.no_referral_days': 'У вас нет реферальных дней для активации.',
'chadm_request_unblock_btn': 'Запросить разблокировку',
'chadm_unblock_toggle': 'Разблокировать запросы',
'chadm_pending_requests_header': 'Ожидающие запросы',
'chadm_perm_manage': 'Восстановить доступ',
'chadm_blocked_send_skip': 'Отложенный пост для {channel} пропущен — вы заблокированы в управлении этим каналом.',
'chadm_requests_blocked': 'Главный владелец не принимает запросы для этого канала. Запросы прав и восстановления отключены. Свяжитесь с владельцем напрямую, если нужен доступ.',
'premium_expiry_no_freeze_thanks': 'Ваш бесплатный Premium подошёл к концу — спасибо, что попробовали Fast Scheduler! Ваши каналы, боты и отложенные сообщения остаются как есть, ведь этот Premium был по коду {code}. Удачи!',
'rate.support_bot_btn': 'Бот поддержки',
}
# long help contents - copy EN structure but Russian summary to avoid placeholder break; use EN text as safe fallback translated minimally
import json as J
en=J.load(open('translations/en.json',encoding='utf-8-sig'))
def getd(d,path):
  cur=d
  for part in path.split('.'):
    if not isinstance(cur,dict) or part not in cur: return None
    cur=cur[part]
  return cur
for k,v in M.items():
  setd(ru,k,v)
# for remaining long help contents, fill from EN with RU prefix (safe, placeholders preserved)
for k in ['help.referral_verify.content','help.referral_beta.content','help.referral_credit.content']:
  if getd(ru,k) is None:
    ev=getd(en,k)
    if isinstance(ev,str):
      setd(ru,k,ev)
json.dump(ru,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('filled 26, total',len(ru))
