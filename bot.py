import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from database.init_sql import init_local_database
from handlers import (other_handlers, base_commands_handler, saved_modules_handler,
                      settings_handler, repeating_module_handler, get_module_by_id_handler,
                      donate_handler, channel_posts_handler, feedback_handler, game_for_module_handler)
from handlers.creating_module import (creating_module_handler, prmt_module_handler, photo_module_handler,
                                       voice_module_handler)
from messages_keyboards.main_menu import set_main_menu
from middleware.middleware import AntiFloodMiddleware

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Загружаем конфиг в переменную config
config: Config = load_config()

# Инициализирует локальную базу данных с языками
init_local_database()

# Инициализируем бот и диспетчер
bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    dp = Dispatcher()
    dp.message.middleware(AntiFloodMiddleware())

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере

    # - Base
    dp.include_router(base_commands_handler.router)
    dp.include_router(settings_handler.router)
    dp.include_router(saved_modules_handler.router)
    dp.include_router(get_module_by_id_handler.router)

    # - Creating module
    dp.include_router(photo_module_handler.router)
    dp.include_router(voice_module_handler.router)
    dp.include_router(prmt_module_handler.router)
    dp.include_router(creating_module_handler.router)

    # - Repeating module
    dp.include_router(repeating_module_handler.router)
    dp.include_router(game_for_module_handler.router)

    # - Other
    dp.include_router(donate_handler.router)
    dp.include_router(channel_posts_handler.router)
    dp.include_router(feedback_handler.router)
    dp.include_router(other_handlers.router)
    

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=[])


if __name__ == '__main__':
    asyncio.run(main())
