import os
import json
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Загрузка переменных окружения
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, 'Backend')

# Список возможных путей к файлам с переменными окружения
env_paths = [
    os.path.join(BASE_DIR, '.env'),                    # Корень проекта
    os.path.join(BACKEND_DIR, 'BOT_TOKEN.env'),       # Папка Backend
    os.path.join(BASE_DIR, 'BOT_TOKEN.env'),          # Корень проекта
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

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Логируем путь к загруженному файлу
if env_path:
    logger.info(f"Загружен файл переменных окружения: {env_path}")

# Инициализация бота и диспетчера
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error(f"BOT_TOKEN не найден. Проверенные пути: {env_paths}")
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Файл для хранения каналов
CHANNELS_FILE = os.path.join(BASE_DIR, "TelegramBot", "channels.json")

# URL API бэкенда
API_URL = os.getenv('API_URL', 'http://localhost:5000')


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


def save_channels(channels):
    """Сохраняет список каналов в файл"""
    try:
        with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'channels': channels}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения каналов: {e}")
        return False


def add_channel(channel_id, channel_name=None):
    """Добавляет канал в список"""
    channels = load_channels()
    channel_info = {
        'id': str(channel_id),
        'name': channel_name or str(channel_id)
    }
    
    # Проверяем, нет ли уже такого канала
    if any(ch['id'] == str(channel_id) for ch in channels):
        return False, "Канал уже добавлен"
    
    channels.append(channel_info)
    if save_channels(channels):
        return True, "Канал успешно добавлен"
    return False, "Ошибка сохранения"


def remove_channel(channel_id):
    """Удаляет канал из списка"""
    channels = load_channels()
    channels = [ch for ch in channels if ch['id'] != str(channel_id)]
    if save_channels(channels):
        return True, "Канал успешно удален"
    return False, "Ошибка сохранения"


# Состояния FSM
class ChannelManagement(StatesGroup):
    waiting_for_channel = State()


async def authorize_user(token: str, user: types.User):
    """Отправляет запрос на авторизацию пользователя через API"""
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'is_bot': user.is_bot,
        'language_code': user.language_code
    }
    
    logger.info(f"Попытка авторизации пользователя {user.id} с токеном {token[:10]}...")
    logger.info(f"API URL: {API_URL}/api/auth/authorize")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{API_URL}/api/auth/authorize',
                json={
                    'token': token,
                    'user_data': user_data
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response_text = await response.text()
                logger.info(f"Ответ API: статус {response.status}, тело: {response_text}")
                
                if response.status == 200:
                    try:
                        result = await response.json()
                        success = result.get('success', False)
                        logger.info(f"Результат авторизации: {success}")
                        return success
                    except Exception as e:
                        logger.error(f"Ошибка парсинга JSON ответа: {e}, тело: {response_text}")
                        return False
                else:
                    logger.error(f"Ошибка авторизации: статус {response.status}, тело: {response_text}")
                    return False
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка подключения к API: {e}")
        return False
    except Exception as e:
        logger.error(f"Неожиданная ошибка при авторизации: {e}", exc_info=True)
        return False


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start с поддержкой deep link"""
    logger.info("=" * 60)
    logger.info(f"📨 Получена команда /start")
    logger.info(f"   Пользователь: {message.from_user.id} (@{message.from_user.username})")
    logger.info(f"   Имя: {message.from_user.first_name}")
    logger.info(f"   Текст сообщения: {message.text}")
    logger.info("=" * 60)
    
    # Проверяем, есть ли токен в аргументах команды
    args = message.text.split()[1:] if message.text and len(message.text.split()) > 1 else []
    
    # Если есть аргумент (токен из deep link)
    if args:
        token = args[0]
        logger.info(f"🔑 Получен токен авторизации: {token[:10]}...{token[-5:]} от пользователя {message.from_user.id}")
        
        # Показываем кнопку авторизации
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Авторизоваться на сайте",
                    callback_data=f"auth_{token}"
                )
            ]
        ])
        
        try:
            await message.answer(
                "🔐 <b>Авторизация на сайте Phoenix Lab</b>\n\n"
                "Нажмите кнопку ниже, чтобы авторизоваться на сайте.\n"
                "Токен действителен в течение 5 минут.",
                parse_mode="HTML",
                reply_markup=keyboard
            )
            logger.info(f"✅ Сообщение с кнопкой авторизации отправлено пользователю {message.from_user.id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки сообщения: {e}")
    else:
        # Обычный старт
        logger.info(f"📝 Обычная команда /start без токена от пользователя {message.from_user.id}")
        try:
            await message.answer(
                "🔥 <b>Phoenix Lab</b> - Управление каналами\n\n"
                "Используйте команды:\n"
                "/channels - Список каналов\n"
                "/add_channel - Добавить канал\n"
                "/help - Помощь",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"❌ Ошибка отправки сообщения: {e}")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Помощь по командам"""
    await message.answer(
        "📋 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу\n"
        "/channels - Показать список каналов\n"
        "/add_channel - Добавить новый канал\n"
        "/cancel - Отменить текущую операцию\n\n"
        "<b>Как добавить канал:</b>\n"
        "1. Добавьте бота в канал как администратора\n"
        "2. Используйте /add_channel\n"
        "3. Перешлите сообщение из канала",
        parse_mode="HTML"
    )


@dp.message(Command("channels"))
async def cmd_channels(message: types.Message):
    """Показывает список каналов для рассылки"""
    channels = load_channels()
    
    if not channels:
        await message.answer(
            "❌ Каналы не настроены.\n\n"
            "Используйте команду /add_channel для добавления канала."
        )
        return
    
    # Создаем клавиатуру с кнопками удаления
    keyboard_buttons = []
    channels_text = "📢 <b>Каналы для рассылки:</b>\n\n"
    
    for i, channel in enumerate(channels):
        channels_text += f"{i+1}. {channel['name']} (<code>{channel['id']}</code>)\n"
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"❌ Удалить {channel['name']}",
                callback_data=f"remove_channel_{channel['id']}"
            )
        ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(
        channels_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


@dp.message(Command("add_channel"))
async def cmd_add_channel(message: types.Message, state: FSMContext):
    """Начинает процесс добавления канала"""
    await message.answer(
        "📝 <b>Добавление канала:</b>\n\n"
        "1. Перешлите сообщение из канала, куда добавлен бот\n"
        "2. Или отправьте ID канала (например: -1001234567890)\n\n"
        "Используйте /cancel для отмены.",
        parse_mode="HTML"
    )
    await state.set_state(ChannelManagement.waiting_for_channel)


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Отменяет текущую операцию"""
    await state.clear()
    await message.answer("❌ Операция отменена.")


@dp.message(ChannelManagement.waiting_for_channel)
async def process_channel(message: types.Message, state: FSMContext):
    """Обрабатывает добавление канала"""
    channel_id = None
    channel_name = None
    
    # Если это пересланное сообщение из канала
    if message.forward_from_chat:
        channel_id = str(message.forward_from_chat.id)
        channel_name = message.forward_from_chat.title or message.forward_from_chat.username or channel_id
    # Если это просто текст с ID
    elif message.text:
        text = message.text.strip()
        # Проверяем, похоже ли на ID канала (начинается с -100)
        if text.startswith('-100') and text[1:].replace('-', '').isdigit():
            channel_id = text
            channel_name = text
        else:
            await message.answer(
                "❌ Неверный формат ID канала.\n"
                "ID канала должен начинаться с -100 и содержать только цифры.\n"
                "Пример: -1001234567890\n\n"
                "Или перешлите сообщение из канала."
            )
            return
    
    if not channel_id:
        await message.answer("❌ Не удалось определить канал. Попробуйте ещё раз.")
        return
    
    # Пытаемся получить информацию о канале
    try:
        chat = await bot.get_chat(channel_id)
        channel_name = chat.title or chat.username or channel_id
    except Exception as e:
        logger.warning(f"Не удалось получить информацию о канале {channel_id}: {e}")
        await message.answer(
            "⚠️ Не удалось получить информацию о канале.\n"
            "Убедитесь, что бот добавлен в канал как администратор."
        )
    
    # Добавляем канал
    success, msg = add_channel(channel_id, channel_name)
    
    if success:
        await message.answer(
            f"✅ {msg}\n\n"
            f"📢 Канал: {channel_name}\n"
            f"🆔 ID: <code>{channel_id}</code>",
            parse_mode="HTML"
        )
    else:
        await message.answer(f"❌ {msg}")
    
    await state.clear()




@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    """Обработчик всех callback запросов"""
    logger.info("=" * 60)
    logger.info(f"🔘 Получен callback запрос")
    logger.info(f"   Пользователь: {callback.from_user.id} (@{callback.from_user.username})")
    logger.info(f"   Данные: {callback.data}")
    logger.info("=" * 60)
    
    if callback.data.startswith("auth_"):
        """Обрабатывает нажатие кнопки авторизации"""
        token = callback.data.replace("auth_", "")
        user = callback.from_user
        
        logger.info(f"Обработка авторизации для пользователя {user.id} с токеном {token[:10]}...")
        
        try:
            await callback.answer("Обработка авторизации...")
        except Exception as e:
            logger.warning(f"Ошибка при ответе на callback: {e}")
        
        # Отправляем запрос на авторизацию
        success = await authorize_user(token, user)
        
        if success:
            logger.info(f"Авторизация успешна для пользователя {user.id}")
            try:
                await callback.message.edit_text(
                    "✅ <b>Авторизация успешна!</b>\n\n"
                    "Вы успешно авторизованы на сайте Phoenix Lab.\n"
                    "Вернитесь на сайт и обновите страницу.",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Ошибка при редактировании сообщения: {e}")
                await callback.message.answer(
                    "✅ <b>Авторизация успешна!</b>\n\n"
                    "Вы успешно авторизованы на сайте Phoenix Lab.\n"
                    "Вернитесь на сайт и обновите страницу.",
                    parse_mode="HTML"
                )
        else:
            logger.warning(f"Авторизация не удалась для пользователя {user.id}")
            try:
                await callback.message.edit_text(
                    "❌ <b>Ошибка авторизации</b>\n\n"
                    "Не удалось авторизоваться. Возможные причины:\n"
                    "• Токен истек (действителен 5 минут)\n"
                    "• Ошибка связи с сервером\n\n"
                    "Попробуйте получить новую ссылку на сайте.",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Ошибка при редактировании сообщения: {e}")
                await callback.message.answer(
                    "❌ <b>Ошибка авторизации</b>\n\n"
                    "Не удалось авторизоваться. Возможные причины:\n"
                    "• Токен истек (действителен 5 минут)\n"
                    "• Ошибка связи с сервером\n\n"
                    "Попробуйте получить новую ссылку на сайте.",
                    parse_mode="HTML"
                )
    elif callback.data.startswith("remove_channel_"):
        """Удаляет канал по callback"""
        channel_id = callback.data.replace("remove_channel_", "")
        
        channels = load_channels()
        channel_name = next((ch['name'] for ch in channels if ch['id'] == channel_id), channel_id)
        
        success, msg = remove_channel(channel_id)
        
        if success:
            await callback.answer(f"Канал {channel_name} удален")
            await callback.message.edit_text(
                f"✅ Канал <b>{channel_name}</b> удален из списка.",
                parse_mode="HTML"
            )
        else:
            await callback.answer(f"Ошибка: {msg}")


@dp.message()
async def handle_other_messages(message: types.Message, state: FSMContext):
    """Обработка прочих сообщений"""
    logger.info(f"Получено сообщение от пользователя {message.from_user.id}: {message.text[:50] if message.text else 'не текст'}")
    
    current_state = await state.get_state()
    if current_state == ChannelManagement.waiting_for_channel:
        await process_channel(message, state)
    else:
        # Проверяем, не является ли это сообщением с токеном (на случай, если пользователь просто отправил токен)
        if message.text and len(message.text) > 20 and not message.text.startswith('/'):
            # Возможно, это токен, отправленный напрямую
            logger.info(f"Возможно, получен токен напрямую: {message.text[:10]}...")
            token = message.text.strip()
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Авторизоваться на сайте",
                        callback_data=f"auth_{token}"
                    )
                ]
            ])
            
            await message.answer(
                "🔐 <b>Авторизация на сайте Phoenix Lab</b>\n\n"
                "Нажмите кнопку ниже, чтобы авторизоваться на сайте.\n"
                "Токен действителен в течение 5 минут.",
                parse_mode="HTML",
                reply_markup=keyboard
            )
        else:
            await message.answer(
                "👋 Используйте команды:\n"
                "/start - Начать работу\n"
                "/channels - Список каналов\n"
                "/add_channel - Добавить канал\n"
                "/help - Помощь\n"
                "/cancel - Отменить операцию"
            )


async def main():
    """Запуск бота"""
    try:
        logger.info("=" * 50)
        logger.info("Запуск бота Phoenix Lab...")
        logger.info(f"Токен бота: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
        logger.info(f"API URL: {API_URL}")
        logger.info(f"Загружен файл переменных окружения: {env_path}")
        channels = load_channels()
        logger.info(f"Настроено каналов: {len(channels)}")
        if channels:
            logger.info(f"Каналы: {', '.join([ch['name'] for ch in channels])}")
        logger.info("Бот готов к работе. Ожидание сообщений...")
        logger.info("=" * 50)
        
        # Пробуем подключиться с повторными попытками
        max_retries = 5
        retry_delay = 10  # секунд
        
        for attempt in range(max_retries):
            try:
                # Запускаем polling со всеми типами обновлений
                await dp.start_polling(
                    bot, 
                    allowed_updates=["message", "callback_query", "edited_message"],
                    drop_pending_updates=True  # Пропускаем старые обновления при запуске
                )
                break  # Если успешно, выходим из цикла
            except Exception as e:
                if "Cannot connect to host" in str(e) or "SSL handshake" in str(e) or "TelegramNetworkError" in str(type(e).__name__):
                    if attempt < max_retries - 1:
                        logger.warning(f"Ошибка подключения к Telegram API (попытка {attempt + 1}/{max_retries}): {e}")
                        logger.info(f"Повторная попытка через {retry_delay} секунд...")
                        await asyncio.sleep(retry_delay)
                    else:
                        logger.error(f"Не удалось подключиться к Telegram API после {max_retries} попыток")
                        logger.error("Возможные причины:")
                        logger.error("1. Проблемы с интернет-соединением")
                        logger.error("2. Telegram заблокирован в вашем регионе (нужен VPN/прокси)")
                        logger.error("3. Проблемы с SSL сертификатами")
                        raise
                else:
                    # Другие ошибки - пробрасываем сразу
                    raise
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

