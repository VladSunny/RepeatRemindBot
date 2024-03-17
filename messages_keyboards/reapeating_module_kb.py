from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.CallbackDataFactory import ConfirmRepeatingCF, MixWordsInRepeatingModuleCF, NextQuestionCF, \
    AnswerWasCorrectCF, BackToSavedModulesCF
from lexicon.lexicon import REPEATING_MODULE_LEXICON, SAVED_MODULES_LEXICON


# Кнопки для подтверждения повторения выбранного модуля
def confirm_repeating_keyboard(lang: str, module_id: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=SAVED_MODULES_LEXICON['back_to_saved_modules'][lang],
            callback_data=BackToSavedModulesCF().pack()
        ),
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


# Кнопки при неправильном ответе
def incorrect_answer_keyboard(lang: str):
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=REPEATING_MODULE_LEXICON['answer_was_correct'][lang],
            callback_data=AnswerWasCorrectCF().pack()
        ),
        InlineKeyboardButton(
            text=REPEATING_MODULE_LEXICON['next_question'][lang],
            callback_data=NextQuestionCF().pack()
        ),
        width=1
    )

    return kb_builder.as_markup()


# Кнопки при правильном ответе
def correct_answer_keyboard(lang: str):
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=REPEATING_MODULE_LEXICON['next_question'][lang],
            callback_data=NextQuestionCF().pack()
        ),
        width=1
    )

    return kb_builder.as_markup()
