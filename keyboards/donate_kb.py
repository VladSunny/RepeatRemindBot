from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.CallbackDataFactory import DonateCF
from config_data.donates_config import suggested_donates_amounts
from lexicon.lexicon import DONATE_LEXICON


def create_donate_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
        InlineKeyboardButton(
            text=str(donate) + "₽",
            callback_data=DonateCF(value=donate).pack()
        )
        for donate in suggested_donates_amounts],
        width=3
    )

    return kb_builder.as_markup()
