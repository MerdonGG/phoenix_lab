# Запуск проекта Phoenix Lab 2

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

## Ручной запуск отдельных компонентов

### 1. Фронтенд (в отдельном терминале):
```powershell
cd Frontend
npm run dev
```
Или используйте батник:
```powershell
Frontend\start_frontend.bat
```

### 2. Бэкенд (в отдельном терминале):
```powershell
cd Backend
python server.py
```
Или используйте батник:
```powershell
Backend\start_server.bat
```

### 3. Telegram бот (в отдельном терминале):
```powershell
cd TelegramBot
python main.py
```
Или используйте батник:
```powershell
TelegramBot\start_bot.bat
```

---

## Проверка работы

После запуска проверьте:

1. **Фронтенд:** http://localhost:3000
   - Должен открыться веб-интерфейс

2. **Бэкенд:** http://localhost:5000/api/health
   - Должен вернуть: `{"status": "ok"}`

3. **Telegram бот:**
   - Откройте Telegram и найдите вашего бота
   - Отправьте команду `/start`

---

## Требования

- **Node.js** 18+ (для Frontend)
- **Python** 3.8+ (для Backend и TelegramBot)
- **npm** (устанавливается вместе с Node.js)

---

## Устранение проблем

### Ошибка "Node.js не найден"
- Установите Node.js: https://nodejs.org/
- Убедитесь, что Node.js добавлен в PATH

### Ошибка "Python не найден"
- Установите Python: https://www.python.org/
- При установке отметьте "Add Python to PATH"

### Ошибка "Модуль не найден"
- Запустите установку зависимостей вручную:
  ```powershell
  cd Frontend
  npm install
  
  cd ..\Backend
  pip install -r requirements.txt
  
  cd ..\TelegramBot
  pip install -r requirements.txt
  ```

### Порт уже занят
- Закройте другие приложения, использующие порты 3000 или 5000
- Или измените порты в конфигурационных файлах

---

## Структура батников

- `start_all.bat` - запуск всех сервисов с окнами
- `start_all_quiet.bat` - запуск всех сервисов в фоне
- `stop_all.bat` - остановка всех сервисов
- `Backend/start_server.bat` - запуск только бэкенда
- `Frontend/start_frontend.bat` - запуск только фронтенда
- `TelegramBot/start_bot.bat` - запуск только бота

