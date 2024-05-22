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
from filters.CallbackDataFactory import SeparatorForPhotoCF, CancelTranslatingPhrasesCF, AutoTranslatePhrasesCF, \
    AddPhrasesFromPhotoCF
from messages_keyboards.new_module_kb import create_separator_on_photo_keyboard, \
    translate_text_from_photo_keyboard, add_translated_phrases_keyboard
from lexicon.lexicon import CREATING_MODULE_LEXICON
from services.auto_translate_service import *
from services.creating_module_service import elements_to_text, add_new_pairs
from services.service import download_photo
from services.tesseract_service import get_eng_from_photo, clear_text, format_phrases_to_text

router = Router()


# Отправлено фото
@router.message(StateFilter(FSMCreatingModule.fill_content), F.photo)
async def process_photo_sent(message: Message, state: FSMContext):
    user = get_user(message.chat.id)

    photo = message.photo[-1]

    data = await state.get_data()

    # Если уже есть отправленное фото, то выходим с функции
    if data.get('cur_photo_path'):
        await message.delete()
        return

    # Скачиваем фото
    path = await download_photo(photo.file_id)

    # Сохраняем путь к нему
    await state.update_data(cur_photo_path=path)

    photo_message = await message.answer(
        text=CREATING_MODULE_LEXICON['sent_first_photo'][user['lang']],
        reply_markup=create_separator_on_photo_keyboard(user['lang']),
        reply_to_message_id=message.message_id
    )

    await state.update_data(photo_message_id=photo_message.message_id)
    await state.update_data(photo_id=message.message_id)


# Получить текст с фото
@router.callback_query(SeparatorForPhotoCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_got_text_from_photo(callback: CallbackQuery,
                                      callback_data: SeparatorForPhotoCF,
                                      state: FSMContext,
                                      bot: Bot):
    user = get_user(callback.from_user.id)
    separator = callback_data.sep

    data = await state.get_data()
    path = data['cur_photo_path']

    text = await get_eng_from_photo(path)  # получение текста
    clean_phrases = clear_text(text, separator)  # очистка полученного текста

    clean_mes_text = format_phrases_to_text(clean_phrases)  # создание из полученных фраз текста для сообщения

    await callback.answer()

    await state.update_data(phrases_to_translate=clean_phrases)  # сохраняем полученные фразы

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=data['photo_message_id'],
                                text=CREATING_MODULE_LEXICON['got_text_from_photo'][user['lang']]
                                .format(phrases=clean_mes_text),
                                reply_markup=translate_text_from_photo_keyboard(user['lang']))
    

# Автоматический перевод полученных фраз с фото
@router.callback_query(AutoTranslatePhrasesCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_auto_translate_phrases(callback: CallbackQuery,
                                         callback_data: AutoTranslatePhrasesCF,
                                         state: FSMContext,
                                         bot: Bot):
    user = get_user(callback.from_user.id)

    data = await state.get_data()
    translated_phrases = translate_all_phrases_into_module_pairs(data['phrases_to_translate'])  # перевод
    translated_phrases_text = elements_to_text(translated_phrases, separator=data['separator'])

    await callback.answer()
    await state.update_data(phrases_to_translate=translated_phrases)

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=data['photo_message_id'],
                                text=CREATING_MODULE_LEXICON['translated_text'][user['lang']]
                                .format(content=translated_phrases_text),
                                reply_markup=add_translated_phrases_keyboard(user['lang']))



# Добавление переведенных фраз
@router.callback_query(AddPhrasesFromPhotoCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_add_translated_phrases(callback: CallbackQuery,
                                         callback_data: AddPhrasesFromPhotoCF,
                                         state: FSMContext,
                                         bot: Bot):
    data = await state.get_data()

    new_pairs = data['phrases_to_translate']

    await bot.delete_message(callback.from_user.id, data['photo_id'])
    await bot.delete_message(callback.from_user.id, data['photo_message_id'])
    await state.update_data(cur_photo_path="")

    await add_new_pairs(state=state, valid_pairs=new_pairs, chat_id=callback.from_user.id, bot=bot)

    await callback.answer()


# Отмена действий с фото
@router.callback_query(CancelTranslatingPhrasesCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_cancel_translating_phrases(callback: CallbackQuery,
                                             callback_data: CancelTranslatingPhrasesCF,
                                             state: FSMContext,
                                             bot: Bot):
    await callback.answer()

    data = await state.get_data()

    # Удаляем фото если оно есть
    try:
        os.remove(data['cur_photo_path'])
    finally:
        await state.update_data(cur_photo_path="")
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['photo_id'])
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['photo_message_id'])
