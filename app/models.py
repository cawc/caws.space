from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Idea(db.Model):
    """An idea"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(512), nullable=False)
    category = db.Column(db.String(128))
    done = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'done': self.done
        }

class URL(db.Model):
    """A shortened URL"""
    token = db.Column(db.String(128), primary_key=True, index=True)
    url = db.Column(db.String(1024), nullable=False)
    clicks = db.Column(db.Integer, default=0)