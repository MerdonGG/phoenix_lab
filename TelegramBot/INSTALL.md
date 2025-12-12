# Установка зависимостей для Telegram бота

## Установка

Выполните в PowerShell:

```powershell
cd TelegramBot
pip install -r requirements.txt
```

Или установите пакеты по отдельности:

```powershell
pip install aiogram python-dotenv aiohttp
```

## Если возникают проблемы с установкой aiogram

Aiogram требует компиляции некоторых зависимостей. Если возникают ошибки:

1. **Установите Rust** (если требуется):
   - Скачайте с https://rustup.rs/
   - Или используйте предкомпилированные wheels

2. **Или установите только необходимые пакеты для авторизации:**
   ```powershell
   pip install aiohttp python-dotenv
   ```
   
   И обновите код бота, чтобы не использовать aiogram для авторизации (но это потребует изменений в коде).

## Проверка установки

После установки проверьте:

```powershell
python -c "import aiohttp; import aiogram; print('Все модули установлены!')"
```

Если нет ошибок - все готово!

