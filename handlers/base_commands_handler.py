from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON, CommandsNames

router = Router()


@router.message(lambda message: message.from_user.id not in get_users_chat_ids())
async def unregistered_user(message: Message):
    await message.answer(LEXICON['/start']['en'])
    add_user(message.from_user.id)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])
    if message.from_user.id not in get_users_chat_ids():
        add_user(message.from_user.id)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/help'][user['lang']])


@router.message(Command(commands=CommandsNames.settings))
async def process_settings_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[CommandsNames.settings][user['lang']])


@router.message(Command(commands=CommandsNames.change_language))
async def process_change_language_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[CommandsNames.change_language][user['lang']],
                         reply_markup=create_change_language_keyboard())


@router.callback_query(LanguageSelectionCF.filter())
async def process_change_language_press(callback: CallbackQuery,
                                        callback_data: LanguageSelectionCF):
    new_lang: str = callback_data.language
    update_value(callback.from_user.id, {'lang': new_lang})
    await callback.answer(LEXICON['changed_language'][new_lang])
