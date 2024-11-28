from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .plugin import Plugin
from app.models.base import Base


class PluginFunction(Base):
    __tablename__ = 'plugin_functions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key for the plugin function
    name = Column(String)  # Name of the function
    function_type = Column(String)  # Type of the function
    description = Column(String)  # Description of the function
    plugin_id = Column(Integer, ForeignKey('plugins.id'))  # Foreign key relationship to the Plugin table

    plugin = relationship('Plugin', back_populates='functions')  # Relationship to the Plugin table (back reference from PluginFunction to Plugin)
