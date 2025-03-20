# Plugin Creation Documentation

## 1. Plugin Metadata Structure

Each plugin is implemented as a Python module containing metadata and core functionality. The metadata is defined as a dictionary at the beginning of the file and follows this structure:

```python
PLUGIN_METADATA = {
    "name": "unique_plugin_name",  # Unique name for the plugin
    "title": "Plugin Title",  # Displayed name of the plugin
    "version": "1.0.0",  # Plugin version
    "description": "A brief description of the plugin’s functionality.",
    "dependencies": []  # List of dependencies required for the plugin
}
```

### Metadata Fields

- **name** (mandatory): A unique identifier for the plugin.
- **title** (optional): The display name of the plugin.
- **version** (optional): The version of the plugin, adhering to semantic versioning.
- **description** (optional): A brief description of what the plugin does.
- **dependencies** (optional): A list of packages required for the plugin. Add each dependency as a separate string in the list.

---

## 2. Core Plugin Code

The plugin's main functionality should use the `aiogram` library. It handles commands, buttons, and background tasks via an `aiogram.Router`.

### Example Plugin

Here’s an example of a plugin that responds to a command and a button press:

```python
PLUGIN_METADATA = {
    "name": "example_plugin",
    "title": "Example Plugin",
    "version": "1.0.0",
    "description": "Demonstrates a plugin structure with command and button actions.",
    "dependencies": []
}

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.middlewares import AccessLevel

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))

@router.message(Command("example"))
async def example_command(message: Message):
    await message.answer("This is an example command response.")

# Metadata for the 'example_command' action
example_command.meta = {
    "name": "example_command",
    "type": "command",
    "description": "Responds to the /example command with a demonstration message."
}

@router.message(F.text == "example_button")
async def example_button(message: Message):
    await message.answer("This is an example button response.")

# Metadata for the 'example_button' action
example_button.meta = {
    "name": "example_button",
    "type": "button",
    "description": "Responds when the button with the text 'example_button' is pressed."
}
```

In this updated structure, **each action** (such as `example_command` or `example_button`) is assigned its own metadata via the `meta` attribute. This allows each action to be uniquely described with:

- **name**: A unique identifier for the action.
- **type**: The type of action (e.g., `command`, `button`).
- **description**: A brief explanation of the action’s behavior.

---

## 3. Action Documentation Format

Each plugin action (e.g., command, button, or task) requires descriptive metadata in the form of the `.meta` attribute for system integration:

```python
action.meta = {
    "name": "action_name",  # Unique identifier for the action
    "type": "action_type",  # The type of action: 'command', 'button', or 'task'
    "description": "A brief explanation of the action’s purpose and behavior."
}
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
PLUGIN_METADATA = {
    "name": "daily_message",
    "title": "Daily Message Plugin",
    "version": "1.0.0",
    "description": "Sends a daily message to all subscribed users at 6:00 AM.",
    "dependencies": []
}

import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from bot.db import get_all_users  # Custom module to retrieve user data

async def daily_task(bot: Bot):
    while True:
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        sleep_duration = (next_run - now).total_seconds()
        await asyncio.sleep(sleep_duration)

        users = get_all_users()  # Retrieve user list from the database
        for user in users:
            await bot.send_message(chat_id=user.id, text="Good morning! 🌅 Here's your daily message.")

# Metadata for the 'daily_task' action
daily_task.meta = {
    "name": "daily_task",
    "type": "task",
    "description": "Sends a daily greeting to all users at 6:00 AM."
}
```

---

## 5. Creating New Plugins

When developing new plugins, follow the same structure for metadata, actions, and implementation. Here's an example of another plugin:

```python
PLUGIN_METADATA = {
    "name": "new_plugin",
    "title": "New Plugin",
    "version": "1.0.0",
    "description": "Demonstrates how to create a new plugin with command and button actions.",
    "dependencies": []
}

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.middlewares import AccessLevel

router = Router()

# Middleware registration to ensure users have the correct access level
router.message.middleware(AccessLevel(1))

@router.message(Command("new_command"))
async def new_command(message: Message):
    """
    name: new_command
    type: command
    description: Handles the /new_command and demonstrates a new plugin command.
    """
    await message.answer("This is a new plugin command response.")

# Metadata for the 'new_command' action
new_command.meta = {
    "name": "new_command",
    "type": "command",
    "description": "Handles the /new_command and demonstrates a new plugin command."
}

@router.message(F.text == "new_button")
async def new_button(message: Message):
    """
    name: new_button
    type: button
    description: Responds when the button with the text 'new_button' is pressed.
    """
    await message.answer("This is a new plugin button response.")

# Metadata for the 'new_button' action
new_button.meta = {
    "name": "new_button",
    "type": "button",
    "description": "Responds when the button with the text 'new_button' is pressed."
}
```

---

## 6. Best Practices

- **Modularity:** Each plugin should be self-contained, with no dependencies on other plugins.
- **Unique Identifiers:** Use unique names for plugins, commands, and actions to avoid conflicts.
- **Clear Descriptions:** Provide concise and clear descriptions for better usability and maintenance.
- **Test Thoroughly:** Verify plugin functionality in isolation and with other plugins in the system.

---

By following these guidelines, you can create robust, maintainable, and expandable plugins for your system.
