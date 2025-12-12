from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import json
import logging
import asyncio
import secrets
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Опциональный импорт aiogram (нужен только для отправки статей)
try:
    from aiogram import Bot
    from aiogram.exceptions import TelegramAPIError
    AIOGRAM_AVAILABLE = True
except ImportError:
    AIOGRAM_AVAILABLE = False

# Загружаем .env из корня проекта или из папки Backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Список возможных путей к файлам с переменными окружения
env_paths = [
    os.path.join(BASE_DIR, '.env'),                    # Корень проекта
    os.path.join(BACKEND_DIR, 'BOT_TOKEN.env'),        # Папка Backend
    os.path.join(BASE_DIR, 'BOT_TOKEN.env'),           # Корень проекта
]

env_path = None
for path in env_paths:
    if os.path.exists(path):
        env_path = path
        load_dotenv(path, override=True)
        break

# Если ни один файл не найден, пробуем загрузить стандартный .env
if env_path is None:
    load_dotenv()

app = Flask(__name__)
# Настройка CORS для разрешения запросов с фронтенда
# Для разработки разрешаем все источники
CORS(app, 
     origins="*",  # Разрешаем все источники для разработки
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=False)

# Логирование всех запросов
@app.before_request
def log_request_info():
    if request.path.startswith('/api/auth'):
        logger.info(f"Запрос: {request.method} {request.path}")
        logger.info(f"Content-Type: {request.content_type}")
        logger.info(f"Headers: {dict(request.headers)}")
        if request.is_json:
            json_data = request.json
            # Скрываем полный токен в логах для безопасности
            if isinstance(json_data, dict) and 'token' in json_data:
                token = json_data['token']
                if token:
                    json_data_copy = json_data.copy()
                    json_data_copy['token'] = token[:10] + '...' if len(token) > 10 else '***'
                    logger.info(f"JSON данные: {json_data_copy}")
                else:
                    logger.info(f"JSON данные: {json_data}")
            else:
                logger.info(f"JSON данные: {json_data}")
        elif request.data:
            logger.info(f"Raw данные: {request.data}")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Логируем путь к загруженному файлу
if env_path:
    logger.info(f"Загружен файл переменных окружения: {env_path}")

# Предупреждение о недоступности aiogram
if not AIOGRAM_AVAILABLE:
    logger.warning("aiogram не установлен. Функция отправки статей будет недоступна.")

# Создаём папку TelegramBot если её нет
TELEGRAM_BOT_DIR = os.path.join(BASE_DIR, "TelegramBot")
if not os.path.exists(TELEGRAM_BOT_DIR):
    os.makedirs(TELEGRAM_BOT_DIR)
    logger.info(f"Создана папка: {TELEGRAM_BOT_DIR}")

CHANNELS_FILE = os.path.join(TELEGRAM_BOT_DIR, "channels.json")
AUTH_TOKENS_FILE = os.path.join(TELEGRAM_BOT_DIR, "auth_tokens.json")

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error(f"BOT_TOKEN не найден. Проверьте файл: {env_path}")
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

# Yandex Cloud API настройки
YANDEX_CLOUD_API_KEY = os.getenv('YANDEX_CLOUD_API_KEY')
YANDEX_CLOUD_PROJECT = os.getenv('YANDEX_CLOUD_PROJECT', 'b1goig30m707ojip72c7')
YANDEX_CLOUD_ASSISTANT_ID = os.getenv('YANDEX_CLOUD_ASSISTANT_ID', 'fvtfdp5dm8r044bnumjl')

if YANDEX_CLOUD_API_KEY:
    try:
        yandex_client = OpenAI(
            api_key=YANDEX_CLOUD_API_KEY,
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=YANDEX_CLOUD_PROJECT
        )
        logger.info("Yandex Cloud API клиент инициализирован")
    except Exception as e:
        yandex_client = None
        logger.error(f"Ошибка инициализации Yandex Cloud API: {e}")
else:
    yandex_client = None
    logger.warning("YANDEX_CLOUD_API_KEY не найден. Функция рерайта статей будет недоступна.")

logger.info("BOT_TOKEN успешно загружен")
logger.info(f"Используется файл каналов: {CHANNELS_FILE}")

# Bot будет создаваться для каждого запроса, чтобы избежать проблем с сессией
logger.info("Aiogram Bot готов к использованию")


def load_channels():
    """Загружает список каналов из файла"""
    if os.path.exists(CHANNELS_FILE):
        try:
            with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('channels', [])
        except Exception as e:
            logger.error(f"Ошибка загрузки каналов: {e}")
            return []
    return []


# Хранилище токенов авторизации (в памяти, можно заменить на Redis/БД)
auth_tokens = {}

def load_auth_tokens():
    """Загружает токены из файла"""
    global auth_tokens
    if os.path.exists(AUTH_TOKENS_FILE):
        try:
            with open(AUTH_TOKENS_FILE, 'r', encoding='utf-8') as f:
                loaded_tokens = json.load(f)
                # Удаляем истекшие токены
                current_time = time.time()
                before_count = len(loaded_tokens)
                auth_tokens = {
                    k: v for k, v in loaded_tokens.items()
                    if v.get('expires_at', 0) > current_time
                }
                after_count = len(auth_tokens)
                if before_count > 0 or after_count > 0:
                    logger.info(f"Загружено токенов из файла: {before_count}, активных: {after_count}")
                # Сохраняем очищенные токены обратно в файл
                if before_count != after_count:
                    save_auth_tokens()
        except json.JSONDecodeError as e:
            logger.warning(f"Файл токенов поврежден или пустой, создаю новый: {e}")
            auth_tokens = {}
        except Exception as e:
            logger.error(f"Ошибка загрузки токенов: {e}", exc_info=True)
            auth_tokens = {}
    else:
        logger.info(f"Файл токенов не найден: {AUTH_TOKENS_FILE}, создам при первой генерации")
        auth_tokens = {}


def save_auth_tokens():
    """Сохраняет токены в файл"""
    try:
        # Создаем директорию, если её нет
        os.makedirs(os.path.dirname(AUTH_TOKENS_FILE), exist_ok=True)
        # Используем временный файл для атомарной записи
        temp_file = AUTH_TOKENS_FILE + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(auth_tokens, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())  # Принудительно записываем на диск
        # Атомарно заменяем старый файл новым с обработкой ошибок доступа
        try:
            if os.path.exists(AUTH_TOKENS_FILE):
                os.replace(temp_file, AUTH_TOKENS_FILE)
            else:
                os.rename(temp_file, AUTH_TOKENS_FILE)
            logger.info(f"Сохранено токенов в файл: {len(auth_tokens)}, файл: {AUTH_TOKENS_FILE}")
        except PermissionError as pe:
            # Если не удалось заменить файл (заблокирован), перезаписываем напрямую
            logger.warning(f"Не удалось атомарно заменить файл, перезаписываем напрямую: {pe}")
            try:
                with open(AUTH_TOKENS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(auth_tokens, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                logger.info(f"Сохранено токенов в файл (прямая запись): {len(auth_tokens)}, файл: {AUTH_TOKENS_FILE}")
            except Exception as e2:
                logger.error(f"Ошибка прямой записи токенов: {e2}")
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
    except Exception as e:
        logger.error(f"Ошибка сохранения токенов: {e}", exc_info=True)
        # Удаляем временный файл при ошибке
        temp_file = AUTH_TOKENS_FILE + '.tmp'
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass


def generate_auth_token():
    """Генерирует новый токен авторизации"""
    global auth_tokens
    # Загружаем существующие токены перед добавлением нового
    load_auth_tokens()
    
    token = secrets.token_urlsafe(32)
    expires_at = time.time() + 300  # Токен действителен 5 минут
    auth_tokens[token] = {
        'expires_at': expires_at,
        'status': 'pending',  # pending, authorized, expired
        'user_data': None
    }
    logger.info(f"Генерация токена {token[:10]}..., токенов в памяти перед сохранением: {len(auth_tokens)}")
    save_auth_tokens()
    
    # Проверяем, что токен действительно сохранился
    import time as time_module
    time_module.sleep(0.1)  # Небольшая задержка для гарантии записи на диск
    
    if os.path.exists(AUTH_TOKENS_FILE):
        try:
            with open(AUTH_TOKENS_FILE, 'r', encoding='utf-8') as f:
                saved_tokens = json.load(f)
                if token in saved_tokens:
                    logger.info(f"✓ Токен {token[:10]}... успешно сохранен в файл, всего в файле: {len(saved_tokens)}")
                else:
                    logger.error(f"✗ Токен {token[:10]}... НЕ найден в файле после сохранения! В файле: {list(saved_tokens.keys())[:3] if saved_tokens else 'нет'}")
        except Exception as e:
            logger.error(f"Ошибка проверки сохранения токена: {e}", exc_info=True)
    else:
        logger.error(f"Файл токенов не существует после сохранения: {AUTH_TOKENS_FILE}")
    
    logger.debug(f"Токен {token[:10]}... добавлен в хранилище, expires_at: {expires_at}")
    return token


def verify_auth_token(token):
    """Проверяет токен и возвращает данные пользователя"""
    if token not in auth_tokens:
        return None
    
    token_data = auth_tokens[token]
    
    # Проверяем срок действия
    if token_data['expires_at'] < time.time():
        del auth_tokens[token]
        save_auth_tokens()
        return None
    
    # Проверяем статус
    if token_data['status'] != 'authorized':
        return None
    
    return token_data.get('user_data')


def authorize_token(token, user_data):
    """Авторизует токен с данными пользователя"""
    global auth_tokens
    logger.info(f"Попытка авторизации токена {token[:10]}..., токенов в памяти: {len(auth_tokens)}")
    logger.info(f"Доступные токены: {list(auth_tokens.keys())[:3] if auth_tokens else 'нет'}")
    
    if token not in auth_tokens:
        # Попробуем перезагрузить токены из файла
        logger.warning(f"Токен {token[:10]}... не найден в памяти, перезагружаю из файла...")
        load_auth_tokens()
        logger.info(f"После перезагрузки токенов в памяти: {len(auth_tokens)}")
        
        if token not in auth_tokens:
            logger.error(f"Токен {token[:10]}... все еще не найден после перезагрузки")
            return False
    
    auth_tokens[token]['status'] = 'authorized'
    auth_tokens[token]['user_data'] = user_data
    auth_tokens[token]['authorized_at'] = time.time()
    save_auth_tokens()
    logger.info(f"Токен {token[:10]}... успешно авторизован")
    return True


# Загружаем токены при старте
load_auth_tokens()


def extract_text_from_url(url):
    """Извлекает текст статьи из URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Удаляем скрипты и стили
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Извлекаем текст из основных тегов
        text_parts = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'div']):
            text = tag.get_text(strip=True)
            if text and len(text) > 20:  # Игнорируем короткие фрагменты
                text_parts.append(text)
        
        article_text = '\n\n'.join(text_parts)
        
        if not article_text or len(article_text) < 100:
            # Если не удалось извлечь текст, пробуем получить весь текст страницы
            article_text = soup.get_text(separator='\n', strip=True)
        
        return article_text[:50000]  # Ограничиваем длину
    except Exception as e:
        logger.error(f"Ошибка извлечения текста из URL {url}: {e}")
        raise


def extract_image_from_url(url):
    """Извлекает изображение из статьи (og:image, article:image, или первое крупное изображение)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Приоритет 1: Open Graph изображение
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = og_image.get('content')
            # Если относительный URL, делаем абсолютным
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(url, image_url)
            logger.info(f"Найдено og:image: {image_url}")
            return image_url
        
        # Приоритет 2: article:image
        article_image = soup.find('meta', property='article:image')
        if article_image and article_image.get('content'):
            image_url = article_image.get('content')
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(url, image_url)
            logger.info(f"Найдено article:image: {image_url}")
            return image_url
        
        # Приоритет 3: Первое крупное изображение в статье
        images = soup.find_all('img')
        for img in images:
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if not src:
                continue
            
            # Пропускаем маленькие изображения (иконки, логотипы)
            width = img.get('width')
            height = img.get('height')
            if width and height:
                try:
                    if int(width) < 200 or int(height) < 200:
                        continue
                except (ValueError, TypeError):
                    pass
            
            # Пропускаем логотипы и иконки по классам/alt
            img_class = img.get('class', [])
            img_alt = (img.get('alt') or '').lower()
            if any(skip in str(img_class).lower() or skip in img_alt for skip in ['logo', 'icon', 'avatar', 'button']):
                continue
            
            # Делаем URL абсолютным
            if src.startswith('//'):
                image_url = 'https:' + src
            elif src.startswith('/'):
                image_url = urljoin(url, src)
            elif not src.startswith('http'):
                image_url = urljoin(url, src)
            else:
                image_url = src
            
            logger.info(f"Найдено изображение в статье: {image_url}")
            return image_url
        
        logger.warning(f"Изображение не найдено в статье: {url}")
        return None
    except Exception as e:
        logger.error(f"Ошибка извлечения изображения из URL {url}: {e}")
        return None


def extract_keywords_for_image_search(article_text, rewritten_text=None):
    """Извлекает ключевые слова из статьи для поиска изображения"""
    import re
    
    # Служебные слова, которые нужно пропускать
    stop_words = {
        'регистрация', 'пройдена', 'успешно', 'пожалуйста', 'перейдите', 'нажмите',
        'вход', 'войти', 'выход', 'выйти', 'далее', 'продолжить', 'отмена',
        'это', 'этот', 'эта', 'эти', 'такой', 'такая', 'такие',
        'быть', 'есть', 'был', 'была', 'было', 'были',
        'и', 'в', 'на', 'с', 'по', 'для', 'из', 'от', 'к', 'о', 'об', 'со', 'во',
        'как', 'что', 'где', 'когда', 'кто', 'куда', 'откуда',
        'не', 'нет', 'ни', 'без', 'про', 'при', 'над', 'под', 'за', 'перед'
    }
    
    # Пробуем извлечь заголовок (первая строка или строка с заглавными буквами)
    lines = article_text.split('\n')
    title_candidates = []
    
    for line in lines[:5]:  # Проверяем первые 5 строк
        line = line.strip()
        if len(line) > 10 and len(line) < 200:  # Разумная длина для заголовка
            # Если строка содержит много заглавных букв или короткая - вероятно заголовок
            if line[0].isupper() or len(line.split()) <= 10:
                title_candidates.append(line)
    
    # Используем первый подходящий заголовок или начало статьи
    text_to_analyze = title_candidates[0] if title_candidates else article_text
    
    # Если есть переписанный текст, используем его (он более структурирован)
    if rewritten_text:
        rewritten_lines = rewritten_text.split('\n')
        for line in rewritten_lines[:3]:
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                if line[0].isupper() or '**' in line:  # Markdown заголовки
                    text_to_analyze = line
                    break
    
    # Убираем markdown разметку и спецсимволы
    text_to_analyze = re.sub(r'\*\*|\*|#|`|\[|\]|\(|\)', '', text_to_analyze)
    text_to_analyze = re.sub(r'[^\w\s]', ' ', text_to_analyze)
    
    # Разбиваем на слова и фильтруем
    words = text_to_analyze.split()
    keywords = []
    
    for word in words:
        word_lower = word.lower().strip()
        # Пропускаем служебные слова, короткие слова и числа
        if (len(word_lower) > 3 and 
            word_lower not in stop_words and 
            not word_lower.isdigit() and
            word_lower.isalpha()):
            keywords.append(word_lower)
            if len(keywords) >= 5:  # Берем первые 5 ключевых слов
                break
    
    # Если не нашли ключевых слов, берем первые существительные из статьи
    if len(keywords) < 3:
        all_words = article_text.split()
        for word in all_words:
            word_lower = word.lower().strip()
            word_clean = re.sub(r'[^\w]', '', word_lower)
            if (len(word_clean) > 4 and 
                word_clean not in stop_words and 
                word_clean.isalpha()):
                keywords.append(word_clean)
                if len(keywords) >= 5:
                    break
    
    # Если все еще нет ключевых слов, используем первые слова статьи
    if len(keywords) < 2:
        words = article_text.split()[:10]
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word.lower().strip())
            if len(word_clean) > 3 and word_clean.isalpha():
                keywords.append(word_clean)
                if len(keywords) >= 3:
                    break
    
    result = ' '.join(keywords[:5])  # Максимум 5 ключевых слов
    return result if result else 'news article'  # Fallback


def search_image_from_pexels(query, api_key=None):
    """Ищет изображение через Pexels API"""
    if not api_key:
        api_key = os.getenv('PEXELS_API_KEY')
    
    if not api_key:
        logger.warning("PEXELS_API_KEY не настроен, пропускаем поиск через Pexels")
        return None
    
    try:
        # Используем весь запрос (уже обработанный функцией extract_keywords_for_image_search)
        # Ограничиваем до 5 слов для лучших результатов
        keywords = query.split()[:5]
        search_query = ' '.join(keywords)
        
        logger.info(f"Поиск в Pexels по запросу: {search_query}")
        
        headers = {
            'Authorization': api_key
        }
        params = {
            'query': search_query,
            'per_page': 1,
            'orientation': 'landscape'
        }
        
        response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('photos') and len(data['photos']) > 0:
            photo = data['photos'][0]
            image_url = photo.get('src', {}).get('large') or photo.get('src', {}).get('original')
            logger.info(f"Найдено изображение через Pexels: {image_url}")
            return image_url
        
        logger.warning(f"Изображение не найдено через Pexels для запроса: {search_query}")
        return None
    except Exception as e:
        logger.error(f"Ошибка поиска изображения через Pexels: {e}")
        return None


def search_image_from_unsplash(query):
    """Ищет изображение через Unsplash Source API (бесплатный вариант без ключа)"""
    try:
        # Используем весь запрос (уже обработанный функцией extract_keywords_for_image_search)
        # Ограничиваем до 5 слов
        keywords = query.split()[:5]
        search_query = ' '.join(keywords)
        
        # Unsplash Source API - генерирует случайное изображение по ключевым словам
        # Формат: https://source.unsplash.com/1600x900/?keyword1,keyword2
        # Убираем спецсимволы и оставляем только буквы и цифры
        import re
        clean_query = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', search_query)
        search_terms = clean_query.replace(' ', ',').lower()[:50]  # Ограничиваем длину
        
        if not search_terms:
            logger.warning("Не удалось извлечь ключевые слова для Unsplash")
            return None
        
        url = f"https://source.unsplash.com/1600x900/?{search_terms}"
        
        # Проверяем, что URL доступен (HEAD запрос для проверки)
        response = requests.head(url, timeout=15, allow_redirects=True)
        final_url = response.url if hasattr(response, 'url') else url
        
        # Если получили редирект на изображение, значит оно доступно
        if response.status_code in [200, 301, 302] and ('unsplash' in final_url or 'images.unsplash.com' in final_url):
            logger.info(f"Найдено изображение через Unsplash: {final_url}")
            return final_url
        
        return None
    except Exception as e:
        logger.error(f"Ошибка поиска изображения через Unsplash: {e}")
        return None


def generate_image_with_kandinsky(prompt, api_key=None, project_id=None):
    """Генерирует изображение через Kandinsky (Yandex Cloud)"""
    if not api_key:
        api_key = YANDEX_CLOUD_API_KEY
    if not project_id:
        project_id = YANDEX_CLOUD_PROJECT
    
    if not api_key:
        logger.warning("YANDEX_CLOUD_API_KEY не настроен, пропускаем генерацию через Kandinsky")
        return None
    
    try:
        # Используем Yandex Cloud Foundation Models API для генерации изображений
        # Kandinsky доступен через этот API
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGeneration"
        
        headers = {
            'Authorization': f'Api-Key {api_key}',
            'Content-Type': 'application/json',
            'x-folder-id': project_id
        }
        
        # Упрощаем промпт для генерации (первые 30 слов для лучшего качества)
        simple_prompt = ' '.join(prompt.split()[:30])
        
        # Формируем промпт для генерации изображения
        image_prompt = f"Изображение на тему: {simple_prompt}"
        
        payload = {
            'model': 'kandinsky',
            'prompt': image_prompt,
            'width': 1024,
            'height': 1024,
            'num_images': 1
        }
        
        logger.info(f"Попытка генерации изображения через Kandinsky с промптом: {image_prompt[:50]}...")
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        
        logger.info(f"Kandinsky API ответил со статусом: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # В зависимости от формата ответа API
            image_url = data.get('imageUrl') or data.get('url') or data.get('image') or data.get('result', {}).get('imageUrl')
            if image_url:
                logger.info(f"Изображение сгенерировано через Kandinsky: {image_url}")
                return image_url
            else:
                logger.warning(f"Kandinsky вернул успешный ответ, но без URL изображения. Ответ: {data}")
        
        # Если endpoint не найден, возможно используется другой API или недоступен в тарифе
        if response.status_code == 404:
            logger.warning("Kandinsky endpoint не найден (404). Генерация изображений может быть недоступна в вашем тарифе Yandex Cloud.")
            logger.info("Рекомендуется использовать оригинальное изображение или изображение из Pexels/Unsplash")
        
        logger.warning(f"Не удалось сгенерировать изображение через Kandinsky. Статус: {response.status_code}, ответ: {response.text[:300]}")
        return None
    except Exception as e:
        logger.error(f"Ошибка генерации изображения через Kandinsky: {e}", exc_info=True)
        return None


def rewrite_article_with_yandex(article_text, style):
    """Обрабатывает статью через Yandex Cloud API"""
    if not yandex_client:
        raise ValueError("Yandex Cloud API не настроен")
    
    style_prompts = {
        'scientific': 'Перепиши статью в научно-деловом стиле, сохраняя основную информацию и факты.',
        'meme': 'Перепиши статью в мемном стиле, сделай её более развлекательной и юмористической.',
        'casual': 'Перепиши статью в повседневном стиле, сделай её более простой и понятной для широкой аудитории.'
    }
    
    prompt = style_prompts.get(style, style_prompts['casual'])
    full_prompt = f"{prompt}\n\nТекст статьи:\n{article_text}"
    
    try:
        response = yandex_client.responses.create(
            prompt={
                "id": YANDEX_CLOUD_ASSISTANT_ID,
            },
            input=full_prompt,
        )
        
        result_text = response.output_text
        
        # Очищаем результат от упоминаний Pexels, Unsplash и других технических терминов
        # которые могут случайно попасть в текст
        import re
        # Убираем упоминания о Pexels, Unsplash, API и других технических терминах
        unwanted_patterns = [
            r'\bpexels\b',
            r'\bPexels\b',
            r'\bPEXELS\b',
            r'\bunsplash\b',
            r'\bUnsplash\b',
            r'\bUNSPLASH\b',
            r'\bapi\s+ключ\b',
            r'\bAPI\s+ключ\b',
            r'\bизображение\s+из\s+pexels\b',
            r'\bизображение\s+из\s+unsplash\b',
            r'\bфото\s+из\s+pexels\b',
            r'\bфото\s+из\s+unsplash\b',
        ]
        
        for pattern in unwanted_patterns:
            result_text = re.sub(pattern, '', result_text, flags=re.IGNORECASE)
        
        # Убираем лишние пробелы и переносы строк
        result_text = re.sub(r'\s+', ' ', result_text)
        result_text = re.sub(r'\n\s*\n', '\n\n', result_text)
        result_text = result_text.strip()
        
        return result_text
    except Exception as e:
        logger.error(f"Ошибка обработки статьи через Yandex Cloud API: {e}", exc_info=True)
        raise
        raise


@app.route('/api/rewrite-article', methods=['POST', 'OPTIONS'])
def rewrite_article():
    """Обрабатывает статью: получает текст по URL и рерайтит через Yandex Cloud"""
    if request.method == 'OPTIONS':
        # flask-cors автоматически обработает OPTIONS запрос
        return '', 200
    
    if not yandex_client:
        return jsonify({
            'success': False,
            'error': 'Yandex Cloud API не настроен. Проверьте YANDEX_CLOUD_API_KEY в переменных окружения.'
        }), 503
    
    try:
        data = request.json
        url = data.get('url')
        style = data.get('style')
        
        if not url:
            return jsonify({'success': False, 'error': 'URL статьи не указан'}), 400
        
        if not style:
            return jsonify({'success': False, 'error': 'Стиль рерайта не указан'}), 400
        
        logger.info(f"Начало обработки статьи: URL={url}, стиль={style}")
        
        # Извлекаем текст статьи
        article_text = extract_text_from_url(url)
        logger.info(f"Текст статьи извлечен, длина: {len(article_text)} символов")
        
        # Обрабатываем через Yandex Cloud
        rewritten_text = rewrite_article_with_yandex(article_text, style)
        logger.info(f"Статья обработана, длина результата: {len(rewritten_text)} символов")
        
        # Получаем три варианта изображений
        logger.info("Начинаем получение изображений...")
        
        # 1. Изображение из оригинальной статьи
        logger.info("Извлечение изображения из оригинальной статьи...")
        original_image = extract_image_from_url(url)
        logger.info(f"Оригинальное изображение: {'найдено' if original_image else 'не найдено'}")
        
        # 2. Поиск через Pexels API или Unsplash
        # Извлекаем ключевые слова из статьи (пропускаем служебные слова в начале)
        search_query = extract_keywords_for_image_search(article_text, rewritten_text)
        logger.info(f"Поиск изображения через API для запроса: {search_query[:50]}...")
        
        pexels_image = search_image_from_pexels(search_query)
        if not pexels_image:
            # Если Pexels не сработал, пробуем Unsplash
            logger.info("Pexels не вернул изображение, пробуем Unsplash...")
            pexels_image = search_image_from_unsplash(search_query)
            if pexels_image:
                logger.info("Найдено изображение через Unsplash")
        
        logger.info(f"Изображение из API: {'найдено' if pexels_image else 'не найдено'}")
        
        # 3. Генерация через Kandinsky (используем начало статьи как промпт)
        generation_prompt = ' '.join(rewritten_text.split()[:30])  # Первые 30 слов переписанной статьи
        logger.info(f"Генерация изображения через Kandinsky с промптом: {generation_prompt[:50]}...")
        generated_image = generate_image_with_kandinsky(generation_prompt)
        logger.info(f"Сгенерированное изображение: {'получено' if generated_image else 'не получено'}")
        
        images = {
            'original': original_image,
            'pexels': pexels_image,
            'generated': generated_image
        }
        
        logger.info(f"Итоговые изображения: original={bool(original_image)}, pexels={bool(pexels_image)}, generated={bool(generated_image)}")
        
        return jsonify({
            'success': True,
            'original_text': article_text[:1000] + '...' if len(article_text) > 1000 else article_text,
            'rewritten_text': rewritten_text,
            'url': url,
            'style': style,
            'images': images
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка обработки статьи: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/send-article', methods=['POST'])
def send_article():
    """Отправляет статью в каналы через Telegram Bot API"""
    if not AIOGRAM_AVAILABLE:
        return jsonify({
            'success': False, 
            'error': 'aiogram не установлен. Установите зависимости: pip install -r requirements.txt'
        }), 503
    
    try:
        data = request.json
        article_text = data.get('article_text', '')
        image_url = data.get('image_url')  # URL выбранного изображения
        selected_channels = data.get('channels', [])  # Список ID каналов для отправки
        
        if not article_text.strip():
            return jsonify({'success': False, 'error': 'Текст статьи не может быть пустым'}), 400
        
        # Загружаем каналы
        all_channels = load_channels()
        
        # Если указаны конкретные каналы, используем их, иначе все
        if selected_channels:
            channels_to_send = [ch for ch in all_channels if ch['id'] in selected_channels]
        else:
            channels_to_send = all_channels
        
        if not channels_to_send:
            return jsonify({'success': False, 'error': 'Каналы не настроены'}), 400
        
        success_count = 0
        failed_channels = []
        
        # Асинхронная функция для отправки сообщений
        async def send_messages():
            nonlocal success_count, failed_channels
            # Создаём новый экземпляр Bot для этого запроса
            current_bot = Bot(token=BOT_TOKEN)
            try:
                for channel in channels_to_send:
                    try:
                        # Отправляем сообщение с изображением, если оно есть
                        if image_url and image_url.strip():
                            try:
                                # Telegram может принимать URL напрямую, но лучше проверить
                                # Если URL не работает, можно скачать изображение и отправить как файл
                                logger.info(f"Попытка отправить изображение {image_url[:50]}... в канал {channel['name']}")
                                
                                await current_bot.send_photo(
                                    chat_id=channel['id'],
                                    photo=image_url,
                                    caption=article_text[:1024],  # Ограничиваем длину подписи (макс 1024 символа)
                                    parse_mode='HTML'
                                )
                                logger.info(f"✅ Статья с изображением отправлена в канал: {channel['name']} ({channel['id']})")
                            except Exception as photo_error:
                                # Если не удалось отправить с фото, пробуем скачать и отправить как файл
                                logger.warning(f"Не удалось отправить фото по URL в {channel['name']}: {photo_error}")
                                try:
                                    # Пробуем скачать изображение и отправить как файл
                                    import aiohttp
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                                            if resp.status == 200:
                                                image_data = await resp.read()
                                                from io import BytesIO
                                                photo_file = BytesIO(image_data)
                                                photo_file.name = 'image.jpg'
                                                
                                                await current_bot.send_photo(
                                                    chat_id=channel['id'],
                                                    photo=photo_file,
                                                    caption=article_text[:1024],
                                                    parse_mode='HTML'
                                                )
                                                logger.info(f"✅ Статья с изображением (скачанным) отправлена в канал: {channel['name']}")
                                            else:
                                                raise Exception(f"Не удалось скачать изображение: статус {resp.status}")
                                except Exception as download_error:
                                    # Если и скачивание не помогло, отправляем только текст
                                    logger.warning(f"Не удалось отправить фото (скачивание тоже не помогло) в {channel['name']}: {download_error}, отправляем только текст")
                                    await current_bot.send_message(
                                        chat_id=channel['id'],
                                        text=article_text,
                                        parse_mode='HTML'
                                    )
                        else:
                            await current_bot.send_message(
                                chat_id=channel['id'],
                                text=article_text,
                                parse_mode='HTML'
                            )
                        success_count += 1
                        logger.info(f"Статья отправлена в канал: {channel['name']} ({channel['id']})")
                    except TelegramAPIError as e:
                        error_msg = str(e)
                        failed_channels.append({
                            'channel': channel['name'],
                            'error': error_msg
                        })
                        logger.error(f"Ошибка отправки в канал {channel['name']}: {error_msg}")
                    except Exception as e:
                        failed_channels.append({
                            'channel': channel.get('name', channel['id']),
                            'error': str(e)
                        })
                        logger.error(f"Ошибка отправки в канал {channel['id']}: {e}")
            finally:
                # Закрываем сессию бота после отправки
                await current_bot.session.close()
        
        # Запускаем асинхронную функцию
        # Всегда создаём новый event loop для каждого запроса
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(send_messages())
        except Exception as e:
            logger.error(f"Ошибка работы с event loop: {e}")
            raise
        finally:
            # Закрываем loop после использования
            try:
                # Отменяем все незавершённые задачи
                pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
                for task in pending:
                    task.cancel()
                # Ждём отмены задач
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                pass
            finally:
                if not loop.is_closed():
                    loop.close()
        
        return jsonify({
            'success': True,
            'sent': success_count,
            'total': len(channels_to_send),
            'failed': failed_channels
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/channels', methods=['GET'])
def get_channels():
    """Возвращает список доступных каналов"""
    try:
        channels = load_channels()
        return jsonify({
            'success': True,
            'channels': channels
        }), 200
    except Exception as e:
        logger.error(f"Ошибка получения каналов: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Проверка работоспособности сервера"""
    return jsonify({'status': 'ok'}), 200


@app.route('/api/auth/generate-token', methods=['POST', 'OPTIONS'])
def generate_token():
    """Генерирует новый токен для авторизации через бота"""
    if request.method == 'OPTIONS':
        # flask-cors автоматически обработает OPTIONS запрос
        logger.info("OPTIONS запрос обработан для /api/auth/generate-token")
        return '', 200
    
    try:
        # Не требуем JSON в теле запроса - это просто POST без данных
        token = generate_auth_token()
        logger.info(f"Сгенерирован новый токен: {token[:10]}..., всего токенов в памяти: {len(auth_tokens)}")
        logger.info(f"Токен сохранен в файл: {AUTH_TOKENS_FILE}")
        return jsonify({
            'success': True,
            'token': token,
            'expires_in': 300  # секунд
        }), 200
    except Exception as e:
        logger.error(f"Ошибка генерации токена: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/verify-token', methods=['POST', 'OPTIONS'])
def verify_token():
    """Проверяет токен и возвращает данные пользователя"""
    if request.method == 'OPTIONS':
        # flask-cors автоматически обработает OPTIONS запрос
        return '', 200
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'error': 'Токен не предоставлен'}), 400
        
        user_data = verify_auth_token(token)
        
        if user_data:
            return jsonify({
                'success': True,
                'authorized': True,
                'user': user_data
            }), 200
        else:
            return jsonify({
                'success': True,
                'authorized': False,
                'message': 'Токен не найден или не авторизован'
            }), 200
            
    except Exception as e:
        logger.error(f"Ошибка проверки токена: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/authorize', methods=['POST', 'OPTIONS'])
def authorize():
    """Авторизует токен с данными пользователя (вызывается ботом)"""
    if request.method == 'OPTIONS':
        # flask-cors автоматически обработает OPTIONS запрос
        logger.info("OPTIONS запрос обработан для /api/auth/authorize")
        return '', 200
    
    try:
        # Всегда загружаем токены из файла перед проверкой
        load_auth_tokens()
        
        data = request.json
        token = data.get('token')
        user_data = data.get('user_data')
        
        logger.info(f"Получен запрос на авторизацию токена: {token[:10] if token else 'None'}...")
        logger.info(f"Данные пользователя: {user_data}")
        logger.info(f"Токенов в памяти после загрузки: {len(auth_tokens)}")
        logger.info(f"Доступные токены (первые 3): {list(auth_tokens.keys())[:3] if auth_tokens else 'нет'}")
        
        if not token or not user_data:
            logger.warning("Недостаточно данных для авторизации")
            return jsonify({'success': False, 'error': 'Недостаточно данных'}), 400
        
        if authorize_token(token, user_data):
            logger.info(f"Токен {token[:10]}... успешно авторизован для пользователя {user_data.get('id')}")
            return jsonify({'success': True}), 200
        else:
            logger.warning(f"Токен {token[:10]}... не найден или истек")
            return jsonify({'success': False, 'error': 'Токен не найден или истек'}), 404
            
    except Exception as e:
        logger.error(f"Ошибка авторизации токена: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

