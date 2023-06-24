from tests.unit.unit_base_test import UnitBaseTest
from utils.user import validate_email


class UserUtilsTest(UnitBaseTest):

    def test_valid_email(self):
        self.assertEqual(validate_email("admin@admin.com"), True)
        self.assertEqual(validate_email("adminadmin.com"), False)
        self.assertEqual(validate_email("admina_dmin.com"), False)
        self.assertEqual(validate_email("@adminadmin.com"), False)
        self.assertEqual(validate_email("adminadmin@.com"), False)
        self.assertEqual(validate_email(""), False)






