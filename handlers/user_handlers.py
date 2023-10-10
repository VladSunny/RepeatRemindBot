from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import *

from lexicon.lexicon import LEXICON

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])
    if message.from_user.id not in get_users():
        add_user(message.from_user.id)


@router.message(lambda message: message.from_user.id not in get_users())
async def unregistered_user(message: Message):
    await message.answer(LEXICON['/start']['en'])
    add_user(message.from_user.id)


@router.message(lambda message: not is_user_updated(message.from_user.id))
async def unregistered_user(message: Message):
    await message.answer(LEXICON['not_updated_user']['en'])
    update_user(message.from_user.id)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text]['en'])
