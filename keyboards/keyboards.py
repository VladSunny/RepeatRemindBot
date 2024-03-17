from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from lexicon.lexicon import main_keyboard_lexicon


def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(*[item[lang] for item in main_keyboard_lexicon.values()])

    return kb_builder.as_markup()


