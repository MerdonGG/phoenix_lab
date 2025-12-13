# Phoenix Lab

<div align="center">
  <img src="Frontend/public/logo.png" alt="Phoenix Lab Logo" width="200" />
</div>

Одностраничный веб-сайт для AI рерайта статей с интеграцией Telegram для рассылки.

## Структура проекта

```
phoenix_lab/
├── Frontend/              # Next.js Frontend
│   ├── app/              # App Router
│   ├── public/           # Статические файлы
│   ├── package.json
│   └── next.config.js
├── Backend/              # Backend компоненты
│   ├── server.py         # Flask API сервер
│   └── requirements.txt
├── TelegramBot/          # Telegram бот
│   ├── main.py
│   ├── requirements.txt
│   └── channels.json     # Файл с каналами (создаётся автоматически)
└── README.md
```

## Компоненты

- **Frontend** (`Frontend/`) - Next.js приложение для обработки статей
- **Backend** (`Backend/server.py`) - Flask API для отправки статей в Telegram
- **Telegram бот** (`TelegramBot/main.py`) - управление каналами

## Установка

### Backend

1. Установите зависимости:
```bash
pip install -r Backend/requirements.txt
pip install -r TelegramBot/requirements.txt
```

2. Создайте файлы с переменными окружения:
   
   **В корне проекта создайте `.env` или `BOT_TOKEN.env`:**
   ```
   BOT_TOKEN=your_bot_token_here
   PORT=5000
   ```
   
   **В папке `Backend/` создайте `openrouter.env`:**
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_MODEL=qwen/qwen2.5-72b-instruct
   OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
   ```
   
   **Или используйте примеры файлов:**
   - `env.example` — пример для корневого `.env`
   - `Backend/openrouter.env.example` — пример для `Backend/openrouter.env`

**Настройка OpenRouter API:**
1. Зарегистрируйтесь на [OpenRouter.ai](https://openrouter.ai/)
2. Создайте API ключ в разделе Keys
3. Добавьте `OPENROUTER_API_KEY` в файл окружения
4. Опционально: укажите модель в `OPENROUTER_MODEL` (по умолчанию: `qwen/qwen2.5-72b-instruct`)
5. Опционально: укажите URL в `OPENROUTER_API_URL` (по умолчанию: `https://openrouter.ai/api/v1/chat/completions`)

### Frontend

1. Установите зависимости:
```bash
cd Frontend
npm install
# или
yarn install
```

2. Создайте файл `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

3. Переместите логотип:
   - Переместите `Без имени-1.png` в папку `Frontend/public/`
   - Переименуйте в `logo.png`

## Запуск

1. Запустите backend сервер:
```bash
cd Backend
python server.py
```

2. Запустите Telegram бота (для управления каналами):
```bash
cd TelegramBot
python main.py
```

3. Запустите Next.js приложение:
```bash
cd Frontend
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

## Использование

1. На сайте: введите URL статьи, выберите стиль рерайта
2. После обработки: нажмите кнопку "Telegram" для отправки в каналы
3. Выберите каналы и отправьте статью
4. Управление каналами: используйте Telegram бота (`/add_channel`, `/channels`)

## API Endpoints

- `GET /api/channels` - получить список каналов
- `POST /api/rewrite-article` - рерайтить статью через OpenRouter API (требует url и style)
- `POST /api/send-article` - отправить статью в каналы
- `GET /api/health` - проверка работоспособности
