import translators as ts
from icecream import ic


def translate_phrase(phrase: str) -> str:
    translation = ts.translate_text(query_text=phrase, from_language='en', to_language='ru')
    return translation


def translate_all_phrases_into_module_pairs(phrases: list[str]) -> dict[str, str]:
    items = {}

    for i in phrases:
        items[i] = translate_phrase(i).strip().lower()

    return items
