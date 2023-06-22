from db import db
from typing import List
from utils.utils import format_created_date, generate_uuid


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(20))
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    imageUrl = db.Column(db.String(200))
    createdAt = db.Column(db.String(10))

    def __init__(self, name, description, price, qty, imageUrl):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.item_id = generate_uuid()
        self.imageUrl = imageUrl
        self.createdAt = format_created_date()

    def __str__(self):
        return f"<Item: ID:{self.id}, name:{self.name}, Qty:{self.qty}, price:{self.price} createdAt: {self.createdAt}>"

    def json(self):
        return {
            "itemId": self.item_id,
            "name": self.name,
            "desc": self.description,
            "imageUrl": self.imageUrl,
            "quantity": self.qty,
            "price": self.price,
            "createdAt": self.createdAt
        }

    @classmethod
    def find_by_name(cls, name: str) -> 'ItemModel':
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_item_id(cls, _id: int) -> 'ItemModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_item_uuid(cls, item_id: str) -> 'ItemModel':
        return cls.query.filter_by(item_id=item_id).first()

    @classmethod
    def find_items(cls) -> List['ItemModel']:
        return cls.query.all()

    def save_item_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_item_db(self) -> None:
        db.session.delete(self)
        db.session.commit()



