from __future__ import annotations

from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from FSM.fsm import FSMCreatingModule
from config_data.user_restrictions import *
from database.database import *
from filters.CallbackDataFactory import OpenSavedModuleCF, DeleteSavedModuleCF, BackToSavedModulesCF, EditModuleCF, \
    RepeatModuleCF, MixWordsInRepeatingModuleCF, ChangeVisibilityModuleCF
from messages_keyboards.new_module_kb import create_new_module_keyboard
from messages_keyboards.reapeating_module_kb import confirm_repeating_keyboard
from messages_keyboards.saved_modules_kb import list_of_saved_modules_keyboard, module_info_keyboard
from lexicon.lexicon import (CommandsNames, CREATING_MODULE_LEXICON, SAVED_MODULES_LEXICON, REPEATING_MODULE_LEXICON,
                             main_keyboard_lexicon, system_lexicon)
from services.repeating_module_service import get_blocks_num, get_blocks, get_blocks_str
from services.service import send_and_delete_message
from services.creating_module_service import new_module_dict

from copy import deepcopy

router = Router()

router.message.filter(StateFilter(default_state))


# Отправляет запрос на подтверждение повторения
async def ask_to_repeating(chat_id, module_id, state, message_id, bot: Bot):
    user = get_user(chat_id)
    user_settings = get_settings(chat_id)
    module = get_module(module_id)

    # Разбиение контента модуля на блоки
    learning_content = get_blocks(module['content'], user_settings['words_in_block'])
    await state.update_data(learning_content=learning_content)

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=REPEATING_MODULE_LEXICON['ask_to_repeating'][user['lang']]
                                .format(module_name=module['name'],
                                        blocks_num=str(
                                            get_blocks_num(len(module['content']), user_settings['words_in_block'])),
                                        words_in_block_num=user_settings['words_in_block'],
                                        repetitions_num=user_settings['repetitions_for_block'],
                                        words_num=len(module['content']),
                                        content=get_blocks_str(module['content'],
                                                               user_settings['words_in_block'],
                                                               module['separator'],
                                                               learning_content)
                                        ),
                                reply_markup=confirm_repeating_keyboard(user['lang'], module_id)
                                )


# Вывод сохраненных модулей
@router.message(Command(commands=CommandsNames.saved_modules))
@router.message(F.text == main_keyboard_lexicon[CommandsNames.saved_modules]['ru'])
@router.message(F.text == main_keyboard_lexicon[CommandsNames.saved_modules]['en'])
async def process_saved_modules_command(message: Message):
    user = get_user(message.from_user.id)
    modules = sorted([(module['name'], module['id']) for module in get_modules(message.chat.id)],
                     key=lambda item: (item[0].lower(), item[1]))

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await message.answer(SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']], reply_markup=reply_markup)


# Вывод информации о модуле
@router.callback_query(OpenSavedModuleCF.filter())
async def process_module_info(callback: CallbackQuery,
                              callback_data: OpenSavedModuleCF,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    module_id = callback_data.module_id

    module = get_module(module_id)

    if module is None:
        await callback.answer(SAVED_MODULES_LEXICON['module_not_found'][user['lang']])

    elements: str = ""

    # Создание текста с элементами
    cnt: int = 0
    for i in module['content'].items():
        cnt += 1
        elements += f"{cnt}. {i[0]} {module['separator']} {i[1]}\n"

    reply_markup = module_info_keyboard(lang=user['lang'], module_id=module_id, module_name=module['name'], public=module['public'])

    await bot.edit_message_text(chat_id=callback.from_user.id,
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


@router.callback_query(ChangeVisibilityModuleCF.filter())
async def process_change_visibility_module(callback: CallbackQuery,
                                           callback_data: ChangeVisibilityModuleCF,
                                           bot: Bot):
    user = get_user(callback.from_user.id)
    module_id = callback_data.module_id
    module = get_module(module_id)

    update_module_params(module_id, {'public': not module['public']})

    reply_markup = module_info_keyboard(
        lang=user['lang'],
        module_id=module_id,
        module_name=module['name'],
        public=not module['public']
    )

    await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=reply_markup
    )

    if (module['public']):
        await callback.answer(SAVED_MODULES_LEXICON['change_to_private'][user['lang']], show_alert=True)
    else:
        await callback.answer(SAVED_MODULES_LEXICON['change_to_public'][user['lang']], show_alert=True)


# Вернуться к списку сохраненных модулей
@router.callback_query(BackToSavedModulesCF.filter())
async def process_back_to_saved_modules(callback: CallbackQuery,
                                        bot: Bot):
    user = get_user(callback.from_user.id)
    modules = sorted([(module['name'], module['id']) for module in get_modules(callback.message.chat.id)],
                     key=lambda item: (item[0].lower(), item[1]))

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=reply_markup,
                                text=SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']]
                                )

    await callback.answer()


# Удаление сохраненного модуля
@router.callback_query(DeleteSavedModuleCF.filter())
async def process_delete_saved_module(callback: CallbackQuery,
                                      callback_data: DeleteSavedModuleCF,
                                      bot: Bot):
    user = get_user(callback.from_user.id)

    module_id = callback_data.module_id
    module_name = callback_data.module_name

    delete_saved_module(module_id=module_id)

    modules = sorted([(module['name'], module['id']) for module in get_modules(callback.message.chat.id)],
                     key=lambda item: (item[0].lower(), item[1]))

    reply_markup = list_of_saved_modules_keyboard(modules=modules)
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=reply_markup,
                                text=SAVED_MODULES_LEXICON['list_of_saved_modules'][user['lang']]
                                )

    await callback.answer(
        SAVED_MODULES_LEXICON['module_has_been_deleted'][user['lang']].format(module_name=module_name)
    )


# Изменение сохраненного модуля
@router.callback_query(EditModuleCF.filter())
async def process_edit_saved_module(callback: CallbackQuery,
                                    callback_data: EditModuleCF,
                                    state: FSMContext,
                                    bot: Bot):
    user = get_user(callback.from_user.id)

    module_id = callback_data.module_id

    module = get_module(module_id)

    await state.set_state(FSMCreatingModule.fill_content)

    await callback.answer(
        SAVED_MODULES_LEXICON['edit_instruction'][user['lang']], show_alert=True
    )

    header_message_id = await bot.send_message(chat_id=callback.from_user.id,
                                               text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']]
                                               .format(module_name=module['name'],
                                                       separator=module['separator'],
                                                       size=len(module['content']),
                                                       max_elements=max_items_in_module
                                                       ),
                                               reply_markup=create_new_module_keyboard(content=module['content'],
                                                                                       lang=user['lang'],
                                                                                       module_name=module['name'],
                                                                                       separator=module['separator'])
                                               )

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                text=SAVED_MODULES_LEXICON['cancel_to_over_editing'][user['lang']]
                                )
    
    module_content = deepcopy(new_module_dict)
    module_content['content'] = module['content']
    module_content['separator'] = module['separator']
    module_content['message_id'] = header_message_id.message_id
    module_content['is_editing'] = True
    module_content['editing_module_id'] = module_id
    module_content['cur_photo_path'] = ""
    module_content['name'] = module['name']

    await state.update_data(**module_content)

    # await state.update_data(name=module['name'],
    #                         content=module['content'],
    #                         separator=module['separator'],
    #                         message_id=header_message_id.message_id,
    #                         is_editing=True,
    #                         editing_module_id=module_id,
    #                         cur_photo_path="")

    await send_and_delete_message(chat_id=callback.from_user.id,
                                  text=system_lexicon['delete_keyboard'][user['lang']],
                                  delete_after=0,
                                  reply_markup=ReplyKeyboardRemove())


# Запрос на подтверждение повторения выбранного модуля
@router.callback_query(RepeatModuleCF.filter())
async def process_ask_to_repeat_saved_module(callback: CallbackQuery,
                                             callback_data: RepeatModuleCF,
                                             state: FSMContext,
                                             bot: Bot):
    module_id = callback_data.module_id

    await ask_to_repeating(callback.from_user.id, module_id, state, callback.message.message_id, bot)
    await callback.answer()


# Перемешать слова между блоками
@router.callback_query(MixWordsInRepeatingModuleCF.filter())
async def process_mix_words_in_repeating_module(callback: CallbackQuery,
                                                callback_data: MixWordsInRepeatingModuleCF,
                                                state: FSMContext,
                                                bot: Bot):
    user = get_user(callback.from_user.id)
    module_id = callback_data.module_id

    await ask_to_repeating(callback.from_user.id, module_id, state, callback.message.message_id, bot)
    await callback.answer(REPEATING_MODULE_LEXICON['words_were_mixed'][user['lang']])
