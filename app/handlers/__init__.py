from aiogram import Dispatcher
from .basic import router as commands_router
from .upload_plugin import router as upload_plugin_router

def register_handlers(dp: Dispatcher):
    dp.include_router(commands_router)
    dp.include_router(upload_plugin_router)
