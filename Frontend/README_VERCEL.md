# Быстрый старт для деплоя на Vercel

## Переменные окружения

Перед деплоем на Vercel необходимо установить следующую переменную окружения:

### NEXT_PUBLIC_API_URL

URL вашего развернутого бэкенда (Flask сервер).

**Примеры:**
- Локально: `http://localhost:5000`
- Railway: `https://your-app.railway.app`
- Render: `https://your-app.onrender.com`
- Heroku: `https://your-app.herokuapp.com`

## Как установить переменные окружения в Vercel

1. Перейдите в настройки проекта на Vercel
2. Откройте раздел "Environment Variables"
3. Добавьте переменную:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: URL вашего бэкенда
   - **Environment**: выберите Production, Preview и Development

## Деплой через веб-интерфейс

1. Зайдите на [vercel.com](https://vercel.com)
2. Нажмите "Add New Project"
3. Импортируйте ваш репозиторий
4. **Важно**: Укажите Root Directory как `Frontend`
5. Добавьте переменную окружения `NEXT_PUBLIC_API_URL`
6. Нажмите "Deploy"

## Деплой через CLI

```bash
cd Frontend
npm install -g vercel
vercel login
vercel
```

При запросе переменных окружения укажите `NEXT_PUBLIC_API_URL`.

## После деплоя

1. Убедитесь, что бэкенд развернут и доступен
2. Проверьте, что в бэкенде настроен CORS для вашего Vercel домена
3. Протестируйте основные функции приложения

Подробная инструкция в файле `DEPLOY.md`.

