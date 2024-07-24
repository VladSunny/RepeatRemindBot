from __future__ import annotations

import os

from aiogram import F, Router, Dispatcher, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message

from FSM.fsm import FSMCreatingModule, creating_module_states
from config_data.user_restrictions import *
from database.database import *
from filters.CallbackDataFactory import DelPairFromNewModuleCF, RenameNewModuleCF, EditNewModuleSeparatorCF, \
    SaveNewModuleCF
from messages_keyboards.new_module_kb import create_new_module_keyboard
from lexicon.lexicon import CommandsNames, CREATING_MODULE_LEXICON
from keyboards.keyboards import get_main_keyboard
from services.auto_translate_service import *
from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs, add_new_pairs, \
    send_and_delete_message, send_new_module_info, new_module_dict
from services.service import send_and_delete_message

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()


# Отмена создания модуля
@router.message(Command(commands=CommandsNames.cancel), StateFilter(*creating_module_states))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    data = await state.get_data()

    # Удаление отправленного фото, если такое имеется
    try:
        if data.get('cur_photo_path'):
            os.remove(data['cur_photo_path'])
    finally:
        if data.get('is_editing'):
            await message.answer(
                text=CREATING_MODULE_LEXICON['cancel_editing_module'][user['lang']],
                reply_markup=get_main_keyboard(user['lang'])
            )
        else:
            await message.answer(
                text=CREATING_MODULE_LEXICON['cancel_creating_module'][user['lang']],
                reply_markup=get_main_keyboard(user['lang'])
            )

        await state.clear()


# Отправлено имя
@router.message(StateFilter(FSMCreatingModule.fill_name))
async def process_name_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    if (message.text is None) or (not is_valid_name(message.text)):
        await message.delete()
        await send_and_delete_message(
            chat_id=message.chat.id,
            text=CREATING_MODULE_LEXICON['not_valid_name'][user['lang']],
            delete_after=5
        )
        return

    await message.delete()

    data = await state.get_data()

    new_user_module = deepcopy(new_module_dict)
    new_user_module['name'] = message.text
    new_user_module['name'] = message.text
    new_user_module['instruction_message_id'] = data['instruction_message_id']

    await state.update_data(new_user_module)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=data['instruction_message_id'],
        text=CREATING_MODULE_LEXICON['fill_content'][user['lang']],
    )

    msg = await message.answer(
        text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].format(module_name=data['name'],
                                                                             separator=data['separator'],
                                                                             size=len(data['content'])),
        reply_markup=create_new_module_keyboard({}, user['lang'], data['name'], data['separator'])
    )

    await state.update_data(message_id=msg.message_id)


# Отправлен контент для нового модуля
@router.message(StateFilter(FSMCreatingModule.fill_content), F.text)
async def process_content_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.chat.id)

    await message.delete()

    data = await state.get_data()

    new_pairs, has_mistake = get_valid_pairs(message.text, data['separator'])

    await add_new_pairs(state=state, valid_pairs=new_pairs, chat_id=message.from_user.id, bot=bot)

    if has_mistake:
        await send_and_delete_message(message.chat.id,
                                      CREATING_MODULE_LEXICON['incorrect_pair'][user['lang']].format(
                                          separator=data['separator']), 7)


# Отправлено новое имя
@router.message(StateFilter(FSMCreatingModule.change_name))
async def process_new_name_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    await message.delete()

    if (message.text is None) or (not is_valid_name(message.text)):
        await send_and_delete_message(
            chat_id=message.chat.id,
            text=CREATING_MODULE_LEXICON['not_valid_name'][user['lang']],
            delete_after=5
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await send_new_module_info(message.from_user.id, data, user, data['content'], bot)

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['new_module_was_renamed'][user['lang']],
                                  delete_after=3
                                  )


# Отправлен новый разделитель
@router.message(StateFilter(FSMCreatingModule.change_separator))
async def process_new_separator_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    await message.delete()

    if (message.text is None) or (not is_valid_separator(message.text)):
        await send_and_delete_message(
            chat_id=message.chat.id,
            text=CREATING_MODULE_LEXICON['not_valid_separator'][user['lang']],
            delete_after=5
        )
        return

    await state.update_data(separator=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await send_new_module_info(message.from_user.id, data, user, data['content'], bot)

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['seperator_was_changed'][user['lang']],
                                  delete_after=3
                                  )


# Удаление пары из модуля
@router.callback_query(DelPairFromNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_delete_pair(callback: CallbackQuery,
                              callback_data: DelPairFromNewModuleCF,
                              state: FSMContext,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    key: str = callback_data.key

    data = await state.get_data()
    content: dict[str, str] = data['content']

    deleted_pair: str = f"{key} {data['separator']} {content[key]}"

    content.pop(key)

    await state.update_data(content=content)
    await callback.answer(
        CREATING_MODULE_LEXICON['deleted_pair_from_new_model'][user['lang']].format(deleted_pair=deleted_pair))

    await send_new_module_info(callback.from_user.id, data, user, data['content'], bot)


# Переименование модуля
@router.callback_query(RenameNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_change_name(callback: CallbackQuery,
                              callback_data: RenameNewModuleCF,
                              state: FSMContext,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=data['message_id'],
                                reply_markup=None,
                                text=CREATING_MODULE_LEXICON['rename_new_module'][user['lang']]
                                )

    await state.set_state(FSMCreatingModule.change_name)


# Изменение разделителя у модуля
@router.callback_query(EditNewModuleSeparatorCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_change_separator(callback: CallbackQuery,
                                   callback_data: EditNewModuleSeparatorCF,
                                   state: FSMContext,
                                   bot: Bot):
    user = get_user(callback.from_user.id)

    data = await state.get_data()

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=data['message_id'],
                                reply_markup=None,
                                text=CREATING_MODULE_LEXICON['edit_separator'][user['lang']]
                                )

    await state.set_state(FSMCreatingModule.change_separator)


# Сохранение модуля
@router.callback_query(SaveNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_save_module(callback: CallbackQuery,
                              callback_data: SaveNewModuleCF,
                              state: FSMContext,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    if len(data['content']) > max_items_in_module:
        await callback.answer(text=CREATING_MODULE_LEXICON['cant_save_module_qz_max_elements'][user['lang']],
                              show_alert=True)

        return

    module = save_module(chat_id=callback.from_user.id, data=data)

    if data['is_editing']:
        delete_saved_module(data['editing_module_id'])
    else:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['instruction_message_id'])

    await state.clear()

    await bot.send_message(chat_id=callback.from_user.id,
                           text=CREATING_MODULE_LEXICON['module_saved'][user['lang']].format(module_name=module_name,
                                                                                             module_id=module['uuid']),
                           reply_markup=get_main_keyboard(user['lang']))

    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['message_id'])


# Непредусмотренная команда
@router.message(StateFilter(*creating_module_states))
async def process_unintended_command(message: Message):
    user = get_user(message.from_user.id)

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['unintended_creating_module'][user['lang']],
                                  delete_after=4)

    await message.delete()
