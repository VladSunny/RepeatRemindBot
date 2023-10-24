from icecream import ic
import asyncio
import bot


async def send_and_delete_message(chat_id: int, text: str, delete_after: int):

    ic(1)

    # Отправляем сообщение
    message = await bot.bot.send_message(chat_id, text)

    # Ожидаем указанное количество секунд
    await asyncio.sleep(delete_after)

    # Удаляем сообщение
    await bot.bot.delete_message(chat_id, message.message_id)