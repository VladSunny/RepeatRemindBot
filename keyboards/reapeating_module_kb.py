from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON, REPEATING_MODULE_LEXICON

from filters.CallbackDataFactory import ConfirmRepeatingCF, MixWordsInRepeatingModuleCF
from icecream import ic

import json


def confirm_repeating_keyboard(lang: str, module_id: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()


    kb_builder.row(
        InlineKeyboardButton(
            text=REPEATING_MODULE_LEXICON['mix_words'][lang],
            callback_data=MixWordsInRepeatingModuleCF(module_id=module_id).pack()
        ),
        InlineKeyboardButton(
            text=REPEATING_MODULE_LEXICON['confirm_repeating'][lang],
            callback_data=ConfirmRepeatingCF(module_id=module_id).pack()
        ),
        width=1
    )

    return kb_builder.as_markup()
