# Plugin Creation Documentation for Your System

## 1. Plugin Structure

Each plugin in the system should be implemented as a Python module containing specific structure and functionality. Below is the basic structure of a plugin:

```python
"""
Plugin: example_plugin  # Unique name for the plugin
Title: Example plugin  # The name that will be displayed in the plugin menu
Version: 1.0.0  # Plugin version
Description: Example plugin to demonstrate structure.  # Plugin description
"""
```

- **Plugin:** (mandatory field) The unique name of the plugin.
- **Title:** (optional field) The name of the plugin that will be displayed in the plugin menu.
- **Version:** (optional field) The version of the plugin.
- **Description:** (optional field) A brief description of the plugin’s functionality.

## 2. Core Plugin Code

After declaring the plugin metadata, you need to implement the plugin's core code. This typically involves handling commands and buttons using the `aiogram` library. The plugin should be registered in a `Router` that manages message handling.

Here is an example of a plugin that handles a command and a button press:

```python
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("example"))  # Command handler for /example
async def example_command(message: Message):
    """
    name: example_1  # Unique name for the command
    type: command  # Action type (command)
    description: An example of a command that demonstrates how the plugin works.
    
    Handles the /example command and sends a response with the plugin description.
    """
    await message.answer("This is an example of a plugin.")

@router.message(F.text == "example")  # Button handler for the text "example"
async def example_command_button(message: Message):
    """
    name: example_2  # Unique name for the button
    type: button  # Action type (button)
    description: An example of a button that demonstrates how the plugin works.
    
    Responds when the button with the text 'example' is pressed.
    """
    await message.answer("This is an example of a plugin.")
```

## 3. Command and Button Description Format

Each action in the plugin (command or button) should be described using special comments so the system can correctly display plugin information:

```python
"""
name: example_1  # Unique name for the action
type: command  # Type of action (e.g., command or button)
description: An example of a command that demonstrates how the plugin works.  # Action description
"""
```

- **name:** (mandatory field) A unique name for the action. It should be short and descriptive.
- **type:** (optional field) The type of action. For example, `command` for a command or `button` for a button press.
- **description:** (optional field) A description of what the action does (e.g., what response is sent to the user).

## 4. Developing Additional Plugins

To create new plugins, you need to follow the structure above and add new command or button handlers. Here's an example of a new plugin:

```python
"""
Plugin: new_plugin
Title: New plugin
Version: 1.0.0
Description: A new plugin to demonstrate plugin creation.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("new_command"))
async def new_command(message: Message):
    """
    name: new_command_1
    type: command
    description: This is a new command that demonstrates how the plugin works.
    
    Handles the /new_command command and sends a new message.
    """
    await message.answer("This is a new plugin command.")

@router.message(F.text == "new_button")
async def new_command_button(message: Message):
    """
    name: new_button_1
    type: button
    description: This is a new button that demonstrates how the plugin works.
    
    Responds when the button with the text 'new_button' is pressed.
    """
    await message.answer("This is a new plugin button.")
```

## 5. Recommendations

- Plugins should be independent and not rely on other plugins to ensure flexibility and modularity.
- Each plugin should have unique names for commands and buttons to avoid conflicts with other plugins.
- Well-structured and clear descriptions will help in further development and usage of plugins.

By following this structure, you can easily create new plugins for your system while maintaining consistency and expandability.
