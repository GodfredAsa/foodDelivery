from flask_restful import Resource
import http.client as status
from constants.item_constants import ITEM_NOT_FOUND
from constants.restaurant_constants import RESTAURANT_ALREADY_EXISTS, REQUEST_UNSUCCESSFUL, RESTAURANT_NOT_OPENED
from model.item import ItemModel
from model.restaurant import RestaurantModel
from utils.restaurant import restaurant_data
from utils.utils import return_message


class RestaurantResource(Resource):
    def post(self):
        try:
            data = restaurant_data()
            if RestaurantModel.find_restaurant_by_name(data['name']):
                return return_message(status.BAD_REQUEST,
                                      RESTAURANT_ALREADY_EXISTS.format(data['name'])), status.BAD_REQUEST
            if ItemModel.find_item_id(data['itemId']):
                restaurant = RestaurantModel(**data)
                restaurant.save_restaurant_db()
                return restaurant.json()
            return return_message(status.NOT_FOUND, ITEM_NOT_FOUND), status.NOT_FOUND
        except Exception as e:
            return return_message(status.BAD_REQUEST, REQUEST_UNSUCCESSFUL)

    def get(self):
        if len(RestaurantModel.find_all_restaurants()) <= 0:
            return return_message(status.OK, RESTAURANT_NOT_OPENED), status.OK
        return [x.json() for x in RestaurantModel.find_all_restaurants()]
