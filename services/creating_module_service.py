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


def is_valid_pairs(pairs: str) -> dict[str, str] | None:
    pairs = ic(pairs.split('\n'))
    return None
