from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *

from lexicon.lexicon import LEXICON, CommandsNames

from FSM.fsm import FSMCreatingModule, creating_module_states

from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs
from services.service import send_and_delete_message, change_reply_markup

from keyboards.new_module_kb import create_new_module_keyboard

from filters.CallbackDataFactory import DelPairFromNewModuleCF, RenameNewModuleCF

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
    await state.update_data(content={})
    await state.set_state(FSMCreatingModule.fill_separator)

    await message.answer(
        text=LEXICON['fill_separator'][user['lang']],
    )


@router.message(StateFilter(FSMCreatingModule.fill_separator))
async def process_separator_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if (message.text is None) or (not is_valid_separator(message.text)):
        await message.answer(
            text=LEXICON['not_valid_separator'][user['lang']]
        )
        return

    await state.update_data(separator=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await message.answer(
        text=LEXICON['fill_content'][user['lang']]
    )
    msg = await message.answer(
        text=LEXICON['new_module_info'][user['lang']].format(module_name=data['name'], separator=data['separator']),
        reply_markup=create_new_module_keyboard({}, user['lang'], data['name'], data['separator'])
    )

    await state.update_data(message_id=msg.message_id)


@router.message(StateFilter(FSMCreatingModule.fill_content))
async def process_content_sent(message: Message, state: FSMContext):
    user = get_user(message.chat.id)

    await message.delete()

    data = await state.get_data()
    valid_pairs: dict[str, str] = get_valid_pairs(message.text, data['separator'])

    if get_valid_pairs(message.text, data['separator']) is None:
        await send_and_delete_message(message.chat.id,
                                      LEXICON['incorrect_pair'][user['lang']].format(separator=data['separator']),
                                      5)
        return

    valid_pairs = data['content'] | valid_pairs

    await state.update_data(content=valid_pairs)

    await change_reply_markup(
        message.chat.id, data['message_id'],
        create_new_module_keyboard(valid_pairs,
                                   user['lang'],
                                   data['name'],
                                   data['separator'])
    )


@router.callback_query(DelPairFromNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_delete_pair(callback: CallbackQuery,
                                        callback_data: DelPairFromNewModuleCF,
                                        state: FSMContext):
    user = get_user(callback.from_user.id)
    key: str = callback_data.key

    data = await state.get_data()
    content: dict[str, str] = ic(data['content'])

    deleted_pair: str = f"{key} {data['separator']} {content[key]}"

    ic(content.pop(key))

    await state.update_data(content=content)
    await callback.answer(LEXICON['deleted_pair_from_new_model'][user['lang']].format(deleted_pair=deleted_pair))

    await change_reply_markup(
        callback.from_user.id, data['message_id'],
        create_new_module_keyboard(content,
                                   user['lang'],
                                   data['name'],
                                   data['separator'])
    )


# @router.callback_query(RenameNewModuleCF.filter())
# async def process_change_name(callback: CallbackQuery,
#                                         callback_data: RenameNewModuleCF,
#                                         state: FSMContext):
#     user = get_user(callback.from_user.id)
#     key: str = callback_data.key
#
#     data = await state.get_data()
#     content: dict[str, str] = ic(data['content'])
#
#     ic(content.pop(key))
#
#     await state.update_data(content=content)
#     await callback.answer(LEXICON['deleted_pair_from_new_model'][user['lang']])
#
#     await change_reply_markup(
#         callback.from_user.id, data['message_id'],
#         create_new_module_keyboard(content,
#                                    user['lang'],
#                                    data['name'],
#                                    data['separator'])
#     )


@router.message(StateFilter(*creating_module_states))
async def process_unintended_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['unintended_creating_module'][user['lang']]
    )


