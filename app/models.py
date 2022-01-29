from flask_login import UserMixin
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        self.description = description

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, number, image):
        self.name = name
        self.email = email
        self.number = number
        self.image = image

    def __repr__(self):
        return f'<Contact {self.id}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name, email, password_hash, image):
        self.username = name
        self.email = email
        self.password_hash = password_hash
        self.image = image

    def __repr__(self):
        return f'<User {self.id}>'