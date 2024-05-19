from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from FSM.fsm import FSMCreatingModule
from config_data.user_restrictions import *
from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF
from messages_keyboards.change_language_kb import create_change_language_keyboard
from lexicon.lexicon import LEXICON, CommandsNames, SETTINGS_LEXICON, main_keyboard_lexicon, system_lexicon
from keyboards.keyboards import get_main_keyboard
from services.service import send_and_delete_message
from services.yandexgpt_service import ai_generate_module

router = Router()


@router.message(Command(commands='prompt'))
async def unregistered_user(message: Message):
    text = await ai_generate_module(message.text[6:])
    await message.answer(text)