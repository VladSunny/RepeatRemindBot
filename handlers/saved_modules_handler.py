from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from keyboards.saved_modules_kb import list_of_saved_modules_keyboard

from lexicon.lexicon import CommandsNames, CREATING_MODULE_LEXICON, SAVED_MODULES_LEXICON

from FSM.fsm import FSMCreatingModule, creating_module_states

from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs
from services.service import send_and_delete_message, change_message, delete_message

from keyboards.new_module_kb import create_new_module_keyboard

from filters.CallbackDataFactory import OpenSavedModuleCF

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

new_module_dict: dict[str, str | dict[str, str]] = {
    "name": "",
    "separator": "",
    "content": {

    },
    "message_id": "",
}

router = Router()

router.message.filter(StateFilter(default_state))


@router.message(Command(commands=CommandsNames.saved_modules))
async def process_saved_modules_command(message: Message):
    user = get_user(message.from_user.id)
    modules = [(module['name'], module['id']) for module in get_modules(message.chat.id)]

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await message.answer(SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']], reply_markup=reply_markup)
