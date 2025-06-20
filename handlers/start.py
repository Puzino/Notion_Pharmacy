from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.kb import main_kb

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hi!", reply_markup=main_kb())
