from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class author_submission(db.Model):
    __tablename__ = 'paper_publications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(200), nullable=False)
    file_content = db.Column(db.LargeBinary, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    submission_date = db.Column(db.Date, server_default=db.func.now())
    author_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(30), nullable=False)

    def __init__(self, title, abstract, keywords, file_content, file_name, submission_date, author_name, user_name):
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.file_content = file_content
        self.file_name = file_name
        self.submission_date = submission_date
        self.author_name = author_name
        self.user_name = user_name

class user(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_role = db.Column(db.String(50), nullable=False, default='viewer')

    def __repr__(self):
        return f"<User {self.username} - Role: {self.role}>"

    def __init__(self, username, password, role, fullname):
        self.username = username
        self.password = password
        self.user_role = role
        self.full_name = fullname