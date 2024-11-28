from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.middlewares import AccessLevel
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.enums import ParseMode

from app.keyboards import main_menu

router = Router()

# Middleware registration
router.message.middleware(AccessLevel(1))


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Welcome to the bot! 😊", 
        reply_markup=main_menu()
    )
