from aiogram.enums import ParseMode
from aiogram import Router, types, F
from bot.middlewares import AccessLevel
from bot.keyboards import commands_menu

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))


# Command to show the list of available commands when the "Commands" button is clicked
@router.message(F.text == "🧭 Commands")
async def show_command_list(message: types.Message):
    # Send a message with instructions and display the command list using the 'commands_menu' keyboard
    await message.answer(
        text="<b>👉 Switching to the commands menu. Please choose a command from the list below.</b>", 
        parse_mode=ParseMode.HTML,
        reply_markup=commands_menu()
    )
