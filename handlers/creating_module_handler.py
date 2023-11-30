from __future__ import annotations

import os

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *

from lexicon.lexicon import CommandsNames, CREATING_MODULE_LEXICON

from FSM.fsm import FSMCreatingModule, creating_module_states

from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs
from services.service import send_and_delete_message, change_message, delete_message, download_file
from services.tesseract_service import get_eng_from_photo, clear_text

from keyboards.new_module_kb import create_new_module_keyboard

from filters.CallbackDataFactory import DelPairFromNewModuleCF, RenameNewModuleCF, EditNewModuleSeparatorCF, \
    SaveNewModuleCF


storage = MemoryStorage()
dp = Dispatcher(storage=storage)

new_module_dict: dict[str, str | dict[str, str]] = {
    "name": "",
    "separator": "=",
    "content": {

    },
    "message_id": "",
    "is_editing": False,
    "editing_module_id": 0
}

router = Router()


@router.message(Command(commands=CommandsNames.cancel), StateFilter(*creating_module_states))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    data = await state.get_data()

    if data.get('is_editing'):
        await message.answer(
            text=CREATING_MODULE_LEXICON['cancel_editing_module'][user['lang']]
        )
    else:
        await message.answer(
            text=CREATING_MODULE_LEXICON['cancel_creating_module'][user['lang']]
        )

    await state.clear()


@router.message(StateFilter(FSMCreatingModule.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    if (message.text is None) or (not is_valid_name(message.text)):
        await message.answer(
            text=CREATING_MODULE_LEXICON['not_valid_name'][user['lang']]
        )
        return

    new_user_module = deepcopy(new_module_dict)
    new_user_module['name'] = message.text
    new_user_module['name'] = message.text

    await state.update_data(new_user_module)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await message.answer(
        text=CREATING_MODULE_LEXICON['fill_content'][user['lang']]
    )
    msg = await message.answer(
        text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].format(module_name=data['name'],
                                                                             separator=data['separator']),
        reply_markup=create_new_module_keyboard({}, user['lang'], data['name'], data['separator'])
    )

    await state.update_data(message_id=msg.message_id)


@router.message(StateFilter(FSMCreatingModule.fill_content), F.text)
async def process_content_sent(message: Message, state: FSMContext):
    user = get_user(message.chat.id)

    await message.delete()

    data = await state.get_data()
    valid_pairs: dict[str, str] = get_valid_pairs(message.text, data['separator'])

    if get_valid_pairs(message.text, data['separator']) is None:
        await send_and_delete_message(message.chat.id,
                                      CREATING_MODULE_LEXICON['incorrect_pair'][user['lang']].format(
                                          separator=data['separator']), 5)
        return

    valid_pairs = data['content'] | valid_pairs

    await state.update_data(content=valid_pairs)

    await change_message(chat_id=message.chat.id,
                         message_id=data['message_id'],
                         reply_markup=create_new_module_keyboard(valid_pairs,
                                                                 user['lang'],
                                                                 data['name'],
                                                                 data['separator']))


@router.message(StateFilter(FSMCreatingModule.fill_content), F.photo)
async def process_photo_sent(message: Message, state: FSMContext):
    user = get_user(message.chat.id)

    photo = message.photo[-1]

    path = await download_file(photo.file_id)

    text = await get_eng_from_photo(path)
    clean_phrases = clear_text(text)

    clean_mes_text = str(clean_phrases)

    await message.answer(text)
    await message.answer(clean_mes_text)


@router.message(StateFilter(FSMCreatingModule.change_name))
async def process_new_name_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    await message.delete()

    if (message.text is None) or (not is_valid_name(message.text)):
        await message.answer(
            text=CREATING_MODULE_LEXICON['not_valid_name'][user['lang']]
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await change_message(chat_id=message.chat.id,
                         message_id=data['message_id'],
                         reply_markup=create_new_module_keyboard(data['content'],
                                                                 user['lang'],
                                                                 data['name'],
                                                                 data['separator']),
                         text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].format(module_name=data['name'],
                                                                                              separator=data[
                                                                                                  'separator']))

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['new_module_was_renamed'][user['lang']],
                                  delete_after=3
                                  )


@router.message(StateFilter(FSMCreatingModule.change_separator))
async def process_new_separator_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    await message.delete()

    if (message.text is None) or (not is_valid_separator(message.text)):
        await message.answer(
            text=CREATING_MODULE_LEXICON['not_valid_separator'][user['lang']]
        )
        return

    await state.update_data(separator=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await change_message(chat_id=message.chat.id,
                         message_id=data['message_id'],
                         reply_markup=create_new_module_keyboard(data['content'],
                                                                 user['lang'],
                                                                 data['name'],
                                                                 data['separator']),
                         text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].format(module_name=data['name'],
                                                                                              separator=data[
                                                                                                  'separator']))

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['seperator_was_changed'][user['lang']],
                                  delete_after=3
                                  )


@router.callback_query(DelPairFromNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_delete_pair(callback: CallbackQuery,
                              callback_data: DelPairFromNewModuleCF,
                              state: FSMContext):
    user = get_user(callback.from_user.id)
    key: str = callback_data.key

    data = await state.get_data()
    content: dict[str, str] = data['content']

    deleted_pair: str = f"{key} {data['separator']} {content[key]}"

    content.pop(key)

    await state.update_data(content=content)
    await callback.answer(
        CREATING_MODULE_LEXICON['deleted_pair_from_new_model'][user['lang']].format(deleted_pair=deleted_pair))

    await change_message(chat_id=callback.from_user.id,
                         message_id=data['message_id'],
                         reply_markup=create_new_module_keyboard(
                             content,
                             user['lang'],
                             data['name'],
                             data['separator'])
                         )


@router.callback_query(RenameNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_change_name(callback: CallbackQuery,
                              callback_data: RenameNewModuleCF,
                              state: FSMContext):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    await change_message(chat_id=callback.from_user.id,
                         message_id=data['message_id'],
                         reply_markup=None,
                         text=CREATING_MODULE_LEXICON['rename_new_module'][user['lang']]
                         )

    await state.set_state(FSMCreatingModule.change_name)


@router.callback_query(EditNewModuleSeparatorCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_change_separator(callback: CallbackQuery,
                                   callback_data: EditNewModuleSeparatorCF,
                                   state: FSMContext):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    await change_message(chat_id=callback.from_user.id,
                         message_id=data['message_id'],
                         reply_markup=None,
                         text=CREATING_MODULE_LEXICON['edit_separator'][user['lang']]
                         )

    await state.set_state(FSMCreatingModule.change_separator)


@router.callback_query(SaveNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_save_module(callback: CallbackQuery,
                              callback_data: SaveNewModuleCF,
                              state: FSMContext):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    module = save_module(chat_id=callback.from_user.id, data=data)

    if data['is_editing']:
        delete_saved_module(data['editing_module_id'])

    await state.clear()

    await callback.answer(text=CREATING_MODULE_LEXICON['module_saved'][user['lang']].format(module_name=module_name,
                                                                                            module_id=module['id']),
                                                                                            show_alert=True)

    await delete_message(chat_id=callback.from_user.id, message_id=data['message_id'])


@router.message(StateFilter(*creating_module_states))
async def process_unintended_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=CREATING_MODULE_LEXICON['unintended_creating_module'][user['lang']]
    )
