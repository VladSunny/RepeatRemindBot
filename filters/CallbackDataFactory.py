from aiogram.filters.callback_data import CallbackData


class LanguageSelectionCF(CallbackData, prefix='lang'):
    language: str
