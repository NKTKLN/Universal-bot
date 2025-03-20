from aiogram import Dispatcher
from .basic import router as basic_router
from .plugins import router as plugins_router
from .comands import router as commands_router
from .settings import router as setting_router
from .upload_plugins import router as upload_plugin_router
from .basic import cmd_start, return_to_main_menu
from .plugins import show_plugin_list, show_plugin_details, cancel_plugin_editing, initiate_plugin_deletion, cancel_plugin_deletion, confirm_plugin_deletion
from .comands import show_command_list 
from .settings import show_settings_menu, show_creator_info, reboot_bot, send_logs, confirm_plugin_deletion, cancel_all_plugin_deletion, delete_all_plugins
from .upload_plugins import cmd_upload_plugin, cmd_cancel_upload, handle_plugin_upload, reboot_bot as reboot_after_plugin_update

def register_handlers(dp: Dispatcher):
    dp.include_router(basic_router)
    dp.include_router(plugins_router)
    dp.include_router(upload_plugin_router)
    dp.include_router(setting_router)
    dp.include_router(commands_router)
