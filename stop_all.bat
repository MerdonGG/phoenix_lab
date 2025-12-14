@echo off
chcp 65001 >nul
echo Остановка всех сервисов Phoenix Lab 2...
echo.

:: Останавливаем процессы Node.js (Next.js)
echo Остановка Frontend (Next.js)...
taskkill /F /IM node.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Фронтенд остановлен
) else (
    echo [INFO] Фронтенд не был запущен
)

:: Останавливаем процессы Python по окнам
echo Остановка Backend и TelegramBot...
taskkill /F /FI "WINDOWTITLE eq Phoenix Lab 2 - Backend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Phoenix Lab 2 - Telegram Bot*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Phoenix Lab 2 - Frontend*" >nul 2>&1

:: Также останавливаем процессы Python, которые могут быть связаны с проектом
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID:"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [OK] Все сервисы остановлены
echo.
pause


