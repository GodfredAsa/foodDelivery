from model.item import ItemModel
from model.restaurant import RestaurantModel
from tests.integration.integration_base_test import IntegrationBaseTest


class RestaurantTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():

            item = ItemModel("item", "desc", 30.5, 3, "image.png")
            restaurant = RestaurantModel("ABC", "A", 1)

            self.assertIsNone(RestaurantModel.find_restaurant_by_name('ABC'))
            self.assertIsNone(ItemModel.find_by_name('test'))

            item.save_item_db()
            restaurant.save_restaurant_db()

            self.assertIsNotNone(ItemModel.find_item_id(1))
            self.assertIsNotNone(RestaurantModel.find_restaurant_by_name('ABC'))

            item.delete_item_db()

            self.assertIsNone(ItemModel.find_item_id(1))

    def test_restaurant_item_relationship(self):
        with self.app_context():
            restaurant = RestaurantModel("ABC", "A", 1)
            item = ItemModel("item", "desc", 30.5, 3, "image.png")
            item.save_item_db()
            restaurant.save_restaurant_db()
            self.assertEqual(item.id, restaurant.item_id)
