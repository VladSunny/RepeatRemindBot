from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import SETTINGS_LEXICON

from filters.CallbackDataFactory import LanguageSelectionCF


# Кнопки для смены языка
def create_change_language_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
        InlineKeyboardButton(
            text=SETTINGS_LEXICON['language'][button],
            callback_data=LanguageSelectionCF(language=button).pack()
        )
        for button in SETTINGS_LEXICON['language'].keys()
    ])

    return kb_builder.as_markup()
