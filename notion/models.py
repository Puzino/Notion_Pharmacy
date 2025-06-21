from datetime import datetime

from dateutil.parser import parse
from pydantic import BaseModel


class Category(BaseModel):
    """
    Model: Category
    """
    _id: str = None
    color: str = None
    name: str = None
    area_type: str = 'multi_select'

    class Config:
        frozen = True


class CountType(BaseModel):
    """
    Model: CountType
    """
    _id: str = None
    color: str = None
    name: str = None
    area_type: str = 'select'

    class Config:
        frozen = True


class PharmacyType(BaseModel):
    """
    Model: PharmacyType
    """
    _id: str = None
    color: str = None
    name: str = None
    area_type: str = 'select'


class Item(BaseModel):
    """
    Main model: Item
    """
    _id: str = None
    title: str = None
    created: datetime = None
    categories: list[Category] = []
    expiration_date: datetime = None
    count_type: CountType = None
    pharmacy_type: PharmacyType = None
    notes: str = None
    quantity: int = None

    def get_created_datetime(self) -> str:
        """
        Func for obtaining the creation date in the database
        :return str:
        """
        return self.created.strftime('%H:%M %d.%m.%Y')

    def get_date_for_notion_create(self) -> str:
        """
        Clean datetime for item before add to the Notion Database
        :return str:
        """
        return self.expiration_date.strftime('%Y-%m-%d')

    def get_date_for_telegram_bot(self) -> str:
        """
        Clean datetime for item text in Aiogram bot
        :return str:
        """
        return self.expiration_date.strftime('%d.%m.%Y')

    def set_expiration_date(self, date: str) -> None:
        """
        Set expiration date in the model.
        :param date: str
        :return None:
        """
        self.expiration_date = parse(date)

    def categories_text(self) -> str:
        """
        Clean categories text for beautiful output in text
        :return str:
        """
        return ', '.join(x.name for x in self.categories)

    def item_text(self) -> str:
        """
        Item text for Aiogram bot.
        :return str:
        """
        text = ("Название: {title} - {quantity} - {count_type}"
                "\nТип: {pharmacy_type}"
                "\nСрок годности до: {expiration_date}"
                "\nОписание: {notes}"
                "\nКатегория: {categories}")

        return text.format(title=self.title, quantity=self.quantity, count_type=self.count_type.name,
                           pharmacy_type=self.pharmacy_type.name, expiration_date=self.get_date_for_telegram_bot(),
                           notes=self.notes, categories=self.categories_text())

    def clean_title(self) -> str:
        """
        Clean title, makes lowercase, add capitalizing, delete spaces
        :return str:
        """
        return self.title.lower().strip().capitalize()
