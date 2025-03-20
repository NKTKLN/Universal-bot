import pytest
from aiogram.types import Message, CallbackQuery
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.plugins import (
    show_plugin_list,
    show_plugin_details,
    cancel_plugin_editing,
    initiate_plugin_deletion,
    cancel_plugin_deletion,
    confirm_plugin_deletion,
)
from bot.loader import plugin_manager
from bot.keyboards import plugins_menu, plugin_action_buttons, plugin_removal_confirmation_buttons


@pytest.mark.asyncio
async def test_show_plugin_list():
    """Test the '🔌 Plugin List' command."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    await show_plugin_list(message, state=AsyncMock())

    message.answer.assert_called_once_with(
        text="<b>👉 Switching to the plugin menu. Please choose a plugin from the list.</b>",
        parse_mode="HTML",
        reply_markup=plugins_menu()
    )


@pytest.mark.asyncio
async def test_show_plugin_details():
    """Test showing plugin details."""
    message = AsyncMock(spec=Message)
    message.text = "Test Plugin"
    message.answer = AsyncMock()

    plugin = MagicMock()
    plugin.name = "test_plugin"
    plugin.title = "Test Plugin"
    plugin.description = "A test plugin"
    plugin.functions = [
        MagicMock(description="Description 1", function_type="command"),
        MagicMock(description="Description 2", function_type="button"),
    ]
    
    plugin.functions[0].name = "function1"
    plugin.functions[1].name = "function2"

    plugin_manager.loaded_plugins = [plugin]

    state = AsyncMock()
    await show_plugin_details(message, state)

    state.update_data.assert_called_once_with(waiting_for_plugin=plugin)
    
    # Now using the correct names for the functions
    message.answer.assert_called_once_with(
        text=(
            "<b>Plugin Information:</b>\n\n"
            "<b>Name:</b> test_plugin\n"
            "<b>Title:</b> Test Plugin\n"
            "<b>Description:</b> A test plugin\n\n"
            "<b>Functions:</b>\n"
            "<b>* /function1</b> - Description 1\n"
            "<b>* function2</b> - Description 2\n"
        ),
        parse_mode="HTML",
        reply_markup=plugin_action_buttons()
    )


@pytest.mark.asyncio
async def test_cancel_plugin_editing():
    """Test canceling plugin editing."""
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()

    await cancel_plugin_editing(callback_query, state=AsyncMock())

    callback_query.message.edit_text.assert_called_once_with(
        text="<b>🛑 The plugin editor has been canceled.</b> No changes were made.",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_initiate_plugin_deletion():
    """Test initiating plugin deletion."""
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()

    state = AsyncMock()
    state.get_data = AsyncMock(return_value={"waiting_for_plugin": MagicMock(name="test_plugin", title="Test Plugin")})

    await initiate_plugin_deletion(callback_query, state)

    callback_query.message.edit_text.assert_called_once_with(
        text="<b>⚠️ Are you sure you want to remove the plugin: 'Test Plugin'?</b>",
        parse_mode="HTML",
        reply_markup=plugin_removal_confirmation_buttons()
    )


@pytest.mark.asyncio
async def test_cancel_plugin_deletion():
    """Test canceling plugin deletion."""
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()

    plugin = MagicMock()
    plugin.name = "test_plugin"
    plugin.title = "Test Plugin"
    plugin.description = "A test plugin"
    plugin.functions = [
        MagicMock(description="Description 1", function_type="command"),
        MagicMock(description="Description 2", function_type="button"),
    ]
    
    plugin.functions[0].name = "function1"
    plugin.functions[1].name = "function2"

    state = AsyncMock()
    state.get_data = AsyncMock(return_value={"waiting_for_plugin": plugin})

    await cancel_plugin_deletion(callback_query, state)

    callback_query.message.edit_text.assert_called_once_with(
        text=(
            "<b>Plugin Information:</b>\n\n"
            "<b>Name:</b> test_plugin\n"
            "<b>Title:</b> Test Plugin\n"
            "<b>Description:</b> A test plugin\n\n"
            "<b>Functions:</b>\n"
            "<b>* /function1</b> - Description 1\n"
            "<b>* function2</b> - Description 2\n"
        ),
        parse_mode="HTML",
        reply_markup=plugin_action_buttons()
    )


@pytest.mark.asyncio
async def test_confirm_plugin_deletion():
    """Test confirming plugin deletion."""
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()

    plugin = MagicMock()
    plugin.name = "test_plugin"
    plugin.title = "Test Plugin"
    state = AsyncMock()
    state.get_data = AsyncMock(return_value={"waiting_for_plugin": plugin})

    plugin_manager.delete_plugin = MagicMock()

    await confirm_plugin_deletion(callback_query, state)

    plugin_manager.delete_plugin.assert_called_once_with(plugin.name)  # Access the `name` attribute
    callback_query.message.edit_text.assert_called_once_with(
        text="<b>✅ The plugin 'Test Plugin' has been successfully removed.</b>",
        parse_mode="HTML",
        reply_markup=plugins_menu()
    )
