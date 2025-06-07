from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.kb import main_kb, settings_kb

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hi!", reply_markup=main_kb())


@start_router.message(F.text == "⚙️ Настройки")
async def settings_keyboard(message: Message):
    await message.answer("Меню настроек", reply_markup=settings_kb())


@start_router.message(F.text == "💼 Вернуться назад")
async def main_menu(message: Message):
    await message.answer("Главное меню.", reply_markup=main_kb())


@start_router.message(F.text == '📖 Проверить задачи')
async def check_list(message: Message):
    await message.answer("Задача всё ещё в процессе. Попробуйте позже.")
