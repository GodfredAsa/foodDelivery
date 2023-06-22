from model.restaurant import RestaurantModel
from tests.unit.unit_base_test import UnitBaseTest


class ItemRestaurant(UnitBaseTest):

    def test_create_restaurant(self) -> None:
        restaurant = RestaurantModel("ABC", "A", 1)
        self.assertEqual(restaurant.name, "ABC")
        self.assertEqual(restaurant.city, "A")
        self.assertIsNotNone(restaurant.restaurant_id)

    def test_restaurant_json(self):
        restaurant = RestaurantModel("ABC", "A", 1)
        restaurant.restaurant_id = "123"
        expected = {'restaurantId': '123', 'name': 'ABC', 'city': 'A'}
        self.assertDictEqual(restaurant.json(), expected)
