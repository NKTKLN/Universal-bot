from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from bot.middlewares import AccessLevel
from bot.keyboards import main_menu

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))


# Command to handle the start of the bot
@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        text="<b>Welcome to the bot! 😊</b>", 
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu()
    )


# Command to go back to the main menu when the "Back" button is pressed
@router.message(F.text == "🔙 Back to Main Menu")
async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()  # Clear state to reset any ongoing process
    await message.answer(
        text="<b>🔙 You are now back to the main menu.</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu()
    )
