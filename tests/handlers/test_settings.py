import os
import sys
import pytest
from aiogram.types import Message, CallbackQuery
from unittest.mock import AsyncMock, MagicMock
from bot.models import Plugin
from bot.config import log_stream
from bot.loader import plugin_manager
from bot.keyboards import settings_menu, creator_info_buttons, all_plugins_removal_confirmation_buttons
from bot.handlers import show_settings_menu, show_creator_info, reboot_bot, send_logs, confirm_plugin_deletion, cancel_all_plugin_deletion, delete_all_plugins


@pytest.mark.asyncio
async def test_show_settings_menu():
    """Test the '⚙️ Settings' command."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    await show_settings_menu(message)

    message.answer.assert_called_once_with(
        text="<b>👉 Switching to the settings menu.</b>",
        parse_mode="HTML",
        reply_markup=settings_menu()
    )


@pytest.mark.asyncio
async def test_show_creator_info():
    """Test the 'ℹ️ Information' command and /info."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    await show_creator_info(message)

    message.answer.assert_called_once_with(
        text="<b>Creator:</b> NKTKLN\n<b>Version:</b> 1.0.0",
        parse_mode="HTML",
        reply_markup=creator_info_buttons() 
    )


@pytest.mark.asyncio
async def test_confirm_plugin_deletion():
    """Test the '🗑 Delete All Plugins' command."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    await confirm_plugin_deletion(message)

    message.answer.assert_called_once_with(
        text="<b>⚠️ Are you sure you want to remove all plugins?</b>", 
        parse_mode="HTML",
        reply_markup=all_plugins_removal_confirmation_buttons()
    )


@pytest.mark.asyncio
async def test_cancel_plugin_deletion():
    """Test canceling plugin deletion."""
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.message = MagicMock(spec=Message)
    callback_query.message.edit_text = AsyncMock()

    await cancel_all_plugin_deletion(callback_query)

    callback_query.message.edit_text.assert_called_once_with(
        text="<b>✅ Plugin removal canceled.</b>", 
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_delete_all_plugins():
    """Test confirming the deletion of all plugins."""
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.message = MagicMock(spec=Message)
    callback_query.message.edit_text = AsyncMock()

    plugin1 = MagicMock(spec=Plugin)
    plugin1.name = "plugin1"

    plugin2 = MagicMock(spec=Plugin)
    plugin2.name = "plugin2"

    plugin_manager.loaded_plugins = [plugin1, plugin2]
    plugin_manager.delete_plugin = MagicMock()

    await delete_all_plugins(callback_query)

    plugin_manager.delete_plugin.assert_any_call("plugin1")
    plugin_manager.delete_plugin.assert_any_call("plugin2")

    callback_query.message.edit_text.assert_called_once_with(
        text="<b>✅ All plugins have been successfully removed.</b>", 
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_reboot_bot(monkeypatch):
    """Test the '🔄 Reboot' command."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()
    message.from_user = MagicMock(id=12345)

    mock_execv = MagicMock()
    monkeypatch.setattr(os, "execv", mock_execv)

    await reboot_bot(message)

    message.answer.assert_called_once_with(
        text="<b>🔄 Rebooting the bot...</b>",
        parse_mode="HTML"
    )
    mock_execv.assert_called_once_with(
        sys.executable, ['python'] + sys.argv + ['--user_id', '12345']
    )


@pytest.mark.asyncio
async def test_send_logs(monkeypatch):
    """Test the '📝 Logs' command."""
    message = AsyncMock(spec=Message)
    message.answer_document = AsyncMock()

    mock_log_content = "Test log content"
    monkeypatch.setattr(log_stream, "getvalue", lambda: mock_log_content)

    await send_logs(message)

    message.answer_document.assert_called_once()
    args, kwargs = message.answer_document.call_args
    assert kwargs["caption"] == "<b>Here is the log file since the bot started.</b>"
    assert kwargs["parse_mode"] == "HTML"
    assert args[0].filename == "logs.txt"
    assert args[0].data.decode("utf-8") == mock_log_content
