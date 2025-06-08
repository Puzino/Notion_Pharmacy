from datetime import datetime

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
