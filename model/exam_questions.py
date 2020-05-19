from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

exam_questions_app = Flask(__name__)
with exam_questions_app.app_context():
    db = SQLAlchemy(current_app)
    session_exam_questions_app = db.session


class ExamQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_owner_id = db.Column(db.Integer)
    question = db.Column(db.String(128))
    choice1 = db.Column(db.String(128))
    choice2 = db.Column(db.String(128))
    choice3 = db.Column(db.String(128))
    choice4 = db.Column(db.String(128))
    choice5 = db.Column(db.String(128))
    correct_answer = db.Column(db.String(45))
    is_multiple_choice = db.Column(db.Integer)
    exam_config_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.exam_owner_id)
