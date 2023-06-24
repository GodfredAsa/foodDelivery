import http.client as status
import bcrypt as bcrypt
from flask import request
from flask_restful import Resource

from model.user import UserModel
from utils.user import user_exist, user_data, verify_credentials, validate_email, get_users, generate_token
from constants.user_constants import (
    USER_ALREADY_EXISTS,
    USER_NOT_REGISTERED,
    INVALID_CREDENTIALS,
    LOGIN_SUCCESSFUL, ATTRIBUTE_ERROR, USER_NOT_FOUND, INVALID_EMAIL, USER_NOT_AUTHORIZE, ERROR_PROCESSING_REQUEST,
    USER_DELETED
)
from utils.utils import return_message
from flask_jwt_extended import jwt_refresh_token_required


class RegisterUser(Resource):
    @classmethod
    def post(cls):
        data = user_data()
        try:
            if user_exist(data['email']):
                return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS), status.BAD_REQUEST
            user = UserModel(**data)
            if not validate_email(user.email):
                return return_message(status.BAD_REQUEST, INVALID_EMAIL), status.BAD_REQUEST

            user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

            if "admin" in user.email.split('@')[0]:
                user.is_admin = True
                user.wallet = 0.0

            user.save_to_db()
            return user.json(), status.CREATED
        except AttributeError as e:
            print(ATTRIBUTE_ERROR.format(e))
            return return_message(status.BAD_REQUEST, USER_NOT_REGISTERED), status.BAD_REQUEST


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        if not verify_credentials(data['email'], data['password']):
            return return_message(status.BAD_REQUEST, INVALID_CREDENTIALS), status.BAD_REQUEST
        user = UserModel.find_by_email(data["email"])
        return {
            'message': LOGIN_SUCCESSFUL,
            "token": generate_token(user),
            'user': user.json()
        }, status.OK


class UserResource(Resource):
    @jwt_refresh_token_required
    def get(self, adminEmail, userEmail):
        try:
            admin, user = get_users(adminEmail, userEmail)
            if not user:
                return return_message(status.NOT_FOUND, USER_NOT_FOUND), status.NOT_FOUND
            if not admin.is_admin:
                return return_message(status.UNAUTHORIZED, USER_NOT_AUTHORIZE), status.UNAUTHORIZED
            return user.json(), status.OK
        except Exception as e:
            print(ERROR_PROCESSING_REQUEST, str(e))
            return return_message(status.BAD_REQUEST, ERROR_PROCESSING_REQUEST), status.BAD_REQUEST

    @jwt_refresh_token_required
    def delete(self, userEmail):
        try:
            _, user = get_users("", userEmail)
            if not user:
                return return_message(status.NOT_FOUND, USER_NOT_FOUND), status.NOT_FOUND
            user.delete_from_db()
            return return_message(status.OK, USER_DELETED), status.OK
        except Exception as e:
            print(ERROR_PROCESSING_REQUEST, str(e))
            return return_message(status.BAD_REQUEST, ERROR_PROCESSING_REQUEST), status.BAD_REQUEST


class UsersResource(Resource):
    @jwt_refresh_token_required
    def get(self):
        return [user.json() for user in UserModel.find_all_users()], status.OK
