from flask_restful import Resource

from constants.item_constants import ITEM_NOT_FOUND, ITEM_OUT_OF_STOCK, INVALID_ITEM_PURCHASE_QTY
from constants.order import ORDER_QTY_INVALID, ERROR_PLACING_ORDER
from constants.user_constants import USER_NOT_FOUND, INADEQUATE_BALANCE
from model.item import ItemModel
from model.order import OrderModel
from model.user import UserModel
from utils.order import get_order_data
from utils.utils import return_message
import http.client as status


class OrderResource(Resource):
    def post(self):

        try:
            data = get_order_data()
            user = UserModel.find_by_id(data['userId'])

            item = ItemModel.find_item_id(data['itemId'])

            if not user:
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST

            if not item:
                return return_message(status.BAD_REQUEST,  ITEM_NOT_FOUND), status.BAD_REQUEST

            if data['qty'] <= 0:
                return return_message(status.BAD_REQUEST, ORDER_QTY_INVALID), status.BAD_REQUEST

            if item.qty == 0:
                return return_message(status.CONFLICT, ITEM_OUT_OF_STOCK.format(item.name)), status.CONFLICT

            if item.qty < data['qty']:
                return return_message(status.BAD_REQUEST, INVALID_ITEM_PURCHASE_QTY), status.BAD_REQUEST

            total_cost = item.price * data['qty']
            cost = item.price

            if user.wallet <= 0 or user.wallet < total_cost:
                return return_message(status.BAD_REQUEST, INADEQUATE_BALANCE), status.BAD_REQUEST

            user.wallet -= total_cost
            item.qty -= data['qty']

            user.save_to_db()

            order = OrderModel(**data)
            order.total_cost = total_cost
            order.unit_cost = cost
            order.save_order_db()

            return order.json(), status.OK
        except Exception as e:
            print(ERROR_PLACING_ORDER, str(e))
            return return_message(status.BAD_REQUEST, ERROR_PLACING_ORDER), status.BAD_REQUEST
