import pytest
from aiogram.types import Message
from unittest.mock import AsyncMock
from bot.keyboards import main_menu
from bot.handlers.basic import cmd_start, return_to_main_menu


@pytest.mark.asyncio
async def test_cmd_start():
    """Test the /start command."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    await cmd_start(message)

    message.answer.assert_called_once_with(
        text="<b>Welcome to the bot! 😊</b>", 
        parse_mode="HTML",
        reply_markup=main_menu()
    )


@pytest.mark.asyncio
async def test_return_to_main_menu():
    """Test the 'Back to Main Menu' button."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()
    state = AsyncMock()
    
    await return_to_main_menu(message, state)
    
    state.clear.assert_called_once()
    message.answer.assert_called_once_with(
        text="<b>🔙 You are now back to the main menu.</b>",
        parse_mode="HTML",
        reply_markup=main_menu()
    )
