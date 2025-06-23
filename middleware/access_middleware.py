from typing import Callable, Dict, Awaitable, List

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from decouple import config

ALLOWED_LIST: List[int] = list(map(int, config('USERS').split(',')))


class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict], Awaitable], event: TelegramObject, data: Dict):
        if isinstance(event, Message):
            user_id = event.from_user.id
            if user_id not in ALLOWED_LIST:
                await event.answer("Доступ запрещен.")
                return None
        return await handler(event, data)
