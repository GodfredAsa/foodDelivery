from utils.utils import generate_uuid

SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
DB_CONNECTION_STRING = "sqlite:///data.db"
SQL_MODIFICATION_STRING = "SQLALCHEMY_TRACK_MODIFICATIONS"
PROPAGATE_EXCEPTIONS = "PROPAGATE_EXCEPTIONS"

JWT_KEY = ''.join(generate_uuid() + 'admin')
JWT_SECRET = "JWT_SECRET_KEY"
