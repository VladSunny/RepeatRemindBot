from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from lexicon.lexicon import LEXICON, CommandsNames

from FSM.fsm import FSMCreatingModule, creating_module_states

from services.creating_module_service import is_valid_name, is_valid_separator, is_valid_pairs

from keyboards.new_module_kb import create_new_module_keyboard


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


@router.message(Command(commands=CommandsNames.cancel), StateFilter(*creating_module_states))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['cancel_creating_module'][user['lang']]
    )
    await state.clear()


@router.message(StateFilter(FSMCreatingModule.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    if (message.text is None) or (not is_valid_name(message.text)):
        await message.answer(
            text=LEXICON['not_valid_name'][user['lang']]
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(FSMCreatingModule.fill_separator)

    await message.answer(
        text=LEXICON['fill_separator'][user['lang']],
    )


@router.message(StateFilter(FSMCreatingModule.fill_separator))
async def process_separator_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if (message.text is None) or (not ic(is_valid_separator(message.text))):
        await message.answer(
            text=LEXICON['not_valid_separator'][user['lang']]
        )
        return

    await state.update_data(separator=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = ic(await state.get_data())

    await message.answer(
        text=LEXICON['fill_content'][user['lang']],
        reply_markup=create_new_module_keyboard({}, user['lang'], data['name'])
    )


@router.message(StateFilter(FSMCreatingModule.fill_content))
async def process_content_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    ic(message.text)
    if is_valid_pairs(message.text) is None:
        return


@router.message(StateFilter(*creating_module_states))
async def process_unintended_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['unintended_creating_module'][user['lang']]
    )


