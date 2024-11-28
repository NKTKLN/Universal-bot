from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.middlewares import AccessLevel
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.enums import ParseMode
from app.keyboards import upload_plugin_buttons

router = Router()

# Middleware registration
router.message.middleware(AccessLevel(2))

class UploadFormState(StatesGroup):
    waiting_for_plugin = State()

@router.message(lambda message: message.text == "📤 Upload Plugin")
async def cmd_upload_plugin(message: types.Message, state: FSMContext):
    await state.set_state(UploadFormState.waiting_for_plugin)
    await message.answer("📦 Please send the plugin file.",
                         reply_markup=upload_plugin_buttons())


@router.callback_query(lambda callback_query: callback_query.data == "cancel_upload")
async def cmd_cancel_upload(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("😐 The file upload was canceled.")
    

@router.message(UploadFormState.waiting_for_plugin)
async def cmd_catch_plugin(message: types.Message, state: FSMContext):
    pass
