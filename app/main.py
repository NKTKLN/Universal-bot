import asyncio
from aiogram import Bot, Dispatcher
from app.config import config, logger
from app.db.database import create_db_and_tables
from app.handlers import register_handlers
from app.db import add_user
from app.plugins import load_plugins


async def main() -> None:
    logger.info("Starting bot...")

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Database initialization
    logger.info("Initializing database...")
    await create_db_and_tables()

    # Owner account creation
    await add_user(config.OWNER_ID, 3)
    logger.info("The owner account has been created.")

    # Handler registration
    register_handlers(dp)

    await load_plugins(dp)

    logger.info("Bot is up and running.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped.")
