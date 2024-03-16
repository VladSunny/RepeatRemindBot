from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from FSM.fsm import FSMFeedback
from config_data.user_restrictions import *
from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF
from keyboards.change_language_kb import create_change_language_keyboard
from lexicon.lexicon import LEXICON, CommandsNames, SETTINGS_LEXICON


from aiogram import Router, Dispatcher, Bot
from aiogram.filters import Command, StateFilter
import time

env = Env()
env.read_env(None)

feedback_counter: dict[str, any] = {}

owner_id = env("OWNER_ID")

router = Router()


@router.message(Command(commands=CommandsNames.send_feedback))
async def process_feedback_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    chat_id = str(message.from_user.id)

    if feedback_counter.get(chat_id) is not None:
        if time.time() - feedback_counter[chat_id]['time'] >= 60 * 60 * 24:
            feedback_counter[chat_id]['time'] = time.time()
            feedback_counter[chat_id]['feedbacks'] = 0

        if feedback_counter[chat_id]['feedbacks'] >= 5:
            await message.answer(LEXICON['feedbacks_limit'][user['lang']])
            await state.clear()
            return

        feedback_counter[chat_id]['feedbacks'] += 1
    else:
        feedback_counter[chat_id] = {'feedbacks': 1, 'time': time.time()}

    await message.answer(LEXICON[CommandsNames.send_feedback][user['lang']])
    await state.set_state(FSMFeedback.send_feedback)


@router.message(StateFilter(FSMFeedback.send_feedback))
async def process_feedback_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    await bot.send_message(chat_id=owner_id,
                           text=f"{message.from_user}\n\n{message.text}")

    await message.answer(LEXICON["feedback_sent"][user['lang']])
    await state.clear()
