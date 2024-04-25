from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from FSM.fsm import FSMGetModuleById
from config_data.user_restrictions import *
from database.database import *
from lexicon.lexicon import CommandsNames, main_keyboard_lexicon
from lexicon.lexicon import GET_MODULE_BY_ID_LEXICON, LEXICON
from services.service import send_and_delete_message

router = Router()


# /get_module_by_id
@router.message(Command(commands=CommandsNames.get_module_by_id), StateFilter(default_state))
@router.message(F.text == main_keyboard_lexicon[CommandsNames.get_module_by_id]['ru'], StateFilter(default_state))
@router.message(F.text == main_keyboard_lexicon[CommandsNames.get_module_by_id]['en'], StateFilter(default_state))
async def process_get_module_by_id_command(message: Message,
                                           state: FSMContext):
    user = get_user(message.from_user.id)

    if get_modules_number(message.from_user.id) >= max_modules:
        await message.answer(LEXICON['maximum_number_of_modules'][user['lang']])
    else:
        await state.set_state(FSMGetModuleById.send_module_id)
        await message.answer(GET_MODULE_BY_ID_LEXICON['get_module_by_id'][user['lang']])


# Отменить получение модуля по id
@router.message(Command(commands=CommandsNames.cancel), StateFilter(FSMGetModuleById.send_module_id))
async def process_cancel_command(message: Message,
                                 state: FSMContext):
    user = get_user(message.from_user.id)

    await state.clear()

    await message.answer(GET_MODULE_BY_ID_LEXICON['cancel'][user['lang']])


# Отправлен id нужного модуля
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

    module: dict = get_module(int(message.text))

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
