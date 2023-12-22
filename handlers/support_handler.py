from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery

from database.database import *
from lexicon.lexicon import CommandsNames, DONATE_LEXICON
from services.donates_service import send_donate_link
from keyboards.donate_kb import create_donate_keyboard
from filters.CallbackDataFactory import DonateCF

router = Router()


@router.message(Command(commands=CommandsNames.donate))
async def process_pay_command(message: Message, bot: Bot):
    user = get_user(message.from_user.id)

    await bot.send_message(
        chat_id=message.from_user.id,
        text=DONATE_LEXICON['choose_value'][user['lang']],
        reply_markup=create_donate_keyboard()
    )


@router.callback_query(DonateCF.filter())
async def process_chose_donate(callback: CallbackQuery,
                               callback_data: DonateCF,
                               bot: Bot):
    await callback.message.delete()

    user = get_user(callback.from_user.id)

    await send_donate_link(bot=bot, chat_id=callback.from_user.id, lang=user['lang'], amount=callback_data.value)


@router.pre_checkout_query()
async def pre_checkout_query_process(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user = get_user(message.from_user.id)
    await message.answer(DONATE_LEXICON['thanks_for_support'][user['lang']])