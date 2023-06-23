from model.item import ItemModel
from model.order import OrderModel
from model.user import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest
from utils.utils import format_created_date


class OrderTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():

            item = ItemModel("item", "desc", 30.5, 3, "image.png")
            user = UserModel("test", "tester", "test@tests@com",  "password", "image.png")

            user.save_to_db()
            item.save_item_db()

            order = OrderModel(5, user.id, user.id)
            self.assertIsNone(OrderModel.find_by_id(order.id), "Verify Order Not Created")

            order.save_order_db()

            self.assertIsNotNone(OrderModel.find_by_id(order.id), "Verify Order Created")
            self.assertIsNone(order.unit_cost)
            self.assertIsNone(order.total_cost)

    def test_order_item_user_relationship(self):
        with self.app_context():
            item = ItemModel("item", "desc", 30.5, 3, "image.png")
            user = UserModel("test", "tester", "test@tests@com", "password", "image.png")

            user.save_to_db()
            item.save_item_db()
            order = OrderModel(5, user.id, user.id)

            order.save_order_db()

            self.assertEqual(item.id, int(order.item_id))

    def test_order_json(self):
        with self.app_context():
            item = ItemModel("item", "desc", 30.5, 3, "image.png")
            user = UserModel("test", "tester", "test@tests@com", "password", "image.png")

            user.save_to_db()
            item.save_item_db()
            order = OrderModel(5, user.id, user.id)

            order.save_order_db()

            order.order_id = "123"

            expected_dict = {
                'orderId': '123',
                'status': 'Pending',
                'qty': 5,
                'unitCost': None,
                'totalCost': None,
                'user': '1',
                'orderedDate': format_created_date()
            }

            self.assertDictEqual(expected_dict, order.json())