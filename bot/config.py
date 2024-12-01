import sys
import logging
from typing import Any
from pathlib import Path
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str
    OWNER_ID: int
    DATABASE_URL: str

    LOG_LEVEL: str = "INFO" 
    PLUGIN_NAME_REGEX: str = r"^[a-zA-Z0-9_]+$"
    PLUGINS_DIR: Any = Path(__file__).resolve().parent / 'custom_plugins'

    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


config = Config()

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)
