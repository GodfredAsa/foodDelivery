from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from constants.uri import REGISTRATION_URI, LOGIN_URI, ITEM_URI, RESTAURANT_URI, ORDER_FULFILMENT_URI, ORDER_URI, \
    USER_URI
from constants.app_constants import DB_URI, DB_CONNECTION_STRING, SQL_MODIFICATION_STRING, PROPAGATE_EXCEPTIONS, \
    JWT_KEY, JWT_SECRET
from db import db
from resource.fulfil_order import FulfilOrderResource
from resource.item import ItemResource
from resource.order import OrderResource
from resource.restaurant import RestaurantResource
from resource.user import RegisterUser, UserLogin, UserResource

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)

app.config[DB_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = JWT_KEY


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RegisterUser, REGISTRATION_URI)
api.add_resource(UserLogin, LOGIN_URI)
api.add_resource(UserResource, USER_URI)
api.add_resource(ItemResource, ITEM_URI)
api.add_resource(RestaurantResource, RESTAURANT_URI)
api.add_resource(OrderResource, ORDER_URI)
api.add_resource(FulfilOrderResource, ORDER_FULFILMENT_URI)


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5001, debug=True)


