PLUGIN_METADATA = {
    "name": "example_plugin",
    "title": "Example Plugin",
    "version": "1.0.0",
    "description": "Demonstrates a plugin structure with command and button actions.",
    "dependencies": []
}

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.middlewares import AccessLevel

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))

@router.message(Command("example"))
async def example_command(message: Message):
    await message.answer("This is an example command response.")

example_command.meta = {
    "name": "example_command",
    "type": "command",
    "description": "Responds to the /example command with a demonstration message."
}

@router.message(F.text == "example_button")
async def example_button(message: Message):
    await message.answer("This is an example button response.")

example_button.meta = {
    "name": "example_button",
    "type": "button",
    "description": "Responds when the button with the text 'example_button' is pressed."
}
