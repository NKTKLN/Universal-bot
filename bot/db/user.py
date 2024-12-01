from sqlalchemy.future import select
from bot.models import User
from bot.config import logger
from .database import get_session


# Adding a new user
async def add_user(user_id: int, access_level: int) -> None:
    """
    Adds a new user to the database if they don't already exist.

    :param user_id: The ID of the user.
    :param access_level: The access level of the user.
    """
    
    async for session in get_session():
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user:
            return  # User already exists, do not add

        new_user = User(id=user_id, access_level=access_level)
        session.add(new_user)
        await session.commit()
    
    logger.info(f"User with id {user_id} and access level {access_level} was created.")


# Getting a user's access level by their user ID
async def get_user_access_level(user_id: int) -> int:
    """
    Retrieves the access level of a user by their ID.

    :param user_id: The ID of the user.
    :return: The access level of the user, or 0 if the user is not found.
    """
    
    async for session in get_session():
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user:
            return user.access_level
        return 0


# Getting all users
async def get_all_users() -> list[User]:
    """
    Retrieves all users from the database.

    :return: A list of User objects.
    """
    users = []
    async for session in get_session():
        result = await session.execute(select(User))
        users = result.scalars().all()
    return users
