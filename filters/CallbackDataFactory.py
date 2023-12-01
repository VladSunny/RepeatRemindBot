from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


# New Module
class LanguageSelectionCF(CallbackData, prefix='lang'):
    language: str


class DelPairFromNewModuleCF(CallbackData, prefix='del_pair'):
    key: str


class RenameNewModuleCF(CallbackData, prefix='rename_new_module'):
    module_name: str


class EditNewModuleSeparatorCF(CallbackData, prefix='edit_new_module_separator'):
    module_name: str


class SaveNewModuleCF(CallbackData, prefix='save_new_module'):
    module_name: str


# Saved Modules
class OpenSavedModuleCF(CallbackData, prefix='open_saved_module'):
    module_id: int


class DeleteSavedModuleCF(CallbackData, prefix='delete_saved_module'):
    module_id: int
    module_name: str


class BackToSavedModulesCF(CallbackData, prefix='back_to_saved_modules'):
    pass


class EditModuleCF(CallbackData, prefix='edit_module'):
    module_id: int


class RepeatModuleCF(CallbackData, prefix='repeat_module'):
    module_id: int


# Repeating Module
class ConfirmRepeatingCF(CallbackData, prefix='confirmed_repeating_module'):
    module_id: int


class MixWordsInRepeatingModuleCF(CallbackData, prefix='shuffle_words_in_repeating_module'):
    module_id: int


class NextQuestionCF(CallbackData, prefix='next_question'):
    pass


class AnswerWasCorrectCF(CallbackData, prefix='answer_was_correct'):
    pass


class SeparatorForPhotoCF(CallbackData, prefix='separator_for_photo'):
    sep: str


class AutoTranslatePhrasesCF(CallbackData, prefix='auto_translate'):
    pass


class CancelTranslatingPhrasesCF(CallbackData, prefix='cancel_translating_phrases'):
    pass
