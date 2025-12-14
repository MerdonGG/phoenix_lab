@echo off
chcp 65001 >nul
echo ========================================
echo   Phoenix Lab 2 - Frontend (Next.js)
echo ========================================
echo.

:: Проверяем, что мы в папке Frontend
if not exist "package.json" (
    echo [ОШИБКА] Файл package.json не найден!
    echo Убедитесь, что вы запускаете скрипт из папки Frontend.
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

:: Проверяем зависимости
if not exist "node_modules" (
    echo [ВНИМАНИЕ] Устанавливаю зависимости...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ОШИБКА] Не удалось установить зависимости
        pause
        exit /b 1
    )
)

echo.
echo Запуск Next.js сервера...
echo Фронтенд будет доступен на: http://localhost:3000
echo.
echo Для остановки нажмите Ctrl+C
echo.

npm run dev

pause


