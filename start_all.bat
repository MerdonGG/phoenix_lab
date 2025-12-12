@echo off
chcp 65001 >nul
echo ========================================
echo   Phoenix Lab - Запуск всех сервисов
echo ========================================
echo.

:: Проверяем, что мы в корневой директории проекта
if not exist "package.json" (
    echo [ОШИБКА] Файл package.json не найден!
    echo Убедитесь, что вы запускаете скрипт из корневой директории проекта.
    pause
    exit /b 1
)

:: Проверяем наличие Node.js
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Node.js не установлен или не найден в PATH!
    echo Установите Node.js: https://nodejs.org/
    pause
    exit /b 1
)

:: Проверяем наличие Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Python не установлен или не найден в PATH!
    echo Установите Python: https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Проверка зависимостей...
echo.

:: Проверяем node_modules
if not exist "node_modules" (
    echo [ВНИМАНИЕ] node_modules не найдены. Устанавливаю зависимости...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ОШИБКА] Не удалось установить зависимости Node.js
        pause
        exit /b 1
    )
)

echo [2/3] Запуск фронтенда (Next.js)...
start "Phoenix Lab - Frontend" cmd /k "cd /d %~dp0 && npm run dev"
timeout /t 2 /nobreak >nul

echo [3/3] Запуск бэкенда (Flask)...
start "Phoenix Lab - Backend" cmd /k "cd /d %~dp0\Backend && python server.py"
timeout /t 2 /nobreak >nul

echo [4/4] Запуск Telegram бота...
start "Phoenix Lab - Telegram Bot" cmd /k "cd /d %~dp0\TelegramBot && python main.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   Все сервисы запущены!
echo ========================================
echo.
echo Фронтенд: http://localhost:3000
echo Бэкенд:   http://localhost:5000
echo Бот:      Запущен и ожидает команды
echo.
echo Для остановки закройте окна с сервисами
echo или нажмите Ctrl+C в каждом окне.
echo.
pause

