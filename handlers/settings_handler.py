from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON, CommandsNames, SETTINGS_LEXICON
from FSM.fsm import FSMChangeSettings

from services.settings_service import is_valid_words_in_block, is_valid_repetitions_for_block
from services.service import send_and_delete_message

router = Router()


@router.message(Command(commands=CommandsNames.change_words_in_block), StateFilter(default_state))
async def process_change_words_in_block_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON[CommandsNames.change_words_in_block][user['lang']])

    await state.set_state(FSMChangeSettings.change_words_in_block)


@router.message(Command(commands=CommandsNames.change_repetitions_for_block), StateFilter(default_state))
async def process_change_repetitions_for_block_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(SETTINGS_LEXICON[CommandsNames.change_repetitions_for_block][user['lang']])

    await state.set_state(FSMChangeSettings.change_repetitions_for_block)


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

    await message.answer(SETTINGS_LEXICON['sent_new_words_in_block'][user['lang']])

    await state.clear()


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

    await message.answer(SETTINGS_LEXICON['sent_new_repetitions_for_block'][user['lang']])

    await state.clear()
