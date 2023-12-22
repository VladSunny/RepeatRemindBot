from aiogram import Bot
from aiogram.types import Message, LabeledPrice
from environs import Env
import json

from config_data.donates_config import *
from lexicon.lexicon import DONATE_LEXICON
from icecream import ic

env = Env()
env.read_env(None)

provider_token = env('PROVIDER_TOKEN')

with open("config_data/receipt.json", "r", encoding='utf-8') as my_file:
    str_receipt = my_file.read()


async def send_donate_link(bot: Bot, chat_id: int, lang: str, amount: int):
    json_receipt = json.loads(str_receipt)
    json_receipt['receipt']['items'][0]['amount']['value'] = str(amount) + '.00'

    await bot.send_invoice(
        chat_id=chat_id,
        title=DONATE_LEXICON['title'][lang],
        description=DONATE_LEXICON['description'][lang],
        payload="Payment done",
        provider_token=provider_token,
        currency='rub',
        prices=[
            LabeledPrice(
                label=DONATE_LEXICON['donate_label'][lang],
                amount=amount * 100
            )
        ],
        max_tip_amount=None,
        # max_tip_amount=max_donate_amount,
        # suggested_tip_amounts=suggested_donates_amounts,
        start_parameter='RepeatRemindBot',
        provider_data=json.dumps(json_receipt, ensure_ascii=False),
        request_timeout=15,
        allow_sending_without_reply=True,
        need_email=True,
        send_email_to_provider=True,
    )
