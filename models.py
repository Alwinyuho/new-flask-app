from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize the database
db = SQLAlchemy()

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
