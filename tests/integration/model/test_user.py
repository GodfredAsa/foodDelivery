from model.user import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest


class UserTest(IntegrationBaseTest):
    def test_crud_user(self):
        with self.app_context():
            user = UserModel("test", "tester", "test@tests@com",  "password", "image.png",)
            self.assertIsNone(UserModel.find_by_email("test@tests@com"), "fetches user by username")
            self.assertIsNone(UserModel.find_by_id(1), "fetches user by user id")
            self.assertEqual(user.password, "password", "password not hashed")
            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_email("test@tests@com"), "user is saved")
