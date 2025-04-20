from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='viewer')

    def __repr__(self):
        return f"<User {self.username} - Role: {self.role}>"

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role