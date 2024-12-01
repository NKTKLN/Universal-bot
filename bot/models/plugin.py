import copy
from typing import List
from .function import Function

class Plugin:
    """
    Represents a plugin with its metadata and functions.
    """
    def __init__(self, name: str, title: str, version: str, description: str, functions: List[Function], file_path: str):
        self.name = name
        self.title = title
        self.version = version
        self.description = description
        self.functions = functions
        self.file_path = file_path

    def copy(self):
        """
        Returns a copy of the plugin.
        """
        return copy.deepcopy(self)
