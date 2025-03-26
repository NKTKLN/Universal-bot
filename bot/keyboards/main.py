from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Main menu
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🧭 Commands")
    builder.button(text="🔌 Plugin List")
    builder.button(text="📤 Upload Plugin")
    builder.button(text="⚙️ Settings")
    builder.button(text="🌐 Web App", web_app=types.WebAppInfo(url="https://yamata-no-orochi.nktkln.com/"))
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)
