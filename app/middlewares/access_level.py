from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message
from aiogram import BaseMiddleware
from app.db import get_user_access_level, add_user
from aiogram.enums import ParseMode


class AccessLevel(BaseMiddleware):
    def __init__(self, access_level: int) -> None:
        self.access_level = access_level
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if await get_user_access_level(event.from_user.id) < self.access_level:
            add_user(event.from_user.id, 0)
            await event.answer("<b>🚫 Access to this section is restricted.</b>\nPlease contact the bot administrator to request permission.", parse_mode=ParseMode.HTML)
            return
        
        return await handler(event, data)
