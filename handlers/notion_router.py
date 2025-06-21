from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.kb import category_inline_kb, item_crud_inline_kb, items_inline_kb
from notion.notion_api_handler import get_items, get_all_unique_categories, get_items_by_category_name, get_item_by_id
from utils.utils import pharmacy_checker

notion_router = Router()


@notion_router.message(F.text == '📖 Все медикаменты')
async def check_list(message: Message):
    await message.answer("Делаю запрос в Notion по всем препаратам!")
    items = get_items()
    await message.answer(text=f'Вот список всех лекарств. Количество в базе: {len(items)}',
                         reply_markup=items_inline_kb(items))


@notion_router.message(F.text == '🧾 Проверить медикаменты')
async def check_pharmacy(message: Message):
    await message.answer('Проверяю медикаменты..')
    pharmacy_checker()


@notion_router.callback_query(F.data.startswith('item_'))
async def get_item(call: CallbackQuery):
    await call.answer('')
    item_id = call.data.replace('item_', '')
    item = get_item_by_id(item_id)
    await call.message.answer(item.item_text(), reply_markup=item_crud_inline_kb(item))


@notion_router.message(F.text == '💼 Посмотреть категории')
async def check_category_list(message: Message):
    await message.answer('Делаю запрос в Notion по всем категориям! Жди..')
    categories = get_all_unique_categories()
    await message.answer('Вот список всех категорий!', reply_markup=category_inline_kb(categories))


@notion_router.callback_query(F.data.startswith('category_'))
async def get_items_by_category(call: CallbackQuery):
    await call.answer('')
    category_name = call.data.replace('category_', '')
    await call.message.answer(f'Делаю за запрос по категории: {category_name}')
    categories_by_name = get_items_by_category_name(category_name)
    await call.message.answer(
        text=f"Вот список всех лекарств по запросу {category_name}.\nВсего элементов: {len(categories_by_name)}",
        reply_markup=items_inline_kb(categories_by_name))
