from aiogram import Router
from aiogram.types import Message
from lexicon import lexicon

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(lexicon.LEXICON['default_response']['en'])
