from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


# Функция, генерирующая клавиатуру для страницы книги
def create_change_language_keyboard() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[
        InlineKeyboardButton(text=LEXICON['language'][button],
                             callback_data=button+"lang")
        for button in LEXICON['language'].keys()
    ])

    print([button for button in LEXICON['language'].keys()])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
