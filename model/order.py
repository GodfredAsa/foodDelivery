from constants.order import ORDER_PENDING
from db import db
from model.user import UserModel
from typing import List
from utils.utils import format_created_date, generate_uuid


class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20))
    status = db.Column(db.String(80))
    qty = db.Column(db.Integer)
    unit_cost = db.Column(db.Float(precision=2))
    total_cost = db.Column(db.Float(precision=2))
    user_id = db.Column(db.String(100), db.ForeignKey("users.id"))
    item_id = db.Column(db.String(100), db.ForeignKey("items.id"))
    order_date = db.Column(db.String(10))

    def __init__(self, qty, userId, itemId):
        self.order_id = generate_uuid()
        self.qty = qty
        self.user_id = userId
        self.item_id = itemId
        self.status = ORDER_PENDING
        self.order_date = format_created_date()

    def __str__(self):
        return f"<Order: ID:{self.id}, " \
               f"quantity:{self.qty}, " \
               f"cost:{self.total_cost}, " \
               f"userId:{self.user_id} " \
               f"ItemId: {self.item_id}" \
               f">"

    def json(self):
        return {
            "orderId": self.order_id,
            "status": self.status,
            "qty": self.qty,
            "unitCost": self.unit_cost,
            "totalCost": self.total_cost,
            "user": self.user_id,
            "orderedDate": self.order_date
        }

    #   TODO CHECK THE STATUS OF JOINING THE MODELS
    # item_id = db.Column(db.String(100), db.ForeignKey("items.id"))
    # items = db.relationship("ItemModel")

    @classmethod
    def find_all_orders(cls) -> List['OrderModel']:
        return cls.query.all()

    @classmethod
    def find_by_order_id(cls, order_id: str) -> 'OrderModel':
        return cls.query.filter_by(order_id=order_id).first()

    @classmethod
    def find_by_id(cls, _id) -> 'OrderModel':
        return cls.query.filter_by(id=_id).first()

    def save_order_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_order_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

