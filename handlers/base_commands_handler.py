from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from FSM.fsm import FSMCreatingModule
from config_data.user_restrictions import *
from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF
from messages_keyboards.change_language_kb import create_change_language_keyboard
from lexicon.lexicon import LEXICON, CommandsNames, SETTINGS_LEXICON

router = Router()

router.message.filter(StateFilter(default_state))


# Функция добавляющая нового пользователя
@router.message(lambda message: message.from_user.id not in get_users_chat_ids())
async def unregistered_user(message: Message):
    add_user(message.from_user.id)
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/start'][user['lang']])


# /start
# Добавляет нового пользователя
@router.message(CommandStart())
async def process_start_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/start'][user['lang']])
    if message.from_user.id not in get_users_chat_ids():
        add_user(message.from_user.id)


# /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/help'][user['lang']])


# /cancel когда нечего отменять
@router.message(Command(commands=CommandsNames.cancel))
async def process_cancel_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['nothing_to_cancel'][user['lang']]
    )


# /change_language для смены языка
@router.message(Command(commands=CommandsNames.change_language))
async def process_change_language_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON[CommandsNames.change_language][user['lang']],
                         reply_markup=create_change_language_keyboard())


# /new_module для создания нового модуля
@router.message(Command(commands=CommandsNames.create_new_module))
async def process_new_module_command(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    if get_modules_number(message.from_user.id) >= max_modules:
        await message.answer(LEXICON['maximum_number_of_modules'][user['lang']])
    else:
        instruction_message = await bot.send_message(chat_id=message.from_user.id,
                                                     text=LEXICON[CommandsNames.create_new_module][user['lang']])
        await state.update_data(instruction_message_id=instruction_message.message_id)
        await state.set_state(FSMCreatingModule.fill_name)


# Смена языка
@router.callback_query(LanguageSelectionCF.filter())
async def process_change_language_press(callback: CallbackQuery,
                                        callback_data: LanguageSelectionCF):
    new_lang: str = callback_data.language
    update_user(callback.from_user.id, {'lang': new_lang})
    await callback.answer(SETTINGS_LEXICON['changed_language'][new_lang])
