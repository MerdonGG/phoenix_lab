# API ключ добавлен!

## Что было сделано:

✅ Секретный ключ добавлен в `Backend/BOT_TOKEN.env`:
```
YANDEX_CLOUD_API_KEY=AQVN2xArSNi6FoytO7KTX7OpSeG11H5jpEAXfDIN
```

## Важно:

- **Идентификатор ключа** (`ajer20lkhm5q2q6aqeti`) - это не то, что нужно для `YANDEX_CLOUD_API_KEY`
- **Секретный ключ** (`AQVN2xArSNi6FoytO7KTX7OpSeG11H5jpEAXfDIN`) - это и есть ваш API ключ

## Что дальше:

### 1. Получите ID инструмента (YANDEX_CLOUD_ASSISTANT_ID)

Вам нужно найти ID вашего инструмента/промпта в AI Studio:

1. Откройте AI Studio → Agent Atelier → МСР-серверы
2. Откройте ваш сервер "phoenix"
3. Найдите ID инструмента (обычно в разделе "Инструменты" или "Обзор")
4. Или используйте ID промпта: `fvtfdp5dm8r044bnumjl` (если он у вас есть)

### 2. Обновите файл (если нужно):

Если ID инструмента отличается от `fvtfdp5dm8r044bnumjl`, обновите в `Backend/BOT_TOKEN.env`:
```env
YANDEX_CLOUD_ASSISTANT_ID=ваш_реальный_id_инструмента
```

### 3. Перезапустите бэкенд:

```powershell
# Остановите бэкенд (Ctrl+C)
# Затем запустите снова:
cd Backend
python server.py
```

### 4. Проверьте логи:

Должно появиться:
```
INFO:__main__:Yandex Cloud API клиент инициализирован
```

Вместо:
```
WARNING:__main__:YANDEX_CLOUD_API_KEY не найден
```

### 5. Протестируйте:

1. Откройте сайт в браузере
2. Введите URL статьи
3. Выберите стиль рерайта
4. Нажмите "Рерайт статьи"
5. Должен появиться результат!

## Если что-то не работает:

1. Проверьте логи бэкенда - там будут ошибки
2. Убедитесь, что ID инструмента правильный
3. Проверьте, что разрешения для ключа правильные (`yc.serverless.mcpGateways.invoke` или `yc.ai.languageModels.execute`)

