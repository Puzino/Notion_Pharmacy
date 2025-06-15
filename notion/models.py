from datetime import datetime

from dateutil.parser import parse
from pydantic import BaseModel


class Category(BaseModel):
    _id: str = None
    color: str = None
    name: str = None
    area_type: str = 'multi_select'

    class Config:
        frozen = True


class CountType(BaseModel):
    _id: str = None
    color: str = None
    name: str = None
    area_type: str = 'select'

    class Config:
        frozen = True


class PharmacyType(BaseModel):
    _id: str = None
    color: str = None
    name: str = None
    area_type: str = 'select'


class Item(BaseModel):
    _id: str = None
    title: str = None
    created: datetime = None
    categories: list[Category] = []
    expiration_date: datetime = None
    count_type: CountType = None
    pharmacy_type: PharmacyType = None
    notes: str = None
    quantity: int = None

    def get_created_datetime(self):
        return self.created.strftime('%H:%M %d.%m.%Y')

    def get_date_for_notion_create(self):
        return self.expiration_date.strftime('%Y-%m-%d')

    def get_date_for_telegram_bot(self):
        return self.expiration_date.strftime('%d.%m.%Y')

    def set_expiration_date(self, date: str):
        self.expiration_date = parse(date)

    def item_text(self):
        text = ("Название: {title} - {quantity} - {count_type}"
                "\nТип: {pharmacy_type}"
                "\nСрок годности до: {expiration_date}"
                "\nОписание: {notes}"
                "\nКатегория: {categories}")

        return text.format(title=self.title, quantity=self.quantity, count_type=self.count_type.name,
                           pharmacy_type=self.pharmacy_type.name, expiration_date=self.get_date_for_telegram_bot(),
                           notes=self.notes, categories=', '.join(x.name for x in self.categories))

    def clean_title(self):
        return self.title.lower().strip().capitalize()
