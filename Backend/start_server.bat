@echo off
chcp 65001 >nul
echo ========================================
echo   Phoenix Lab 2 - Backend Server
echo ========================================
echo.

:: Проверяем, что мы в папке Backend
if not exist "server.py" (
    echo [ОШИБКА] Файл server.py не найден!
    echo Убедитесь, что вы запускаете скрипт из папки Backend.
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
python -c "import flask" >nul 2>&1
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
echo Запуск Flask сервера...
echo Бэкенд будет доступен на: http://localhost:5000
echo.
echo Для остановки нажмите Ctrl+C
echo.

python server.py

pause


