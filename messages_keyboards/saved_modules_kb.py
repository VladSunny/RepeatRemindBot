from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.CallbackDataFactory import OpenSavedModuleCF, \
    DeleteSavedModuleCF, \
    BackToSavedModulesCF, \
    EditModuleCF, \
    RepeatModuleCF, \
    GameForModuleCF, \
    ChangeVisibilityModuleCF
from lexicon.lexicon import SAVED_MODULES_LEXICON


# Список сохраненных модулей в виде кнопок
def list_of_saved_modules_keyboard(modules: list[tuple[str, int]]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[
        InlineKeyboardButton(
            text=f"{module[0]}_id:{module[1]}",
            callback_data=OpenSavedModuleCF(module_id=module[1]).pack()
        )
        for module in modules
    ],
                   width=1
                   )

    return kb_builder.as_markup()


# Кнопки для выбранного сохраненного модуля
def module_info_keyboard(lang: str, module_id: int, module_name: str, public: bool) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['repeat_module'][lang],
            callback_data=RepeatModuleCF(module_id=module_id).pack()
        ),
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['game_of_module'][lang],
            callback_data=GameForModuleCF(module_id=module_id).pack()
        ),
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['edit_saved_module'][lang],
            callback_data=EditModuleCF(module_id=module_id).pack()
        ),
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['delete_module'][lang],
            callback_data=DeleteSavedModuleCF(module_id=module_id, module_name=module_name).pack()
        ),
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['visibility_of_module'][lang].format(visibility="🔓" if public else "🔒"),
            callback_data=ChangeVisibilityModuleCF(module_id=module_id).pack()
        ),
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['back_to_saved_modules'][lang],
            callback_data=BackToSavedModulesCF().pack()
        ),
        width=1
    )

    return kb_builder.as_markup()
