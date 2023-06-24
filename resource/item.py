
from flask_restful import Resource
import http.client as status

from constants.general_constants import REQUEST_PROCESS_NOT_SUCCESSFUL
from constants.item_constants import ITEM_ALREADY_EXISTS, ITEM_NOT_CREATED, ITEM_NOT_FOUND, ITEM_DELETED
from model.item import ItemModel
from utils.item import item_data, item_exist, update_item
from flask_jwt_extended import jwt_refresh_token_required
from utils.utils import return_message


class ListOfItemsResource(Resource):

    def get(self):
        return [item.json() for item in ItemModel.find_items()]


class CreateItemResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        data = item_data()
        try:
            item = ItemModel(**data)
            if item_exist(item.name):
                return return_message(status.BAD_REQUEST, ITEM_ALREADY_EXISTS), status.BAD_REQUEST
            item.save_item_db()
            return item.json(), status.CREATED
        except Exception as e:
            print(ITEM_NOT_CREATED, str(e))
            return return_message(status.BAD_REQUEST, ITEM_NOT_CREATED), status.BAD_REQUEST


class ItemResource(Resource):

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return return_message(status.BAD_REQUEST, ITEM_NOT_FOUND), status.BAD_REQUEST
        return item.json(), status.OK

    @jwt_refresh_token_required
    def put(self, name):
        try:
            data = item_data()
            old_item = ItemModel.find_by_name(name)
            if not old_item:
                return return_message(status.BAD_REQUEST, ITEM_NOT_FOUND), status.BAD_REQUEST
            if ItemModel.find_by_name(data['name']):
                return return_message(status.CONFLICT, ITEM_ALREADY_EXISTS), status.CONFLICT
            new_item = ItemModel(**data)
            item = update_item(old_item, new_item)
            item.save_item_db()
            return item.json(), status.OK
        except Exception as e:
            print(REQUEST_PROCESS_NOT_SUCCESSFUL, str(e))
            return_message(status.BAD_REQUEST, REQUEST_PROCESS_NOT_SUCCESSFUL), status.BAD_REQUEST

    @jwt_refresh_token_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return return_message(status.BAD_REQUEST, ITEM_NOT_FOUND), status.BAD_REQUEST
        item.delete_item_db()
        return return_message(status.OK, ITEM_DELETED), status.OK

