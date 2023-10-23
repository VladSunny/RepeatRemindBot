from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF
from keyboards.change_language_kb import create_change_language_keyboard
from lexicon.lexicon import LEXICON, CommandsNames
from FSM.fsm import FSMCreatingModule, creating_module_states

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

new_module_dict: dict[str, str | dict[str, str]] = {
    "name": "",
    "content": {
        
    }
}

router = Router()


@router.message(Command(commands=CommandsNames.cancel), StateFilter(*creating_module_states))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['cancel_creating_module'][user['lang']]
    )
    await state.clear()


@router.message(StateFilter(*creating_module_states))
async def process_unintended_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['unintended_creating_module'][user['lang']]
    )


