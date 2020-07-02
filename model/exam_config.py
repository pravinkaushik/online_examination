from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
from datetime import datetime
import pytz

exam_config_app = Flask(__name__)
with exam_config_app.app_context():
    db = SQLAlchemy(current_app)
    session_exam_config_app = db.session


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class ExamConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_owner_id = db.Column(db.Integer)
    random_question = db.Column(db.Integer)
    question_per_page = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_minute = db.Column(db.Integer)
    exam_title = db.Column(db.String(45))
    exam_name = db.Column(db.String(45))
    time_zone = db.Column(db.String(45))
    total_question = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.exam_owner_id)

    def __init__(self, id, exam_owner_id, random_question, start_time, end_time, duration_minute, exam_title, exam_name,
                 time_zone, question_per_page,
                 total_question, *args, **kwargs):
        self.id = id
        self.exam_owner_id = exam_owner_id
        self.random_question = random_question
        self.question_per_page = question_per_page
        self.start_time = start_time
        self.end_time = end_time
        self.duration_minute = duration_minute
        self.exam_title = exam_title
        self.exam_name = exam_name
        self.time_zone = time_zone
        self.total_question = total_question

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        pacific_now = datetime.now(pytz.timezone(self.time_zone))
        stime = self.start_time.replace(tzinfo=pytz.utc).timestamp() + pacific_now.utcoffset().total_seconds()
        etime = self.end_time.replace(tzinfo=pytz.utc).timestamp() + pacific_now.utcoffset().total_seconds()
        return {
            'id': self.id,
            'exam_owner_id': self.exam_owner_id,
            'random_question': self.random_question,
            'duration_minute': self.duration_minute,
            'question_per_page': self.question_per_page,
            'exam_title': self.exam_title,
            'exam_name': self.exam_name,
            'start_time': stime,
            'end_time': etime,
            'time_zone': self.time_zone,
            'total_question': self.total_question
        }


def convert_local(time_zone, utc_time):
    tz = pytz.timezone(time_zone)
    local_dt = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)
    local_dt_none_tz = local_dt.replace(tzinfo=None)

    return local_dt_none_tz
