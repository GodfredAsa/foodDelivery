from model.item import ItemModel
from tests.integration.integration_base_test import IntegrationBaseTest


class ItemTest(IntegrationBaseTest):
    def test_crud_crud(self):
        with self.app_context():
            item = ItemModel("item", "desc", 30.5, 3, "image.png")
            self.assertIsNone(ItemModel.find_by_name('test'))
            item.save_item_db()
            self.assertIsNotNone(ItemModel.find_item_id(1))
            item.delete_item_db()
            self.assertIsNone(ItemModel.find_by_name('test'))

