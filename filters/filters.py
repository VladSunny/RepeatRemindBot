from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsChangeLanguage(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('lang')
