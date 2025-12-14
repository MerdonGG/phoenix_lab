# Исправление ошибки "Railpack could not determine how to build the app"

## Проблема
Railway не может определить, как собрать приложение.

## Решение

### Вариант 1: Установка Root Directory (обязательно!)

1. В Railway откройте ваш сервис
2. Перейдите в **Settings → Source**
3. Найдите **Root Directory**
4. Установите: `Backend`
5. Сохраните
6. Перезапустите деплой (Redeploy)

### Вариант 2: Проверка файлов

Убедитесь, что в папке `Backend` есть следующие файлы:
- ✅ `Procfile` - команда запуска
- ✅ `requirements.txt` - зависимости Python
- ✅ `runtime.txt` - версия Python
- ✅ `nixpacks.toml` - конфигурация сборки (создан)
- ✅ `railway.json` - конфигурация Railway (создан)

### Вариант 3: Ручная настройка Build Command

Если автоматическое определение не работает:

1. В Railway откройте Settings → Build
2. Установите **Build Command**:
   ```
   pip install -r requirements.txt
   ```
3. Установите **Start Command**:
   ```
   gunicorn server:app --bind 0.0.0.0:$PORT
   ```

### Вариант 4: Использование Dockerfile (если ничего не помогает)

Создайте `Dockerfile` в папке `Backend`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD gunicorn server:app --bind 0.0.0.0:$PORT
```

Затем в Railway:
1. Settings → Build
2. Builder: **Dockerfile**
3. Dockerfile Path: `Backend/Dockerfile`

## Проверка

После исправления:
1. Railway должен начать сборку
2. В логах должно быть: "Installing dependencies..."
3. После сборки сервис должен запуститься

## Если проблема сохраняется

1. Проверьте логи в Railway
2. Убедитесь, что все файлы закоммичены и запушены
3. Попробуйте удалить сервис и создать заново с правильным Root Directory

