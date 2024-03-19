import translators as ts


#  Перевод фраз
def translate_phrase(phrase: str, from_lang: str, to_lang: str) -> str:
    translation = ts.translate_text(query_text=phrase, from_language=from_lang, to_language=to_lang)
    return translation


# Создание удобного словаря с переведенными фразами
def translate_all_phrases_into_module_pairs(phrases: list[str]) -> dict[str, str]:
    items = {}

    phrases_line = '. '.join(phrases)
    translated_phrases: list[str] = translate_phrase(phrases_line, 'en', 'ru').strip().lower().split('. ')

    for i in range(len(phrases)):
         items[phrases[i]] = translated_phrases[i]

    return items

