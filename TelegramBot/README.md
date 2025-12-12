# Phoenix Lab Telegram Bot

Telegram бот для AI рерайта статей.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Добавьте токен бота в `.env`:
```
BOT_TOKEN=your_bot_token_here
```

## Запуск

```bash
python main.py
```

## Использование

1. Отправьте команду `/start`
2. Отправьте URL статьи
3. Выберите стиль рерайта (Вконтакте, Telegram, Instagram)
4. Получите результат

