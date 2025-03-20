from aiogram.utils.keyboard import InlineKeyboardBuilder

# Upload plugin inline buttons
def upload_plugin_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Cancel", callback_data="cancel_upload")
    return builder.as_markup()


# Inline buttons for rebooting the bot after plugin installation
def reboot_after_plugin_installation_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Reboot", callback_data="reboot_bot_after_plugin_update")
    return builder.as_markup()
