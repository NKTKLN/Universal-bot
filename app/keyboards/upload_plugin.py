from aiogram.utils.keyboard import InlineKeyboardBuilder

# Upload plugin inline buttons
def upload_plugin_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Cancel", callback_data="cancel_upload")
    return builder.as_markup()

