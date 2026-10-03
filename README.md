# Fast Scheduler for Telegram

**Fast Scheduler** is a Telegram bot for preparing, scheduling, and managing posts in Telegram channels.

▶️ **Try the bot:** [@FastSchedulerBot](https://t.me/FastSchedulerBot)

## What makes it different

### Schedule many messages from one message

You can send several date/message pairs in one conversation instead of creating every scheduled post separately. For example:

```text
2026-12-24 18:00
First holiday message

2026-12-25 12:00
Second holiday message

2026-12-31 23:00
New Year message
```

The bot reads the date/time followed by its content and creates the scheduled messages together. The exact accepted date and time formats are shown by the bot during the scheduling flow. Each message keeps its own text and media settings.

### Formatting is preserved

Scheduled text can retain Telegram rich formatting and message entities, including supported bold, italic, links, code, spoilers, custom emoji and other formatting that Telegram provides for the original message. The bot validates unsupported inline-button syntax before saving a post.

## Main features

- Schedule one-time channel messages for a chosen date and time.
- Create several scheduled messages in one batch using date/message pairs.
- Use a user or channel timezone instead of relying on the server timezone.
- Create recurring messages using simple schedules or custom five-field cron expressions.
- View upcoming scheduled and recurring messages in lists and the calendar.
- Search scheduled content and open its actions.
- Edit, delete, duplicate, replace, preview, or otherwise manage supported scheduled messages.
- Send text, photos, videos, documents, animations, audio, voice messages, video notes, polls, locations and other Telegram-supported content where the current Telegram API and bot permissions allow it.
- Keep captions and supported formatting together with media.
- Add a reusable signature automatically at the beginning or end of posts, with configurable blank lines before it.
- Connect one or more Telegram channels according to the current account limits.
- Post through the main bot or connect a separate sender bot so channel posts can appear from that bot.
- Use media storage to save reusable Telegram media references and select them later without uploading the same file again.
- Choose a media mode for a batch: reuse one item, assign media sequentially, assign it randomly, or select items from media storage.
- Export and back up account data, then import supported backups when needed.
- View sending statistics and channel-related analytics available to the bot.
- Use language selection, help, feedback, referral, and support flows.
- Manage Premium through Telegram Stars when Premium purchases are enabled.

## Media modes

When a scheduled batch contains several messages, the bot can handle media in different ways:

1. **One media item** — reuse the selected media with the scheduled messages.
2. **Sequential media** — the first media item is assigned to the first message, the second to the second, and so on.
3. **Random media** — the bot chooses from the provided media for each message.
4. **Media storage** — select previously saved Telegram media instead of uploading it again.

Limits and available media types depend on the account plan, Telegram restrictions, and the connected channel's permissions. Telegram albums/media groups have Telegram-specific behavior, so the bot displays the applicable flow when an album is received.

## A typical setup

1. Open [@FastSchedulerBot](https://t.me/FastSchedulerBot).
2. Complete the built-in tutorial.
3. Add the bot as an administrator in your channel with at least **Post Messages** permission.
4. Connect the channel in the bot.
5. Optionally connect a sender bot and add that sender bot as an administrator in the same channel.
6. Set your timezone.
7. Choose **Schedule**, send the content, choose the date/time or batch format, select the channel and media options, then confirm.
8. Manage the result from **Messages**, **Calendar**, or **Search**.

For editing or deleting channel posts, the bot or sender bot may also need the corresponding Telegram administrator permissions. Telegram can reject an operation when a message is too old, permissions changed, the channel is unavailable, or the content is not supported.

## Recurring messages

Recurring messages can be configured with built-in recurring options or a custom cron expression. Examples:

```text
0 9 * * 1     every Monday at 09:00
30 18 * * *   every day at 18:30
0 8 1 * *     on the first day of every month at 08:00
```

Recurring messages keep their selected content, media, channel, and schedule until you edit, pause, or delete them through the available controls.

## Telegram channels and sender bots

The bot must be able to access the channel where it posts. For a sender bot, both the sender bot and the required channel relationship must be configured. Public channels can usually be identified by username or link; private channels may require forwarding a post or providing the channel ID.

The bot cannot bypass Telegram permissions, deleted channels, Telegram rate limits, or Telegram content restrictions.

## Premium

Premium availability and limits are shown inside the bot. The current user-facing payment flow uses **Telegram Stars**. The available plan terms are displayed before payment; recurring and prepaid/one-time terms are not interchangeable, so review the plan description in Telegram before confirming.

## Data and legal information

The bot's Privacy Policy, Terms of Service, and Refund Policy are published in this repository's GitHub Pages site. Use the links configured in the bot or the repository's Pages deployment to open the current versions.

This README describes the implemented product at a high level. Telegram's own rules, channel permissions, plan limits, and the bot's current in-app instructions control when a particular action is available.

---

# Fast Scheduler для Telegram (русская версия)

**Fast Scheduler** — это Telegram-бот для подготовки, планирования и управления публикациями в Telegram-каналах.

▶️ **Попробовать бота:** [@FastSchedulerBot](https://t.me/FastSchedulerBot)

## Главное отличие

### Несколько публикаций одним сообщением

Не нужно создавать каждую запланированную публикацию отдельно. Можно отправить несколько пар «дата/время + текст» в одном сообщении:

```text
2026-12-24 18:00
Первое праздничное сообщение

2026-12-25 12:00
Второе праздничное сообщение

2026-12-31 23:00
Новогоднее сообщение
```

Бот распознаёт дату и время, относящиеся к следующему содержимому, и создаёт публикации вместе. Поддерживаемые форматы даты и времени бот показывает непосредственно в процессе планирования. У каждой публикации сохраняются собственный текст и выбранные настройки медиа.

### Сохранение форматирования

Запланированный текст может сохранять поддерживаемое Telegram форматирование и сущности сообщения: жирный и курсивный текст, ссылки, код, спойлеры, custom emoji и другие возможности, которые Telegram передаёт для исходного сообщения. Перед сохранением бот проверяет неподдерживаемый синтаксис inline-кнопок.

## Основные функции

- Планирование разовых публикаций в канал.
- Создание нескольких публикаций одним сообщением в формате «дата/время + сообщение».
- Использование часового пояса пользователя или канала.
- Повторяющиеся публикации по готовым вариантам или через пятикомпонентное cron-выражение.
- Просмотр запланированных и повторяющихся сообщений в списках и календаре.
- Поиск по запланированному содержимому.
- Просмотр, редактирование, удаление, дублирование, замена и другие доступные действия над сообщениями.
- Поддержка текста, фотографий, видео, документов, анимаций, аудио, голосовых сообщений, видеосообщений, опросов, геопозиций и других типов, разрешённых текущим Telegram API и правами бота.
- Сохранение подписей и поддерживаемого форматирования вместе с медиа.
- Автоматическая подпись в начале или конце публикации с настройкой пустых строк перед ней.
- Подключение Telegram-каналов в пределах текущих лимитов аккаунта.
- Публикация через основной бот или через отдельный sender bot.
- Media storage для повторного выбора ранее сохранённых Telegram media без повторной загрузки.
- Режимы медиа для пакетных публикаций: одно медиа, последовательный выбор, случайный выбор или выбор из хранилища.
- Экспорт и резервное копирование данных с возможностью импорта поддерживаемых backup-файлов.
- Статистика отправленных публикаций и доступная боту аналитика каналов.
- Настройки языка, tutorial, помощь, feedback, referrals и поддержка.
- Premium через Telegram Stars, если покупки Premium включены.

## Режимы медиа

Для нескольких запланированных сообщений можно выбрать:

1. **Одно медиа** — использовать выбранный файл для публикаций.
2. **По порядку** — первое медиа к первому сообщению, второе ко второму и так далее.
3. **Случайный выбор** — выбирать медиа из набора для каждой публикации.
4. **Media storage** — выбрать ранее сохранённые Telegram media.

Ограничения, типы медиа и доступность функций зависят от тарифа, ограничений Telegram и прав в канале. Для альбомов/media groups Telegram использует особую модель сообщений, поэтому бот показывает отдельный подход, когда получает альбом.

## Быстрая настройка

1. Откройте [@FastSchedulerBot](https://t.me/FastSchedulerBot).
2. Пройдите встроенный tutorial.
3. Добавьте бота администратором канала минимум с правом **Post Messages**.
4. Подключите канал в боте.
5. При необходимости подключите sender bot и добавьте его администратором в тот же канал.
6. Укажите часовой пояс.
7. Нажмите **Schedule**, отправьте содержимое, выберите дату/время или пакетный формат, канал и параметры медиа, затем подтвердите.
8. Управляйте публикациями через **Messages**, **Calendar** или **Search**.

Для редактирования или удаления публикаций могут понадобиться соответствующие права администратора Telegram. Telegram может отклонить действие из-за возраста сообщения, изменения прав, недоступности канала, неподдерживаемого контента или ограничений API.

## Повторяющиеся публикации

Можно выбрать готовый вариант повторения или указать cron-выражение. Примеры:

```text
0 9 * * 1     каждый понедельник в 09:00
30 18 * * *   каждый день в 18:30
0 8 1 * *     первого числа каждого месяца в 08:00
```

Повторяющаяся публикация сохраняет выбранные содержимое, медиа, канал и расписание, пока вы не измените, не приостановите или не удалите её доступными действиями.

## Каналы и sender bots

Бот должен иметь доступ к каналу, в который публикуются сообщения. Для sender bot необходимо отдельно настроить sender bot и его права в канале. Публичный канал обычно можно указать через username или ссылку; для приватного канала может понадобиться переслать публикацию или отправить ID канала.

Бот не может обойти права Telegram, ограничения частоты, удаление канала или ограничения Telegram на контент.

## Premium

Доступность Premium и лимиты показываются внутри бота. Текущий пользовательский способ оплаты — **Telegram Stars**. Перед оплатой бот показывает условия конкретного тарифа; условия подписки и разовой/предоплаченной покупки различаются, поэтому проверяйте описание тарифа в Telegram перед подтверждением.

## Данные и юридическая информация

Политика конфиденциальности, Условия использования и Политика возвратов опубликованы в GitHub Pages этого репозитория. Открывайте актуальные версии через ссылки, настроенные в боте, или через страницу GitHub Pages репозитория.

README описывает функции на высоком уровне. Для конкретного действия действуют правила Telegram, права канала, текущие лимиты тарифа и инструкции, показанные ботом.