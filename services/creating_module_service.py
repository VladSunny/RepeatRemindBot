from __future__ import annotations

import re

from aiogram import Bot
from config_data.user_restrictions import max_name_length, max_element_length, max_key_length
from config_data.user_restrictions import *
from database.database import *
from lexicon.lexicon import CREATING_MODULE_LEXICON
from services.auto_translate_service import *
from services.service import send_and_delete_message
from messages_keyboards.new_module_kb import create_new_module_keyboard


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
    "phrases_to_translate": [],
    "gpt_module": None,
    "gpt_message_id":0,
    "prompt_message_id":0
}


# Проверка имени
def is_valid_name(name: str) -> bool:
    pattern = r'^[a-zA-Z0-9 ]+$'
    return bool(re.match(pattern, name)) and len(name) <= max_name_length


# Проверка разделителя
def is_valid_separator(separator: str) -> bool:
    if len(separator) > 1:
        return False

    pattern = r'^[^a-zA-Z0-9а-яА-Я]$'
    return bool(re.match(pattern, separator))


# Получить пары ключ-значение из отправленного сообщения
def get_valid_pairs(pairs: str, separator: str) -> tuple[dict[str, str], bool]:
    pairs: list[str] = pairs.split('\n')

    valid_pairs: dict[str, str] = {}

    has_mistake: bool = False

    for pair in pairs:
        pair = pair.split(f' {separator} ')
        if (len(pair) != 2) or (len(pair[0]) > max_key_length) or (len(pair[0]) + len(pair[1]) > max_element_length):
            has_mistake = True
            continue
        valid_pairs[pair[0].strip()] = pair[1].strip()

    return valid_pairs, has_mistake


# Перевести словарь с парами в текст
def elements_to_text(elements: dict[str, str], separator: str) -> str:
    text = ""
    items = list(elements.items())
    for i in range(len(elements)):
        text += f"{i + 1}. {items[i][0]} {separator} {items[i][1]}\n"

    return text

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


async def add_new_pairs(state, valid_pairs: dict, chat_id, bot):
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
