# Настройка Yandex Cloud API

## Шаги настройки:

1. **Добавьте переменные окружения в файл `Backend/BOT_TOKEN.env`:**

```env
BOT_TOKEN=ваш_токен_бота
PORT=5000
YANDEX_CLOUD_API_KEY=ваш_api_ключ_yandex_cloud
YANDEX_CLOUD_PROJECT=b1goig30m707ojip72c7
YANDEX_CLOUD_ASSISTANT_ID=fvtfdp5dm8r044bnumjl
```

2. **Установите зависимости:**

```bash
cd Backend
pip install -r requirements.txt
```

3. **Перезапустите бэкенд:**

```bash
python server.py
```

## Как получить YANDEX_CLOUD_API_KEY:

1. Зайдите в [Yandex Cloud Console](https://console.cloud.yandex.ru/)
2. Создайте или выберите проект
3. Перейдите в раздел "API ключи"
4. Создайте новый API ключ
5. Скопируйте ключ и добавьте в `BOT_TOKEN.env`

## Проверка работы:

После настройки в логах бэкенда должно появиться:
```
INFO:__main__:Yandex Cloud API клиент инициализирован
```

Если ключ не найден, будет предупреждение:
```
WARNING:__main__:YANDEX_CLOUD_API_KEY не найден. Функция рерайта статей будет недоступна.
```

