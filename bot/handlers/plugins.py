from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.loader import plugin_manager
from bot.middlewares import AccessLevel
from bot.keyboards import plugins_menu, plugin_action_buttons, plugin_removal_confirmation_buttons, main_menu

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))

# State class for handling the plugin upload form process
class PluginState(StatesGroup):
    waiting_for_plugin = State()  # Waiting for user to select a plugin


# Command to show the list of plugins when the "Plugins List" button is clicked
@router.message(F.text == "🔌 Plugin List")
async def show_plugin_list(message: types.Message, state: FSMContext):
    await state.set_state(PluginState.waiting_for_plugin)  # Set state to waiting for plugin
    await message.answer(
        text="<b>👉 Switching to the plugin menu. Please choose a plugin from the list.</b>", 
        parse_mode=ParseMode.HTML,
        reply_markup=plugins_menu()
    )


# Command to show plugin details after selecting a plugin from the list
@router.message(PluginState.waiting_for_plugin, F.text)
async def show_plugin_details(message: types.Message, state: FSMContext):
    # Find the plugin based on the user's message (either title or name)
    selected_plugin = next((plugin for plugin in plugin_manager.loaded_plugins if (plugin.title or plugin.name) == message.text), None)

    if selected_plugin is None:
        await message.answer(
            text="<b>❌ Sorry, we couldn't find a plugin with that name.</b> Please check the list and try again.",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Save selected plugin in the state
    await state.update_data(waiting_for_plugin=selected_plugin)

    # Display the plugin's information and its functions
    functions_list = ''.join([f"<b>* {'/' if function.function_type == 'command' else ''}{function.name}</b> - {function.description}\n" for function in selected_plugin.functions])

    await message.answer(
        text=f"<b>Plugin Information:</b>\n\n"
        f"<b>Name:</b> {selected_plugin.name}\n"
        f"<b>Title:</b> {selected_plugin.title}\n"
        f"<b>Description:</b> {selected_plugin.description}\n\n"
        f"<b>Functions:</b>\n{functions_list}",
        parse_mode=ParseMode.HTML,
        reply_markup=plugin_action_buttons()
    )


# Command to cancel plugin editing process using callback query
@router.callback_query(F.data == "plugin_action_cancel")
async def cancel_plugin_editing(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(PluginState.waiting_for_plugin)  # Reset to the plugin selection state
    await callback_query.message.edit_text(
        text="<b>🛑 The plugin editor has been canceled.</b> No changes were made.",
        parse_mode=ParseMode.HTML
    )


# Command to initiate plugin deletion process
@router.callback_query(F.data == "plugin_action_delete")
async def initiate_plugin_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()  # Retrieve current state data
    plugin_to_delete = data['waiting_for_plugin']  # Get the selected plugin
    # Ask for confirmation to delete the plugin
    await callback_query.message.edit_text(
        text=f"<b>⚠️ Are you sure you want to remove the plugin: '{plugin_to_delete.title or plugin_to_delete.name}'?</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=plugin_removal_confirmation_buttons()
    )


# Command to cancel plugin deletion and return to plugin settings
@router.callback_query(F.data == "plugin_removal_cancel")
async def cancel_plugin_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()  # Retrieve current state data
    plugin_to_restore = data['waiting_for_plugin']  # Get the selected plugin
    # Display the plugin's information again
    functions_list = ''.join([f"<b>* {'/' if function.function_type == 'command' else ''}{function.name}</b> - {function.description}\n" for function in plugin_to_restore.functions])

    await callback_query.message.edit_text(
        text=f"<b>Plugin Information:</b>\n\n"
        f"<b>Name:</b> {plugin_to_restore.name}\n"
        f"<b>Title:</b> {plugin_to_restore.title}\n"
        f"<b>Description:</b> {plugin_to_restore.description}\n\n"
        f"<b>Functions:</b>\n{functions_list}",
        parse_mode=ParseMode.HTML,
        reply_markup=plugin_action_buttons()
    )


# Command to confirm plugin deletion and remove it
@router.callback_query(F.data == "plugin_removal_confirm")
async def confirm_plugin_deletion(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()  # Retrieve current state data
    plugin_to_delete = data['waiting_for_plugin']  # Get the selected plugin
    plugin_manager.delete_plugin(plugin_to_delete.name)  # Delete the plugin using the plugin manager
    await state.set_state(PluginState.waiting_for_plugin)  # Reset to plugin selection state
    await callback_query.message.edit_text(
        text=f"<b>✅ The plugin '{plugin_to_delete.title or plugin_to_delete.name}' has been successfully removed.</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=plugins_menu()
    )
