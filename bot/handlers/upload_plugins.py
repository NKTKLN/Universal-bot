import io
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.middlewares import AccessLevel
from aiogram.enums import ParseMode
from bot.keyboards import upload_plugin_buttons
from bot.plugins import plugin_manager

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

# Handle the incoming file for the plugin upload
@router.message(UploadFormState.waiting_for_plugin)
async def cmd_catch_plugin(message: types.Message, state: FSMContext):
    # If no document was sent, prompt the user again
    if not message.document:
        await message.answer(
            text="<b>⚠️ No file received!</b>\n"
                 "Please send a valid Python (.py) file for upload.",
            parse_mode=ParseMode.HTML
        )
        return

    # If the file is not a Python file, inform the user
    if not message.document.file_name.endswith('.py'):
        await message.answer(
            text="<b>⚠️ Please send a valid Python (.py) file.</b>\n"
                 "Only files with <i>.py</i> extension are accepted.",
            parse_mode=ParseMode.HTML
        )
        return

    # Download the file to an in-memory buffer
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_content = await message.bot.download_file(file_path)

    status = await plugin_manager.install_plugin_from_io(file_content)
    if status:
        # Acknowledge successful upload
        await message.answer(
            text="<b>📥 The plugin file has been uploaded successfully!</b>\n",
            parse_mode=ParseMode.HTML
        )
    else:
        # Acknowledge failure
        await message.answer(
            text="<b>❌ Failed to upload the plugin file. Please try again.</b>\n",
            parse_mode=ParseMode.HTML
        )

    # Clear the state after processing the file
    await state.clear()
