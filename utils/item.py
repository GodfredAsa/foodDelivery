from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.item import ItemModel
from utils.utils import format_created_date

_item_parser = reqparse.RequestParser()
_item_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_item_parser.add_argument("description", type=str, help=BLANK_ERROR.format("description"))
_item_parser.add_argument("price", type=float, required=True, help=BLANK_ERROR.format("price"))
_item_parser.add_argument("imageUrl", type=str, help=BLANK_ERROR.format("imageUrl"))
_item_parser.add_argument("qty", type=int, required=True, help=BLANK_ERROR.format("qty"))


def create_item_request_data(data) -> ItemModel:
    return ItemModel(data['name'], data['description'], data['price'], data['imageUrl'], data['qty'])


def item_data():
    return _item_parser.parse_args()


def item_exist(name):
    if not ItemModel.find_by_name(name):
        return False
    else:
        return True


def update_item(old_item: 'ItemModel', new_item: 'ItemModel') -> 'ItemModel':
    old_item.name = new_item.name
    old_item.id = old_item.id
    old_item.item_id = old_item.item_id
    old_item.description = new_item.description
    old_item.qty = new_item.qty
    old_item.imageUrl = new_item.imageUrl
    old_item.price = new_item.price
    old_item.createdAt = format_created_date()
    return old_item
