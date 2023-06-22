from flask import request
from flask_restful import Resource
from constants.order import ORDER_FULFILLED, USER_NOT_AUTHORIZE, ORDER_ALREADY_FULFILLED, ORDER_SUCCESSFULLY_FULFILLED, \
    ORDER_NOT_FOUND, ORDER_NOT_FULFILLED
from model.order import OrderModel
import http.client as status

from model.user import UserModel
from utils.utils import return_message


class FulfilOrderResource(Resource):
    def put(self):
        try:
            data = request.get_json()
            user = UserModel.find_by_email(data['email'])
            order = OrderModel.find_order_by_id(data['orderId'])

            if not user.is_admin:
                return return_message(status.UNAUTHORIZED, USER_NOT_AUTHORIZE), status.UNAUTHORIZED

            if order:
                if order.status == ORDER_FULFILLED:
                    return return_message(status.CONFLICT, ORDER_ALREADY_FULFILLED.format(order.order_id))
                order.status = ORDER_FULFILLED
                order.save_order_db()
                return return_message(status.OK, ORDER_SUCCESSFULLY_FULFILLED.format(order.order_id)), status.OK
            return return_message(status.NOT_FOUND, ORDER_NOT_FOUND)
        except Exception as e:
            print(str(e))
            return return_message(status.BAD_REQUEST, ORDER_NOT_FULFILLED), status.BAD_REQUEST
