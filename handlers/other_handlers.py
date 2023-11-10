from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon import lexicon
from services.service import send_and_delete_message

from icecream import ic

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message, state: FSMContext):
    ic(await state.get_state())
    await message.delete()
    await send_and_delete_message(message.from_user.id, lexicon.LEXICON['default_response']['en'], 4)
