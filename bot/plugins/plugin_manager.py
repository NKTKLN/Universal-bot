import os
import re
import io
import sys
import pkgutil
import asyncio
import subprocess
import importlib.util
from aiogram import Bot, Dispatcher
from typing import List, Optional
from bot.models import Plugin
from bot.config import logger, config
from .parser import get_plugin_metadata, get_plugin_metadata_from_content


class PluginManager:
    """
    Manages the loading and synchronization of plugins.
    """
    def __init__(self, db: Dispatcher, bot: Bot):
        """
        Initializes the PluginManager with a directory for plugins and an internal list of loaded plugins.

        :param plugins_dir: Directory where plugins are located.
        """
        self.plugins_dir = config.PLUGINS_DIR
        self.dispatcher = db
        self.bot = bot
        self.loaded_plugins: List[Plugin] = []

    def _install_dependencies(self, dependencies: List[str]) -> bool:
        """
        Installs the given list of dependencies using pip.
        
        :param dependencies: List of dependencies to install.
        :return: True if the package was installed successfully, False otherwise.
        """
        for dependency in dependencies:
            try:
                logger.info(f"Installing dependency: {dependency}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install dependency '{dependency}': {e}")
                return False  # Return False if installation fails
        return True

    def _load_plugin(self, plugin: Plugin) -> Optional[any]:
        """
        Loads the plugin dynamically and executes its tasks.

        :param plugin: The plugin object containing its name, path, and functions.
        :return: The router object if found, None otherwise.
        """

        # Ensure the plugin file exists
        if not os.path.exists(plugin.file_path):
            raise FileNotFoundError(f"Plugin file {plugin.name}.py not found")

        # Load the plugin module dynamically
        spec = importlib.util.spec_from_file_location(plugin.name, plugin.file_path)
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)

        # Find and execute functions marked as "task"
        for function in plugin.functions:
            if function.function_type != "task":
                continue

            task_function = getattr(plugin_module, function.name, None)
            if not callable(task_function):
                logger.warning(f"Task function {function.name} not found in plugin {plugin.name}")
                continue

            asyncio.create_task(task_function(self.bot))  

        return getattr(plugin_module, 'router', None)

    def _scan_plugins(self) -> List[str]:
        """
        Scans the plugins directory for valid plugin files and processes them.

        :return: A list of valid plugin names found in the directory.
        """
        logger.info("Scanning plugin files in the directory...")
        valid_plugins = []

        for _, plugin_file_name, _ in pkgutil.iter_modules([self.plugins_dir]):
            try:
                plugin_metadata = get_plugin_metadata(plugin_file_name)
                plugin_name = plugin_metadata.name

                # Validate the plugin name
                if plugin_name is None or not bool(re.match(config.PLUGIN_NAME_REGEX, plugin_name)):
                    logger.warning(f"Skipping invalid plugin: {plugin_file_name}.")
                    continue

                # Rename the file if necessary
                if plugin_file_name != plugin_name:
                    self._rename_plugin_file(plugin_file_name, plugin_name)

                # Install dependencies
                if plugin_metadata.dependencies:
                    if not self._install_dependencies(plugin_metadata.dependencies):
                        logger.warning(f"Skipping plugin '{plugin_name}' due to installation failure.")
                        continue

                valid_plugins.append(plugin_name)
            except Exception as error:
                logger.error(f"Failed to process plugin '{plugin_file_name}': {error}")

        return valid_plugins

    def _rename_plugin_file(self, old_name: str, new_name: str) -> None:
        """
        Renames a plugin file to match its validated name.

        :param old_name: The current name of the plugin file.
        :param new_name: The new name for the plugin file.
        :return: None
        """
        try:
            old_path = os.path.join(self.plugins_dir, f"{old_name}.py")
            new_path = os.path.join(self.plugins_dir, f"{new_name}.py")
            os.rename(old_path, new_path)
            logger.info(f"Renamed plugin file '{old_name}.py' to '{new_name}.py'.")
        except Exception as error:
            logger.error(f"Failed to rename plugin file '{old_name}.py': {error}")

    def _synchronize_plugins(self, valid_plugins: List[str]) -> None:
        """
        Synchronizes the internal list of loaded plugins with the valid plugins found in the directory.

        :param valid_plugins: A list of valid plugin names found in the directory.
        :return: None
        """
        # Remove plugins that are no longer valid
        self.loaded_plugins = [plugin for plugin in self.loaded_plugins if plugin.name in valid_plugins]

        # Add new plugins
        for plugin_name in valid_plugins:
            if plugin_name not in [plugin.name for plugin in self.loaded_plugins]:
                try:
                    plugin_metadata = get_plugin_metadata(plugin_name)

                    # Create and add the plugin object
                    self.loaded_plugins.append(plugin_metadata)
                    logger.info(f"Added plugin '{plugin_metadata.name}' (v{plugin_metadata.version}) to the manager.")
                except Exception as error:
                    logger.error(f"Failed to add plugin '{plugin_name}': {error}")

    async def _register_plugin_routers(self, dp: Dispatcher) -> None:
        """
        Registers plugin routers with the dispatcher.

        :param dp: Dispatcher instance.
        :return: None
        """
        for plugin in self.loaded_plugins:
            try:
                router = self._load_plugin(plugin)
                if router:
                    dp.include_router(router)
                    logger.info(f"Registered router for plugin '{plugin.name}'.")
            except Exception as error:
                logger.error(f"Failed to register router for plugin '{plugin.name}': {error}")

    async def load_plugins(self) -> None:
        """
        Main method to manage the loading and registration of plugins.

        :return: None
        """
        logger.info("Starting plugin loading process...")

        valid_plugins = self._scan_plugins()
        self._synchronize_plugins(valid_plugins)
        await self._register_plugin_routers(self.dispatcher)

        logger.info("All plugins have been successfully loaded and registered.")

    def delete_plugin(self, plugin_name: str) -> None:
        """
        Deletes a plugin from the loaded plugins list and its corresponding file.

        :param plugin_name: The name of the plugin to delete.
        :return: None
        """
        plugin = next((p for p in self.loaded_plugins if p.name == plugin_name), None)
        if not plugin:
            logger.warning(f"Plugin '{plugin_name}' not found in the loaded plugins list.")
            return

        try:
            # Remove the plugin file
            os.remove(plugin.file_path)
            logger.info(f"Deleted plugin file '{plugin.file_path}'.")

            # Remove the plugin from the loaded list
            self.loaded_plugins.remove(plugin)
            logger.info(f"Removed plugin '{plugin_name}' from the manager.")
        except Exception as error:
            logger.error(f"Failed to delete plugin '{plugin_name}': {error}")

    async def install_plugin_from_io(self, io_stream: io.BytesIO) -> bool:
        """
        Installs a plugin from an I/O stream containing the plugin's content (Python file).

        :param io_stream: The I/O stream containing the plugin Python file content.
        :return: True if the plugin was installed successfully, False otherwise.
        """
        try:
            # Read the I/O stream and save the content as a Python file
            plugin_content = io_stream.read().decode('utf-8')

            # Extract metadata from the plugin content (assuming a function exists for this)
            plugin_metadata = get_plugin_metadata_from_content(plugin_content)

            # Create the plugin filename based on the metadata
            plugin_name = plugin_metadata.name
            plugin_file_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")

            # Save the plugin content as a Python file in the plugins directory
            with open(plugin_file_path, 'w', encoding='utf-8') as plugin_file:
                plugin_file.write(plugin_content)

            # Validate and synchronize the plugin after installation
            logger.info(f"Plugin '{plugin_name}' has been installed.")

            valid_plugins = self._scan_plugins()
            self._synchronize_plugins(valid_plugins)
            await self._register_plugin_routers(self.dispatcher)
 
        except Exception as error:
            logger.error(f"Failed to install plugin from I/O stream: {error}")
            return False # Indicate failure
        
        return True # Plugin installed successfully
