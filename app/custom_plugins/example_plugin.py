"""
Plugin: example_plugin
Version: 1.0.0
Description: Пример плагина для демонстрации структуры.
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("example"))
async def example_command(message: Message):
    """
    name: example
    type: button / command
    description: Пример команды, демонстрирующей работу плагина.
    """
    await message.answer("Это пример плагина.")
