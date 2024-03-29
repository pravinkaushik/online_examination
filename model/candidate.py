from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

candidate_app = Flask(__name__)

with candidate_app.app_context():
    db = SQLAlchemy(current_app)
    session_candidate_app = db.session


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), index=True)
    exam_owner_id = db.Column(db.Integer)
    exam_config_id = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    c_name = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def __init__(self, id, email, exam_config_id, exam_owner_id, password_hash, c_name, start_time, end_time, *args,
                 **kwargs):
        self.id = id
        self.email = email
        self.exam_config_id = exam_config_id
        self.exam_owner_id = exam_owner_id
        self.password_hash = password_hash
        self.c_name = c_name
        self.end_time = end_time
        self.start_time = start_time

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'exam_owner_id': self.exam_owner_id,
            'email': self.email,
            'c_name': self.c_name,
            'end_time': self.end_time,
            'start_time': self.start_time,
            'password_hash': self.password_hash,
            'exam_config_id': self.exam_config_id
        }
