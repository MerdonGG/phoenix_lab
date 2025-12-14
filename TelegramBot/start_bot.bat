@echo off
chcp 65001 >nul
echo ========================================
echo   Phoenix Lab 2 - Telegram Bot
echo ========================================
echo.

:: Проверяем, что мы в папке TelegramBot
if not exist "main.py" (
    echo [ОШИБКА] Файл main.py не найден!
    echo Убедитесь, что вы запускаете скрипт из папки TelegramBot.
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

:: Проверяем зависимости
echo Проверка зависимостей...
python -c "import aiogram" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ВНИМАНИЕ] Устанавливаю зависимости...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ОШИБКА] Не удалось установить зависимости
        pause
        exit /b 1
    )
)

echo.
echo Запуск Telegram бота...
echo Бот готов к работе и ожидает команды
echo.
echo Для остановки нажмите Ctrl+C
echo.

python main.py

pause


