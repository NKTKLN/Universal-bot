from app.models import Plugin, PluginFunction
from sqlalchemy.future import select
from .database import get_session
from app.config import logger
from typing import Optional, List


async def clear_plugins() -> None:
    """
    Removes all plugins from the database, including their associated functions.
    This function iterates through all plugins and deletes them one by one.
    The deletion of the plugins also removes their associated functions.
    """
    # Retrieve all plugins from the database
    all_plugins_in_db = await get_all_plugins()

    for plugin in all_plugins_in_db:
        # Delete the plugin and its associated functions (cascade handles functions)
        await delete_plugin(plugin.name)
        logger.info(f"Plugin {plugin.name} removed from the database.")


async def get_all_plugins() -> List[Plugin]:
    """
    Retrieves all plugins stored in the database.

    :return: A list of Plugin objects.
    """
    async for session in get_session():
        # Fetch all plugins from the database using SQLAlchemy's select statement
        result = await session.execute(select(Plugin))
        plugins = result.scalars().all()  # Extract the plugins from the query result
        return plugins


async def add_plugin(plugin_name: str, version: str, description: str, file_path: str) -> None:
    """
    Adds a new plugin to the database if it does not already exist.

    :param plugin_name: The name of the plugin.
    :param version: The version of the plugin.
    :param description: A description of the plugin.
    :param file_path: The file path of the plugin.
    """
    async for session in get_session():
        # Check if the plugin already exists in the database
        result = await session.execute(select(Plugin).filter(Plugin.name == plugin_name))
        plugin = result.scalars().first()
        if plugin:
            # If the plugin exists, do not add it again
            return

        # Create and add the new plugin to the session
        new_plugin = Plugin(name=plugin_name, version=version, description=description, file_path=file_path)
        session.add(new_plugin)
        await session.commit()  # Commit the transaction to save the plugin to the database
    
    # Log the creation of the new plugin
    logger.info(f"Plugin {plugin_name} with version {version} was created.")


async def get_plugin_by_name(plugin_name: str) -> Optional[Plugin]:
    """
    Retrieves a plugin from the database by its name.

    :param plugin_name: The name of the plugin to retrieve.
    :return: The Plugin object if found, or None if the plugin does not exist.
    """
    async for session in get_session():
        # Query the plugin by name
        result = await session.execute(select(Plugin).filter(Plugin.name == plugin_name))
        plugin = result.scalars().first()
        return plugin


async def update_plugin(plugin_name: str, version: str, description: str, file_path: str) -> None:
    """
    Updates the details of an existing plugin in the database.

    :param plugin_name: The name of the plugin to update.
    :param version: The new version of the plugin.
    :param description: The new description of the plugin.
    :param file_path: The new file path of the plugin.
    """
    async for session in get_session():
        # Fetch the plugin to be updated
        plugin = await get_plugin_by_name(plugin_name)
        if plugin:
            # Log if the plugin is not found in the database
            logger.warning(f"Plugin {plugin_name} not found to update.")
            return
        
        # Update the plugin's attributes
        plugin.version = version
        plugin.description = description
        plugin.file_path = file_path
        await session.commit()  # Commit the changes to the database
        logger.info(f"Plugin {plugin_name} updated.")


async def delete_plugin(plugin_name: str) -> None:
    """
    Deletes a plugin and its associated functions from the database.

    :param plugin_name: The name of the plugin to delete.
    """
    async for session in get_session():
        # Fetch the plugin by its name
        plugin = await get_plugin_by_name(plugin_name)
        if not plugin:
            # Log if the plugin does not exist in the database
            logger.warning(f"Plugin {plugin_name} not found in the database.")
            return
        
        # Delete all functions related to the plugin
        result = await session.execute(select(PluginFunction).filter(PluginFunction.plugin_id == plugin.id))
        functions_to_delete = result.scalars().all()  # Fetch all functions for the plugin
        for func in functions_to_delete:
            # Delete each function associated with the plugin
            result = await session.execute(select(PluginFunction).filter(PluginFunction.plugin_id == plugin.id,
                                                                         PluginFunction.name == func.name))
            function = result.scalars().first()
            if not function:
                # Log if a function is not found
                logger.warning(f"Function {func.name} not found for plugin {plugin_name}.")
                return

            await session.delete(function)  # Delete the function from the session
            await session.commit()  # Commit the deletion of the function
            logger.info(f"Function {func.name} removed from plugin {plugin_name}.")
        
        # Delete the plugin itself
        await session.delete(plugin)
        await session.commit()  # Commit the deletion of the plugin
        logger.info(f"Plugin {plugin_name} removed.")
