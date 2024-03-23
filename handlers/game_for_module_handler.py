from __future__ import annotations

from aiogram import Router, Bot, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from filters.CallbackDataFactory import GameForModuleCF
from database.database import *

router = Router()
router.message.filter(StateFilter(default_state))

env = Env()
env.read_env(None)


GAME_SHORT_NAME = env("GAME_SHORT_NAME")
game_message_ids = {}


@router.callback_query(GameForModuleCF.filter())
async def process_mix_words_in_repeating_module(callback: CallbackQuery,
                                                callback_data: GameForModuleCF,
                                                state: FSMContext,
                                                bot: Bot):
    user = get_user(callback.from_user.id)
    module_id = callback_data.module_id
    chat_id = callback.from_user.id

    await state.update_data(module_id=module_id)

    game_message = await bot.send_game(chat_id=chat_id, game_short_name=GAME_SHORT_NAME)
    # Сохраняем message_id в словарь с ключом по user_id
    game_message_ids[chat_id] = game_message.message_id

    await callback.answer()


@router.callback_query(lambda call: call.game_short_name == GAME_SHORT_NAME)
async def query_inline_game(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback_query.from_user.id
    game_message_id = game_message_ids.get(user_id)
    data = await state.get_data()

    # Базовый URL игры
    game_url = f'https://repeatclicker.netlify.app/repeat-remind-game?module_id={data["module_id"]}'

    # Для inline сообщений добавляем inline_message_id, иначе добавляем chat_id
    if callback_query.inline_message_id:
        game_url += f'&inline_message_id={callback_query.inline_message_id}'
    else:
        game_url += f'&chat_id={callback_query.message.chat.id}&game_id={game_message_id}'

    # Ответ на callback_query с URL игры
    await bot.answer_callback_query(callback_query.id, url=game_url)

