from sqlalchemy import Column, Integer, String
from app.models.base import Base
from sqlalchemy.orm import relationship


class Plugin(Base):
    __tablename__ = 'plugins'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key for the plugin
    name = Column(String, unique=True)  # Name of the plugin, must be unique
    version = Column(String)  # Version of the plugin
    description = Column(String)  # Description of the plugin
    file_path = Column(String)  # Path to the plugin file

    functions = relationship("PluginFunction", back_populates="plugin", cascade="all, delete-orphan")  # Relationship to PluginFunction with cascade delete
