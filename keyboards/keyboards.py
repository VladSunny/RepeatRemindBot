from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from lexicon.lexicon import main_keyboard_lexicon


def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.row(*[KeyboardButton(text=item[lang]) for item in main_keyboard_lexicon.values()], width=2)

    kb_builder.add(KeyboardButton(text="Каталог", web_app=WebAppInfo(url="https://repeatremind.netlify.app/modules-library")))

    return ReplyKeyboardMarkup(keyboard=kb_builder.export(), resize_keyboard=True)


