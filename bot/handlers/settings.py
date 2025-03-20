import os
import sys
from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.filters import Command
from bot.config import log_stream
from bot.loader import plugin_manager
from bot.middlewares import AccessLevel
from bot.keyboards import settings_menu, all_plugins_removal_confirmation_buttons, creator_info_buttons

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(2))

# Command to show settings menu
@router.message(F.text == "⚙️ Settings")
async def show_settings_menu(message: types.Message):
    await message.answer(
        text="<b>👉 Switching to the settings menu.</b>", 
        parse_mode=ParseMode.HTML,
        reply_markup=settings_menu()
    )

# Command to show creator information
@router.message(Command("info"))
@router.message(F.text == "ℹ️ Information")
async def show_creator_info(message: types.Message):
    await message.answer(
        text="<b>Creator:</b> NKTKLN\n<b>Version:</b> 1.0.0", 
        parse_mode=ParseMode.HTML,
        reply_markup=creator_info_buttons()
    )

# Command to reboot the bot
@router.message(Command("reboot"))
@router.message(F.text == "🔄 Reboot")
async def reboot_bot(message: types.Message):
    await message.answer(
        text="<b>🔄 Rebooting the bot...</b>",
        parse_mode=ParseMode.HTML
    )
    
    # Pass user_id as arguments when restarting the bot
    os.execv(sys.executable, ['python'] + sys.argv + ['--user_id', str(message.from_user.id)])

# Command to send logs
@router.message(Command("logs"))
@router.message(F.text == "📝 Logs")
async def send_logs(message: types.Message):
    # Retrieve the log content from StringIO
    log_content = log_stream.getvalue()
    
    # Create a BufferedInputFile with the log content, encoded in UTF-8
    log_file = types.BufferedInputFile(log_content.encode('utf-8'), filename="logs.txt")

    # Send the log file to the user with a caption
    await message.answer_document(log_file, caption="<b>Here is the log file since the bot started.</b>", parse_mode=ParseMode.HTML)

# Command to ask for confirmation to delete all plugins
@router.message(F.text == "🗑 Delete All Plugins")
async def confirm_plugin_deletion(message: types.Message):
    await message.answer(
        text="<b>⚠️ Are you sure you want to remove all plugins?</b>", 
        parse_mode=ParseMode.HTML,
        reply_markup=all_plugins_removal_confirmation_buttons()
    )

# Command to cancel plugin deletion and return to settings menu
@router.callback_query(F.data == "cancel_all_plugins_removal")
async def cancel_all_plugin_deletion(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="<b>✅ Plugin removal canceled.</b>", 
        parse_mode=ParseMode.HTML
    )

# Command to confirm and delete all plugins
@router.callback_query(F.data == "confirm_all_plugins_removal")
async def delete_all_plugins(callback_query: types.CallbackQuery):
    # Loop through all loaded plugins and delete them
    for plugin in plugin_manager.loaded_plugins:
        plugin_manager.delete_plugin(plugin.name)

    await callback_query.message.edit_text(
        text="<b>✅ All plugins have been successfully removed.</b>", 
        parse_mode=ParseMode.HTML
    )
