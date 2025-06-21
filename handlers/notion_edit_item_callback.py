"""
File for callback edit item
"""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.kb import item_edit_inline_kb, main_kb
from notion.notion_api_handler import get_item_by_id, update_item_by_id

callback_notion_edit_router = Router()


class ItemEditForm(StatesGroup):
    """
    Form for edit States group
    """
    item = State()
    quantity = State()


@callback_notion_edit_router.callback_query(F.data.startswith('change_item_'))
async def edit_item(call: CallbackQuery, state: FSMContext):
    """
    Main callback func for edit item, receives item for editing.
    :param call:
    :param state:
    :return:
    """
    await call.answer()
    await call.message.answer('Одну секунду..')
    item_id = call.data.replace('change_item_', '')
    item = get_item_by_id(item_id)
    await state.update_data(item=item)
    await call.message.answer(f"<b>Редактируем</b>\n{item.item_text()}", reply_markup=item_edit_inline_kb(item))


@callback_notion_edit_router.callback_query(F.data.startswith('change_count_item_'))
async def edit_item_count(call: CallbackQuery, state: FSMContext):
    """
    Set state quantity item.
    :param call:
    :param state:
    :return:
    """
    await call.answer()
    await state.set_state(ItemEditForm.quantity)
    await call.message.answer('Напиши новое количество:')


@callback_notion_edit_router.message(F.text, ItemEditForm.quantity)
async def new_count_item(message: Message, state: FSMContext):
    """
    Set quantity item. Update item in the Notion database.
    :param message:
    :param state:
    :return:
    """
    await message.answer('Обновляю информацию..')
    new_quantity = int(''.join(x for x in message.text if x.isdigit()))
    data = await state.get_data()
    item = data.get('item')
    item.quantity = new_quantity
    update_item_by_id(item._id, item)
    await state.clear()
    await message.answer(f'Супер! Мы установили новое количество!\nНовое количество у {item.title} - {item.quantity}',
                         reply_markup=main_kb())
