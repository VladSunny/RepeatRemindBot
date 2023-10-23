from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON, CommandsNames
from FSM.fsm import FSMCreatingModule

router = Router()

router.message.filter(StateFilter(default_state))

# message

# base commands


@router.message(lambda message: message.from_user.id not in get_users_chat_ids())
async def unregistered_user(message: Message):
    await message.answer(LEXICON['/start']['en'])
    add_user(message.from_user.id)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start']['en'])
    if message.from_user.id not in get_users_chat_ids():
        add_user(message.from_user.id)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/help'][user['lang']])


@router.message(Command(commands=CommandsNames.settings))
async def process_settings_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[CommandsNames.settings][user['lang']])


@router.message(Command(commands=CommandsNames.change_language))
async def process_change_language_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[CommandsNames.change_language][user['lang']],
                         reply_markup=create_change_language_keyboard())


@router.message(Command(commands=CommandsNames.cancel))
async def process_cancel_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['nothing_to_cancel'][user['lang']]
    )

# interactive commands


@router.message(Command(commands=CommandsNames.create_new_module))
async def process_new_module_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON[CommandsNames.create_new_module][user['lang']])
    await state.set_state(FSMCreatingModule.fill_name)

# callback query


@router.callback_query(LanguageSelectionCF.filter())
async def process_change_language_press(callback: CallbackQuery,
                                        callback_data: LanguageSelectionCF):
    new_lang: str = callback_data.language
    update_value(callback.from_user.id, {'lang': new_lang})
    await callback.answer(LEXICON['changed_language'][new_lang])


