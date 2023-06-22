
from flask_restful import Resource
import http.client as status
from constants.item_constants import ITEM_ALREADY_EXISTS, ITEM_NOT_CREATED
from model.item import ItemModel
from utils.item import item_data, item_exist
from utils.utils import return_message


class ItemResource(Resource):
    def post(self):
        try:
            data = item_data()
            if item_exist(data['name']):
                return return_message(status.BAD_REQUEST, ITEM_ALREADY_EXISTS), status.BAD_REQUEST
            item = ItemModel(**data)
            item.save_item_db()
            return item.json(), status.CREATED
        except Exception as e:
            print(ITEM_NOT_CREATED, str(e))
            return return_message(status.BAD_REQUEST, ITEM_NOT_CREATED), status.BAD_REQUEST

    def get(self):
        return [item.json() for item in ItemModel.find_items()]
