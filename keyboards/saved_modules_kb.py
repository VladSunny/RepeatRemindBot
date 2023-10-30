from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON, CREATING_MODULE_LEXICON

from filters.CallbackDataFactory import OpenSavedModuleCF


def list_of_saved_modules_keyboard(modules: list[tuple[str, int]]) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
        InlineKeyboardButton(
            text=f"{module[0]}_id:{module[1]}",
            callback_data=OpenSavedModuleCF(module_name=module[0], id=module[1]).pack()
        )
        for module in modules
        ],
        width=1
    )

    return kb_builder.as_markup()
