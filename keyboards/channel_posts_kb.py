from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.CallbackDataFactory import SendPostFromChannelCF


def send_channel_post_keyboard(post_id: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text="Да ✅",
            callback_data=SendPostFromChannelCF(post_id=post_id).pack()
        )
    )

    return kb_builder.as_markup()
