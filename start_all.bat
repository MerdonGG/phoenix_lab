@echo off
chcp 65001 >nul
echo ========================================
echo   Phoenix Lab 2 - Запуск всех сервисов
echo ========================================
echo.

:: Проверяем, что мы в корневой директории проекта
if not exist "Backend\server.py" (
    echo [ОШИБКА] Файл Backend\server.py не найден!
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

echo [1/4] Проверка зависимостей...
echo.

:: Проверяем node_modules во Frontend
if not exist "Frontend\node_modules" (
    echo [ВНИМАНИЕ] node_modules не найдены. Устанавливаю зависимости Frontend...
    cd Frontend
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ОШИБКА] Не удалось установить зависимости Node.js
        pause
        exit /b 1
    )
    cd ..
)

:: Проверяем зависимости Python для Backend
echo [INFO] Проверка зависимостей Backend...
cd Backend
python -c "import flask" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ВНИМАНИЕ] Устанавливаю зависимости Backend...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ОШИБКА] Не удалось установить зависимости Python
        cd ..
        pause
        exit /b 1
    )
)
cd ..

:: Проверяем зависимости Python для TelegramBot
echo [INFO] Проверка зависимостей TelegramBot...
cd TelegramBot
python -c "import aiogram" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ВНИМАНИЕ] Устанавливаю зависимости TelegramBot...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ОШИБКА] Не удалось установить зависимости TelegramBot
        cd ..
        pause
        exit /b 1
    )
)
cd ..

echo [2/4] Запуск фронтенда (Next.js)...
start "Phoenix Lab 2 - Frontend" cmd /k "cd /d %~dp0\Frontend && npm run dev"
timeout /t 3 /nobreak >nul

echo [3/4] Запуск бэкенда (Flask)...
start "Phoenix Lab 2 - Backend" cmd /k "cd /d %~dp0\Backend && python server.py"
timeout /t 3 /nobreak >nul

echo [4/4] Запуск Telegram бота...
start "Phoenix Lab 2 - Telegram Bot" cmd /k "cd /d %~dp0\TelegramBot && python main.py"
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
echo или используйте stop_all.bat
echo.
pause


