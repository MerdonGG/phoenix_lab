# Добавление Yandex Cloud API ключа

## Проблема
В логах бэкенда видно:
```
WARNING:__main__:YANDEX_CLOUD_API_KEY не найден. Функция рерайта статей будет недоступна.
```

## Решение

1. **Откройте файл `Backend/BOT_TOKEN.env`** в текстовом редакторе

2. **Добавьте следующие строки:**
   ```env
   YANDEX_CLOUD_API_KEY=ваш_api_ключ_здесь
   YANDEX_CLOUD_PROJECT=b1goig30m707ojip72c7
   YANDEX_CLOUD_ASSISTANT_ID=fvtfdp5dm8r044bnumjl
   ```

3. **Полный файл должен выглядеть так:**
   ```env
   BOT_TOKEN=8223416474:AAEr8DXOtlNzIR25B7vm3v37hTZPfPKw5BM
   PORT=5000
   YANDEX_CLOUD_API_KEY=ваш_api_ключ_здесь
   YANDEX_CLOUD_PROJECT=b1goig30m707ojip72c7
   YANDEX_CLOUD_ASSISTANT_ID=fvtfdp5dm8r044bnumjl
   ```

4. **Сохраните файл**

5. **Перезапустите бэкенд** (Ctrl+C, затем `python server.py`)

6. **Проверьте логи** - должно появиться:
   ```
   INFO:__main__:Yandex Cloud API клиент инициализирован
   ```

## Как получить YANDEX_CLOUD_API_KEY:

1. Зайдите в [Yandex Cloud Console](https://console.cloud.yandex.ru/)
2. Создайте или выберите проект
3. Перейдите в раздел "API ключи" или "IAM"
4. Создайте новый API ключ
5. Скопируйте ключ и вставьте в `BOT_TOKEN.env`

