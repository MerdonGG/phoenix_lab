# Инструкция по настройке OpenRouter API

## Получение API ключа

1. Зарегистрируйтесь на [OpenRouter.ai](https://openrouter.ai/)
2. Перейдите в раздел **Keys** в личном кабинете
3. Нажмите **"Create Key"** или **"New Key"**
4. Скопируйте API ключ (формат: `sk-or-v1-...`)

## Настройка в проекте

Создайте файл `Backend/openrouter.env`:

```
OPENROUTER_API_KEY=sk-or-v1-your_api_key_here
OPENROUTER_MODEL=qwen/qwen2.5-72b-instruct
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
```

## Доступные модели Qwen

OpenRouter поддерживает множество моделей Qwen:

- `qwen/qwen2.5-72b-instruct` (рекомендуется, по умолчанию)
- `qwen/qwen2.5-32b-instruct`
- `qwen/qwen2.5-14b-instruct`
- `qwen/qwen2.5-7b-instruct`
- `qwen/qwen2-72b-instruct`
- Другие модели, доступные в OpenRouter

Полный список моделей: [OpenRouter Models](https://openrouter.ai/models)

## Проверка настройки

После настройки перезапустите backend сервер и проверьте логи:
```
INFO: OpenRouter API настроен
INFO: OpenRouter модель: qwen/qwen2.5-72b-instruct
INFO: OpenRouter URL: https://openrouter.ai/api/v1/chat/completions
```

## Преимущества OpenRouter

- ✅ Доступ к множеству моделей через единый API
- ✅ OpenAI-совместимый формат
- ✅ Прозрачное ценообразование
- ✅ Надёжная инфраструктура
- ✅ Поддержка различных моделей Qwen

## Дополнительные параметры

OpenRouter поддерживает дополнительные заголовки для отслеживания:
- `HTTP-Referer` - URL вашего сайта (уже настроено)
- `X-Title` - название вашего приложения (уже настроено)

Эти заголовки помогают OpenRouter отслеживать использование API.

