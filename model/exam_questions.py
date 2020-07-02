from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
import os

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
    is_choice1_correct = db.Column(db.Integer)
    is_choice2_correct = db.Column(db.Integer)
    is_choice3_correct = db.Column(db.Integer)
    is_choice4_correct = db.Column(db.Integer)
    is_choice5_correct = db.Column(db.Integer)
    question_type = db.Column(db.Integer)
    exam_config_id = db.Column(db.Integer)
    positive_marks = db.Column(db.Integer)
    negative_marks = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.exam_owner_id)

    def __init__(self, id, exam_owner_id, question, choice1, choice2, choice3, choice4, choice5, is_choice1_correct,
                 is_choice2_correct, is_choice3_correct, is_choice4_correct, is_choice5_correct, question_type,
                 exam_config_id, positive_marks, negative_marks, *args, **kwargs):
        self.id = id
        self.exam_owner_id = exam_owner_id
        self.question = question
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice3 = choice3
        self.choice4 = choice4
        self.choice5 = choice5
        self.is_choice1_correct = is_choice1_correct
        self.is_choice2_correct = is_choice2_correct 
        self.is_choice3_correct = is_choice3_correct 
        self.is_choice4_correct = is_choice4_correct 
        self.is_choice5_correct = is_choice5_correct 
        self.question_type = question_type
        self.exam_config_id = exam_config_id
        self.positive_marks = positive_marks
        self.negative_marks = negative_marks

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
        'id': self.id,
        'exam_owner_id': self.exam_owner_id,
        'question': self.question,
        'choice1': self.choice1,
        'choice2': self.choice2,
        'choice3': self.choice3,
        'choice4': self.choice4,
        'choice5': self.choice5,
        'is_choice1_correct': self.is_choice1_correct,  
        'is_choice2_correct': self.is_choice2_correct,  
        'is_choice3_correct': self.is_choice3_correct,
        'is_choice4_correct': self.is_choice4_correct,
        'is_choice5_correct': self.is_choice5_correct,
        'question_type': self.question_type,
        'exam_config_id': self.exam_config_id,
        'positive_marks': self.positive_marks,
        'negative_marks': self.negative_marks
       }
