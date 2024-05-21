from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


# Settings

# Callback для ивента "смена языка"
class LanguageSelectionCF(CallbackData, prefix='lang'):
    language: str


# Creating module --

# Callback для ивента "удаление пары из создаваемого модуля"
class DelPairFromNewModuleCF(CallbackData, prefix='del_pair'):
    key: str


# Callback для ивента "изменение названия модуля"
class RenameNewModuleCF(CallbackData, prefix='rename_new_module'):
    module_name: str


# Callback для ивента "изменение разделителя"
class EditNewModuleSeparatorCF(CallbackData, prefix='edit_new_module_separator'):
    module_name: str


# Callback для ивента "сохранение модуля"
class SaveNewModuleCF(CallbackData, prefix='save_new_module'):
    module_name: str


class SeparatorForPhotoCF(CallbackData, prefix='separator_for_photo'):
    sep: str


class AutoTranslatePhrasesCF(CallbackData, prefix='auto_translate'):
    pass


class CancelTranslatingPhrasesCF(CallbackData, prefix='cancel_translating_phrases'):
    pass


class AddPhrasesFromPhotoCF(CallbackData, prefix='add_translating_phrases'):
    pass


class AddVoicePhraseCF(CallbackData, prefix='add_voice_phrase'):
    lang: str


class CancelVoiceCF(CallbackData, prefix='cancel_voice'):
    pass


class GPTModuleCF(CallbackData, prefix='gpt_module'):
    pass


# Saved model --

# Callback для ивента "открытие сохраненного модуля"
class OpenSavedModuleCF(CallbackData, prefix='open_saved_module'):
    module_id: int


# Callback для ивента "удаление сохраненного модуля"
class DeleteSavedModuleCF(CallbackData, prefix='delete_saved_module'):
    module_id: int
    module_name: str


class GameForModuleCF(CallbackData, prefix='game_for_module'):
    module_id: int


class ChangeVisibilityModuleCF(CallbackData, prefix='change_visibility_module'):
    module_id: int


# Callback для ивента "возвращение к сохраненным модулям"
class BackToSavedModulesCF(CallbackData, prefix='back_to_saved_modules'):
    pass


# Callback для ивента "изменение модуля"
class EditModuleCF(CallbackData, prefix='edit_module'):
    module_id: int


# Repeating module --


# Callback для ивента "повторение модуля"
class RepeatModuleCF(CallbackData, prefix='repeat_module'):
    module_id: int


# Callback для ивента "подтверждение начала повторения модуля"
class ConfirmRepeatingCF(CallbackData, prefix='confirmed_repeating_module'):
    module_id: int


# Callback для ивента "перемешать слова в повторяемом модуле"
class MixWordsInRepeatingModuleCF(CallbackData, prefix='shuffle_words_in_repeating_module'):
    module_id: int


class NextQuestionCF(CallbackData, prefix='next_question'):
    pass


class AnswerWasCorrectCF(CallbackData, prefix='answer_was_correct'):
    pass

# Other --


class SendPostFromChannelCF(CallbackData, prefix='send_post'):
    post_id: int


class ChangeGetUpdatesCF(CallbackData, prefix='change_get_updates'):
    get_updates: bool


class ChangeShowInTableCF(CallbackData, prefix='change_show_in_donate_table'):
    show_in_donate_table: bool


class DonateCF(CallbackData, prefix='donate'):
    value: int

