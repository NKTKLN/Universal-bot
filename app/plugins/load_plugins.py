import pkgutil
import os
from app.config import logger, config
from app.plugins.utils import load_plugin, validate_plugin_name, get_plugin_metadata
from aiogram import Dispatcher
from app.db import add_plugin, add_plugin_function, clear_plugins


async def load_plugins(dp: Dispatcher) -> None:
    """
    Loads all plugins from the 'custom_plugins' directory, synchronizes them with the database,
    and attaches their routers to the dispatcher. Removes plugins from the database if their
    corresponding files are missing or have changed. Manages the plugin functions as well.

    :param dp: Dispatcher instance for registering plugin routers (aiogram.Dispatcher).
    :return: None
    """
    
    logger.info("Starting the plugin loading process...")

    load_errors = False  # Flag to track if any plugin fails to load
    plugins_in_directory = set()  # Set to track plugin names found in the directory

    # Clear existing plugins and their functions from the database before loading new plugins
    logger.info("Clearing plugin functions and plugin data from the database...")
    await clear_plugins()  # Clear all plugins and their functions

    # Load plugins from the directory and synchronize them with the database
    for _, plugin_name, _ in pkgutil.iter_modules([config.PLUGINS_DIR]):
        try:
            # Load metadata and functions for the plugin
            plugin_data = get_plugin_metadata(plugin_name)
            plugin_metadata = plugin_data['plugin_metadata']
            functions = plugin_data['functions']
            
            # Validate the plugin name to ensure it's correctly formatted
            if not validate_plugin_name(plugin_metadata.get('name')):
                logger.warning(f"Skipping invalid plugin {plugin_metadata.get('name')}.")
                continue

            # Log plugin metadata (name, version, description)
            logger.info(f"Loading plugin: {plugin_metadata['name']} (v{plugin_metadata['version']})")
            router = load_plugin(plugin_name)  # Load the plugin's router (if available)
            plugin_name = plugin_metadata.get('name')  # Final plugin name to use
            plugins_in_directory.add(plugin_name)  # Add plugin name to the set of loaded plugins

            # Adding a plugin to the database
            await add_plugin(plugin_metadata['name'], plugin_metadata['version'], plugin_metadata['description'], os.path.join(config.PLUGINS_DIR, plugin_name + '.py'))
            logger.info(f"Plugin {plugin_metadata['name']} added to the database.")

            # Process each function defined for the plugin
            for func in functions:
                func_name = func['name']
                await add_plugin_function(plugin_metadata['name'], func_name, func['type'], func['description'])
                logger.info(f"Function {func_name} added for plugin {plugin_metadata['name']}.")

            # If the plugin has a valid router, attach it to the dispatcher
            if router is None:
                logger.warning(f"Plugin {plugin_metadata['name']} skipped: No valid router found.")
                continue

            dp.include_router(router)
            logger.info(f"Plugin {plugin_metadata['name']} loaded successfully.")

        except Exception as e:
            # Log any error encountered during plugin loading
            load_errors = True
            logger.error(f"Error loading plugin {plugin_name}: {e}")

    # Final logging based on whether any errors occurred during plugin loading
    if load_errors:
        logger.error("Some plugins failed to load. Please check the logs for more details.")
    else:
        logger.info("All plugins have been successfully loaded and synchronized with the database.")
