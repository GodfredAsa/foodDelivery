from model.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest
from utils.utils import format_created_date


class ItemTest(UnitBaseTest):

    def test_create_item(self) -> None:
        item = ItemModel("item", "desc", 30.5, 3, "image.png")
        self.assertNotEqual(item.item_id, "123")
        self.assertEqual(item.name, "item")
        self.assertEqual(item.imageUrl, "image.png")
        self.assertEqual(item.price, 30.5)
        self.assertEqual(item.id, None)

    def test_item_json(self):
        """ since the itemId is dynamically generated I need to wrote it """
        item = ItemModel("item", "desc", 30.5, 3, "image.png")
        expected = {
            'itemId': '123',
            'name': 'item',
            'desc': 'desc',
            'imageUrl': 'image.png',
            'quantity': 3,
            'price': 30.5,
            'createdAt': format_created_date()}

        item.item_id = "123"

        self.assertDictEqual(item.json(), expected)




