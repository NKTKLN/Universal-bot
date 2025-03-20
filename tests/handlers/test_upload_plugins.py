import os
import sys
import pytest
from io import BytesIO
from aiogram.types import Message, CallbackQuery, Document, File
from unittest.mock import AsyncMock, MagicMock
from bot.loader import plugin_manager
from bot.plugins import extract_plugin_metadata_from_io
from bot.handlers.upload_plugins import cmd_upload_plugin, cmd_cancel_upload, handle_plugin_upload, reboot_bot
from bot.keyboards.upload_plugin import upload_plugin_buttons


@pytest.mark.asyncio
async def test_cmd_upload_plugin():
    """Test the '📤 Upload Plugin' command."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()
    state = AsyncMock()

    await cmd_upload_plugin(message, state)

    state.set_state.assert_called_once_with("UploadFormState:waiting_for_plugin")
    message.answer.assert_called_once_with(
        text="<b>📦 Please send the plugin file in <i>Python (.py)</i> format.</b>\n"
             "Ensure that the file is valid before uploading.",
        parse_mode="HTML",
        reply_markup=upload_plugin_buttons()
    )


@pytest.mark.asyncio
async def test_cmd_cancel_upload():
    """Test canceling the plugin upload."""
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()
    state = AsyncMock()

    await cmd_cancel_upload(callback_query, state)

    state.clear.assert_called_once()
    callback_query.message.edit_text.assert_called_once_with(
        text="<b>😐 The file upload was canceled.</b>\n"
             "No file has been uploaded.\n"
             "<i>If you wish to upload a file again, press the 'Upload Plugin' button.</i>",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_handle_plugin_upload_valid_file(monkeypatch):
    """Test uploading a valid plugin file."""
    message = AsyncMock(spec=Message)
    message.document = AsyncMock(spec=Document)
    message.document.file_name = "test_plugin.py"
    message.document.file_id = "file_id"
    message.bot.get_file = AsyncMock(return_value=AsyncMock(spec=File, file_path="tests/src/example_plugin.py"))
    
    with open("tests/src/example_plugin.py", "rb") as f:
        plugin_content = f.read()
    
    message.bot.download_file = AsyncMock(return_value=BytesIO(plugin_content))
    message.answer = AsyncMock()

    state = AsyncMock()

    await handle_plugin_upload(message, state)

    state.clear.assert_called_once()
    message.answer.assert_called_once_with(
        text="<b>📥 The plugin file has been uploaded successfully!</b>",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_handle_plugin_upload_invalid_file():
    """Test uploading an invalid file (non-Python)."""
    message = AsyncMock(spec=Message)
    message.document = AsyncMock(spec=Document)
    message.document.file_name = "test_plugin.txt"
    message.answer = AsyncMock()

    state = AsyncMock()

    await handle_plugin_upload(message, state)

    state.clear.assert_not_called()
    message.answer.assert_called_once_with(
        text="<b>⚠️ Please send a valid Python (.py) file.</b>\n"
             "Only files with the <i>.py</i> extension are accepted.",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_handle_plugin_upload_no_file():
    """Test when no file is sent."""
    message = AsyncMock(spec=Message)
    message.document = None
    message.answer = AsyncMock()

    state = AsyncMock()

    await handle_plugin_upload(message, state)

    state.clear.assert_not_called()
    message.answer.assert_called_once_with(
        text="<b>⚠️ No file received!</b>\n"
             "Please send a valid Python (.py) file for upload.",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_reboot_bot(monkeypatch):
    """Test rebooting the bot after plugin update."""
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()
    callback_query.from_user = MagicMock(id=12345)

    mock_execv = MagicMock()
    monkeypatch.setattr(os, "execv", mock_execv)

    await reboot_bot(callback_query)

    callback_query.message.edit_text.assert_called_once_with(
        text="<b>🔄 Rebooting the bot...</b>\n"
             "The bot is restarting to apply the latest changes. Please wait a moment. ",
        parse_mode="HTML"
    )
    mock_execv.assert_called_once_with(
        sys.executable, ['python'] + sys.argv + ['--user_id', '12345']
    )
