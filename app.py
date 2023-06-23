from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from constants.uri import REGISTRATION_URI, LOGIN_URI, ITEM_URI, CREATE_RESTAURANT_URI, ORDER_FULFILMENT_URI, \
    PLACE_ORDER_URI, \
    USER_URI, ORDER_URI, PLACED_ORDERS_URI, USERS_URI, CREATE_ITEM_URI, RESTAURANT_URI
from constants.app_constants import DB_URI, DB_CONNECTION_STRING, SQL_MODIFICATION_STRING, PROPAGATE_EXCEPTIONS, \
    JWT_KEY, JWT_SECRET
from db import db
from resource.item import ItemsResource, CreateItemResource
from resource.order import PlaceOrderResource, FulfilOrderResource, OrderResource, PlacedOrders
from resource.restaurant import CreateRestaurantResource, RestaurantResource
from resource.user import RegisterUser, UserLogin, UserResource, UsersResource

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)

app.config[DB_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = 'joe'


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RegisterUser, REGISTRATION_URI)
api.add_resource(UserLogin, LOGIN_URI)
api.add_resource(UserResource, USER_URI)
api.add_resource(UsersResource, USERS_URI)

api.add_resource(CreateItemResource, CREATE_ITEM_URI)
api.add_resource(ItemsResource, ITEM_URI)

api.add_resource(CreateRestaurantResource, CREATE_RESTAURANT_URI)
api.add_resource(RestaurantResource, RESTAURANT_URI)

api.add_resource(PlaceOrderResource, PLACE_ORDER_URI)
api.add_resource(FulfilOrderResource, ORDER_FULFILMENT_URI)
api.add_resource(OrderResource, ORDER_URI)
api.add_resource(PlacedOrders, PLACED_ORDERS_URI)


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5001, debug=True)


