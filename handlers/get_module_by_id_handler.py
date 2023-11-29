from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update, ReplyKeyboardRemove
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from keyboards.reapeating_module_kb import correct_answer_keyboard, incorrect_answer_keyboard

from lexicon.lexicon import REPEATING_MODULE_LEXICON, CommandsNames

from FSM.fsm import FSMGetModuleById

from services.service import send_and_delete_message, change_message, delete_message, send_message
from services.repeating_module_service import get_current_questions, get_all_questions

from filters.CallbackDataFactory import RepeatModuleCF, ConfirmRepeatingCF, AnswerWasCorrectCF, NextQuestionCF

from lexicon.lexicon import GET_MODULE_BY_ID_LEXICON

router = Router()


@router.message(Command(commands=CommandsNames.get_module_by_id), StateFilter(default_state))
async def process_get_module_by_id_command(message: Message,
                                           state: FSMContext):
    user = get_user(message.from_user.id)

    await state.set_state(FSMGetModuleById.send_module_id)

    await message.answer(GET_MODULE_BY_ID_LEXICON['get_module_by_id'][user['lang']])


@router.message(Command(commands=CommandsNames.cancel), StateFilter(FSMGetModuleById.send_module_id))
async def process_cancel_command(message: Message,
                                 state: FSMContext):
    user = get_user(message.from_user.id)

    await state.clear()

    await message.answer(GET_MODULE_BY_ID_LEXICON['cancel'][user['lang']])


@router.message(StateFilter(FSMGetModuleById.send_module_id))
async def process_sent_module_id(message: Message,
                                 state: FSMContext):
    user = get_user(message.from_user.id)

    if message.text is None or not message.text.isdigit():
        await message.delete()
        await send_and_delete_message(chat_id=message.from_user.id,
                                      text=GET_MODULE_BY_ID_LEXICON['incorrect_type'][user['lang']],
                                      delete_after=3)
        return

    module: dict = get_module_by_id(int(message.text))

    if module is None:
        await message.delete()
        await send_and_delete_message(chat_id=message.from_user.id,
                                      text=GET_MODULE_BY_ID_LEXICON['cant_find_module'][user['lang']],
                                      delete_after=5)
        return

    await state.clear()

    module['chat_id'] = message.from_user.id
    del module['id']

    saved_module: dict = save_module(message.from_user.id, module)

    await message.answer(text=GET_MODULE_BY_ID_LEXICON['module_was_saved'][user['lang']].format(
        module_name=saved_module['name'],
        module_id=saved_module['id']
    )
    )
