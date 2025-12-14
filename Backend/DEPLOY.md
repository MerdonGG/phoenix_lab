# Инструкция по деплою бэкенда

Этот файл содержит инструкции по развертыванию Flask бэкенда на различных платформах.

## Варианты развертывания

### 1. Railway (Рекомендуется)

Railway автоматически определяет Python приложения и развертывает их.

#### Шаги:

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Создайте новый проект
3. Подключите ваш GitHub репозиторий
4. Выберите папку `Backend` как корневую директорию
5. Railway автоматически определит Flask приложение

#### Переменные окружения:

Добавьте следующие переменные окружения в настройках проекта:

```bash
# Yandex API
YANDEX_API_KEY=your_yandex_api_key
YANDEX_FOLDER_ID=your_folder_id

# OpenRouter API
OPENROUTER_API_KEY=your_openrouter_key

# Telegram Bot
BOT_TOKEN=your_bot_token

# Pexels (опционально)
PEXELS_API_KEY=your_pexels_key

# FusionBrain (опционально)
FUSIONBRAIN_API_KEY=your_fusionbrain_key
FUSIONBRAIN_SECRET_KEY=your_fusionbrain_secret
FUSIONBRAIN_EMAIL=your_email
FUSIONBRAIN_PASSWORD=your_password

# CORS (важно для работы с фронтендом)
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com

# Порт (Railway устанавливает автоматически)
PORT=5000
```

#### Создание файла для Railway:

Создайте файл `Procfile` в папке Backend:

```
web: gunicorn server:app --bind 0.0.0.0:$PORT
```

Или используйте `runtime.txt` для указания версии Python:

```
python-3.11
```

### 2. Render

#### Шаги:

1. Зарегистрируйтесь на [render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите репозиторий
4. Настройки:
   - **Root Directory**: `Backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Environment**: Python 3

5. Добавьте переменные окружения (см. выше)

### 3. Heroku

#### Шаги:

1. Установите Heroku CLI
2. Войдите: `heroku login`
3. Создайте приложение: `heroku create your-app-name`
4. Установите переменные окружения:
   ```bash
   heroku config:set YANDEX_API_KEY=your_key
   heroku config:set YANDEX_FOLDER_ID=your_id
   # ... и т.д.
   ```
5. Деплой: `git push heroku main`

#### Необходимые файлы:

**Procfile** (в папке Backend):
```
web: gunicorn server:app --bind 0.0.0.0:$PORT
```

**runtime.txt** (в папке Backend):
```
python-3.11.0
```

### 4. PythonAnywhere

1. Зарегистрируйтесь на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Загрузите файлы через веб-интерфейс или Git
3. Настройте WSGI файл
4. Установите переменные окружения через веб-интерфейс

## Общие требования

### Установка зависимостей

Убедитесь, что `requirements.txt` содержит все необходимые зависимости:

```txt
flask
flask-cors
python-dotenv
requests
beautifulsoup4
lxml
openai
aiohttp
nest-asyncio
```

### Настройка CORS

В `server.py` должна быть правильная настройка CORS:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))
```

### Использование Gunicorn

Для продакшена используйте Gunicorn вместо встроенного сервера Flask:

```bash
pip install gunicorn
gunicorn server:app --bind 0.0.0.0:5000
```

## Проверка после деплоя

1. Проверьте, что сервер отвечает: `curl https://your-backend-url.com/api/health`
2. Проверьте CORS настройки
3. Протестируйте основные эндпоинты
4. Проверьте логи на наличие ошибок

## Troubleshooting

### Проблема: Приложение не запускается

- Проверьте логи на платформе
- Убедитесь, что все переменные окружения установлены
- Проверьте, что порт правильно настроен

### Проблема: CORS ошибки

- Убедитесь, что `CORS_ORIGINS` содержит URL фронтенда
- Проверьте, что URL указаны без завершающего слеша

### Проблема: Зависимости не устанавливаются

- Проверьте `requirements.txt`
- Убедитесь, что указаны правильные версии пакетов

## Рекомендации

1. Используйте переменные окружения для всех секретных данных
2. Не коммитьте файлы с реальными ключами
3. Используйте HTTPS для всех сервисов
4. Регулярно обновляйте зависимости
5. Настройте мониторинг и логирование

