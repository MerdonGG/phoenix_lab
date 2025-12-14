@echo off
chcp 65001 >nul
echo Запуск всех сервисов Phoenix Lab 2...

:: Проверяем, что мы в корневой директории проекта
if not exist "Backend\server.py" (
    echo [ОШИБКА] Запустите скрипт из корневой директории проекта!
    pause
    exit /b 1
)

:: Устанавливаем зависимости Frontend, если нужно
if not exist "Frontend\node_modules" (
    echo Установка зависимостей Frontend...
    cd Frontend
    call npm install >nul 2>&1
    cd ..
)

:: Запускаем все сервисы в фоне
echo Запуск Frontend...
start /B "Frontend" cmd /c "cd /d %~dp0\Frontend && npm run dev >nul 2>&1"
timeout /t 3 /nobreak >nul

echo Запуск Backend...
start /B "Backend" cmd /c "cd /d %~dp0\Backend && python server.py >nul 2>&1"
timeout /t 3 /nobreak >nul

echo Запуск TelegramBot...
start /B "TelegramBot" cmd /c "cd /d %~dp0\TelegramBot && python main.py >nul 2>&1"
timeout /t 2 /nobreak >nul

echo.
echo Все сервисы запущены в фоне.
echo Фронтенд: http://localhost:3000
echo Бэкенд:   http://localhost:5000
echo.
echo Для остановки используйте stop_all.bat
pause

