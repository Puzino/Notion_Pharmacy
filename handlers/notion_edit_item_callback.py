from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.kb import item_edit_inline_kb
from notion.notion_api_handler import get_item_by_id

callback_notion_edit_router = Router()


# class ItemForm(StatesGroup):
#     title = State()
#     categories = State()
#     expiration_date = State()
#     count_type = State()
#     pharmacy_type = State()
#     notes = State()
#     quantity = State()


@callback_notion_edit_router.callback_query(F.data.startswith('change_item_'))
async def edit_item(call: CallbackQuery):
    await call.answer()
    await call.message.answer('Одну секунду..')
    item_id = call.data.replace('change_item_', '')
    item = get_item_by_id(item_id)
    await call.message.answer(f"<b>Редактируем</b>\n{item.item_text()}", reply_markup=item_edit_inline_kb(item))

# @callback_notion_add_router.message(F.text, ItemForm.title)
# async def capture_name(message: Message, state: FSMContext):
#     await state.update_data(title=message.text)
#     await message.answer('Супер! А теперь напиши категорию (если их несколько напиши через запятую ","):')
#     await state.set_state(ItemForm.categories)


# @callback_notion_add_router.message(F.text, ItemForm.quantity)
# async def capture_quantity(message: Message, state: FSMContext):
#     await state.update_data(quantity=message.text)
#     await message.answer("Спасибо!")
#     data = await state.get_data()
#     item = Item(title=data.get("title"),
#                 categories=[Category(name=category) for category in data.get('categories').split(',')],
#                 count_type=CountType(name=data.get('count_type')),
#                 pharmacy_type=PharmacyType(name=data.get('pharmacy_type')),
#                 notes=data.get('notes'),
#                 quantity=int(data.get('quantity')))
#     item.set_expiration_date(data.get('expiration_date'))
#     request = create_page(item)
#     await message.answer(
#         f"Препарат успешно добавлен {item.title}, {item.quantity} - {item.count_type.name}\nId: {request.get('id')}",
#         reply_markup=main_kb())
#     await state.clear()
