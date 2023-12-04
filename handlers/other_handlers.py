from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon import lexicon
from services.service import send_and_delete_message
from database.database import get_user
from icecream import ic

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def process_default_response(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.delete()
    await send_and_delete_message(message.from_user.id, lexicon.LEXICON['default_response'][user['lang']], 4)
