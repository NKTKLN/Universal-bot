from app.models import PluginFunction
from sqlalchemy.future import select
from .database import get_session
from app.config import logger
from .plugin import get_plugin_by_name
from typing import List


# Adding a new plugin function
async def add_plugin_function(plugin_name: str, function_name: str, function_type: str, description: str) -> None:
    """
    Adds a new function to the specified plugin.

    :param plugin_name: The name of the plugin to which the function will be added.
    :param function_name: The name of the function to be added.
    :param description: The description of the function.
    """

    async for session in get_session():
        plugin = await get_plugin_by_name(plugin_name)
        if not plugin:
            logger.warning(f"Plugin {plugin_name} not found to add function {function_name}.")
            return

        result = await session.execute(select(PluginFunction).filter(PluginFunction.plugin_id == plugin.id, 
                                                                     PluginFunction.name == function_name))
        existing_function = result.scalars().first()
        if existing_function:
            return  # Function already exists, so do not add

        new_function = PluginFunction(name=function_name, description=description, plugin_id=plugin.id, function_type=function_type)
        session.add(new_function)
        await session.commit()
        logger.info(f"Function {function_name} added to plugin {plugin_name}.")


# Get all functions for a plugin
async def get_functions_by_plugin(plugin_name: str) -> List[PluginFunction]:
    """
    Retrieves all functions associated with the specified plugin.

    :param plugin_name: The name of the plugin to get the functions for.
    :return: A list of functions associated with the plugin.
    """

    async for session in get_session():
        plugin = await get_plugin_by_name(plugin_name)
        if not plugin:
            logger.warning(f"Plugin {plugin_name} not found to get functions.")
            return []

        result = await session.execute(select(PluginFunction).filter(PluginFunction.plugin_id == plugin.id))
        return result.scalars().all()
