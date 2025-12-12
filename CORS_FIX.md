# Исправление ошибки CORS

## Проблема
Ошибка CORS при запросе к `/api/rewrite-article`:
```
Запрос из постороннего источника заблокирован: Политика одного источника запрещает чтение удаленного ресурса
```

## Решение

1. **Убедитесь, что бэкенд запущен:**
   ```bash
   cd Backend
   python server.py
   ```

2. **Проверьте, что бэкенд слушает на порту 5000:**
   В логах должно быть:
   ```
   * Running on http://0.0.0.0:5000
   ```

3. **Перезапустите бэкенд после изменений:**
   - Остановите бэкенд (Ctrl+C)
   - Запустите снова: `python server.py`

4. **Проверьте, что CORS настроен правильно:**
   В файле `Backend/server.py` должно быть:
   ```python
   from flask_cors import CORS, cross_origin
   
   CORS(app, 
        origins="*",
        methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        supports_credentials=False)
   ```

   И для endpoint:
   ```python
   @app.route('/api/rewrite-article', methods=['POST', 'OPTIONS'])
   @cross_origin(origins='*', methods=['POST', 'OPTIONS'], allow_headers=['Content-Type'])
   def rewrite_article():
   ```

5. **Обновите страницу в браузере:**
   - Нажмите Ctrl+F5 для полной перезагрузки
   - Или откройте DevTools (F12) → Network → отключите кэш

6. **Проверьте логи бэкенда:**
   При запросе должны появиться логи:
   ```
   INFO:werkzeug:127.0.0.1 - - [дата] "OPTIONS /api/rewrite-article HTTP/1.1" 200 -
   INFO:werkzeug:127.0.0.1 - - [дата] "POST /api/rewrite-article HTTP/1.1" 200 -
   ```

## Если проблема сохраняется:

1. Проверьте, что фронтенд работает на `http://localhost:3000`
2. Проверьте, что бэкенд работает на `http://localhost:5000`
3. Попробуйте открыть `http://localhost:5000/api/health` в браузере - должно вернуться `{"status": "ok"}`

