import io
import sys
import logging
from typing import Any
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str
    OWNER_ID: int
    DATABASE_URL: str

    LOG_LEVEL: str = "INFO" 
    PLUGIN_NAME_REGEX: str = r"^[a-zA-Z0-9_]+$"
    PLUGINS_DIR: Any = Path(__file__).resolve().parent / 'custom_plugins'

    VERSION: str = "1.1.0"

    model_config = ConfigDict(env_file=".env")


config = Config()

# Create a StringIO object for logging to a string
log_stream = io.StringIO()

# Configure basic logging settings
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

# Create a logger
logger = logging.getLogger(__name__)

# Create a handler for logging to StringIO
string_handler = logging.StreamHandler(log_stream)
string_handler.setLevel(config.LOG_LEVEL)

# Set the log format for the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
string_handler.setFormatter(formatter)

# Add the StringIO handler to the logger
logger.addHandler(string_handler)
