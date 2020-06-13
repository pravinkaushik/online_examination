from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
from model.exam_questions import ExamQuestions

candidate_exam_app = Flask(__name__)
with candidate_exam_app.app_context():
    db = SQLAlchemy(current_app)
    session_candidate_exam_app = db.session


class CandidateExam(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_questions_id = db.Column(db.Integer)
    candidate_id = db.Column(db.Integer)
    exam_config_id = db.Column(db.Integer)
    is_choice1_selected = db.Column(db.Integer)
    is_choice2_selected = db.Column(db.Integer)
    is_choice3_selected = db.Column(db.Integer)
    is_choice4_selected = db.Column(db.Integer)
    is_choice5_selected = db.Column(db.Integer)
    answer = db.Column(db.String(128))

    def __repr__(self):
        return '<CandidateExam {}>'.format(self.exam_questions_id)

    def __init__(self, id, exam_questions_id, candidate_id, exam_config_id, is_choice1_selected, is_choice2_selected,
                 is_choice3_selected, is_choice4_selected, is_choice5_selected, answer,
                 *args, **kwargs):
        self.id = id
        self.exam_questions_id = exam_questions_id
        self.candidate_id = candidate_id
        self.exam_config_id = exam_config_id
        self.is_choice1_selected = is_choice1_selected
        self.is_choice2_selected = is_choice2_selected
        self.is_choice3_selected = is_choice3_selected
        self.is_choice4_selected = is_choice4_selected
        self.is_choice5_selected = is_choice5_selected
        self.answer = answer

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'exam_questions_id': self.exam_questions_id,
           'candidate_id': self.candidate_id,
           'exam_config_id': self.exam_config_id,
           'is_choice1_selected': self.is_choice1_selected,
           'is_choice2_selected': self.is_choice2_selected,
           'is_choice3_selected': self.is_choice3_selected,
           'is_choice4_selected': self.is_choice4_selected,
           'is_choice5_selected': self.is_choice5_selected,
           'answer': self.answer

       }