from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery

from database.database import *
from lexicon.lexicon import CommandsNames, DONATE_LEXICON
from services.donates_service import send_donate_link

router = Router()


@router.message(Command(commands=CommandsNames.donate))
async def process_pay_command(message: Message, bot: Bot):
    user = get_user(message.from_user.id)

    await send_donate_link(bot=bot, message=message, lang=user['lang'])


@router.pre_checkout_query()
async def pre_checkout_query_process(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(DONATE_LEXICON['thanks_for_support'][user['lang']])