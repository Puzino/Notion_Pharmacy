"""
File for callback delete item
"""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.kb import del_buttons, main_kb
from notion.notion_api_handler import delete_item

callback_notion_del_upd_router = Router()


class ItemDelForm(StatesGroup):
    """
    Form States group
    """
    item_id = State()
    are_you_sure = State()


@callback_notion_del_upd_router.callback_query(F.data.startswith('delete_item_'))
async def del_callback_pharmacy(call: CallbackQuery, state: FSMContext):
    """
    Main callback func for delete item, receives item for deleting.
    :param call:
    :param state:
    :return:
    """
    await call.answer()
    item_id = call.data.replace('delete_item_', '')
    text = 'Вы уверенны что хотите удалить лекарство - <b>(Да, нет)?</b>:'
    await call.message.answer(text=text, reply_markup=del_buttons())
    await state.set_state(ItemDelForm.are_you_sure)
    await state.update_data(item_id=item_id)


@callback_notion_del_upd_router.message(F.text, ItemDelForm.are_you_sure)
async def del_pharmacy(message: Message, state: FSMContext):
    """
    Checks whether the user is sure about deleting, if `yes` delete the item from the Notion database.
    :param call:
    :param state:
    :return:
    """
    answer = ''.join(x for x in message.text.lower().strip() if x.isalpha())
    await state.update_data(are_you_sure=answer)
    await state.set_state(ItemDelForm.are_you_sure)
    await message.answer(f'Ваш ответ: {answer.capitalize()}', reply_markup=main_kb())
    data = await state.get_data()
    page_id = data.get('item_id')
    if answer == 'да':
        delete_item(page_id)
        await message.answer(f'Удалил: {page_id}')
    else:
        await message.answer('Не удаляем.')
    await state.clear()
