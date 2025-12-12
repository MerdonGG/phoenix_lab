# Установка зависимостей для Yandex Cloud API

## Проблема
Ошибка: `ModuleNotFoundError: No module named 'openai'`

## Решение

### Вариант 1: Использовать batch-файл (Windows)
Дважды кликните на файл `Backend/install_dependencies.bat`

### Вариант 2: Установить вручную в PowerShell

Откройте PowerShell в папке `Backend` и выполните:

```powershell
pip install openai beautifulsoup4 requests lxml
```

Или установите все зависимости из файла:

```powershell
pip install -r requirements.txt
```

### Вариант 3: Установить через pip напрямую

```powershell
pip install openai==1.12.0 beautifulsoup4==4.12.2 requests==2.31.0 lxml==5.1.0
```

## Проверка установки

После установки проверьте:

```powershell
python -c "import openai; print('openai установлен')"
python -c "import bs4; print('beautifulsoup4 установлен')"
python -c "import requests; print('requests установлен')"
python -c "import lxml; print('lxml установлен')"
```

## Запуск бэкенда

После установки запустите:

```powershell
cd Backend
python server.py
```

