from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.loader import plugin_manager

# Function to create a menu with the list of available commands
def commands_menu():
    builder = ReplyKeyboardBuilder()

    # Iterate over each loaded plugin and its functions
    for plugin in plugin_manager.loaded_plugins:
        for function in plugin.functions:
            # Only add buttons for functions with function_type set to 'button' and non-empty names
            if function.function_type != "button" or function.name is None:
                continue

            # Add the function's name as a button to the keyboard
            builder.button(text=function.name)

    # Add a 'Back' button to navigate back to the main menu
    builder.button(text="🔙 Back to Main Menu")
    
    builder.adjust(1, repeat=True) # Arrange buttons in one column, with one button per row
    return builder.as_markup(resize_keyboard=True)
