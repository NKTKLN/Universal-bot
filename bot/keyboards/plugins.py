from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.loader import plugin_manager

# Menu with the list of available plugins
def plugins_menu():
    builder = ReplyKeyboardBuilder()

    # Add a button for each loaded plugin with its title or name
    for plugin in plugin_manager.loaded_plugins:
        builder.button(text=(plugin.title or plugin.name))

    # Add the 'Back' button to navigate to the main menu
    builder.button(text="🔙 Back to Main Menu")
    builder.adjust(1, repeat=True)  # Arrange the buttons to have 1 per row
    return builder.as_markup(resize_keyboard=True)


# Inline buttons for plugin settings (options to delete or cancel plugin operations)
def plugin_action_buttons():
    builder = InlineKeyboardBuilder()
    
    # Button to delete the selected plugin
    builder.button(text="🗑 Delete Plugin", callback_data="plugin_action_delete")
    # Button to cancel plugin editing or actions
    builder.button(text="❌ Cancel Action", callback_data="plugin_action_cancel")
    
    builder.adjust(1, repeat=True)  # Arrange buttons to appear in a single column
    return builder.as_markup()


# Inline confirmation buttons for confirming plugin removal (Yes/No)
def plugin_removal_confirmation_buttons():
    builder = InlineKeyboardBuilder()
    
    # Button to confirm deletion of the plugin
    builder.button(text="✅ Yes, Delete", callback_data="plugin_removal_confirm")
    # Button to cancel the plugin deletion action
    builder.button(text="❌ No, Cancel", callback_data="plugin_removal_cancel")
    
    builder.adjust(2)  # Arrange the buttons in two columns for better layout
    return builder.as_markup()
