from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import *

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON

router = Router()


@router.message(lambda message: message.from_user.id not in get_users())
async def unregistered_user(message: Message):
    await message.answer(LEXICON['/start']['en'])
    add_user(message.from_user.id)


@router.message(lambda message: not is_user_updated(message.from_user.id))
async def unregistered_user(message: Message):
    await message.answer(LEXICON['not_updated_user']['en'])
    update_user(message.from_user.id)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])
    if message.from_user.id not in get_users():
        add_user(message.from_user.id)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])


@router.message(Command(commands='settings'))
async def process_settings_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])


@router.message(Command(commands='change_lang'))
async def process_change_language_command(message: Message):
    await message.answer(LEXICON[message.text]['en'], reply_markup=create_change_language_keyboard())
