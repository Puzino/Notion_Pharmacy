from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from notion.models import Category, Item


def main_kb():
    kb_list = [[KeyboardButton(text="📖 Все медикаменты"), KeyboardButton(text="💼 Посмотреть категории")],
               [KeyboardButton(text="✏️ Добавить в аптечку"), KeyboardButton(text="🧾 Проверить медикаменты")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def items_inline_kb(items: list[Item]):
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки вопросов
    for item in items:
        text = f'✅{item.title} - {item.categories_text()}. {item.quantity}' \
            if item.quantity else f'❌{item.title} - {item.categories_text()}'
        builder.row(
            InlineKeyboardButton(
                text=text,
                callback_data=f'item_{item._id}'
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def category_inline_kb(categories: list[Category]):
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки вопросов
    for category in categories:
        builder.row(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f'category_{category.name}'
            )
        )
    # Добавляем кнопку "На главную"
    # builder.row(
    #     InlineKeyboardButton(
    #         text='На главную',
    #         callback_data='back_home'
    #     )
    # )
    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()


def item_crud_inline_kb(item: Item):
    inline_kb_list = [
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f'change_item_{item._id}'),
         InlineKeyboardButton(text="🗑 Удалить",
                              callback_data=f'delete_item_{item._id}')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def del_buttons():
    kb_list = [[KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def item_edit_inline_kb(item: Item):
    inline_kb_list = [
        [InlineKeyboardButton(text="✏️ Количество", callback_data=f'change_count_item_{item._id}')]]
    # InlineKeyboardButton(text="✏️ Название", callback_data=f'change_item_count_{item._id}')],
    # [InlineKeyboardButton(text="✏️ Описание", callback_data=f'change_item_count_{item._id}'),
    #  InlineKeyboardButton(text="✏️ Тип лекарства", callback_data=f'change_item_count_{item._id}')],
    # [InlineKeyboardButton(text="✏️ Срок годности", callback_data=f'change_item_count_{item._id}'),
    #  InlineKeyboardButton(text="✏️ Категорию", callback_data=f'change_item_count_{item._id}')]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def edit_count_inline_kb(categories: list[Category]):
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки вопросов
    for category in categories:
        builder.row(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f'category_{category.name}'
            )
        )
    # Добавляем кнопку "На главную"
    # builder.row(
    #     InlineKeyboardButton(
    #         text='На главную',
    #         callback_data='back_home'
    #     )
    # )
    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()
