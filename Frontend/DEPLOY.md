# Инструкция по деплою на Vercel

Это руководство поможет вам развернуть фронтенд приложения Phoenix Lab на Vercel.

## Предварительные требования

1. Аккаунт на [Vercel](https://vercel.com)
2. GitHub репозиторий с вашим кодом (или GitLab/Bitbucket)
3. Развернутый бэкенд (Flask) на отдельном сервисе (Railway, Render, Heroku и т.д.)

## Шаг 1: Подготовка бэкенда

Перед деплоем фронтенда убедитесь, что ваш Flask бэкенд развернут и доступен по публичному URL.

### Варианты развертывания бэкенда:

1. **Railway** (рекомендуется)
   - Зарегистрируйтесь на [railway.app](https://railway.app)
   - Создайте новый проект
   - Подключите репозиторий с бэкендом
   - Установите переменные окружения из `Backend/yandex.env`, `Backend/openrouter.env`, `Backend/BOT_TOKEN.env`
   - Railway автоматически определит Flask и развернет его

2. **Render**
   - Зарегистрируйтесь на [render.com](https://render.com)
   - Создайте новый Web Service
   - Подключите репозиторий
   - Укажите команду запуска: `gunicorn server:app`
   - Установите переменные окружения

3. **Heroku**
   - Используйте стандартный процесс деплоя Heroku для Flask приложений

## Шаг 2: Настройка переменных окружения бэкенда

Убедитесь, что в бэкенде настроены следующие переменные окружения:

- `YANDEX_API_KEY` - ключ Yandex GPT API
- `YANDEX_FOLDER_ID` - ID папки в Yandex Cloud
- `OPENROUTER_API_KEY` - ключ OpenRouter API
- `BOT_TOKEN` - токен Telegram бота
- `PEXELS_API_KEY` - ключ Pexels API (опционально)
- `FUSIONBRAIN_API_KEY` - ключ FusionBrain API (опционально)
- `FUSIONBRAIN_SECRET_KEY` - секретный ключ FusionBrain (опционально)
- `CORS_ORIGINS` - разрешенные источники для CORS (укажите URL вашего Vercel приложения)

## Шаг 3: Деплой фронтенда на Vercel

### Вариант A: Через веб-интерфейс Vercel

1. Перейдите на [vercel.com](https://vercel.com) и войдите в аккаунт
2. Нажмите "Add New Project"
3. Импортируйте ваш GitHub репозиторий
4. Настройте проект:
   - **Root Directory**: выберите папку `Frontend`
   - **Framework Preset**: Next.js (должен определиться автоматически)
   - **Build Command**: `npm run build` (по умолчанию)
   - **Output Directory**: `.next` (по умолчанию)
   - **Install Command**: `npm install` (по умолчанию)

5. Добавьте переменные окружения:
   - Перейдите в Settings → Environment Variables
   - Добавьте переменную:
     - **Name**: `NEXT_PUBLIC_API_URL`
     - **Value**: URL вашего развернутого бэкенда (например, `https://your-app.railway.app`)
     - **Environment**: Production, Preview, Development (выберите все)

6. Нажмите "Deploy"

### Вариант B: Через Vercel CLI

1. Установите Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Перейдите в папку Frontend:
   ```bash
   cd Frontend
   ```

3. Войдите в Vercel:
   ```bash
   vercel login
   ```

4. Запустите деплой:
   ```bash
   vercel
   ```

5. Следуйте инструкциям в терминале:
   - Выберите проект или создайте новый
   - Подтвердите настройки

6. Добавьте переменные окружения:
   ```bash
   vercel env add NEXT_PUBLIC_API_URL
   ```
   Введите URL вашего бэкенда при запросе.

7. Запустите продакшн деплой:
   ```bash
   vercel --prod
   ```

## Шаг 4: Настройка домена (опционально)

1. В настройках проекта на Vercel перейдите в "Domains"
2. Добавьте ваш домен
3. Следуйте инструкциям для настройки DNS записей

## Шаг 5: Проверка работы

После деплоя проверьте:

1. Откройте ваш Vercel URL
2. Проверьте, что фронтенд загружается
3. Попробуйте выполнить рерайт статьи
4. Проверьте авторизацию через Telegram бота

## Обновление переменных окружения

Если нужно изменить переменные окружения:

1. Перейдите в Settings → Environment Variables в Vercel
2. Отредактируйте или добавьте переменные
3. Перезапустите деплой (Redeploy)

## Troubleshooting

### Проблема: CORS ошибки

**Решение**: Убедитесь, что в бэкенде в переменной `CORS_ORIGINS` указан URL вашего Vercel приложения:
```
CORS_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com
```

### Проблема: API запросы не работают

**Решение**: 
1. Проверьте, что `NEXT_PUBLIC_API_URL` правильно установлен в Vercel
2. Убедитесь, что бэкенд доступен по указанному URL
3. Проверьте логи бэкенда на наличие ошибок

### Проблема: Изображения не загружаются

**Решение**: 
1. Проверьте настройки `images.domains` в `next.config.js`
2. Убедитесь, что внешние сервисы (Pexels, Unsplash) доступны
3. Проверьте, что бэкенд правильно генерирует URL изображений

## Полезные ссылки

- [Документация Vercel](https://vercel.com/docs)
- [Документация Next.js](https://nextjs.org/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)

## Структура проекта после деплоя

```
Frontend (Vercel)
  └── Отдает статические файлы и обрабатывает Next.js страницы
      └── API запросы → Backend (Railway/Render/Heroku)
                          └── Обрабатывает бизнес-логику
                              └── Telegram Bot (отдельный сервер)
```

## Примечания

- Бэкенд и Telegram бот должны быть развернуты отдельно от фронтенда
- Убедитесь, что все API ключи и токены правильно настроены в переменных окружения
- Для продакшена рекомендуется использовать HTTPS для всех сервисов
- Регулярно обновляйте зависимости для безопасности

