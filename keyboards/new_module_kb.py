from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

from filters.CallbackDataFactory import \
    DelPairFromNewModuleCF, RenameNewModuleCF, EditNewModuleSeparatorCF, SaveNewModuleCF


def create_new_module_keyboard(content: dict[str, str], lang: str, module_name: str, separator: str)\
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
            text=LEXICON['rename_module_button'][lang],
            callback_data=RenameNewModuleCF(module_name=module_name).pack()
        ),
        # Кнопка для изменения разделителя
        InlineKeyboardButton(
            text=LEXICON['edit_module_separator_button'][lang],
            callback_data=EditNewModuleSeparatorCF(module_name=module_name).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON['finish_module_button'][lang],
            callback_data=SaveNewModuleCF(module_name=module_name).pack()
        ),
        width=1
    )

    return kb_builder.as_markup()
