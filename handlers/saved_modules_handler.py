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

from lexicon.lexicon import CommandsNames, CREATING_MODULE_LEXICON, SAVED_MODULES_LEXICON

from FSM.fsm import FSMCreatingModule, FSMRepeatingModule

from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs
from services.service import send_and_delete_message, change_message, delete_message

from filters.CallbackDataFactory import OpenSavedModuleCF,\
    DeleteSavedModuleCF, \
    BackToSavedModulesCF,\
    EditModuleCF,\
    RepeatModuleCF

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
    modules = sorted([(module['name'], module['id']) for module in get_modules(message.chat.id)],
                     key=lambda item: (item[0].lower(), item[1]))

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await message.answer(SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']], reply_markup=reply_markup)


@router.callback_query(OpenSavedModuleCF.filter())
async def process_module_info(callback: CallbackQuery,
                              callback_data: OpenSavedModuleCF):
    user = get_user(callback.from_user.id)
    module_id = callback_data.module_id

    module = get_module(module_id)

    if module is None:
        await callback.answer(SAVED_MODULES_LEXICON['module_not_found'][user['lang']])

    elements: str = ""

    cnt: int = 0
    for i in module['content'].items():
        cnt += 1
        elements += f"{cnt}. {i[0]} {module['separator']} {i[1]}\n"

    reply_markup = module_info_keyboard(lang=user['lang'], module_id=module_id, module_name=module['name'])

    await change_message(chat_id=callback.from_user.id,
                         message_id=callback.message.message_id,
                         reply_markup=reply_markup,
                         text=SAVED_MODULES_LEXICON['module_info'][user['lang']].format(
                             name=module['name'],
                             id=module_id,
                             number_of_elements=len(module['content']),
                             elements=elements,
                             separator=module['separator']
                         ))

    await callback.answer()


@router.callback_query(BackToSavedModulesCF.filter())
async def process_back_to_saved_modules(callback: CallbackQuery):
    user = get_user(callback.from_user.id)
    modules = sorted([(module['name'], module['id']) for module in get_modules(callback.message.chat.id)],
                     key=lambda item: (item[0].lower(), item[1]))

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await change_message(chat_id=callback.from_user.id,
                         message_id=callback.message.message_id,
                         reply_markup=reply_markup,
                         text=SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']]
                         )

    await callback.answer()


@router.callback_query(DeleteSavedModuleCF.filter())
async def process_delete_saved_module(callback: CallbackQuery,
                                      callback_data: DeleteSavedModuleCF):
    user = get_user(callback.from_user.id)

    module_id = callback_data.module_id
    module_name = callback_data.module_name

    delete_saved_module(module_id=module_id)

    modules = sorted([(module['name'], module['id']) for module in get_modules(callback.message.chat.id)],
                     key=lambda item: (item[0].lower(), item[1]))

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await change_message(chat_id=callback.from_user.id,
                         message_id=callback.message.message_id,
                         reply_markup=reply_markup,
                         text=SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']]
                         )

    await callback.answer(
        SAVED_MODULES_LEXICON['module_has_been_deleted'][user['lang']].format(module_name=module_name)
    )


@router.callback_query(EditModuleCF.filter())
async def process_edit_saved_module(callback: CallbackQuery,
                                    callback_data: EditModuleCF,
                                    state: FSMContext):
    user = get_user(callback.from_user.id)

    module_id = callback_data.module_id

    module = get_module(module_id)

    await state.update_data(name=module['name'],
                            content=module['content'],
                            separator=module['separator'],
                            message_id=callback.message.message_id)

    await state.set_state(FSMCreatingModule.fill_content)

    await callback.answer(
        SAVED_MODULES_LEXICON['edit_instruction'][user['lang']], show_alert=True
    )

    await change_message(chat_id=callback.from_user.id,
                         message_id=callback.message.message_id,
                         text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']]
                         .format(module_name=module['name'],
                                 separator=module['separator']
                                 ),
                         reply_markup=create_new_module_keyboard(content=module['content'],
                                                                 lang=user['lang'],
                                                                 module_name=module['name'],
                                                                 separator=module['separator'])
                         )


@router.callback_query(RepeatModuleCF.filter())
async def process_repeat_saved_module(callback: CallbackQuery,
                                      callback_data: RepeatModuleCF,
                                      state: FSMContext):
    user = get_user(callback.from_user.id)

    module_id = callback_data.module_id

    await state.set_state(FSMRepeatingModule.repeating_module)
