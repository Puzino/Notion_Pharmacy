import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from keyboards.kb import category_kb, main_kb
from notion.notion_api_handler import get_pages, get_all_unique_categories, get_items_by_category_name
from utils.create_bot import bot

notion_router = Router()

pharmacy_item_text = ("Название: {title} - {quantity} - {count_type}"
                      "\nТип: {pharmacy_type}"
                      "\nСрок годности до: {expiration_date}"
                      "\nОписание: {notes}"
                      "\nКатегория: {categories}")


@notion_router.message(F.text == '📖 Все медикаменты')
async def check_list(message: Message):
    await message.answer("Делаю запрос в Notion по всем препаратам!")
    for item in get_pages():
        await message.answer(
            text=pharmacy_item_text.format(title=item.title, quantity=item.quantity, count_type=item.count_type.name,
                                           pharmacy_type=item.pharmacy_type.name,
                                           expiration_date=item.get_date_for_telegram_bot(),
                                           notes=item.notes, categories=''.join(cat.name for cat in item.categories)),
            reply_markup=main_kb())


@notion_router.message(F.text == '💼 Посмотреть категории')
async def check_category_list(message: Message):
    await message.answer('Делаю запрос в Notion по всем категориям! Жди..')
    categories = get_all_unique_categories()
    await message.answer('Вот список всех категорий!', reply_markup=category_kb(categories))


@notion_router.callback_query(F.data.startswith('category_'))
async def get_items_by_category(call: CallbackQuery):
    await call.answer('')
    category_name = call.data.replace('category_', '')
    await call.message.answer(f'Делаю за запрос по категории: {category_name}')
    categories_by_name = get_items_by_category_name(category_name)
    await call.message.answer("", reply_markup=main_kb())
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        for item in categories_by_name:
            categories_text = ', '.join(cat.name for cat in item.categories)
            text = pharmacy_item_text.format(title=item.title, quantity=item.quantity,
                                             count_type=item.count_type.name,
                                             pharmacy_type=item.pharmacy_type.name,
                                             expiration_date=item.get_date_for_telegram_bot(),
                                             notes=item.notes, categories=categories_text)
            await call.message.answer(text=text)
