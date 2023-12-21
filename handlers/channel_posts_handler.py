from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery

from keyboards import channel_posts_kb
from filters.CallbackDataFactory import SendPostFromChannelCF
from environs import Env
from database.database import get_all_settings

router = Router()


env = Env()
env.read_env(None)

owner_id = env("OWNER_ID")
channel_id = env("CHANNEL_ID")


@router.channel_post()
async def channel_post_process(post: Message, bot: Bot):
    if str(post.chat.id) != str(channel_id):
        return

    forward_post = await bot.forward_message(chat_id=owner_id, from_chat_id=channel_id, message_id=post.message_id)

    await bot.send_message(chat_id=owner_id,
                           text="Разослать пост?",
                           reply_to_message_id=forward_post.message_id,
                           reply_markup=channel_posts_kb.send_channel_post_keyboard(post_id=post.message_id)
                           )


@router.callback_query(SendPostFromChannelCF.filter())
async def send_post_to_users_process(callback: CallbackQuery,
                                     callback_data: SendPostFromChannelCF,
                                     bot: Bot):
    await callback.answer()

    users_settings = get_all_settings()

    for user in users_settings:
        if user['get_updates']:
            await bot.forward_message(
                chat_id=user['chat_id'],
                from_chat_id=channel_id,
                message_id=callback_data.post_id
            )

    await bot.edit_message_text(text="Пост разослан",
                                chat_id=owner_id,
                                message_id=callback.message.message_id,
                                reply_markup=None)

