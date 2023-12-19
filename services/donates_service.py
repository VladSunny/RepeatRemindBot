from aiogram import Bot
from aiogram.types import Message, LabeledPrice
from environs import Env

from config_data.donates_config import *
from lexicon.lexicon import DONATE_LEXICON

env = Env()
env.read_env(None)

provider_token = env('PROVIDER_TOKEN')


async def send_donate_link(bot: Bot, message: Message, lang: str):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title=DONATE_LEXICON['title'][lang],
        description=DONATE_LEXICON['description'][lang],
        payload="Payment done",
        provider_token=provider_token,
        currency='rub',
        prices=[
            LabeledPrice(
                label=DONATE_LEXICON['donate_label'][lang],
                amount=coffee_donate
            )
        ],
        max_tip_amount=max_donate_amount,
        suggested_tip_amounts=suggested_donates_amounts,
        start_parameter='RepeatRemindBot',
        provider_data=None,
        request_timeout=15,
        allow_sending_without_reply=True
    )