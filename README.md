# Fast Scheduler for Telegram

Fast Scheduler is a Telegram bot for scheduling and managing posts in Telegram channels.

▶️ **Try the bot:** [@FastSchedulerBot](https://t.me/FastSchedulerBot)

## What the bot does

- Schedule one-time channel posts in a selected timezone.
- Create multiple scheduled posts from one message by sending date/time and message pairs:

  ```text
  2026-12-24 18:00
  First message

  2026-12-25 12:00
  Second message
  ```

- Create recurring posts with built-in schedules or custom cron expressions.
- Preserve supported Telegram text formatting and captions.
- Schedule text, photos, videos, documents, animations, audio, voice messages, polls, locations, and other supported Telegram content.
- Choose media handling for a batch: one reusable item, sequential assignment, random assignment, or selection from Media Storage.
- Add reusable signatures automatically at the beginning or end of posts.
- View scheduled and recurring messages in lists and the calendar.
- Search, preview, edit, delete, duplicate, replace, and manage supported messages.
- Connect Telegram channels and optionally publish through a separate sender bot.
- Export and back up supported account data.
- View available sending statistics and channel analytics.
- Use Premium through Telegram Stars when Premium purchases are enabled.

The exact available limits and actions depend on the current bot plan, Telegram permissions, Telegram API restrictions, and the message type.

## Basic setup

1. Open [@FastSchedulerBot](https://t.me/FastSchedulerBot).
2. Complete the tutorial.
3. Add the bot as a Telegram channel administrator with at least **Post Messages** permission.
4. Connect the channel in the bot.
5. Optionally connect a sender bot and add it as an administrator in the same channel.
6. Set the timezone and create a scheduled or recurring post.

## Legal documents

- [Privacy Policy](legal/privacy.html)
- [Terms of Service](legal/terms.html)
- [Refund Policy](legal/refundpolicy.html)

---

# Fast Scheduler для Telegram

Fast Scheduler — это Telegram-бот для планирования и управления публикациями в Telegram-каналах.

▶️ **Попробовать бота:** [@FastSchedulerBot](https://t.me/FastSchedulerBot)

## Возможности бота

- Планирование разовых публикаций с учётом выбранного часового пояса.
- Создание нескольких публикаций одним сообщением через пары «дата/время + текст»:

  ```text
  2026-12-24 18:00
  Первое сообщение

  2026-12-25 12:00
  Второе сообщение
  ```

- Повторяющиеся публикации по готовым вариантам или через cron.
- Сохранение поддерживаемого Telegram форматирования и подписей к медиа.
- Планирование текста, фотографий, видео, документов, анимаций, аудио, голосовых сообщений, опросов, геопозиций и других поддерживаемых типов.
- Режимы медиа: один файл, последовательное назначение, случайный выбор или Media Storage.
- Автоматические подписи в начале или конце публикации.
- Списки и календарь запланированных и повторяющихся сообщений.
- Поиск, предпросмотр, редактирование, удаление, дублирование и замена поддерживаемых сообщений.
- Подключение каналов и публикация через отдельный sender bot.
- Экспорт и резервное копирование поддерживаемых данных.
- Доступная боту статистика отправок и аналитика каналов.
- Premium через Telegram Stars, если покупки Premium включены.

Доступные лимиты и действия зависят от тарифа, прав Telegram, ограничений API и типа сообщения.

## Быстрая настройка

1. Откройте [@FastSchedulerBot](https://t.me/FastSchedulerBot).
2. Пройдите tutorial.
3. Добавьте бота администратором канала минимум с правом **Post Messages**.
4. Подключите канал в боте.
5. При необходимости подключите sender bot и добавьте его администратором в тот же канал.
6. Укажите часовой пояс и создайте публикацию.

## Юридические документы

- [Политика конфиденциальности](legal/privacy.html)
- [Условия использования](legal/terms.html)
- [Политика возвратов](legal/refundpolicy.html)

---

## Website files

This folder is also the static GitHub Pages website for the bot.

- `index.html` — minimal landing page with the bot name, Telegram link, and legal-document links.
- `legal/privacy.html` — Privacy Policy.
- `legal/terms.html` — Terms of Service.
- `legal/refundpolicy.html` — Refund Policy.
- `styles/main.css` — shared stylesheet for the legal pages.
- `scripts/` — JavaScript used by the legal pages.
- `_build/build_site.py` — generator for rebuilding legal pages from the Markdown files in `../docs/`.

## Regenerating the legal pages

From the repository root:

```bash
python website/_build/build_site.py
```

This regenerates the three HTML files under `website/legal/`. The `_build/` folder is needed for regeneration in the repository, but it is not required in the published static GitHub Pages output.

## GitHub Pages structure

Publish these files and folders together:

```text
index.html
styles/
scripts/
legal/
```

Do not publish `.env` files, bot tokens, databases, logs, virtual environments, or local runtime data with this website.
