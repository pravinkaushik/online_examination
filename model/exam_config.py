from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

exam_config_app = Flask(__name__)
with exam_config_app.app_context():
    db = SQLAlchemy(current_app)
    session_exam_config_app = db.session


class ExamConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_owner_id = db.Column(db.Integer)
    random_question = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_minute = db.Column(db.Integer)
    exam_title = db.Column(db.String(45))
    exam_name = db.Column(db.String(45))

    def __repr__(self):
        return '<User {}>'.format(self.exam_owner_id)

    def __init__(self, id, exam_owner_id, random_question, start_time, end_time, duration_minute, exam_title, exam_name,
                 *args, **kwargs):
        self.id = id
        self.exam_owner_id = exam_owner_id
        self.random_question = random_question
        self.start_time = start_time
        self.end_time = end_time
        self.duration_minute = duration_minute
        self.exam_title = exam_title
        self.exam_name = exam_name
