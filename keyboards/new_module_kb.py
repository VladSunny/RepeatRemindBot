from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON, CREATING_MODULE_LEXICON

from filters.CallbackDataFactory import \
    DelPairFromNewModuleCF, RenameNewModuleCF, EditNewModuleSeparatorCF, SaveNewModuleCF, SeparatorForPhotoCF, \
    AutoTranslatePhrasesCF, CancelTranslatingPhrasesCF


def create_new_module_keyboard(content: dict[str, str], lang: str, module_name: str, separator: str) \
        -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
        InlineKeyboardButton(
            text=f"{pair[0]} {separator} {pair[1]}",
            callback_data=DelPairFromNewModuleCF(key=pair[0]).pack()
        )
        for pair in content.items()
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


def translate_text_from_photo(lang: str) -> InlineKeyboardMarkup:
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
