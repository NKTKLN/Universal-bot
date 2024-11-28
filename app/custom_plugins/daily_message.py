"""
Plugin: daily_message
Version: 1.0.0
Description: Sends a message to users every day at 6:00 AM.
"""

import asyncio
from datetime import datetime, timedelta
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

# Router for the plugin
router = Router()

# List of user IDs to send messages to
subscribed_users = []  # This can be replaced by a database in a real implementation


@router.message(Command("subscribe"))
async def subscribe_user(message: Message):
    """
    name: subscribe
    type: time
    description: Adds the user to the daily notification list.
    """
    user_id = message.from_user.id
    if user_id not in subscribed_users:
        subscribed_users.append(user_id)
        await message.answer("You have been subscribed to daily notifications.")
    else:
        await message.answer("You are already subscribed.")


@router.message(Command("unsubscribe"))
async def unsubscribe_user(message: Message):
    """
    name: unsubscribe
    description: Removes the user from the daily notification list.
    """
    user_id = message.from_user.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        await message.answer("You have been unsubscribed from daily notifications.")
    else:
        await message.answer("You are not subscribed.")


async def daily_task(bot: Bot):
    """
    Sends a daily message to all subscribed users at 6:00 AM.
    """
    while True:
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()

        # Log the next run time
        print(f"[DAILY TASK] Sleeping for {sleep_time} seconds until {next_run}")

        # Wait until the next run
        await asyncio.sleep(sleep_time)

        # Send the message to all subscribed users
        for user_id in subscribed_users:
            try:
                await bot.send_message(chat_id=user_id, text="Good morning! 🌅 Here's your daily message.")
            except Exception as e:
                print(f"[DAILY TASK] Failed to send message to {user_id}: {e}")


# Startup handler to start the daily task
async def on_startup(bot: Bot):
    """
    Starts the daily task when the bot launches.
    """
    asyncio.create_task(daily_task(bot))
