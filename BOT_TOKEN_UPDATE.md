# Обновление токена бота

## Проблема

В файле `Backend/BOT_TOKEN.env` указан токен для бота `@ZZZGPTZZZ_bot`, но нужен токен для бота `@PhoenixLogIN_bot`.

## Решение

### 1. Получите токен для бота @PhoenixLogIN_bot

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/mybots`
3. Выберите бота `PhoenixLogIN_bot` из списка
4. Нажмите "API Token" или отправьте команду `/token`
5. Скопируйте токен (он будет выглядеть примерно так: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Обновите файл BOT_TOKEN.env

Откройте файл `Backend/BOT_TOKEN.env` и замените токен:

```
BOT_TOKEN=ваш_новый_токен_для_PhoenixLogIN_bot
PORT=5000
```

**Важно:** Не добавляйте пробелы вокруг знака `=`

### 3. Перезапустите бота

После обновления токена:

1. Остановите бота (Ctrl+C в терминале)
2. Запустите снова:
   ```powershell
   cd TelegramBot
   python main.py
   ```

### 4. Проверка

После перезапуска в логах должно быть:

```
INFO:aiogram.dispatcher:Run polling for bot @PhoenixLogIN_bot id=XXXXX - 'Phoenix LogIN'
```

Вместо:
```
INFO:aiogram.dispatcher:Run polling for bot @ZZZGPTZZZ_bot id=8291751381 - 'GPTZZZ'
```

## Альтернативный способ

Если у вас нет доступа к BotFather или нужно создать нового бота:

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям и создайте бота с именем `PhoenixLogIN_bot`
4. Скопируйте токен и обновите файл `Backend/BOT_TOKEN.env`

