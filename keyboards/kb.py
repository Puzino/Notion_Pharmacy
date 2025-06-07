from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def settings_kb():
    kb_list = [[KeyboardButton(text="💼 Вернуться назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def main_kb():
    kb_list = [[KeyboardButton(text="📖 Проверить задачи"), KeyboardButton(text="💼 Посмотреть историю")],
               [KeyboardButton(text="⚙️ Настройки")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
