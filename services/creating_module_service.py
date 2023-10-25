from __future__ import annotations

import re

from icecream import ic


def is_valid_name(name: str) -> bool:
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, name))


def is_valid_separator(separator: str) -> bool:
    if len(separator) > 1:
        return False

    pattern = r'^[^a-zA-Z0-9а-яА-Я]$'
    return bool(re.match(pattern, separator))


def get_valid_pairs(pairs: str, separator: str) -> dict[str, str] | None:
    pairs: list[str] = pairs.split('\n')

    valid_pairs: dict[str, str] = {}

    for pair in pairs:
        pair = pair.split(f' {separator} ')
        if len(pair) != 2:
            return None
        valid_pairs[pair[0]] = pair[1]

    return valid_pairs
