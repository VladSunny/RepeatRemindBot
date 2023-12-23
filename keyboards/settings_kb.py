from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.CallbackDataFactory import ChangeGetUpdatesCF, ChangeShowInTableCF
from lexicon.lexicon import SETTINGS_LEXICON


# Кнопки для смены языка
def create_settings_keyboard(get_updates: bool, show_in_donate_table: bool, lang: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=SETTINGS_LEXICON['get_updates'][lang] + ('❌', '✅')[get_updates],
            callback_data=ChangeGetUpdatesCF(get_updates=get_updates).pack()
        ),
        InlineKeyboardButton(
            text=SETTINGS_LEXICON['show_in_donate_table'][lang] + ('❌', '✅')[show_in_donate_table],
            callback_data=ChangeShowInTableCF(show_in_donate_table=show_in_donate_table).pack()
        ),
        width=1
    )

    return kb_builder.as_markup()
