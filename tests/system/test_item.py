
from constants.uri import CREATE_ITEM_URI
from tests.base_test import BaseTest
from tests.system.test_data import ITEM_DATA
import http.client as status


class ItemTest(BaseTest):

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(CREATE_ITEM_URI, data=ITEM_DATA)
                self.assertEqual(response.status_code, status.UNAUTHORIZED)

            response = client.get(CREATE_ITEM_URI, data=ITEM_DATA)
            self.assertEqual(response.status_code, status.UNAUTHORIZED)