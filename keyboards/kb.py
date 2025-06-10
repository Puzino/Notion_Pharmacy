from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from notion.models import Category, Item


def settings_kb():
    kb_list = [[KeyboardButton(text="💼 Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def main_kb():
    kb_list = [[KeyboardButton(text="📖 Все медикаменты"), KeyboardButton(text="💼 Посмотреть категории")],
               [KeyboardButton(text="✏️ Добавить в аптечку")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


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
