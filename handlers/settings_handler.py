from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from FSM.fsm import FSMChangeSettings
from database.database import *
from lexicon.lexicon import LEXICON, CommandsNames, SETTINGS_LEXICON, main_keyboard_lexicon
from services.service import send_and_delete_message
from services.settings_service import is_valid_words_in_block, is_valid_repetitions_for_block
from messages_keyboards.settings_kb import create_settings_keyboard
from filters.CallbackDataFactory import ChangeGetUpdatesCF, ChangeShowInTableCF

router = Router()


# Отправка доступных команд для изменения параметров
@router.message(Command(commands=CommandsNames.settings), StateFilter(default_state))
@router.message(F.text == main_keyboard_lexicon[CommandsNames.settings]['ru'])
@router.message(F.text == main_keyboard_lexicon[CommandsNames.settings]['en'])
async def process_settings_command(message: Message):
    user = get_user(message.from_user.id)
    user_settings = get_settings(message.from_user.id)

    await message.answer(text=LEXICON[CommandsNames.settings][user['lang']].format(
        words_in_block_number=user_settings['words_in_block'],
        repetitions_for_block_number=user_settings['repetitions_for_block']
    ),
        reply_markup=create_settings_keyboard(get_updates=user_settings['get_updates'],
                                              show_in_donate_table=user_settings['show_in_donate_table'],
                                              lang=user['lang'])
    )


# Изменение параметра получения уведомлений об обновлениях бота
@router.callback_query(ChangeGetUpdatesCF.filter())
async def process_change_get_updates(callback: CallbackQuery,
                                     callback_data: ChangeGetUpdatesCF):
    user = get_user(callback.from_user.id)
    user_settings = get_settings(callback.from_user.id)

    update_settings(chat_id=callback.from_user.id,
                    update={'get_updates': not callback_data.get_updates})

    await callback.message.edit_reply_markup(
        reply_markup=create_settings_keyboard(get_updates=not callback_data.get_updates,
                                              show_in_donate_table=user_settings['show_in_donate_table'],
                                              lang=user['lang'])
    )

    await callback.answer()


# Изменение параметра, который разрешает показывать имя пользовтеля в таблице поддержавших проект
@router.callback_query(ChangeShowInTableCF.filter())
async def process_change_show_in_donate_table(callback: CallbackQuery,
                                              callback_data: ChangeShowInTableCF):
    user = get_user(callback.from_user.id)
    user_settings = get_settings(callback.from_user.id)

    update_settings(chat_id=callback.from_user.id,
                    update={'show_in_donate_table': not callback_data.show_in_donate_table})

    await callback.message.edit_reply_markup(
        reply_markup=create_settings_keyboard(get_updates=user_settings['get_updates'],
                                              show_in_donate_table=not callback_data.show_in_donate_table,
                                              lang=user['lang'])
    )

    await callback.answer()


# Отмена ввода
@router.message(Command(commands=CommandsNames.cancel),
                StateFilter(FSMChangeSettings.change_words_in_block,
                            FSMChangeSettings.change_repetitions_for_block),
                )
async def process_cancel_input_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON['cancel_input'][user['lang']])

    await state.clear()


# Изменить количество слов в блоке
@router.message(Command(commands=CommandsNames.change_words_in_block), StateFilter(default_state))
async def process_change_words_in_block_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON[CommandsNames.change_words_in_block][user['lang']])

    await state.set_state(FSMChangeSettings.change_words_in_block)


# Изменить количество повторений блока
@router.message(Command(commands=CommandsNames.change_repetitions_for_block), StateFilter(default_state))
async def process_change_repetitions_for_block_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON[CommandsNames.change_repetitions_for_block][user['lang']])

    await state.set_state(FSMChangeSettings.change_repetitions_for_block)


# Отправленно новое количество слов в блоке
@router.message(StateFilter(FSMChangeSettings.change_words_in_block))
async def process_sent_new_words_in_block_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    await message.delete()

    if message.text is None or not is_valid_words_in_block(message.text):
        await send_and_delete_message(chat_id=message.from_user.id,
                                      text=SETTINGS_LEXICON['not_valid_words_in_block'][user['lang']],
                                      delete_after=3
                                      )
        return

    update = {"words_in_block": message.text}

    update_settings(message.from_user.id, update)

    await message.answer(SETTINGS_LEXICON['sent_new_words_in_block'][user['lang']].format(number=message.text))

    await state.clear()


# Отправленно новое количество повторений блока
@router.message(StateFilter(FSMChangeSettings.change_repetitions_for_block))
async def process_sent_new_repetitions_for_block_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    await message.delete()

    if message.text is None or not is_valid_repetitions_for_block(message.text):
        await send_and_delete_message(chat_id=message.from_user.id,
                                      text=SETTINGS_LEXICON['not_valid_repetitions_for_block'][user['lang']],
                                      delete_after=3
                                      )
        return

    update = {"repetitions_for_block": message.text}

    update_settings(message.from_user.id, update)

    await message.answer(SETTINGS_LEXICON['sent_new_repetitions_for_block'][user['lang']].format(number=message.text))

    await state.clear()
