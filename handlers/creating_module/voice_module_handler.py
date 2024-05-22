from __future__ import annotations

import os

from aiogram import F, Router, Dispatcher, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message

from FSM.fsm import FSMCreatingModule, creating_module_states
from config_data.user_restrictions import *
from database.database import *
from filters.CallbackDataFactory import DelPairFromNewModuleCF, RenameNewModuleCF, EditNewModuleSeparatorCF, \
    SaveNewModuleCF, SeparatorForPhotoCF, CancelTranslatingPhrasesCF, AutoTranslatePhrasesCF, AddPhrasesFromPhotoCF, \
    AddVoicePhraseCF, CancelVoiceCF
from messages_keyboards.new_module_kb import create_new_module_keyboard, create_separator_on_photo_keyboard, \
    translate_text_from_photo_keyboard, add_translated_phrases_keyboard, voice_keyboard
from lexicon.lexicon import CommandsNames, CREATING_MODULE_LEXICON
from keyboards.keyboards import get_main_keyboard
from services.auto_translate_service import *
from services.creating_module_service import add_new_pairs
from services.service import send_and_delete_message, download_photo, download_voice
from services.tesseract_service import get_eng_from_photo, clear_text, format_phrases_to_text
from services.get_voice_text_service import get_text_from_voice

router = Router()

# Отправлено голосовое сообщение
@router.message(StateFilter(FSMCreatingModule.fill_content), F.voice)
async def process_voice_sent(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    voice = message.voice

    data = await state.get_data()

    if data.get('cur_voice_path'):
        await message.delete()
        return

    path = await download_voice(voice.file_id)


    voice_message = await message.answer(text=CREATING_MODULE_LEXICON['choose_voice_lang'][user['lang']],
                                         reply_markup=voice_keyboard(user['lang']),
                                         reply_to_message_id=message.message_id)

    await state.update_data(cur_voice_path=path)
    await state.update_data(voice_id=message.message_id)
    await state.update_data(voice_message_id=voice_message.message_id)


@router.callback_query(AddVoicePhraseCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_got_text_from_voice(callback: CallbackQuery,
                                      callback_data: AddVoicePhraseCF,
                                      state: FSMContext,
                                      bot: Bot):
    data = await state.get_data()

    voice_text = get_text_from_voice(data['cur_voice_path'], callback_data.lang).lower()
    translated_voice_text = translate_phrase(voice_text,
                                             ('ru', 'en')[callback_data.lang == 'en-EN'],
                                             ('ru', 'en')[callback_data.lang == 'ru-RU']).lower()

    try:
        os.remove(data['cur_voice_path'])
    finally:
        await state.update_data(cur_voice_path="")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['voice_id'])
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['voice_message_id'])

    await add_new_pairs(state=state,
                        valid_pairs={voice_text: translated_voice_text},
                        chat_id=callback.from_user.id,
                        bot=bot)

    await callback.answer()


@router.callback_query(CancelVoiceCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_cancel_voice(callback: CallbackQuery,
                                             callback_data: CancelVoiceCF,
                                             state: FSMContext,
                                             bot: Bot):
    await callback.answer()

    data = await state.get_data()

    try:
        os.remove(data['cur_voice_path'])
    finally:
        await state.update_data(cur_voice_path="")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['voice_id'])
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['voice_message_id'])