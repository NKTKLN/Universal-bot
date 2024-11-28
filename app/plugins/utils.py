import re
import os
import importlib.util
from app.config import config
from typing import Dict, List, Optional, Any


def load_plugin(plugin_name: str) -> Any:
    """
    Loads the plugin dynamically by its name from the plugin directory.

    :param plugin_name: The name of the plugin to load.
    :return: The router object if found, None otherwise.
    """

    plugin_path = os.path.join(config.PLUGINS_DIR, plugin_name + '.py')

    # Ensure the plugin file exists
    if not os.path.exists(plugin_path):
        raise FileNotFoundError(f"Plugin file {plugin_name}.py not found")

    # Load the plugin module dynamically
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)

    return getattr(plugin_module, 'router', None)


def get_plugin_metadata(plugin_name: str) -> Dict[str, Optional[dict]]:
    """
    Retrieves the metadata (name, version, description) and functions of the plugin.

    :param plugin_name: The name of the plugin to get metadata for.
    :return: A dictionary containing plugin metadata and function descriptions.
    """

    plugin_path = os.path.join(config.PLUGINS_DIR, plugin_name + '.py')

    # Ensure the plugin file exists
    if not os.path.exists(plugin_path):
        raise FileNotFoundError(f"Plugin file {plugin_name}.py not found")

    # Read the plugin code for further analysis
    with open(plugin_path, 'r', encoding='utf-8') as f:
        plugin_code = f.read()

    # Parse the plugin's metadata (name, version, description)
    plugin_metadata = parse_plugin_metadata(plugin_code)

    # Parse the plugin's functions and their descriptions
    functions = parse_functions_and_descriptions(plugin_code)

    return {
        'plugin_metadata': plugin_metadata,
        'functions': functions
    }


def parse_plugin_metadata(plugin_code: str) -> Dict[str, Optional[str]]:
    """
    Extracts the metadata (name, version, description) from the plugin code.

    :param plugin_code: The full content of the plugin's source code.
    :return: A dictionary with keys 'name', 'version', and 'description'.
    """

    metadata = {
        'name': None,
        'version': None,
        'description': None
    }

    # Search for plugin name, version, and description in the comments at the start of the file
    name_match = re.search(r'Plugin:\s*(\S+)', plugin_code)
    if name_match:
        metadata['name'] = name_match.group(1)

    version_match = re.search(r'Version:\s*(\S+)', plugin_code)
    if version_match:
        metadata['version'] = version_match.group(1)

    description_match = re.search(r'Description:\s*(.*)', plugin_code)
    if description_match:
        metadata['description'] = description_match.group(1)

    return metadata


def parse_functions_and_descriptions(plugin_code: str) -> List[Dict[str, str]]:
    """
    Parses all the functions and their descriptions from the plugin code.

    :param plugin_code: The full content of the plugin's source code.
    :return: A list of dictionaries, each containing function metadata.
    """
    functions = []

    # Look for function definitions with comments starting with "name:", "type:", and "description:"
    function_matches = re.findall(
        r'\s*name:\s*(\w+).*?type:\s*(\w+).*?description:\s*(.*?)\s*\"\"\"', 
        plugin_code, re.DOTALL
    )

    for match in function_matches:
        functions.append({
            'name': match[0],        # The alias name for the function
            'type': match[1],        # The type of the function
            'description': match[2]  # The description of the function
        })

    return functions


def validate_plugin_name(plugin_name: str) -> bool:
    """
    Validates that the plugin name matches the allowed pattern (letters, digits, dash, and underscore).

    :param plugin_name: The plugin name to validate.
    :return: True if the plugin name matches the pattern, False otherwise.
    """
    return plugin_name is not None and bool(re.match(config.PLUGIN_NAME_REGEX, plugin_name))
