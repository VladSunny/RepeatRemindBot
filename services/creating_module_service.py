from __future__ import annotations

import re

from config_data.user_restrictions import max_name_length, max_element_length, max_key_length


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
        if (len(pair) != 2) or (len(pair[0]) >= max_key_length) or (len(pair[0]) + len(pair[1]) > max_element_length):
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
