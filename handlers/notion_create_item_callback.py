from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from notion.models import Item, Category, CountType, PharmacyType
from notion.notion_api_handler import create_page

callback_notion_add_router = Router()


class ItemForm(StatesGroup):
    title = State()
    categories = State()
    expiration_date = State()
    count_type = State()
    pharmacy_type = State()
    notes = State()
    quantity = State()


@callback_notion_add_router.message(F.text == '✏️ Добавить в аптечку')
async def add_to_pharmacy(message: Message, state: FSMContext):
    text = ("Чтобы добавить новый препарат в аптечку нужно написать текст последовательно в таком формате:"
            "\nНазвание"
            "\nКатегория"
            "\nДень конца срока в формате: 01.01.1970"
            "\nТип подсчета (Шт., мг., мл., и тд.)"
            "\nТип лекарства (Таблетки, капсулы и тд.)"
            "\nПримечание (если нужно)"
            "\nКоличество")
    await message.answer(text=text)
    await message.answer(text="Начнем с названия препарата")
    await state.set_state(ItemForm.title)


@callback_notion_add_router.message(F.text, ItemForm.title)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer('Супер! А теперь напиши категорию (если их несколько напиши через запятую ","):')
    await state.set_state(ItemForm.categories)


@callback_notion_add_router.message(F.text, ItemForm.categories)
async def capture_categories(message: Message, state: FSMContext):
    await state.update_data(categories=message.text)
    await message.answer('Супер! А теперь напиши дату окончания срока годности (01.01.1970):')
    await state.set_state(ItemForm.expiration_date)


@callback_notion_add_router.message(F.text, ItemForm.expiration_date)
async def capture_expiration_date(message: Message, state: FSMContext):
    await state.update_data(expiration_date=message.text)
    await message.answer('Супер! А теперь напиши тип исчисления (Шт. мг. мл.):')
    await state.set_state(ItemForm.count_type)


@callback_notion_add_router.message(F.text, ItemForm.count_type)
async def capture_count_type(message: Message, state: FSMContext):
    await state.update_data(count_type=message.text)
    await message.answer('Супер! А теперь напиши тип препарата (Таблетки, сироп, капсулы и тд.):')
    await state.set_state(ItemForm.pharmacy_type)


@callback_notion_add_router.message(F.text, ItemForm.pharmacy_type)
async def capture_pharmacy_type(message: Message, state: FSMContext):
    await state.update_data(pharmacy_type=message.text)

    await message.answer('Супер! А теперь напиши примечание к препарату (если нужно):')
    await state.set_state(ItemForm.notes)


@callback_notion_add_router.message(F.text, ItemForm.notes)
async def capture_notes(message: Message, state: FSMContext):
    await state.update_data(notes=message.text)
    await message.answer('Супер! А теперь напиши количество препарата (10, 20 и тд.):')
    await state.set_state(ItemForm.quantity)


@callback_notion_add_router.message(F.text, ItemForm.quantity)
async def capture_quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await message.answer("Спасибо!")
    data = await state.get_data()
    item = Item(title=data.get("title"),
                categories=[Category(name=category) for category in data.get('categories').split(',')],
                count_type=CountType(name=data.get('count_type')),
                pharmacy_type=PharmacyType(name=data.get('pharmacy_type')),
                notes=data.get('notes'),
                quantity=int(data.get('quantity')))
    item.set_expiration_date(data.get('expiration_date'))
    request = create_page(item)
    await message.answer(
        f"Препарат успешно добавлен {item.title}, {item.quantity} - {item.count_type.name}\nId: {request.get('id')}")
    await state.clear()
