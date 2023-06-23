from flask_jwt_extended import jwt_refresh_token_required
from flask_restful import Resource
import http.client as status
from constants.general_constants import REQUEST_PROCESS_NOT_SUCCESSFUL
from constants.item_constants import ITEM_NOT_FOUND
from constants.restaurant_constants import RESTAURANT_ALREADY_EXISTS, REQUEST_UNSUCCESSFUL, RESTAURANT_NOT_OPENED, \
    RESTAURANT_NOT_FOUND, RESTAURANT_DELETED, RESTAURANT_EXISTS
from model.item import ItemModel
from model.restaurant import RestaurantModel
from utils.restaurant import restaurant_data, update_restaurants
from utils.utils import return_message


class CreateRestaurantResource(Resource):
    @jwt_refresh_token_required
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
            print(str(e))
            return return_message(status.BAD_REQUEST, REQUEST_UNSUCCESSFUL)

    def get(self):
        if len(RestaurantModel.find_all_restaurants()) <= 0:
            return return_message(status.OK, RESTAURANT_NOT_OPENED), status.OK
        return [x.json() for x in RestaurantModel.find_all_restaurants()]


class RestaurantResource(Resource):
    def get(self, name):
        restaurant = RestaurantModel.find_restaurant_by_name(name)
        if not restaurant:
            return return_message(status.NOT_FOUND, RESTAURANT_NOT_FOUND), status.NOT_FOUND
        return restaurant.json()

    @jwt_refresh_token_required
    def put(self, name):
        try:
            data = restaurant_data()
            new_restaurant = RestaurantModel(**data)
            old_restaurant: 'RestaurantModel' = RestaurantModel.find_restaurant_by_name(name)
            if not old_restaurant:
                return return_message(status.NOT_FOUND, RESTAURANT_NOT_FOUND), status.NOT_FOUND
            if not ItemModel.find_item_id(new_restaurant.item_id):
                return return_message(status.BAD_REQUEST, ITEM_NOT_FOUND), status.BAD_REQUEST
            if RestaurantModel.find_restaurant_by_name(new_restaurant.name):
                return return_message(status.NOT_FOUND, RESTAURANT_EXISTS), status.NOT_FOUND
            restaurant = update_restaurants(old_restaurant, new_restaurant)
            restaurant.save_restaurant_db()
            return restaurant.json(), status.OK
        except Exception as e:
            print(REQUEST_PROCESS_NOT_SUCCESSFUL, str(e))
            return return_message(status.BAD_REQUEST, REQUEST_PROCESS_NOT_SUCCESSFUL), status.BAD_REQUEST

    @jwt_refresh_token_required
    def delete(self, name):
        restaurant: 'RestaurantModel' = RestaurantModel.find_restaurant_by_name(name)
        if not restaurant:
            return return_message(status.NOT_FOUND, RESTAURANT_NOT_FOUND), status.NOT_FOUND
        restaurant.delete_from_db()
        return return_message(status.OK, RESTAURANT_DELETED), status.OK
