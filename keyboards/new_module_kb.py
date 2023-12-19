from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.CallbackDataFactory import \
    DelPairFromNewModuleCF, RenameNewModuleCF, EditNewModuleSeparatorCF, SaveNewModuleCF, SeparatorForPhotoCF, \
    AutoTranslatePhrasesCF, CancelTranslatingPhrasesCF, AddPhrasesFromPhotoCF
from lexicon.lexicon import CREATING_MODULE_LEXICON


# Кнопки при создании нового модуля
def create_new_module_keyboard(content: dict[str, str], lang: str, module_name: str, separator: str) \
        -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    items = list(content.items())

    kb_builder.row(*[
        InlineKeyboardButton(
            text=f"{i + 1}. {items[i][0]} {separator} {items[i][1]}",
            callback_data=DelPairFromNewModuleCF(key=items[i][0]).pack()
        )
        for i in range(len(items))
    ],
                   # Кнопка для изменения названия модуля
                   InlineKeyboardButton(
                       text=CREATING_MODULE_LEXICON['rename_module_button'][lang],
                       callback_data=RenameNewModuleCF(module_name=module_name).pack()
                   ),
                   # Кнопка для изменения разделителя
                   InlineKeyboardButton(
                       text=CREATING_MODULE_LEXICON['edit_module_separator_button'][lang],
                       callback_data=EditNewModuleSeparatorCF(module_name=module_name).pack()
                   ),
                   InlineKeyboardButton(
                       text=CREATING_MODULE_LEXICON['finish_module_button'][lang],
                       callback_data=SaveNewModuleCF(module_name=module_name).pack()
                   ),
                   width=1
                   )

    return kb_builder.as_markup()


# Кнопки для выбора разделителя на фото
def create_separator_on_photo_keyboard(lang: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['cancel_getting_text_from_photo_button'][lang],
            callback_data=CancelTranslatingPhrasesCF().pack()
        ),
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['comma_button'][lang],
            callback_data=SeparatorForPhotoCF(sep=',').pack()
        ),
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['n_button'][lang],
            callback_data=SeparatorForPhotoCF(sep='\n').pack()
        ),
        width=1
    )

    return kb_builder.as_markup()


# Кнопки для автоматического перевода текста с фото
def translate_text_from_photo_keyboard(lang: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['cancel_translating_photo_button'][lang],
            callback_data=CancelTranslatingPhrasesCF().pack()
        ),
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['auto_translate_photo_button'][lang],
            callback_data=AutoTranslatePhrasesCF().pack()
        ),
        width=1
    )

    return kb_builder.as_markup()


# Кнопки для добавления переведенных фраз
def add_translated_phrases_keyboard(lang: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['cancel_adding_phrases_from_photo_button'][lang],
            callback_data=CancelTranslatingPhrasesCF().pack()
        ),
        InlineKeyboardButton(
            text=CREATING_MODULE_LEXICON['add_phrases_from_photo_button'][lang],
            callback_data=AddPhrasesFromPhotoCF().pack()
        ),
        width=1
    )

    return kb_builder.as_markup()
