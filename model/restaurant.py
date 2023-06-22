from db import db
from typing import List

from model.item import ItemModel
from utils.utils import generate_uuid


class RestaurantModel(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.String(20))
    name = db.Column(db.String(80), unique=True)
    city = db.Column(db.String(80))

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    items = db.relationship('ItemModel')

    def __init__(self, name, city, itemId):
        self.restaurant_id = generate_uuid()
        self.city = city
        self.name = name
        self.item_id = itemId

    def __str__(self) -> str:
        return f"<Restaurant: ID:{self.restaurant_id}, Name: {self.name} city:{self.city} itemId: {self.item_id}>"

    def json(self):
        return {
            "restaurantId": self.restaurant_id,
            'name': self.name,
            'city': self.city,
        }

    @classmethod
    def find_all_restaurants(cls) -> List['ItemModel']:
        return cls.query.all()

    @classmethod
    def find_restaurant_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_restaurant_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
