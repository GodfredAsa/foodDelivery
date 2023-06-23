from flask_jwt_extended import jwt_required, jwt_refresh_token_required
from flask_restful import Resource
from flask import request
from constants.item_constants import ITEM_NOT_FOUND, ITEM_OUT_OF_STOCK, INVALID_ITEM_PURCHASE_QTY
from constants.order import ORDER_QTY_INVALID, ORDER_REQUEST_ERROR, ORDER_CANCELLED, ORDER_DELETED_SUCCESS, \
    ORDER_DELETE_UNSUCCESSFUL, ORDER_UPDATE_UNSUCCESSFUL
from constants.user_constants import USER_NOT_FOUND, INADEQUATE_BALANCE, USER_NOT_AUTHORIZE
from model.item import ItemModel
from model.order import OrderModel
from model.user import UserModel
from utils.order import get_order_data
from utils.user import get_users
from utils.utils import return_message
import http.client as status
from constants.order import ORDER_FULFILLED, ORDER_ALREADY_FULFILLED, ORDER_SUCCESSFULLY_FULFILLED, \
    ORDER_NOT_FOUND, ORDER_NOT_FULFILLED


class PlaceOrderResource(Resource):

    @jwt_required
    def post(self):

        try:
            data = get_order_data()
            user = UserModel.find_by_id(data['userId'])
            item = ItemModel.find_item_id(data['itemId'])
            if not user:
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST
            if not item:
                return return_message(status.BAD_REQUEST, ITEM_NOT_FOUND), status.BAD_REQUEST
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

            item.save_item_db()
            user.save_to_db()
            order = OrderModel(**data)
            order.total_cost = total_cost
            order.unit_cost = cost
            order.save_order_db()
            return order.json(), status.OK
        except Exception as e:
            print(ORDER_REQUEST_ERROR, str(e))
            return return_message(status.BAD_REQUEST, ORDER_REQUEST_ERROR), status.BAD_REQUEST


class OrderResource(Resource):
    @jwt_required
    def get(self, email, orderId):
        try:
            user = UserModel.find_by_email(email)
            order = OrderModel.find_by_order_id(orderId)

            if not user:
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST
            if not order:
                return return_message(status.BAD_REQUEST, ORDER_NOT_FOUND), status.BAD_REQUEST
            return order.json(), status.OK
        except Exception as e:
            print(ORDER_REQUEST_ERROR, str(e))
            return return_message(status.BAD_REQUEST, ORDER_REQUEST_ERROR), status.BAD_REQUEST

    @jwt_required
    def put(self, email, orderId):
        try:
            data = request.get_json()
            user = UserModel.find_by_email(email)
            order = OrderModel.find_by_order_id(orderId)

            if not user:
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST

            if not order:
                return return_message(status.BAD_REQUEST, ORDER_NOT_FOUND), status.BAD_REQUEST

            if order.status == ORDER_FULFILLED or order.status == ORDER_CANCELLED:
                return return_message(status.BAD_REQUEST, ORDER_UPDATE_UNSUCCESSFUL), status.BAD_REQUEST

            item = ItemModel.find_item_id(order.item_id)

            if item.qty < 1:
                return return_message(status.BAD_REQUEST, ITEM_OUT_OF_STOCK.format(item.name)), status.BAD_REQUEST

            if data['qty'] <= 0:
                return return_message(status.BAD_REQUEST, ORDER_QTY_INVALID), status.BAD_REQUEST

            if item.qty < data['qty']:
                return return_message(status.BAD_REQUEST, INVALID_ITEM_PURCHASE_QTY), status.BAD_REQUEST

            user.wallet += order.total_cost
            item.qty += order.qty

            total_cost = item.price * data['qty']

            cost = item.price

            if user.wallet < total_cost:
                return return_message(status.BAD_REQUEST, INADEQUATE_BALANCE), status.BAD_REQUEST

            user.wallet -= total_cost
            item.qty -= data['qty']

            item.save_item_db()
            user.save_to_db()

            order.total_cost = total_cost
            order.unit_cost = cost
            order.save_order_db()

            return order.json(), status.OK
        except Exception as e:
            print(ORDER_UPDATE_UNSUCCESSFUL, str(e))
            return return_message(status.BAD_REQUEST, ORDER_UPDATE_UNSUCCESSFUL), status.BAD_REQUEST

    @jwt_required
    def delete(self, email, orderId):
        try:
            order = OrderModel.find_by_order_id(orderId)
            if not UserModel.find_by_email(email):
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST
            if not order:
                return return_message(status.BAD_REQUEST, ORDER_NOT_FOUND), status.BAD_REQUEST
            if order.status == ORDER_FULFILLED:
                return return_message(status.CONFLICT, ORDER_DELETE_UNSUCCESSFUL), status.CONFLICT
            order.delete_order_db()
            return return_message(status.NO_CONTENT, ORDER_DELETED_SUCCESS), status.BAD_REQUEST
        except Exception as e:
            print(ORDER_DELETE_UNSUCCESSFUL, str(e))
            return return_message(status.BAD_REQUEST, ORDER_DELETE_UNSUCCESSFUL), status.BAD_REQUEST


class FulfilOrderResource(Resource):
    @jwt_refresh_token_required
    def put(self):
        try:
            data = request.get_json()
            if not UserModel.find_by_email(data['email']):
                return return_message(status.NOT_FOUND, USER_NOT_FOUND), status.NOT_FOUND
            order = OrderModel.find_by_id(data['orderId'])
            if not order:
                return return_message(status.BAD_REQUEST, ORDER_NOT_FOUND), status.BAD_REQUEST
            if order:
                if order.status == ORDER_FULFILLED:
                    return return_message(status.CONFLICT, ORDER_ALREADY_FULFILLED.format(order.order_id))
                order.status = ORDER_FULFILLED
                order.save_order_db()
                return return_message(status.OK, ORDER_SUCCESSFULLY_FULFILLED.format(order.order_id)), status.OK
        except Exception as e:
            print(ORDER_NOT_FULFILLED, str(e))
            return return_message(status.BAD_REQUEST, ORDER_NOT_FULFILLED), status.BAD_REQUEST


class PlacedOrders(Resource):
    @jwt_refresh_token_required
    def get(self, email):
        try:
            user, _ = get_users(email, "")
            if not user:
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST
            if user.is_admin:
                return [order.json() for order in OrderModel.find_all_orders()]
            return return_message(status.UNAUTHORIZED, USER_NOT_AUTHORIZE), status.UNAUTHORIZED
        except Exception as e:
            print(ORDER_REQUEST_ERROR, str(e))
            return return_message(status.BAD_REQUEST, ORDER_REQUEST_ERROR), status.BAD_REQUEST
