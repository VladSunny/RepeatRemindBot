from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from keyboards.saved_modules_kb import list_of_saved_modules_keyboard, module_info_keyboard
from keyboards.new_module_kb import create_new_module_keyboard

from lexicon.lexicon import REPEATING_MODULE_LEXICON, CommandsNames

from FSM.fsm import FSMRepeatingModule

from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs
from services.service import send_and_delete_message, change_message, delete_message

from filters.CallbackDataFactory import RepeatModuleCF, ConfirmRepeatingCF

import json

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_data_template = {
    'current_block': 0,
    'current_repetitions': 0,
    'header_message_id': 0,
    'module_id': 0,
    'learning_content': {}
}


router = Router()


@router.callback_query(ConfirmRepeatingCF.filter(), StateFilter(default_state))
async def process_start_repeating_module(callback: CallbackQuery,
                                                callback_data: ConfirmRepeatingCF,
                                                state: FSMContext):
    user = get_user(callback.from_user.id)
    module_id = callback_data.module_id
    module = get_module(module_id)
    learning_data = get_learning_data(callback.from_user.id)

    new_user_data = deepcopy(user_data_template)
    new_user_data['header_message_id'] = callback.message.message_id
    new_user_data['module_id'] = module_id
    new_user_data['learning_content'] = learning_data['learning_content']

    await state.update_data(new_user_data)
    await state.set_state(FSMRepeatingModule.repeating_module)

    await change_message(chat_id=callback.from_user.id,
                         message_id=callback.message.message_id,
                         reply_markup=None,
                         text=REPEATING_MODULE_LEXICON['repeating_module_header'][user['lang']]
                         .format(module_name=module['name'], current_repetitions=0, cur_block=0))

    await callback.answer()


router.message.filter(StateFilter(FSMRepeatingModule.repeating_module))


@router.message(Command(commands=CommandsNames.cancel))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(
        text=REPEATING_MODULE_LEXICON['cancel_repeating_module'][user['lang']]
    )

    await state.clear()
