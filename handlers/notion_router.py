from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.kb import category_inline_kb, main_kb, item_crud_inline_kb
from notion.notion_api_handler import get_pages, get_all_unique_categories, get_items_by_category_name

notion_router = Router()

pharmacy_item_text = ("Название: {title} - {quantity} - {count_type}"
                      "\nТип: {pharmacy_type}"
                      "\nСрок годности до: {expiration_date}"
                      "\nОписание: {notes}"
                      "\nКатегория: {categories}")


@notion_router.message(F.text == '📖 Все медикаменты')
async def check_list(message: Message):
    await message.answer("Делаю запрос в Notion по всем препаратам!")
    items = get_pages()
    for item in items:
        await message.answer(
            text=pharmacy_item_text.format(title=item.title, quantity=item.quantity, count_type=item.count_type.name,
                                           pharmacy_type=item.pharmacy_type.name,
                                           expiration_date=item.get_date_for_telegram_bot(),
                                           notes=item.notes, categories=', '.join(cat.name for cat in item.categories)),
            reply_markup=item_crud_inline_kb(item))
    await message.answer(f'Вот список всех лекарств. Количество в базе: {len(items)}', reply_markup=main_kb())


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
    for item in categories_by_name:
        categories_text = ', '.join(cat.name for cat in item.categories)
        text = pharmacy_item_text.format(title=item.title, quantity=item.quantity,
                                         count_type=item.count_type.name,
                                         pharmacy_type=item.pharmacy_type.name,
                                         expiration_date=item.get_date_for_telegram_bot(),
                                         notes=item.notes, categories=categories_text)
        await call.message.answer(text=text, reply_markup=item_crud_inline_kb(item))
    await call.message.answer(
        text=f"Вот список всех лекарств по запросу {category_name}.\nВсего элементов: {len(categories_by_name)}",
        reply_markup=main_kb())
