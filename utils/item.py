from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.item import ItemModel

_item_parser = reqparse.RequestParser()
_item_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_item_parser.add_argument("description", type=str, help=BLANK_ERROR.format("description"))
_item_parser.add_argument("price", type=float, required=True, help=BLANK_ERROR.format("price"))
_item_parser.add_argument("imageUrl", type=str, help=BLANK_ERROR.format("imageUrl"))
_item_parser.add_argument("qty", type=int, help=BLANK_ERROR.format("qty"))



def item_data():
    return _item_parser.parse_args()


def item_exist(name):
    if not ItemModel.find_by_name(name):
        return False
    else:
        return True
