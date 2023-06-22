import http.client as status
import bcrypt as bcrypt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from model.user import UserModel
from utils.user import user_exist, user_data, verify_credentials
from constants.user_constants import (
    USER_ALREADY_EXISTS,
    USER_NOT_REGISTERED,
    INVALID_CREDENTIALS,
    LOGIN_SUCCESS, ATTRIBUTE_ERROR, USER_NOT_FOUND
)
from utils.utils import return_message


class RegisterUser(Resource):
    @classmethod
    def post(cls):
        data = user_data()
        try:
            if user_exist(data['email']):
                return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS), status.BAD_REQUEST
            user = UserModel(**data)
            user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
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
        access_token = create_access_token(identity=user.id, fresh=True)
        return {
            'message': LOGIN_SUCCESS,
            'status': status.OK,
            "access_token": access_token,
            'user': user.json()
        }, status.OK


class UserResource(Resource):
    def get(self, userId):
        user = UserModel.find_by_uuid(userId)
        if not user:
            return return_message(status.NOT_FOUND, USER_NOT_FOUND), status.NOT_FOUND
        return user.json(), status.OK



