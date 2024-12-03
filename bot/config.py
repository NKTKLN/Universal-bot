import io
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

# Создание объекта StringIO для записи логов в строку
log_stream = io.StringIO()

# Настройка базовой конфигурации логирования
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

# Создаем логгер
logger = logging.getLogger(__name__)

# Создание обработчика для записи в StringIO
string_handler = logging.StreamHandler(log_stream)

# Настройка уровня логирования для нового обработчика
string_handler.setLevel(config.LOG_LEVEL)

# Создание формата для лога и привязка его к обработчику
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
string_handler.setFormatter(formatter)

# Добавление обработчика для записи в StringIO
logger.addHandler(string_handler)
