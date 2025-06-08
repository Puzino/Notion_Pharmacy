import pytz
from dateutil.parser import parse
from decouple import config
from notion_client import Client

from notion.models import Item, Category, PharmacyType, CountType

NOTION_TOKEN = config("NOTION_TOKEN")
DATABASE_ID = config("DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)


def notion_items_formatter(results: dict) -> list[Item]:
    items = []
    for result in results:
        item = Item()
        item._id = result['id']
        item.created = parse(result['created_time']).astimezone(pytz.timezone(config("TIME_ZONE")))
        properties = result['properties']

        expiration_date_dict = properties.get('Expiration_date').get('date')
        if expiration_date_dict:
            item.expiration_date = parse(expiration_date_dict.get('start'))

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


def get_pages():
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


def get_items_by_category_name(category_name: Category) -> list[Item]:
    results = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Categories",
                category_name.type: {
                    "contains": category_name.name,
                },
            },
        }
    ).get('results')
    return notion_items_formatter(results)


def delete_page(page_id) -> None:
    response = notion.pages.update(
        page_id=page_id,
        archived=True,
    )
    return response


def create_page(item: Item):
    page_data = {
        "properties": {
            "Categories": {
                "type": "multi_select",
                "multi_select": [{'color': category.color, 'id': category._id, 'name': category.name} for category in
                                 item.categories]
            },
            "Count_type": {
                "type": "select",
                "select": {'color': item.count_type.color,
                           'id': item.count_type.id,
                           'name': item.count_type.name}
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
            'Pharmacy_type': {'select': {'color': item.pharmacy_type.color,
                                         'id': item.pharmacy_type.id,
                                         'name': item.pharmacy_type.name},
                              'type': item.pharmacy_type.type},
            'Quantity': {'number': item.quantity, 'type': 'number'}
        }
    }
    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=page_data['properties'],

    )
    return response


def get_all_unique_count_type():
    unique_count_type = set()
    items = get_pages()
    for item in items:
        unique_count_type.add(
            CountType(_id=item.count_type._id, name=item.count_type.name, color=item.count_type.color))
    return unique_count_type


def get_all_unique_categories():
    unique_categories = set()
    items = get_pages()
    for item in items:
        for category in item.categories:
            unique_categories.add(Category(_id=category._id, name=category.name, color=category.color))
    return unique_categories
