# Быстрое решение для локальной разработки

## Проблема:
BotFather не принимает `localhost` - Telegram Login Widget требует реальный домен.

## Решение: Используйте ngrok

### 1. Установите ngrok:

**Через npm (если установлен Node.js):**
```bash
npm install -g ngrok
```

**Или скачайте с сайта:**
https://ngrok.com/download

### 2. Запустите ваш Next.js сервер:
```bash
npm run dev
```

### 3. В новом терминале запустите ngrok:
```bash
ngrok http 3000
```

### 4. Скопируйте HTTPS URL из ngrok:
Вы увидите что-то вроде:
```
Forwarding  https://abc123-def456.ngrok.io -> http://localhost:3000
```

### 5. Отправьте BotFather только домен (БЕЗ https://):
```
abc123-def456.ngrok.io
```

### 6. После подтверждения:
- Откройте сайт через ngrok URL: `https://abc123-def456.ngrok.io`
- Виджет должен работать!

## Важно:
- Каждый раз при перезапуске ngrok URL меняется
- Нужно будет обновлять домен в BotFather
- Для постоянной работы используйте реальный домен

## Альтернатива:
Можно использовать другие туннели:
- **Cloudflare Tunnel** (бесплатно, постоянный URL)
- **localtunnel** (npm пакет)
- **serveo.net** (без установки)

