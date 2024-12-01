class Function:
    """
    Represents a plugin function with its metadata.
    """
    def __init__(self, name: str, function_type: str, description: str):
        self.name = name
        self.function_type = function_type
        self.description = description
