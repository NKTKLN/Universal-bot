from sqlalchemy import Column, Integer
from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # Primary key for the user
    access_level = Column(Integer)  # Access level as an integer (e.g., 0 = unauthorized user, 1 = regular user, 2 = admin, 3 = owner)
