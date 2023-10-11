from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import *
from filters.filters import IsChangeLanguage

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON

router = Router()


@router.message(lambda message: message.from_user.id not in get_users())
async def unregistered_user(message: Message):
    await message.answer(LEXICON['/start']['en'])
    add_user(message.from_user.id)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])
    if message.from_user.id not in get_users():
        add_user(message.from_user.id)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    print(user)
    await message.answer(LEXICON[message.text][user['lang']])


@router.message(Command(commands='settings'))
async def process_settings_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[message.text][user['lang']])


@router.message(Command(commands='change_lang'))
async def process_change_language_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[message.text][user['lang']], reply_markup=create_change_language_keyboard())


@router.callback_query(IsChangeLanguage())
async def process_del_bookmark_press(callback: CallbackQuery):
    new_lang: str = callback.data[:-4]
    print(new_lang)
    update_value(callback.from_user.id, {'lang': new_lang})
    await callback.answer(LEXICON['change_language'][new_lang])
