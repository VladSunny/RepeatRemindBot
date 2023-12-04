from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON, CommandsNames, SETTINGS_LEXICON
from FSM.fsm import FSMCreatingModule

from config_data.user_restrictions import *
from services.service import send_message

router = Router()

router.message.filter(StateFilter(default_state))


# message

# base commands


@router.message(lambda message: message.from_user.id not in get_users_chat_ids())
async def unregistered_user(message: Message):
    add_user(message.from_user.id)
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/start'][user['lang']])


@router.message(CommandStart())
async def process_start_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/start'][user['lang']])
    if message.from_user.id not in get_users_chat_ids():
        add_user(message.from_user.id)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(LEXICON['/help'][user['lang']])


@router.message(Command(commands=CommandsNames.cancel))
async def process_cancel_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(
        text=LEXICON['nothing_to_cancel'][user['lang']]
    )


# interactive commands


@router.message(Command(commands=CommandsNames.change_language))
async def process_change_language_command(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON[CommandsNames.change_language][user['lang']],
                         reply_markup=create_change_language_keyboard())


@router.message(Command(commands=CommandsNames.create_new_module))
async def process_new_module_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    if get_modules_number(message.from_user.id) >= max_modules:
        await message.answer(LEXICON['maximum_number_of_modules'][user['lang']])
    else:
        instruction_message = await send_message(chat_id=message.from_user.id,
                                                 text=LEXICON[CommandsNames.create_new_module][user['lang']])
        await state.update_data(instruction_message_id=instruction_message.message_id)
        await state.set_state(FSMCreatingModule.fill_name)


# callback query


@router.callback_query(LanguageSelectionCF.filter())
async def process_change_language_press(callback: CallbackQuery,
                                        callback_data: LanguageSelectionCF):
    new_lang: str = callback_data.language
    update_user(callback.from_user.id, {'lang': new_lang})
    await callback.answer(SETTINGS_LEXICON['changed_language'][new_lang])
