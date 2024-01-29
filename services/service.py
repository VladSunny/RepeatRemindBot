from __future__ import annotations

import asyncio
import os

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, Message

# Загружаем конфиг в переменную config
from config_data.config import Config, load_config

config: Config = load_config()


PHOTOS_FOLDER = 'photos'
VOICES_FOLDER = 'voices'

os.makedirs(PHOTOS_FOLDER, exist_ok=True)


bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')


# Отправить сообщение на время
async def send_and_delete_message(chat_id: int, text: str, delete_after: int):
    # Отправляем сообщение
    message = await bot.send_message(chat_id, text)

    # Ожидаем указанное количество секунд
    await asyncio.sleep(delete_after)

    # Удаляем сообщение
    await bot.delete_message(chat_id, message.message_id)


# Скачать файл
async def download_photo(file_id) -> str:
    # Получаем объект файла
    file = await bot.get_file(file_id)

    # Составляем путь для сохранения файла
    file_path = os.path.join(PHOTOS_FOLDER, f"{file_id}.jpg")

    # Скачиваем фотографию используя метод download_file
    await bot.download_file(file_path=file.file_path, destination=file_path)

    return file_path


async def download_voice(file_id) -> str:
    # Получаем объект файла
    file = await bot.get_file(file_id)

    # Составляем путь для сохранения файла
    file_path = os.path.join(VOICES_FOLDER, f"{file_id}.WAV")

    # Скачиваем фотографию используя метод download_file
    await bot.download_file(file_path=file.file_path, destination=file_path)

    return file_path
