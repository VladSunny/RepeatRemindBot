from abc import ABC
from typing import Callable, Dict, Any, Awaitable

from aiogram import types, Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from aiocache import SimpleMemoryCache
import time

from icecream import ic

# Загружаем конфиг в переменную config
from config_data.config import Config, load_config

config: Config = load_config()

# Инициализируем бот и диспетчер
bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')


# Класс для обработки апдейтов и предотвращения спама
class AntiFloodMiddleware(BaseMiddleware, ABC):

    def __init__(self, limit=5, interval=5):  # Интервал в секундах
        self.limit = limit
        self.interval = interval
        self.cache = SimpleMemoryCache()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = message.from_user.id
        current_time = time.time()

        # Получаем список временных меток сообщений для пользователя
        user_messages = await self.cache.get(user_id) or []

        # Отфильтровываем временные метки, чтобы оставить только актуальные
        user_messages = [msg_time for msg_time in user_messages if current_time - msg_time < self.interval]

        if len(user_messages) >= self.limit:
            # Пользователь превысил лимит, блокируем его
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            raise RuntimeError("AntiFlood limit exceeded")
        else:
            # Добавляем текущее время к списку и сохраняем в кэше
            user_messages.append(current_time)
            await self.cache.set(user_id, user_messages, ttl=self.interval)
            return await handler(message, data)

