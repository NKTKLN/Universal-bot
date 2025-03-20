from aiogram import Bot, Dispatcher
from bot.config import config
from bot.plugins import PluginManager

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

plugin_manager = PluginManager(dp, bot)
