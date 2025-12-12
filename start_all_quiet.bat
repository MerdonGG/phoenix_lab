@echo off
chcp 65001 >nul
echo Запуск всех сервисов Phoenix Lab...

:: Проверяем, что мы в корневой директории проекта
if not exist "package.json" (
    echo [ОШИБКА] Запустите скрипт из корневой директории проекта!
    pause
    exit /b 1
)

:: Устанавливаем зависимости, если нужно
if not exist "node_modules" (
    echo Установка зависимостей...
    call npm install >nul 2>&1
)

:: Запускаем все сервисы в фоне
start /B "Frontend" cmd /c "cd /d %~dp0 && npm run dev >nul 2>&1"
timeout /t 2 /nobreak >nul

start /B "Backend" cmd /c "cd /d %~dp0\Backend && python server.py >nul 2>&1"
timeout /t 2 /nobreak >nul

start /B "TelegramBot" cmd /c "cd /d %~dp0\TelegramBot && python main.py >nul 2>&1"
timeout /t 2 /nobreak >nul

echo Все сервисы запущены в фоне.
echo Фронтенд: http://localhost:3000
echo Бэкенд:   http://localhost:5000
echo.
echo Для остановки используйте stop_all.bat
pause

