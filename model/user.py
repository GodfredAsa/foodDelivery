from db import db
from utils.utils import generate_uuid


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    imageUrl = db.Column(db.String(250))
    wallet = db.Column(db.Float)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, firstName, lastName, email, password, imageUrl):
        self.first_name = firstName
        self.last_name = lastName
        self.email = email
        self.imageUrl = imageUrl
        self.password = password
        self.is_admin = False
        self.user_id = generate_uuid()
        self.wallet = 50.0

    def __str__(self):
        return f"<User: ID:{self.id}, Email:{self.email}, wallet:{self.wallet}>"

    def json(self):
        return {
            "userId": self.user_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "imageUrl": self.imageUrl,
            "isAdmin": self.is_admin,
            "wallet": self.wallet,
        }

    @classmethod
    def find_by_email(cls, email: str) -> 'UserModel':
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_uuid(cls, userId: str) -> 'UserModel':
        return cls.query.filter_by(user_id=userId).first()

    @classmethod
    def find_all_users(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
