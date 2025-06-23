import pytz
from dateutil.parser import parse
from decouple import config
from notion_client import Client

from notion.models import Item, Category, PharmacyType, CountType

NOTION_TOKEN = config("NOTION_TOKEN")
DATABASE_ID = config("DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)


def notion_items_formatter(results: dict) -> list[Item]:
    """
    Formating dict to model Items
    :param results: dict
    :return list[Item]:
    """
    items = []
    for result in results:
        item = Item()
        item._id = result['id']
        item.created = parse(result['created_time']).astimezone(pytz.timezone(config("TIME_ZONE")))
        properties = result['properties']

        expiration_date_dict = properties.get('Expiration_date').get('date')
        if expiration_date_dict:
            item.set_expiration_date(expiration_date_dict.get('start'))

        title_dict = properties.get('Name')
        if title_dict:
            item.title = title_dict.get('title')[0].get('plain_text')

        categories_dict = properties.get('Categories')
        if categories_dict:
            item.categories = [Category(_id=category.get("id"), name=category.get('name'), color=category.get('color'))
                               for
                               category in categories_dict.get('multi_select')]

        count_type_dict = properties.get('Count_type').get('select')
        if count_type_dict:
            item.count_type = CountType(_id=count_type_dict.get("id"), name=count_type_dict.get('name'),
                                        color=count_type_dict.get('color'))

        pharmacy_type_dict = properties.get('Pharmacy_type').get('select')
        if pharmacy_type_dict:
            item.pharmacy_type = PharmacyType(_id=pharmacy_type_dict.get("id"), name=pharmacy_type_dict.get('name'),
                                              color=pharmacy_type_dict.get('color'))

        quantity_dict = properties.get('Quantity')
        if quantity_dict:
            item.quantity = quantity_dict.get('number')

        notes_dict = properties.get('Notes').get('rich_text')
        if notes_dict:
            item.notes = notes_dict[0].get('text').get('content')

        items.append(item)
    return items


def get_items() -> list[Item]:
    """
    Get all items dict from the Notion database.
    :return list[Item]:
    """
    data = notion.databases.query(database_id=DATABASE_ID)
    has_more = data['has_more']
    next_cursor = data['next_cursor']
    while has_more:
        data_while = notion.databases.query(database_id=DATABASE_ID, start_cursor=next_cursor)
        for row in data_while['results']:
            data['results'].append(row)
        has_more = data_while['has_more']
        next_cursor = data_while['next_cursor']

    return notion_items_formatter(data['results'])


def get_items_by_category_name(category_name: str) -> list[Item]:
    """
    Get items by category name
    :param category_name: str
    :return list[Item]:
    """
    results = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Categories",
                "multi_select": {
                    "contains": category_name,
                },
            },
        }
    ).get('results')
    return notion_items_formatter(results)


def delete_item(item_id) -> None:
    """
    Delete item from the Notion database
    :param item_id:
    :return:
    """
    response = notion.pages.update(
        page_id=item_id,
        archived=True,
    )
    return response


def create_data_for_create_update(item: Item) -> dict:
    """
    Create data from Item for update.
    :param item:
    :return dict:
    """
    page_data = {
        "properties": {
            "Categories": {
                "type": "multi_select",
                "multi_select": [{'name': category.name.strip().lower().capitalize()} for category in
                                 item.categories]
            },
            "Count_type": {
                "type": "select",
                "select": {'name': item.count_type.name}
            },
            "Expiration_date": {
                "type": "date",
                "date": {
                    'start': item.get_date_for_notion_create()
                }
            },
            "Notes": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": item.notes
                        }
                    }
                ]
            },
            "Name": {
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": item.title
                        }
                    }
                ]
            },
            'Pharmacy_type': {'select': {'name': item.pharmacy_type.name},
                              'type': item.pharmacy_type.area_type},
            'Quantity': {'number': item.quantity, 'type': 'number'}
        }
    }
    return page_data


def create_item(item: Item):
    """
    Add item to the Notion database
    :param item:
    :return:
    """
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=create_data_for_create_update(item)['properties'],
    )
    return response


def get_all_unique_categories() -> list:
    """
    Get all unique categories from the database
    :return list:
    """
    unique_categories = list()
    items = get_items()
    for item in items:
        for category in item.categories:
            if category not in unique_categories:
                unique_categories.append(Category(_id=category._id, name=category.name, color=category.color))
    return sorted(unique_categories, key=lambda x: x.name)


def get_item_by_id(item_id: str) -> Item:
    """
    Get item by id
    :param item_id:
    :return:
    """
    data = [notion.pages.retrieve(page_id=item_id)]
    item = notion_items_formatter(data)[0]
    return item


def update_item_by_id(item_id: str, item: Item) -> None:
    """
    Update item by id
    :param item_id:
    :param item:
    :return None:
    """
    notion.pages.update(
        page_id=item_id,
        properties=create_data_for_create_update(item)['properties'])
    return None
