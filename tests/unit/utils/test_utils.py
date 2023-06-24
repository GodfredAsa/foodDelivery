from tests.unit.unit_base_test import UnitBaseTest
from utils.utils import generate_uuid, format_created_date, return_message
from datetime import datetime


class UtilsTest(UnitBaseTest):
    @staticmethod
    def test_generate_uuid() -> None:
        assert generate_uuid() is not None
        assert len(generate_uuid()) == 36

    @staticmethod
    def test_format_created_date() -> None:
        expected_date = f"{datetime.today().day}-{datetime.today().month}-{datetime.today().year}"
        assert expected_date == format_created_date()

    @staticmethod
    def test_return_message() -> None:
        expected_message = {"status": 200, "message": "my test message"}
        assert expected_message == return_message(200, "my test message")
