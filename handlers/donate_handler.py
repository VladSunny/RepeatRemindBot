from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery
from aiogram.methods.get_chat import GetChat

from database.database import *
from lexicon.lexicon import CommandsNames, DONATE_LEXICON
from services.donates_service import send_donate_link
from keyboards.donate_kb import create_donate_keyboard
from filters.CallbackDataFactory import DonateCF
from environs import Env

# Читаем Env
env = Env()
env.read_env(None)

provider_token: str = env("PROVIDER_TOKEN")
owner_chat_id: int = env("OWNER_ID")

router = Router()


# Команда /donate
@router.message(Command(commands=CommandsNames.donate))
async def process_pay_command(message: Message, bot: Bot):
    user = get_user(message.from_user.id)

    donaters: list = sorted(get_donaters(), reverse=True)  # Получаем список кортежей вида (общая сумма донатов, chat_id)

    donaters_text = DONATE_LEXICON['donaters_table'][user['lang']]
    successful_donaters_count = 0

    if len(donaters):
        for donater in donaters:
            try:
                chat = await bot(GetChat(chat_id=donater[1]))
                successful_donaters_count += 1
                donaters_text += f"{successful_donaters_count}. {chat.first_name} - {donater[0]}₽\n"
            except Exception as e:
                continue

        await message.answer(
            text=donaters_text
        )

    await message.answer(
        text=DONATE_LEXICON['choose_value'][user['lang']],
        reply_markup=create_donate_keyboard()
    )


# Пользователь выбрал сумму для доната
@router.callback_query(DonateCF.filter())
async def process_chose_donate(callback: CallbackQuery,
                               callback_data: DonateCF,
                               bot: Bot):
    await callback.message.delete()

    user = get_user(callback.from_user.id)

    await send_donate_link(bot=bot, chat_id=callback.from_user.id, lang=user['lang'], amount=callback_data.value)


# Подтверждение доната
@router.pre_checkout_query()
async def pre_checkout_query_process(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Донат был успешно совершен
@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user = get_user(message.from_user.id)

    if "TEST" in provider_token:
        if str(message.from_user.id) != str(owner_chat_id):
            return

    user_donate(message.from_user.id, message.successful_payment.total_amount // 100)

    await message.answer(DONATE_LEXICON['thanks_for_support'][user['lang']])
