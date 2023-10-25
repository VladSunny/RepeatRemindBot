from icecream import ic
import asyncio
import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

Bot = bot.bot


async def send_and_delete_message(chat_id: int, text: str, delete_after: int):
    # Отправляем сообщение
    message = await bot.bot.send_message(chat_id, text)

    # Ожидаем указанное количество секунд
    await asyncio.sleep(delete_after)

    # Удаляем сообщение
    await Bot.delete_message(chat_id, message.message_id)


async def change_reply_markup(chat_id: int, message_id: int, reply_markup: InlineKeyboardMarkup):
    await Bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
