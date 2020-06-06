from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

user_app = Flask(__name__)
with user_app.app_context():
    db = SQLAlchemy(current_app)
    session_user_app = db.session

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    activation_link = db.Column(db.String(128))
    is_active = db.Column(db.Integer)
    is_social_login = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def __init__(self, id, email, password_hash, activation_link, is_active, is_social_login, *args, **kwargs):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.activation_link = activation_link
        self.is_active = is_active
        self.is_social_login = is_social_login