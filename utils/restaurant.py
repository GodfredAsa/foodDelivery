from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.restaurant import RestaurantModel

_restaurant_parser = reqparse.RequestParser()
_restaurant_parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))
_restaurant_parser.add_argument("itemId", type=int, help=BLANK_ERROR.format("itemId"))
_restaurant_parser.add_argument("city", type=str, required=True, help=BLANK_ERROR.format("city"))


def restaurant_data():
    return _restaurant_parser.parse_args()


def restaurant_exist(name):
    if not RestaurantModel.find_restaurant_by_name(name):
        return False
    else:
        return True
