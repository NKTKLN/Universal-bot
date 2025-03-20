import pytest
from aiogram.types import Message
from unittest.mock import AsyncMock
from bot.keyboards import commands_menu
from bot.handlers import show_command_list


@pytest.mark.asyncio
async def test_show_command_list():
    """Test the '🧭 Commands' command handler."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    await show_command_list(message)

    message.answer.assert_called_once_with(
        text="<b>👉 Switching to the commands menu. Please choose a command from the list below.</b>",
        parse_mode="HTML",
        reply_markup=commands_menu()
    )
