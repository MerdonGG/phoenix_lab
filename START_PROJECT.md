# Запуск проекта Phoenix Lab

## Быстрый старт

### Вариант 1: Запуск с окнами (рекомендуется)

Запустите файл:
```
start_all.bat
```

Этот скрипт:
- ✅ Проверит наличие Node.js и Python
- ✅ Установит зависимости, если нужно
- ✅ Запустит все три сервиса в отдельных окнах:
  - **Фронтенд** (Next.js) - порт 3000
  - **Бэкенд** (Flask) - порт 5000
  - **Telegram бот** - ожидает команды

**Преимущества:**
- Видны логи каждого сервиса
- Легко отслеживать ошибки
- Можно остановить каждый сервис отдельно (Ctrl+C)

---

### Вариант 2: Запуск в фоне (тихий режим)

Запустите файл:
```
start_all_quiet.bat
```

Все сервисы запустятся в фоне без окон.

**Для остановки:**
```
stop_all.bat
```

---

## Остановка сервисов

### Если использовали `start_all.bat`:
- Закройте каждое окно (Ctrl+C или крестик)
- Или используйте `stop_all.bat`

### Если использовали `start_all_quiet.bat`:
- Используйте `stop_all.bat`

---

## Ручной запуск (если bat-файлы не работают)

### 1. Фронтенд (в отдельном терминале):
```powershell
npm run dev
```

### 2. Бэкенд (в отдельном терминале):
```powershell
cd Backend
python server.py
```

### 3. Telegram бот (в отдельном терминале):
```powershell
cd TelegramBot
python main.py
```

---

## Проверка работы

После запуска проверьте:

1. **Фронтенд:** http://localhost:3000
   - Должна открыться главная страница

2. **Бэкенд:** http://localhost:5000/api/health
   - Должен вернуть `{"status":"ok"}`

3. **Telegram бот:**
   - Откройте бота в Telegram
   - Отправьте `/start`
   - Бот должен ответить

---

## Возможные проблемы

### Порт уже занят

**Ошибка:** `Port 3000 is already in use` или `Port 5000 is already in use`

**Решение:**
1. Закройте все запущенные сервисы (`stop_all.bat`)
2. Или найдите и завершите процесс, занимающий порт:
   ```powershell
   netstat -ano | findstr :3000
   netstat -ano | findstr :5000
   taskkill /PID <номер_процесса> /F
   ```

### Node.js не найден

**Ошибка:** `Node.js не установлен или не найден в PATH`

**Решение:**
1. Установите Node.js: https://nodejs.org/
2. Перезапустите терминал
3. Проверьте: `node --version`

### Python не найден

**Ошибка:** `Python не установлен или не найден в PATH`

**Решение:**
1. Установите Python: https://www.python.org/
2. При установке отметьте "Add Python to PATH"
3. Перезапустите терминал
4. Проверьте: `python --version`

### Зависимости не установлены

**Ошибка:** Модули не найдены

**Решение:**
```powershell
# Для фронтенда
npm install

# Для бэкенда
cd Backend
pip install -r requirements.txt

# Для бота
cd TelegramBot
pip install -r requirements.txt
```

---

## Структура проекта

```
phoenix_lab/
├── start_all.bat          # Запуск всех сервисов (с окнами)
├── start_all_quiet.bat    # Запуск всех сервисов (тихий)
├── stop_all.bat           # Остановка всех сервисов
├── app/                   # Фронтенд (Next.js)
├── Backend/               # Бэкенд (Flask)
│   └── server.py
└── TelegramBot/           # Telegram бот
    └── main.py
```

---

## Полезные команды

### Проверка портов:
```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :5000
```

### Просмотр процессов:
```powershell
tasklist | findstr node.exe
tasklist | findstr python.exe
```

### Очистка кэша Next.js:
```powershell
rmdir /s /q .next
npm run dev
```

---

## Автозапуск при старте Windows (опционально)

Если хотите, чтобы проект запускался автоматически:

1. Создайте ярлык для `start_all.bat`
2. Переместите ярлык в папку автозагрузки:
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
   ```

**Внимание:** Это запустит проект при каждом входе в Windows.

