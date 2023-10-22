from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON

router = Router()


@router.message(Command(commands='new_module'))
async def process_new_module_command(message: Message):
    user = get_user(message.from_user.id)

    module_name = message.text.split('/new_module ')

    if not module_name:
        await message.answer(LEXICON[message.text][user['lang']])
        return

