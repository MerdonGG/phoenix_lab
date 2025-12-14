# Руководство по деплою Phoenix Lab

Это краткое руководство по развертыванию проекта Phoenix Lab на Vercel (фронтенд) и Railway/Render (бэкенд).

## Архитектура деплоя

```
┌─────────────────┐
│  Frontend       │
│  (Vercel)       │  ← Пользователи
└────────┬────────┘
         │ API запросы
         ▼
┌─────────────────┐
│  Backend        │
│  (Railway/      │  ← Бизнес-логика
│   Render)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Telegram Bot   │  ← Отправка статей
│  (VPS/Server)   │
└─────────────────┘
```

## Быстрый старт

### 1. Деплой бэкенда

Выберите один из вариантов:

- **Railway** (рекомендуется): См. `Backend/DEPLOY.md`
- **Render**: См. `Backend/DEPLOY.md`
- **Heroku**: См. `Backend/DEPLOY.md`

**Важно**: После деплоя бэкенда сохраните его URL (например, `https://your-app.railway.app`)

### 2. Деплой фронтенда на Vercel

1. Перейдите на [vercel.com](https://vercel.com)
2. Импортируйте репозиторий
3. **Root Directory**: `Frontend`
4. Добавьте переменную окружения:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: URL вашего бэкенда (из шага 1)
5. Нажмите "Deploy"

Подробная инструкция: `Frontend/DEPLOY.md`

### 3. Настройка CORS в бэкенде

В переменных окружения бэкенда добавьте:

```
CORS_ORIGINS=https://your-app.vercel.app
```

Замените `your-app.vercel.app` на ваш реальный Vercel URL.

### 4. Деплой Telegram бота (опционально)

Telegram бот должен работать на отдельном сервере или VPS:

1. Загрузите код бота на сервер
2. Установите зависимости: `pip install -r requirements.txt`
3. Настройте переменные окружения
4. Запустите: `python main.py`

Или используйте сервисы вроде Railway/Render для бота.

## Переменные окружения

### Frontend (Vercel)

- `NEXT_PUBLIC_API_URL` - URL бэкенда

### Backend (Railway/Render)

- `YANDEX_API_KEY` - ключ Yandex GPT API
- `YANDEX_FOLDER_ID` - ID папки Yandex Cloud
- `OPENROUTER_API_KEY` - ключ OpenRouter API
- `BOT_TOKEN` - токен Telegram бота
- `PEXELS_API_KEY` - ключ Pexels (опционально)
- `FUSIONBRAIN_API_KEY` - ключ FusionBrain (опционально)
- `FUSIONBRAIN_SECRET_KEY` - секретный ключ FusionBrain (опционально)
- `CORS_ORIGINS` - разрешенные домены для CORS

### Telegram Bot

- `BOT_TOKEN` - токен бота
- `API_URL` - URL бэкенда

## Проверка работы

После деплоя проверьте:

1. ✅ Фронтенд открывается по Vercel URL
2. ✅ API запросы работают (проверьте Network в DevTools)
3. ✅ Рерайт статей работает
4. ✅ Авторизация через Telegram работает
5. ✅ Отправка статей в Telegram работает

## Troubleshooting

### CORS ошибки

**Проблема**: `Access-Control-Allow-Origin` ошибки в браузере

**Решение**: 
1. Убедитесь, что `CORS_ORIGINS` в бэкенде содержит ваш Vercel URL
2. URL должен быть без завершающего слеша
3. Перезапустите бэкенд после изменения переменных

### API не отвечает

**Проблема**: Запросы к API не проходят

**Решение**:
1. Проверьте, что `NEXT_PUBLIC_API_URL` правильно установлен в Vercel
2. Проверьте логи бэкенда на наличие ошибок
3. Убедитесь, что бэкенд запущен и доступен

### Изображения не загружаются

**Проблема**: Изображения не отображаются

**Решение**:
1. Проверьте настройки `images.domains` в `next.config.js`
2. Убедитесь, что внешние сервисы (Pexels, Unsplash) доступны
3. Проверьте CORS для изображений с бэкенда

## Полезные ссылки

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)

## Поддержка

Если возникли проблемы:

1. Проверьте логи на всех платформах
2. Убедитесь, что все переменные окружения установлены
3. Проверьте документацию в `Frontend/DEPLOY.md` и `Backend/DEPLOY.md`

