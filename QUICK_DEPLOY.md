# 🚀 Быстрый деплой бэкенда и бота

## Шаг 1: Деплой бэкенда на Railway

1. Перейдите на [railway.app](https://railway.app)
2. Создайте новый проект → Deploy from GitHub
3. Выберите репозиторий `phoenix_lab`
4. **ВАЖНО: Root Directory**: `Backend`
   - В настройках сервиса (Settings → Source)
   - Установите Root Directory как `Backend`
5. Если Railway показывает ошибку "Railpack could not determine":
   - Убедитесь, что Root Directory установлен как `Backend`
   - Файлы `nixpacks.toml` и `railway.json` уже созданы в папке Backend
   - Перезапустите деплой
6. Добавьте переменные окружения:

```bash
YANDEX_CLOUD_API_KEY=AQVN2xArSNi6FoytO7KTX7OpSeG11H5jpEAXfDIN
YANDEX_CLOUD_PROJECT=b1goig30m707ojip72c7
YANDEX_CLOUD_ASSISTANT_ID=fvtfdp5dm8r044bnumjl
BOT_TOKEN=8223416474:AAEr8DXOtlNzIR25B7vm3v37hTZPfPKw5BM
PEXELS_API_KEY=5NZHVjmbNSSA1CmlIMqY6dh9Nq33m3EXvRwEHu3mO0tZ7HdEayD2HtFt
FUSIONBRAIN_API_KEY=FA70505746FFCD7BB7E2A6BF6DC392E6
FUSIONBRAIN_SECRET_KEY=FAD3C6ECAF2ECB4241425B30F192970A
CORS_ORIGINS=https://your-app.vercel.app
```

**⚠️ Замените `https://your-app.vercel.app` на ваш реальный Vercel URL!**

6. Сохраните URL бэкенда (например: `https://your-app.railway.app`)

## Шаг 2: Обновите фронтенд

1. На [vercel.com](https://vercel.com) откройте проект
2. Settings → Environment Variables
3. Добавьте/обновите:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: URL бэкенда из шага 1.6
4. Redeploy

## Шаг 3: Деплой Telegram бота

### На Railway (в том же проекте):

1. В Railway создайте **новый сервис**
2. Подключите тот же репозиторий
3. **Root Directory**: `TelegramBot`
4. Добавьте переменную:
   ```bash
   BOT_TOKEN=8223416474:AAEr8DXOtlNzIR25B7vm3v37hTZPfPKw5BM
   ```
5. Railway автоматически запустит бота

### Или на Render:

1. [render.com](https://render.com) → New → Background Worker
2. Подключите репозиторий
3. **Root Directory**: `TelegramBot`
4. **Start Command**: `python main.py`
5. Добавьте `BOT_TOKEN` (см. выше)

## ✅ Проверка

- Бэкенд: `https://your-backend.railway.app/api/channels`
- Фронтенд: ваш Vercel URL
- Бот: `/start` в Telegram

Подробная инструкция: `DEPLOY_BACKEND_AND_BOT.md`

