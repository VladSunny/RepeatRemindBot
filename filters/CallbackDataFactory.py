from aiogram.filters.callback_data import CallbackData


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
