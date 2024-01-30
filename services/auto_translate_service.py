import translators as ts


#  Перевод фраз
def translate_phrase(phrase: str, from_lang: str, to_lang: str) -> str:
    translation = ts.translate_text(query_text=phrase, from_language=from_lang, to_language=to_lang)
    return translation


# Создание удобного словаря с переведенными фразами
def translate_all_phrases_into_module_pairs(phrases: list[str]) -> dict[str, str]:
    items = {}

    for i in phrases:
        items[i] = translate_phrase(i, 'en', 'ru').strip().lower()

    return items

