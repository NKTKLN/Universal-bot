import re
import os
from bot.config import config
from typing import Dict, List, Optional
from bot.models import Plugin, Function


class PluginNotFoundError(Exception):
    """Custom exception raised when a plugin id is not found."""
    pass


def get_plugin_metadata_from_content(plugin_code: str) -> Plugin:
    """
    Extracts the plugin metadata and functions from the given plugin code.

    :param plugin_code: The full content of the plugin's source code.
    :return: A Plugin instance containing metadata and functions.
    """
    plugin_metadata = parse_plugin_metadata(plugin_code)
    functions = parse_functions_and_descriptions(plugin_code)

    # Create and return the Plugin instance
    return Plugin(
        name=plugin_metadata['name'],
        title=plugin_metadata['title'],
        version=plugin_metadata['version'],
        description=plugin_metadata['description'],
        dependencies=plugin_metadata['dependencies'],
        functions=functions,
        file_path=None
    )


def get_plugin_metadata(plugin_name: str) -> Plugin:
    """
    Retrieves the metadata (name, version, description) and functions of the plugin.

    :param plugin_name: The name of the plugin to get metadata for.
    :return: A Plugin instance containing metadata and function descriptions.
    """

    plugin_path = os.path.join(config.PLUGINS_DIR, f"{plugin_name}.py")

    # Ensure the plugin file exists
    if not os.path.exists(plugin_path):
        raise FileNotFoundError(f"Plugin file {plugin_name}.py not found")

    # Read the plugin code for further analysis
    with open(plugin_path, 'r', encoding='utf-8') as f:
        plugin_code = f.read()

    plugin = get_plugin_metadata_from_content(plugin_code)
    plugin.file_path = plugin_path

    return plugin


def parse_plugin_metadata(plugin_code: str) -> Dict[str, Optional[str]]:
    """
    Extracts the metadata (name, version, description) from the plugin code.

    :param plugin_code: The full content of the plugin's source code.
    :return: A dictionary with keys 'name', 'version', and 'description'.
    """

    metadata = {
        'name': None,
        'title': None,
        'version': None,
        'description': None,
        'dependencies': []
    }

    # Search for plugin id, name, version, and description in the comments at the start of the file
    name_match = re.search(r'Plugin:\s*(\S+)', plugin_code)
    if name_match:
        metadata['name'] = name_match.group(1)
    else:
        raise PluginNotFoundError("Plugin name not found in the plugin code.")
    
    title_match = re.search(r'Title:\s*(.*)', plugin_code)
    if title_match:
        metadata['title'] = title_match.group(1)

    version_match = re.search(r'Version:\s*(\S+)', plugin_code)
    if version_match:
        metadata['version'] = version_match.group(1)

    description_match = re.search(r'Description:\s*(.*)', plugin_code)
    if description_match:
        metadata['description'] = description_match.group(1)

    install_matches = re.findall(r'Install:\s*(\S+)', plugin_code)
    if install_matches:
        metadata['dependencies'] = install_matches

    return metadata


def parse_functions_and_descriptions(plugin_code: str) -> List[Function]:
    """
    Parses all the functions and their descriptions from the plugin code.

    :param plugin_code: The full content of the plugin's source code.
    :return: A list of Function instances, each containing function metadata.
    """
    functions = []

    # Look for function definitions with comments starting with "name:", "type:", and "description:"
    function_matches = re.findall(
        r'\s*name:\s*(\w+).*?type:\s*(\w+).*?description:\s*(.*?)\s*\"\"\"', 
        plugin_code, re.DOTALL
    )

    for match in function_matches:
        function = Function(
            name=match[0],           # The alias name for the function
            function_type=match[1],  # The type of the function
            description=match[2]     # The description of the function
        )
        functions.append(function)

    return functions
