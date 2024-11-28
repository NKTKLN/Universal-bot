from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Settings menu
def settings_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="ℹ️ Information")
    builder.button(text="👤 Edit Owners")
    builder.button(text="🗑 Delete All Plugins")
    builder.button(text="🧹 Reset Plugin Settings")
    builder.button(text="🔄 Reload")
    builder.button(text="🔙 Back")
    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True)

