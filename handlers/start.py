from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.kb import main_kb

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    First message from bot, func for start
    :param message:
    :return:
    """
    await message.answer("Hi!\nI`m Telegram bot that helps manage and structure medical data in Notion.",
                         reply_markup=main_kb())
