import logging

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from notion.models import Category, Item


def main_kb() -> ReplyKeyboardMarkup:
    """
    Main keyboard
    :return ReplyKeyboardMarkup:
    """
    kb_list = [[KeyboardButton(text="📖 Все медикаменты"), KeyboardButton(text="💼 Посмотреть категории")],
               [KeyboardButton(text="✏️ Добавить в аптечку"), KeyboardButton(text="🧾 Проверить медикаменты")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def items_inline_kb(items: list[Item]) -> InlineKeyboardMarkup:
    """
    Items inline keyboard, generate kb from items list.
    :param items:
    :return InlineKeyboardMarkup:
    """
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


def category_inline_kb(categories: list[Category]) -> InlineKeyboardMarkup:
    """
    Categories inline keyboard, generate kb from the category list.
    :param categories:
    :return InlineKeyboardMarkup:
    """
    logging.warning(f"Categories: {categories}")
    builder = InlineKeyboardBuilder()
    for category in categories:
        callback_value = f'category_{abs(hash(category.name))}'
        builder.row(
            InlineKeyboardButton(
                text=category.name,
                callback_data=callback_value
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def item_crud_inline_kb(item: Item) -> InlineKeyboardMarkup:
    """
    Inline keyboard for update item.
    :param item:
    :return InlineKeyboardMarkup:
    """
    inline_kb_list = [
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f'change_item_{item._id}'),
         InlineKeyboardButton(text="🗑 Удалить",
                              callback_data=f'delete_item_{item._id}')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def del_buttons() -> ReplyKeyboardMarkup:
    """
    Delete Keyboard Buttons
    :return ReplyKeyboardMarkup:
    """
    kb_list = [[KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")]]
    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)


def item_edit_inline_kb(item: Item) -> InlineKeyboardMarkup:
    """
    Inline keyboard for callback edit item quantity.
    :param item:
    :return InlineKeyboardMarkup:
    """
    inline_kb_list = [
        [InlineKeyboardButton(text="✏️ Количество", callback_data=f'change_count_item_{item._id}')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def edit_count_inline_kb(categories: list[Category]) -> InlineKeyboardMarkup:
    """
    Inline keyboard for categories list.
    :param categories:
    :return InlineKeyboardMarkup:
    """
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.row(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f'category_{category.name}'
            )
        )
    builder.adjust(1)
    return builder.as_markup()
