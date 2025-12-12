@echo off
chcp 65001 >nul
echo Остановка всех сервисов Phoenix Lab...
echo.

:: Останавливаем процессы Node.js (Next.js)
taskkill /F /IM node.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Фронтенд остановлен
) else (
    echo [INFO] Фронтенд не был запущен
)

:: Останавливаем процессы Python (Flask и бот)
taskkill /F /FI "WINDOWTITLE eq Phoenix Lab - Backend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Phoenix Lab - Telegram Bot*" >nul 2>&1

:: Также останавливаем по имени процесса (на случай, если окна закрыты)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID:"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [OK] Все сервисы остановлены
echo.
pause

