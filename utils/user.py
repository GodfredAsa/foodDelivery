import re
import bcrypt
from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR
from model.user import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
   )

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("firstName", type=str, required=True, help=BLANK_ERROR.format("firstName"))
_user_parser.add_argument("lastName", type=str, required=True, help=BLANK_ERROR.format("lastName"))
_user_parser.add_argument("email", type=str, required=True, help=BLANK_ERROR.format("email"))
_user_parser.add_argument("imageUrl", type=str, help=BLANK_ERROR.format("imageUrl"))
_user_parser.add_argument("password", type=str, required=True, help=BLANK_ERROR.format("password"))


def user_data():
    return _user_parser.parse_args()


def user_exist(email):
    if not UserModel.find_by_email(email):
        return False
    else:
        return True


def verify_credentials(email, password):
    if not UserModel.find_by_email(email):
        return False
    hashed_password = UserModel.find_by_email(email).password
    if bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password:
        return True
    else:
        return False


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def get_users(adminEmail, userEmail):
    return UserModel.find_by_email(adminEmail), UserModel.find_by_email(userEmail)


def generate_token(user: 'UserModel') -> str:
    return create_refresh_token(user.user_id) if user.is_admin else create_access_token(identity=user.user_id)





