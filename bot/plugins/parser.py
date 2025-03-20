import os
import io
import random
import string
import importlib.util
from typing import Dict, List, Optional, Any
from bot.config import logger, config
from bot.models import Plugin, Function


def check_plugin_exists(plugin_name: str) -> str:
    """
    Verifies if the plugin file exists in the plugins directory.

    :param plugin_name: The name of the plugin file (without extension).
    :return: Full path to the plugin file if it exists.
    """
    plugin_path = os.path.join(config.PLUGINS_DIR, f"{plugin_name}.py")
    if not os.path.exists(plugin_path):
        raise FileNotFoundError(f"Plugin file {plugin_name}.py not found")
    return plugin_path


def load_plugin_module(plugin_name: str, plugin_path: str) -> Any:
    """
    Loads the plugin module from the given file path.

    :param plugin_name: Name of the plugin module.
    :param plugin_path: Path to the plugin file.
    :return: The loaded plugin module.
    """
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)
    return plugin_module


def extract_plugin_metadata(plugin_module: Any) -> Dict[str, Optional[str]]:
    """
    Extracts metadata from the loaded plugin module.

    :param plugin_module: The plugin module.
    :return: A dictionary containing the plugin's metadata.
    """
    plugin_metadata = getattr(plugin_module, "PLUGIN_METADATA", None)
    if not plugin_metadata:
        raise ValueError(f"The plugin does not contain any metadata.")
    
    if 'name' not in plugin_metadata:
        raise ValueError(f"The plugin metadata does not contain a 'name' field.")
    
    if not plugin_metadata['name']:
        raise ValueError(f"The plugin metadata contains an empty 'name' field.")

    return plugin_metadata


def extract_plugin_functions(plugin_module: Any) -> List[Function]:
    """
    Extracts functions from the plugin module.

    :param plugin_module: The plugin module.
    :return: A list of Function objects representing the plugin's callable functions.
    """
    plugin_functions = [
        Function(
            name=getattr(func, "meta", {}).get("name", func.__name__),
            function_type=getattr(func, "meta", {}).get("type", "unknown"),
            description=getattr(func, "meta", {}).get("description", "")
        )
        for _, func in plugin_module.__dict__.items()
        if callable(func)
        and hasattr(func, "meta")
        and func.__module__ == plugin_module.__name__
    ]
    return plugin_functions


def get_plugin_metadata(plugin_name: str) -> Plugin:
    """
    Retrieves the metadata (name, version, description) and functions of the plugin.

    :param plugin_name: The name of the plugin to get metadata for.
    :return: A Plugin instance containing metadata and function descriptions.
    """
    plugin_path = check_plugin_exists(plugin_name)
    plugin_module = load_plugin_module(plugin_name, plugin_path)
    plugin_metadata = extract_plugin_metadata(plugin_module)
    plugin_functions = extract_plugin_functions(plugin_module)

    return Plugin(
        name=plugin_metadata["name"],
        title=plugin_metadata["title"],
        version=plugin_metadata["version"],
        description=plugin_metadata["description"],
        dependencies=plugin_metadata.get("dependencies", []),
        functions=plugin_functions,
        file_path=plugin_path
    )

def _generate_random_filename(length: int = 5) -> str:
    """
    Generates a random filename for the plugin file.

    :param length: Length of the random filename.
    :return: Randomly generated filename.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def extract_plugin_metadata_from_io(io_stream: io.BytesIO)-> Dict[str, Optional[str]]:
    """
    Process the plugin from the I/O stream, extract its metadata, and remove the file after processing.

    :param io_stream: The I/O stream containing the plugin Python file content.
    :return: A dictionary containing the plugin's metadata.
    """
    # Read the I/O stream and save the content as a Python file
    plugin_content = io_stream.read().decode('utf-8')

    # Create the random plugin filename
    random_plugin_name = _generate_random_filename()
    plugin_file_path = os.path.join(config.PLUGINS_DIR, f"{random_plugin_name}.py")

    # Save the plugin content as a Python file in the plugins directory
    with open(plugin_file_path, 'w', encoding='utf-8') as plugin_file:
        plugin_file.write(plugin_content)

    try:
        plugin_module = load_plugin_module(random_plugin_name, plugin_file_path)
        plugin_metadata = extract_plugin_metadata(plugin_module)
        return plugin_metadata
    
    finally:
        # Remove the plugin file after processing
        if os.path.exists(plugin_file_path):
            os.remove(plugin_file_path)
            logger.info(f"Plugin file {random_plugin_name} has been removed.")
