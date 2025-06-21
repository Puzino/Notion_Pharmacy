from datetime import datetime

import requests
from decouple import config

from notion.notion_api_handler import get_items

BOT_TOKEN = config('TOKEN')
USERS = config("USERS").split(',')

numbers_dict = {
    0: '0️⃣',
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣'
}


async def send_text_to_telegram(text: str) -> None:
    """
    Send a message about expiration date and quantity to the user list
    :param text:
    :return:
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for telegram_id in USERS:
        payload = {
            "chat_id": telegram_id,
            "text": text,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload)


def days_between(d1, d2) -> int:
    """
    Counts the number of days between the current date and the expiration date.
    :param d1:
    :param d2:
    :return int:
    """
    return (d2 - d1).days


async def pharmacy_checker() -> None:
    """
    Checks all items for expiration date and quantity
    :return:
    """
    items = get_items()
    today = datetime.now().date()
    for item in items:
        expiration_date = days_between(item.expiration_date.date(), today)
        quantity = item.quantity
        if -3 <= expiration_date <= 0:
            expiration_date = abs(expiration_date)
            text = f'<b>⚠️Срок годности заканчивается через {expiration_date} дня:</b>\n{item.item_text()}' \
                if expiration_date != 0 else f'<b>🚫Закончился срок годности:</b>\n{item.item_text()}'
            await send_text_to_telegram(text)
        elif quantity <= 5:
            text = f'<b>{numbers_dict[quantity]} Осталось малое количество лекарства:</b>\n{item.item_text()}' \
                if quantity > 0 else f'<b>{numbers_dict[0]} Закончился препарат:</b>\n{item.item_text()}'
            await send_text_to_telegram(text)
