import json
from constants.uri import REGISTRATION_URI, LOGIN_URI, USERS_URI
from constants.user_constants import INVALID_EMAIL, USER_ALREADY_EXISTS, USER_NOT_AUTHORIZE
from tests.base_test import BaseTest
from tests.system.test_data import REGISTRATION_DATA, LOGIN_DATA, HEADERS, EMAILS, ADMIN_LOGIN_DATA_MULTIPLE_USERS
import http.client as status
from utils.utils import return_message


class UserTest(BaseTest):

    def test_register_user_with_invalid_email(self):
        with self.app() as client:
            with self.app_context():
                REGISTRATION_DATA['email'] = "test_.com"
                response = client.post(REGISTRATION_URI, data=REGISTRATION_DATA)
                self.assertEqual(response.status_code, status.BAD_REQUEST)
                response_dict = json.loads(response.data)
                self.assertDictEqual(return_message(status.BAD_REQUEST, INVALID_EMAIL), response_dict)

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(REGISTRATION_URI, data=REGISTRATION_DATA)
                self.assertEqual(response.status_code, status.CREATED)
                response_dict = json.loads(response.data)
                self.assertEqual(REGISTRATION_DATA['email'], response_dict['email'])
                self.assertEqual(REGISTRATION_DATA['firstName'], response_dict['firstName'])
                self.assertEqual(REGISTRATION_DATA['lastName'], response_dict['lastName'])
                self.assertEqual(REGISTRATION_DATA['imageUrl'], response_dict['imageUrl'])
                self.assertEqual(False, response_dict['isAdmin'])
                self.assertEqual(50.0, response_dict['wallet'])
                self.assertIsNotNone(response_dict['userId'])

    def test_existing_user_registration(self):
        with self.app() as client:
            with self.app_context():
                # first user registration
                client.post(REGISTRATION_URI, data=REGISTRATION_DATA)
                # second registration with same details
                response = client.post(REGISTRATION_URI, data=REGISTRATION_DATA)
                response_dict = json.loads(response.data)
                self.assertDictEqual(return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS), response_dict)

    def test_registration_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post(REGISTRATION_URI, data=REGISTRATION_DATA)
                auth_response = client.post(LOGIN_URI, data=json.dumps(LOGIN_DATA), headers=HEADERS)
                auth_response_dict = json.loads(auth_response.data)
                for k, v in auth_response_dict.items():
                    if k == 'token':
                        self.assertTrue(v)


class AdminRegistrationTest(BaseTest):
    def test_register_admin(self):
        with self.app() as client:
            with self.app_context():
                REGISTRATION_DATA['email'] = "admin@testers.io"
                response = client.post(REGISTRATION_URI, data=REGISTRATION_DATA)
                self.assertEqual(response.status_code, status.CREATED)
                response_dict = json.loads(response.data)
                self.assertEqual(True, response_dict['isAdmin'], "Verifies Registered User Is Admin")
                self.assertEqual(00.0, response_dict['wallet'], "Verifies Admin Has no Cash in Wallet")

    def test_get_all_registered_users_by_admin(self):
        with self.app() as client:
            with self.app_context():
                # REGISTER LISTS OF USERS WITH ONE AS AN ADMIN
                for email in EMAILS:
                    REGISTRATION_DATA['email'] = email
                    client.post(REGISTRATION_URI, data=REGISTRATION_DATA)

            #  ADMIN REGISTERED LOGS IN
            admin_login_response = client.post(
                LOGIN_URI, data=json.dumps(ADMIN_LOGIN_DATA_MULTIPLE_USERS), headers=HEADERS)

            # OBTAIN ADMIN REFRESH TOKEN
            refresh_token = json.loads(admin_login_response.data)['token']

            # ADMIN GETTING A LIST OF USERS
            response = client.get(USERS_URI, headers={'Authorization': f"Bearer {refresh_token}"})

            self.assertIsNotNone(response.data)
            users = json.loads(response.data)
            self.assertEqual(2, len(users), "Verifies That Out of The 3 Registers 2 are Not admin")
            self.assertNotEqual(users[0]['email'], users[1]['email'], "Verifies 2 users do not have the same email")

            # GET BY ADMIN USER BY EMAIL
            user_email = "admin@test.io"
            response = client.get(f"/api/users/admin/{user_email}",
                                  headers={'Authorization': f"Bearer {refresh_token}"})

            self.assertIsNotNone(response.data)
            response_email = json.loads(response.data)['email']
            self.assertEqual(response_email, user_email)

            # ADMIN DELETE ADMIN BY EMAIL
            delete_admin_response = client.delete(
                f"/api/users/admin/{user_email}",
                headers={'Authorization': f"Bearer {refresh_token}"})

            self.assertEqual(delete_admin_response.status_code, status.UNAUTHORIZED)

            self.assertDictEqual(
                return_message(status.UNAUTHORIZED, USER_NOT_AUTHORIZE),
                json.loads(delete_admin_response.data), "Enforces Admin Cannot Delete Another Admin")

            # ADMIN DELETE USER BY EMAIL

            delete_user_response = client.delete(
                f"/api/users/admin/dev@test.com",
                headers={'Authorization': f"Bearer {refresh_token}"})

            self.assertEqual(delete_user_response.status_code, status.OK)
            self.assertDictEqual(return_message(status.OK, "User Deleted Successfully."), json.loads(delete_user_response.data))



