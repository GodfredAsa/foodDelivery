from model.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):

    def test_create_user(self) -> None:
        user = UserModel("test", "tester", "test@tests@com", "image.png", "pass")
        self.assertNotEqual(user.user_id, "123")
        self.assertEqual(user.email, "test@tests@com")
        self.assertNotEqual(user.is_admin, True, "Created User are not admin")
        self.assertEqual(user.wallet, 50.0, "Created User have  wallet worth of 50.0")
        self.assertEqual(user.id, None)

    def test_user_json(self):
        """ since the userId is dynamically generated I need to wrote it """
        user = UserModel("test", "tester", "test@tests@com", "image.png", "pass")
        expected = {
            'userId': '1234',
            'firstName': 'test',
            'lastName': 'tester',
            'email': 'test@tests@com',
            'imageUrl': 'pass',
            'isAdmin': False,
            'wallet': 50.0
        }
        user.user_id = "1234"
        actual = user.json()
        self.assertDictEqual(actual, expected)




