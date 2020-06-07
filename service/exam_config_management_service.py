from model.exam_config import ExamConfig, session_exam_config_app
from model.candidate import session_candidate_app, Candidate
from model.exam_questions import session_exam_questions_app, ExamQuestions


def create_exam_config(exam_config):
    session_exam_config_app.add(exam_config)
    session_exam_config_app.commit()


def update_exam_config(exam_config):
    session_exam_config_app.query(ExamConfig).filter_by(id=exam_config.id,
                                                        exam_owner_id=exam_config.exam_owner_id).update(
        {'random_question': exam_config.random_question, 'start_time': exam_config.start_time,
         'end_time': exam_config.end_time, 'question_per_page': exam_config.question_per_page,
         'duration_minute': exam_config.duration_minute, 'exam_title': exam_config.exam_title,
         'exam_name': exam_config.exam_name, 'time_zone': exam_config.time_zone,
         'time_zone': exam_config.time_zone, 'total_question': exam_config.total_question})
    session_exam_config_app.commit()


def delete_exam_config(exam_config):
    exam_config = ExamConfig.query.filter_by(id=exam_config.id, exam_owner_id=exam_config.exam_owner_id).first()
    session_exam_config_app.delete(exam_config)
    session_exam_config_app.commit()


def get_exam_config_all(exam_owner_id):
    exam_config_all = ExamConfig.query.filter_by(exam_owner_id=exam_owner_id).all()
    return exam_config_all

def get_exam_config(exam_config_id, exam_owner_id):
    exam_config = ExamConfig.query.filter_by(id=exam_config_id, exam_owner_id=exam_owner_id).first()
    return exam_config

def get_exam_config_by_id(exam_config_id):
    exam_config = ExamConfig.query.filter_by(id=exam_config_id).first()
    return exam_config


###################################################################
def create_candidate(candidate):
    # validation required exam_owner_id belongs same user
    session_candidate_app.add(candidate)
    session_candidate_app.commit()


def update_candidate(candidate):
    session_candidate_app.query(Candidate).filter_by(id=candidate.id, exam_owner_id=candidate.exam_owner_id).update(
        {'email': candidate.email, 'password_hash': candidate.password_hash})
    session_candidate_app.commit()


def delete_candidate(candidate):
    candidate = Candidate.query.filter_by(id=candidate.id, exam_owner_id=candidate.exam_owner_id).first()
    session_candidate_app.delete(candidate)
    session_candidate_app.commit()

def get_candidate_all(exam_owner_id, exam_config_id):
    candidate_all = Candidate.query.filter_by(exam_owner_id=exam_owner_id, exam_config_id=exam_config_id).all()
    return candidate_all

def get_candidate(candidate_id, exam_owner_id):
    candidate = Candidate.query.filter_by(id=candidate_id, exam_owner_id=exam_owner_id).first()
    return candidate

def candidate_login(email, exam_config_id, password_hash):
    candidate = Candidate.query.filter_by(email=email, exam_config_id=exam_config_id, password_hash=password_hash).first()
    return candidate

###################################################################
def create_exam_question(exam_question):
    # validation required exam_owner_id belongs same user
    session_exam_questions_app.add(exam_question)
    session_exam_questions_app.commit()


def update_exam_question(exam_question):
    session_exam_questions_app.query(ExamQuestions).filter_by(id=exam_question.id,
                                                              exam_owner_id=exam_question.exam_owner_id).update(
        {'question': exam_question.question, 'choice1': exam_question.choice1, 'choice2': exam_question.choice2,
         'choice3': exam_question.choice3, 'choice4': exam_question.choice4, 'choice5': exam_question.choice5,
         'is_choice1_correct': exam_question.is_choice1_correct, 'is_choice2_correct': exam_question.is_choice2_correct,
         'is_choice3_correct': exam_question.is_choice3_correct, 'is_choice4_correct': exam_question.is_choice4_correct,
         'is_choice5_correct': exam_question.is_choice5_correct, 'question_type':exam_question.question_type})
    session_exam_questions_app.commit()


def delete_exam_question(exam_question):
    exam_question = ExamQuestions.query.filter_by(id=exam_question.id,
                                                  exam_owner_id=exam_question.exam_owner_id).first()
    session_exam_questions_app.delete(exam_question)
    session_exam_questions_app.commit()

def get_exam_question_all(exam_owner_id, exam_config_id):
    question_all = ExamQuestions.query.filter_by(exam_owner_id=exam_owner_id, exam_config_id=exam_config_id).all()
    return question_all

def get_exam_question(exam_question_id, exam_owner_id):
    exam_question = ExamQuestions.query.filter_by(id=exam_question_id, exam_owner_id=exam_owner_id).first()
    return exam_question