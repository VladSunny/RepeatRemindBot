from aiogram import Router
from aiogram.types import Message
from lexicon import lexicon
from services.service import send_and_delete_message

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await send_and_delete_message(message.from_user.id, lexicon.LEXICON['default_response']['en'], 4)
