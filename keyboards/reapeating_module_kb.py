from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON, REPEATING_MODULE_LEXICON

from filters.CallbackDataFactory import ConfirmRepeatingCF, MixWordsInRepeatingModuleCF, NextQuestionCF,\
    AnswerWasCorrectCF
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
