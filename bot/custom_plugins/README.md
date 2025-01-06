# Plugin Creation Documentation

## 1. Plugin Metadata Structure

Each plugin is implemented as a Python module containing metadata and core functionality. The metadata is defined as a comment block at the beginning of the file and follows this structure:

```python
"""
Plugin: unique_plugin_name  # Unique name for the plugin
Title: Plugin Title  # Displayed name of the plugin
Version: 1.0.0  # Plugin version
Description: A brief description of the plugin’s functionality.

Install: package_name  # Dependencies required for the plugin
Install: another_package  # Add as many dependencies as needed
"""
```

### Metadata Fields

- **Plugin** (mandatory): A unique identifier for the plugin.
- **Title** (optional): The display name of the plugin.
- **Version** (optional): The version of the plugin, adhering to semantic versioning.
- **Description** (optional): A brief description of what the plugin does.
- **Install** (optional): Specifies the packages required for the plugin. Add one line for each dependency.

---

## 2. Core Plugin Code

The plugin's main functionality should use the `aiogram` library. It handles commands, buttons, and background tasks via an `aiogram.Router`.

### Example Plugin

Here’s an example of a plugin that responds to a command and a button press:

```python
"""
Plugin: example_plugin
Title: Example Plugin
Version: 1.0.0
Description: Demonstrates a plugin structure with command and button actions.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.middlewares import AccessLevel

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))

@router.message(Command("example"))
async def handle_example_command(message: Message):
    """
    name: example_command
    type: command
    description: Responds to the /example command with a demonstration message.
    """
    await message.answer("This is an example command response.")

@router.message(F.text == "example_button")
async def handle_example_button(message: Message):
    """
    name: example_button
    type: button
    description: Responds when the button with the text 'example_button' is pressed.
    """
    await message.answer("This is an example button response.")
```

---

## 3. Action Documentation Format

Each plugin action (e.g., command, button, or task) requires descriptive metadata in the form of comments for system integration:

```python
"""
name: action_name  # Unique identifier for the action
type: action_type  # The type of action: 'command', 'button', or 'task'
description: A brief explanation of the action’s purpose and behavior.
"""
```

### Fields

- **name** (mandatory): Unique identifier for the action.
- **type** (mandatory): Type of the action:
  - `command` for slash commands.
  - `button` for text-based buttons.
  - `task` for background tasks.
- **description** (optional): Describes the action's purpose and behavior.

---

## 4. Background Tasks with `asyncio`

Background tasks are actions that run continuously or at specific intervals. They use the `asyncio` library and should include metadata.

### Example Background Task Plugin

```python
"""
Plugin: daily_message
Title: Daily Message Plugin
Version: 1.0.0
Description: Sends a daily message to all subscribed users at 6:00 AM.
"""

import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from bot.db import get_all_users  # Custom module to retrieve user data

async def daily_task(bot: Bot):
    """
    name: daily_task
    type: task
    description: Sends a daily greeting to all users at 6:00 AM.
    """
    while True:
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        sleep_duration = (next_run - now).total_seconds()
        await asyncio.sleep(sleep_duration)

        users = get_all_users()  # Retrieve user list from database
        for user in users:
            await bot.send_message(chat_id=user.id, text="Good morning! 🌅 Here's your daily message.")
```

---

## 5. Creating New Plugins

When developing new plugins, follow the same structure for metadata, actions, and implementation. Here's an example of another plugin:

```python
"""
Plugin: new_plugin
Title: New Plugin
Version: 1.0.0
Description: Demonstrates how to create a new plugin with command and button actions.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.middlewares import AccessLevel

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))

@router.message(Command("new_command"))
async def handle_new_command(message: Message):
    """
    name: new_command
    type: command
    description: Handles the /new_command and demonstrates a new plugin command.
    """
    await message.answer("This is a new plugin command response.")

@router.message(F.text == "new_button")
async def handle_new_button(message: Message):
    """
    name: new_button
    type: button
    description: Responds when the button with the text 'new_button' is pressed.
    """
    await message.answer("This is a new plugin button response.")
```

---

## 6. Best Practices

- **Modularity:** Each plugin should be self-contained, with no dependencies on other plugins.
- **Unique Identifiers:** Use unique names for plugins, commands, and actions to avoid conflicts.
- **Clear Descriptions:** Provide concise and clear descriptions for better usability and maintenance.
- **Test Thoroughly:** Verify plugin functionality in isolation and with other plugins in the system.

---

By adhering to these guidelines, you can create robust, maintainable, and expandable plugins for your system.
