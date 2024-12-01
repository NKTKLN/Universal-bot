import asyncio
from aiogram import Bot, Dispatcher
from bot.db import add_user
from bot.config import config, logger
from bot.plugins import plugin_manager
from bot.handlers import register_handlers
from bot.db.database import create_db_and_tables


async def main() -> None:
    logger.info("Starting bot...")

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    plugin_manager.dispatcher = dp

    # Database initialization
    logger.info("Initializing database...")
    await create_db_and_tables()

    # Owner account creation
    await add_user(config.OWNER_ID, 3)
    logger.info("The owner account has been created.")

    # Handler registration
    register_handlers(dp)

    await plugin_manager.load_plugins()

    logger.info("Bot is up and running.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped.")
