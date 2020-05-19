from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app

candidate_exam_app = Flask(__name__)
with candidate_exam_app.app_context():
    db = SQLAlchemy(current_app)
    session_candidate_exam_app = db.session


class CandidateExam(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_questions_id = db.Column(db.Integer)
    provided_answer = db.Column(db.String(10))
    candidate_id = db.Column(db.Integer)
    exam_config_id = db.Column(db.Integer)

    def __repr__(self):
        return '<CandidateExam {}>'.format(self.exam_questions_id)
