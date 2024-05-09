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
from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs, elements_to_text
from services.service import send_and_delete_message, download_photo, download_voice
from services.tesseract_service import get_eng_from_photo, clear_text, format_phrases_to_text
from services.get_voice_text_service import get_text_from_voice

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Шаблон словаря нового модуля
new_module_dict: dict[str, str | dict[str, str]] = {
    "name": "",
    "separator": "=",
    "content": {

    },
    "instruction_message_id": 0,
    "message_id": "",
    "is_editing": False,
    "editing_module_id": 0,
    "cur_photo_path": "",
    "cur_voice_path": "",
    "photo_id": "",
    "voice_id": "",
    "photo_message_id": 0,
    "voice_message_id": 0,
    "phrases_to_translate": []
}

router = Router()


# Отправка сообщения с информацией о новом модуле
async def send_new_module_info(chat_id, data, user, content, bot: Bot):
    new_keyboard = create_new_module_keyboard(
        content,
        user['lang'],
        data['name'],
        data['separator'])

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=data['message_id'],
                                text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].format(
                                    module_name=data['name'],
                                    separator=data['separator'],
                                    size='...'
                                ),
                                reply_markup=new_keyboard)
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=data['message_id'],
                                reply_markup=new_keyboard,
                                text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].
                                format(module_name=data['name'],
                                       separator=data['separator'],
                                       size=len(content)
                                       )
                                )


async def add_new_pairs(state, valid_pairs, chat_id, bot):
    data = await state.get_data()
    user = get_user(chat_id)

    valid_pairs = data['content'] | valid_pairs

    reach_local_max = False

    if len(valid_pairs) > max_local_items_in_module:
        valid_pairs = list(valid_pairs.items())[:max_local_items_in_module]
        valid_pairs = dict(valid_pairs)
        reach_local_max = True

    await state.update_data(content=valid_pairs)

    await send_new_module_info(chat_id, data, user, valid_pairs, bot)

    if reach_local_max:
        await send_and_delete_message(chat_id,
                                      CREATING_MODULE_LEXICON['max_local_items_in_module'][user['lang']],
                                      delete_after=7)
    elif len(valid_pairs) > max_items_in_module:
        await send_and_delete_message(chat_id,
                                      CREATING_MODULE_LEXICON['max_items_in_module'][user['lang']],
                                      delete_after=7)


# Отмена создания модуля
@router.message(Command(commands=CommandsNames.cancel), StateFilter(*creating_module_states))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)

    data = await state.get_data()

    # Удаление отправленного фото, если такое имеется
    try:
        if data.get('cur_photo_path'):
            os.remove(data['cur_photo_path'])
    finally:
        if data.get('is_editing'):
            await message.answer(
                text=CREATING_MODULE_LEXICON['cancel_editing_module'][user['lang']],
                reply_markup=get_main_keyboard(user['lang'])
            )
        else:
            await message.answer(
                text=CREATING_MODULE_LEXICON['cancel_creating_module'][user['lang']],
                reply_markup=get_main_keyboard(user['lang'])
            )

        await state.clear()


# Отправлено имя
@router.message(StateFilter(FSMCreatingModule.fill_name))
async def process_name_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    if (message.text is None) or (not is_valid_name(message.text)):
        await message.delete()
        await send_and_delete_message(
            chat_id=message.chat.id,
            text=CREATING_MODULE_LEXICON['not_valid_name'][user['lang']],
            delete_after=5
        )
        return

    await message.delete()

    data = await state.get_data()

    new_user_module = deepcopy(new_module_dict)
    new_user_module['name'] = message.text
    new_user_module['name'] = message.text
    new_user_module['instruction_message_id'] = data['instruction_message_id']

    await state.update_data(new_user_module)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=data['instruction_message_id'],
        text=CREATING_MODULE_LEXICON['fill_content'][user['lang']],
    )

    msg = await message.answer(
        text=CREATING_MODULE_LEXICON['new_module_info'][user['lang']].format(module_name=data['name'],
                                                                             separator=data['separator'],
                                                                             size=len(data['content'])),
        reply_markup=create_new_module_keyboard({}, user['lang'], data['name'], data['separator'])
    )

    await state.update_data(message_id=msg.message_id)


# Отправлен контент для нового модуля
@router.message(StateFilter(FSMCreatingModule.fill_content), F.text)
async def process_content_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.chat.id)

    await message.delete()

    data = await state.get_data()

    new_pairs, has_mistake = get_valid_pairs(message.text, data['separator'])

    await add_new_pairs(state=state, valid_pairs=new_pairs, chat_id=message.from_user.id, bot=bot)

    if has_mistake:
        await send_and_delete_message(message.chat.id,
                                      CREATING_MODULE_LEXICON['incorrect_pair'][user['lang']].format(
                                          separator=data['separator']), 7)


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


# Отправлено новое имя
@router.message(StateFilter(FSMCreatingModule.change_name))
async def process_new_name_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    await message.delete()

    if (message.text is None) or (not is_valid_name(message.text)):
        await send_and_delete_message(
            chat_id=message.chat.id,
            text=CREATING_MODULE_LEXICON['not_valid_name'][user['lang']],
            delete_after=5
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await send_new_module_info(message.from_user.id, data, user, data['content'], bot)

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['new_module_was_renamed'][user['lang']],
                                  delete_after=3
                                  )


# Отправлен новый разделитель
@router.message(StateFilter(FSMCreatingModule.change_separator))
async def process_new_separator_sent(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)

    await message.delete()

    if (message.text is None) or (not is_valid_separator(message.text)):
        await send_and_delete_message(
            chat_id=message.chat.id,
            text=CREATING_MODULE_LEXICON['not_valid_separator'][user['lang']],
            delete_after=5
        )
        return

    await state.update_data(separator=message.text)
    await state.set_state(FSMCreatingModule.fill_content)

    data = await state.get_data()

    await send_new_module_info(message.from_user.id, data, user, data['content'], bot)

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['seperator_was_changed'][user['lang']],
                                  delete_after=3
                                  )


# Удаление пары из модуля
@router.callback_query(DelPairFromNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_delete_pair(callback: CallbackQuery,
                              callback_data: DelPairFromNewModuleCF,
                              state: FSMContext,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    key: str = callback_data.key

    data = await state.get_data()
    content: dict[str, str] = data['content']

    deleted_pair: str = f"{key} {data['separator']} {content[key]}"

    content.pop(key)

    await state.update_data(content=content)
    await callback.answer(
        CREATING_MODULE_LEXICON['deleted_pair_from_new_model'][user['lang']].format(deleted_pair=deleted_pair))

    await send_new_module_info(callback.from_user.id, data, user, data['content'], bot)


# Переименование модуля
@router.callback_query(RenameNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_change_name(callback: CallbackQuery,
                              callback_data: RenameNewModuleCF,
                              state: FSMContext,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=data['message_id'],
                                reply_markup=None,
                                text=CREATING_MODULE_LEXICON['rename_new_module'][user['lang']]
                                )

    await state.set_state(FSMCreatingModule.change_name)


# Изменение разделителя у модуля
@router.callback_query(EditNewModuleSeparatorCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_change_separator(callback: CallbackQuery,
                                   callback_data: EditNewModuleSeparatorCF,
                                   state: FSMContext,
                                   bot: Bot):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=data['message_id'],
                                reply_markup=None,
                                text=CREATING_MODULE_LEXICON['edit_separator'][user['lang']]
                                )

    await state.set_state(FSMCreatingModule.change_separator)


# Сохранение модуля
@router.callback_query(SaveNewModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_save_module(callback: CallbackQuery,
                              callback_data: SaveNewModuleCF,
                              state: FSMContext,
                              bot: Bot):
    user = get_user(callback.from_user.id)
    module_name = callback_data.module_name

    data = await state.get_data()

    if len(data['content']) > max_items_in_module:
        await callback.answer(text=CREATING_MODULE_LEXICON['cant_save_module_qz_max_elements'][user['lang']],
                              show_alert=True)

        return

    module = save_module(chat_id=callback.from_user.id, data=data)

    if data['is_editing']:
        delete_saved_module(data['editing_module_id'])
    else:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=data['instruction_message_id'])

    await state.clear()

    await bot.send_message(chat_id=callback.from_user.id,
                           text=CREATING_MODULE_LEXICON['module_saved'][user['lang']].format(module_name=module_name,
                                                                                             module_id=module['id']),
                           reply_markup=get_main_keyboard(user['lang']))

    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['message_id'])


# Непредусмотренная команда
@router.message(StateFilter(*creating_module_states))
async def process_unintended_command(message: Message):
    user = get_user(message.from_user.id)

    await send_and_delete_message(chat_id=message.chat.id,
                                  text=CREATING_MODULE_LEXICON['unintended_creating_module'][user['lang']],
                                  delete_after=4)

    await message.delete()
