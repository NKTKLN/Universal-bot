from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Settings menu with different management options for the bot
def settings_menu():
    builder = ReplyKeyboardBuilder()
    
    # Button to show bot information
    builder.button(text="ℹ️ Information")
    # Button to delete all plugins (currently commented out)
    # builder.button(text="👤 Edit Owners")
    # Button to remove all plugins
    builder.button(text="🗑 Delete All Plugins")
    # Button to reset plugin settings (currently commented out)
    # builder.button(text="🧹 Reset Plugin Settings")
    # Button to return to the main menu
    builder.button(text="🔙 Back to Main Menu")
    
    builder.adjust(2, repeat=True) # Arrange buttons in two columns for better layout
    return builder.as_markup(resize_keyboard=True)


# Inline buttons for confirming the removal of all plugins (Yes/No)
def all_plugins_removal_confirmation_buttons():
    builder = InlineKeyboardBuilder()
    
    # Button to confirm the removal of all plugins
    builder.button(text="✅ Yes, Delete All Plugins", callback_data="confirm_all_plugins_removal")
    # Button to cancel the removal action
    builder.button(text="❌ No, Cancel", callback_data="cancel_all_plugins_removal")
    
    builder.adjust(2) # Arrange buttons in two columns for better layout
    return builder.as_markup()


# Inline buttons for providing creator information (Telegram and Github)
def creator_info_buttons():
    builder = InlineKeyboardBuilder()
    
    # Button to redirect to the creator's Telegram profile
    builder.button(text="📞 Telegram", url="http://t.me/NKTKLN")
    # Button to redirect to the creator's GitHub profile
    builder.button(text="🗃 GitHub", url="http://github.com/NKTKLN")
    
    builder.adjust(1, repeat=True) # Arrange buttons in one column for better layout
    return builder.as_markup()
