from aiogram import Dispatcher
from .basic import router as basic_router # Done
from .plugins import router as plugins_router # Done
from .comands import router as commands_router # Done
from .settings import router as setting_router # Done
from .upload_plugins import router as upload_plugin_router

def register_handlers(dp: Dispatcher):
    dp.include_router(basic_router)
    dp.include_router(plugins_router)
    dp.include_router(upload_plugin_router)
    dp.include_router(setting_router)
    dp.include_router(commands_router)
