import asyncio
import argparse
from aiogram.enums import ParseMode
from bot.db import add_user
from bot.config import config, logger
from bot.plugins import plugin_manager
from bot.handlers import register_handlers
from bot.db.database import create_db_and_tables
from bot.loader import plugin_manager, bot, dp


# Function to parse command-line arguments
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bot reboot")
    parser.add_argument('--user_id', type=int, help='User ID', default=None)
    return parser.parse_args()


# Main bot initialization and startup logic
async def main() -> None:
    logger.info("Starting bot...")

    # Initialize the database
    logger.info("Initializing database...")
    await create_db_and_tables()

    # Create the owner account
    await add_user(config.OWNER_ID, 3)
    logger.info("The owner account has been created.")

    # Register handlers
    register_handlers(dp)

    # Load plugins
    await plugin_manager.load_plugins()

    # Parse command-line arguments
    args = parse_arguments()

    # Send reboot notification if user_id is provided
    if args.user_id:
        await bot.send_message(
            args.user_id,
            text="<b>✅ The bot has successfully rebooted!</b>\n",
            parse_mode=ParseMode.HTML
        )

    # Start polling the bot for new updates
    logger.info("Bot is up and running.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped.")
