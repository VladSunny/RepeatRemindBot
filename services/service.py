from __future__ import annotations
#
from aiogram import Bot
from icecream import ic
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message
#
# Bot = bot.bot

# Загружаем конфиг в переменную config
from config_data.config import Config, load_config

config: Config = load_config()

bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')


async def send_message(chat_id: int, text: str, reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None)\
        -> Message:
    message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    return message


async def delete_message(chat_id: int, message_id: int):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


async def send_and_delete_message(chat_id: int, text: str, delete_after: int):
    # Отправляем сообщение
    message = await bot.send_message(chat_id, text)

    # Ожидаем указанное количество секунд
    await asyncio.sleep(delete_after)

    # Удаляем сообщение
    await bot.delete_message(chat_id, message.message_id)


async def change_message(chat_id: int, message_id: int,
                         reply_markup: InlineKeyboardMarkup | None | int = None,
                         text: str | None = None,
                         can_repeat: bool = False):
    if text is not None:
        if can_repeat:
            await bot.edit_message_text(text="...", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
    else:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
