# Настройка Vercel для деплоя

## ✅ Исправлено

1. **TypeScript ошибка исправлена** - обновлена логика обновления состояния изображений
2. **Конфигурация Vercel исправлена** - команды в `vercel.json` теперь переходят в папку `Frontend` перед выполнением

## Проблема: Быстрая сборка (98-103ms)

Если сборка завершается слишком быстро, это означает, что Vercel не находит папку `Frontend` или не выполняет правильную сборку.

## ⚠️ ВАЖНО: Настройка Root Directory в Vercel Dashboard

**Это обязательный шаг!** Vercel должен знать, где находится Next.js приложение.

### Шаги:

1. Откройте проект на [vercel.com](https://vercel.com)
2. Перейдите в **Settings → General**
3. Найдите секцию **Root Directory**
4. Нажмите **Edit**
5. Введите: `Frontend` (или выберите из списка)
6. Нажмите **Save**
7. Перезапустите деплой:
   - Перейдите в **Deployments**
   - Найдите последний деплой
   - Нажмите **⋯** (три точки)
   - Выберите **Redeploy**

## Файлы конфигурации

- **`vercel.json`** (в корне) - команды сборки с переходом в папку `Frontend`:
  ```json
  {
    "buildCommand": "cd Frontend && npm run build",
    "installCommand": "cd Frontend && npm install",
    "outputDirectory": "Frontend/.next"
  }
  ```
- **`Frontend/vercel.json`** - настройки для Next.js приложения (используется, если Root Directory = `Frontend`)

**Примечание:** Если Root Directory настроен в Dashboard как `Frontend`, то корневой `vercel.json` может быть не нужен, так как Vercel будет работать напрямую из папки `Frontend`.

## Проверка правильной сборки

После правильной настройки вы должны увидеть в логах:

```
Running "npm install"
Installing dependencies...
Running "npm run build"
> next build
...
Build Completed in /vercel/output [XXs] (не 98ms!)
```

**Сборка должна занимать 1-3 минуты**, а не 98-103ms!

## Переменные окружения

**Обязательно добавьте** в настройках Vercel (**Settings → Environment Variables**):

- **Name**: `NEXT_PUBLIC_API_URL`
- **Value**: URL вашего бэкенда (например, `https://your-backend.railway.app` или `http://localhost:5000` для разработки)
- **Environment**: Выберите все (Production, Preview, Development)

## Чек-лист перед деплоем

- [ ] Root Directory установлен как `Frontend` в Vercel Dashboard
- [ ] Переменная окружения `NEXT_PUBLIC_API_URL` добавлена
- [ ] Изменения закоммичены и запушены в репозиторий
- [ ] Деплой перезапущен после настройки Root Directory

## Если сборка всё ещё быстрая

1. Убедитесь, что Root Directory установлен в Dashboard (не только в vercel.json)
2. Проверьте, что вы закоммитили и запушили изменения
3. Попробуйте удалить проект и создать заново, указав Root Directory сразу при создании

