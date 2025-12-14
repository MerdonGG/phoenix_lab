# Настройка Vercel для деплоя

## ✅ Исправлено

1. **TypeScript ошибка исправлена** - обновлена логика обновления состояния изображений
2. **Next.js обновлен** - версия обновлена с `14.0.4` до `^14.2.15` для устранения критической уязвимости
3. **Корневой `vercel.json` удален** - он мешал Vercel автоматически определять Next.js. Теперь нужно настроить Root Directory в Dashboard.

## Проблема: Быстрая сборка (98-103ms)

Если сборка завершается слишком быстро, это означает, что Vercel не находит папку `Frontend` или не выполняет правильную сборку.

## ⚠️ КРИТИЧЕСКИ ВАЖНО: Настройка Root Directory в Vercel Dashboard

**Это ОБЯЗАТЕЛЬНЫЙ шаг!** Без этого Vercel не сможет найти Next.js и выдаст ошибку:
```
Error: No Next.js version detected. Make sure your package.json has "next" in either "dependencies" or "devDependencies".
```

### Шаги (ОБЯЗАТЕЛЬНО):

1. Откройте проект на [vercel.com](https://vercel.com)
2. Перейдите в **Settings → General**
3. Найдите секцию **Root Directory**
4. Нажмите **Edit**
5. Введите: `Frontend` (или выберите из списка)
6. Нажмите **Save**
7. **Убедитесь, что корневой `vercel.json` удален** (он уже удален из репозитория)
8. Перезапустите деплой:
   - Перейдите в **Deployments**
   - Найдите последний деплой
   - Нажмите **⋯** (три точки)
   - Выберите **Redeploy**

**Почему это важно:** Vercel автоматически определяет Next.js только если `package.json` находится в корневой директории проекта (Root Directory). Если Root Directory = `Frontend`, то Vercel будет искать `package.json` в папке `Frontend` и автоматически определит Next.js.

## Файлы конфигурации

- **`Frontend/vercel.json`** - настройки для Next.js приложения (опционально, Vercel может работать и без него)
- **Корневой `vercel.json` НЕ НУЖЕН** - удалите его, если он есть. Vercel автоматически определит Next.js, если Root Directory настроен правильно.

**Важно:** После настройки Root Directory = `Frontend` в Dashboard, Vercel будет:
- Автоматически находить `package.json` в папке `Frontend`
- Автоматически определять Next.js
- Выполнять `npm install` и `npm run build` в правильной директории

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

