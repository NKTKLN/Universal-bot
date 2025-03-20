import os
import sys
from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.middlewares import AccessLevel
from bot.loader import plugin_manager
from bot.plugins import parse_plugin_metadata
from bot.keyboards import upload_plugin_buttons, reboot_after_plugin_installation_buttons

router = Router()

# Middleware registration to ensure the correct access level
router.message.middleware(AccessLevel(2))

# Define state class for managing the plugin upload form process
class UploadFormState(StatesGroup):
    waiting_for_plugin = State()  # State when the bot is waiting for a plugin file

# Command to handle the "Upload Plugin" request
@router.message(lambda message: message.text == "📤 Upload Plugin")
async def cmd_upload_plugin(message: types.Message, state: FSMContext):
    # Set the state to waiting for a plugin file
    await state.set_state(UploadFormState.waiting_for_plugin)
    # Send a message asking for the plugin file with relevant buttons
    await message.answer(
        text="<b>📦 Please send the plugin file in <i>Python (.py)</i> format.</b>\n"
             "Ensure that the file is valid before uploading.",
        parse_mode=ParseMode.HTML,
        reply_markup=upload_plugin_buttons()
    )

# Command to handle the cancel upload action
@router.callback_query(lambda callback_query: callback_query.data == "cancel_upload")
async def cmd_cancel_upload(callback_query: types.CallbackQuery, state: FSMContext):
    # Clear the state and inform the user the upload was canceled
    await state.clear()
    await callback_query.message.edit_text(
        text="<b>😐 The file upload was canceled.</b>\n"
             "No file has been uploaded.\n"
             "<i>If you wish to upload a file again, press the 'Upload Plugin' button.</i>",
        parse_mode=ParseMode.HTML
    )

# Handle the incoming file for plugin upload
@router.message(UploadFormState.waiting_for_plugin)
async def handle_plugin_upload(message: types.Message, state: FSMContext):
    # Check if no document was sent, prompt the user to send a valid Python file
    if not message.document:
        await message.answer(
            text="<b>⚠️ No file received!</b>\n"
                 "Please send a valid Python (.py) file for upload.",
            parse_mode=ParseMode.HTML
        )
        return

    # Check if the file is a Python file, inform the user if not
    if not message.document.file_name.endswith('.py'):
        await message.answer(
            text="<b>⚠️ Please send a valid Python (.py) file.</b>\n"
                 "Only files with the <i>.py</i> extension are accepted.",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Clear the state after processing the file
    await state.clear()

    # Download the file to an in-memory buffer
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_content = await message.bot.download_file(file_path)

    # Parse the plugin metadata from the file content
    file_content.seek(0)
    plugin_metadata = parse_plugin_metadata(file_content.read().decode('utf-8'))

    # Check if the plugin is already loaded or if it is an update
    is_plugin_update = plugin_metadata["name"] in [plugin.name for plugin in plugin_manager.loaded_plugins]

    # Try installing the plugin from the uploaded file
    file_content.seek(0)
    installation_status = await plugin_manager.install_plugin_from_io(file_content)
    
    # If installation failed, notify the user
    if not installation_status:
        await message.answer(
            text="<b>❌ Failed to upload the plugin file. Please try again.</b>",
            parse_mode=ParseMode.HTML
        )
        return

    # If the plugin is updated, prompt the user to restart the bot
    if is_plugin_update:
        await message.answer(
            text="<b>📥 The plugin file has been uploaded successfully!</b>\n"
                 "Please restart the bot for the new plugin version to work correctly.",
            parse_mode=ParseMode.HTML,
            reply_markup=reboot_after_plugin_installation_buttons()
        )
        return
    
    # Successful upload, notify the user
    await message.answer(
        text="<b>📥 The plugin file has been uploaded successfully!</b>",
        parse_mode=ParseMode.HTML
    )

# Command to reboot the bot
@router.callback_query(F.data == "reboot_bot_after_plugin_update")
async def reboot_bot(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="<b>🔄 Rebooting the bot...</b>\n"
             "The bot is restarting to apply the latest changes. Please wait a moment. ",
        parse_mode=ParseMode.HTML
    )
    
    # Pass user_id as arguments when restarting the bot
    os.execv(sys.executable, ['python'] + sys.argv + ['--user_id', str(callback_query.from_user.id)])
