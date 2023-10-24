from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

from filters.CallbackDataFactory import LanguageSelectionCF


def create_change_language_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
        InlineKeyboardButton(
            text=LEXICON['language'][button],
            callback_data=LanguageSelectionCF(language=button).pack()
        )
        for button in LEXICON['language'].keys()
    ])

    return kb_builder.as_markup()
