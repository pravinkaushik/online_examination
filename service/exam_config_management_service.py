from webApp.model.candidate_exam import CandidateExam
from webApp.model.exam_config import ExamConfig, session_exam_config_app
from webApp.model.candidate import session_candidate_app, Candidate
from webApp.model.exam_questions import session_exam_questions_app, ExamQuestions
from datetime import datetime


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


def delete_exam_config(exam_config_id, exam_owner_id):
    exam_config = ExamConfig.query.filter_by(id=exam_config_id, exam_owner_id=exam_owner_id).first()
    session_exam_config_app.delete(exam_config)
    session_exam_config_app.commit()


def get_exam_config_all(exam_owner_id):
    exam_config_all = session_exam_config_app.query(ExamConfig).filter_by(exam_owner_id=exam_owner_id).all()
    session_exam_config_app.commit()
    return exam_config_all


def get_exam_config(exam_config_id, exam_owner_id):
    exam_config = session_exam_config_app.query(ExamConfig).filter_by(id=exam_config_id, exam_owner_id=exam_owner_id).first()
    session_exam_config_app.commit()
    return exam_config


def get_exam_config_by_id(exam_config_id):
    exam_config = session_exam_config_app.query(ExamConfig).filter_by(id=exam_config_id).first()
    session_exam_config_app.commit()
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


def delete_candidate(exam_owner_id, candidate_id):
    candidate = session_candidate_app.query(Candidate).filter_by(id=candidate_id, exam_owner_id=exam_owner_id).first()
    session_candidate_app.delete(candidate)
    session_candidate_app.commit()


def get_candidate_all(exam_owner_id, exam_config_id):
    candidate_all = session_candidate_app.query(Candidate).filter_by(exam_owner_id=exam_owner_id,
                                                                     exam_config_id=exam_config_id).all()
    session_candidate_app.commit()
    return candidate_all


def get_candidate(candidate_id, exam_owner_id):
    candidate = session_candidate_app.query(Candidate).filter_by(id=candidate_id, exam_owner_id=exam_owner_id).first()
    session_candidate_app.commit()
    return candidate


def get_candidate_by_eid_cid(candidate_id, exam_config_id):
    candidate = session_candidate_app.query(Candidate).filter_by(id=candidate_id, exam_config_id=exam_config_id).first()
    session_candidate_app.commit()
    return candidate


def candidate_login(email, exam_config_id, password_hash):
    candidate = session_candidate_app.query(Candidate).filter_by(email=email, exam_config_id=exam_config_id,
                                                                 password_hash=password_hash).first()
    session_candidate_app.commit()
    dt = datetime.utcnow()
    if candidate is not None:
        if candidate.end_time is not None:
            return "C"
        exam_config = session_exam_config_app.query(ExamConfig).\
            filter_by(id=candidate.exam_config_id, exam_owner_id=candidate.exam_owner_id).first()
        session_exam_config_app.commit()
        if exam_config.end_time < dt:
            return "TO"
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
         'is_choice5_correct': exam_question.is_choice5_correct, 'question_type': exam_question.question_type})
    session_exam_questions_app.commit()


def delete_exam_question(exam_owner_id, exam_question_id):
    exam_question = session_exam_questions_app.query(ExamQuestions).filter_by(id=exam_question_id,
                                                                              exam_owner_id=exam_owner_id).first()
    session_exam_questions_app.delete(exam_question)
    session_exam_questions_app.commit()


def get_exam_question_all(exam_owner_id, exam_config_id):
    question_all = session_exam_questions_app.query(ExamQuestions).filter_by(exam_owner_id=exam_owner_id,
                                                                             exam_config_id=exam_config_id).all()
    session_exam_questions_app.commit()
    return question_all


def get_exam_result_all(exam_owner_id, exam_config_id):
    result = session_exam_questions_app.execute(
        'SELECT candidate_id, c_name, email, exam_config_id, time_zone, start_time, end_time, SUM(subjective_mark) AS '
        'total_sub, SUM(positive_marks) AS total_pos, SUM(negative_marks) AS total_neg, SUM(CASE WHEN question_type = 3'
        ' AND subjective_mark IS NULL THEN -1 ELSE 0 END) AS is_completed from RESULT_LIST_VIEW '
        'where exam_owner_id=:val1 and exam_config_id= :val2 '
        'group by candidate_id, exam_config_id, time_zone ', {'val1': exam_owner_id, 'val2': exam_config_id})
    session_exam_questions_app.commit()
    return result


def get_exam_result(exam_owner_id, exam_config_id, candidate_id):
    result = session_exam_questions_app.execute(
        'SELECT ce.id, ce.exam_questions_id, ce.is_choice1_selected, ce.is_choice2_selected, ce.is_choice3_selected, '
        'ce.is_choice4_selected, ce.is_choice5_selected, ce.answer, ce.subjective_mark, eq.is_choice1_correct, '
        'eq.is_choice2_correct, eq.is_choice3_correct, eq.is_choice4_correct, eq.is_choice5_correct, eq.positive_marks,'
        'eq.negative_marks, eq.question_type FROM candidate_exam ce inner join exam_questions eq on '
        'ce.exam_questions_id = eq.id  where eq.exam_owner_id=:val1 and ce.exam_config_id= :val2 and ce.candidate_id= '
        ':val3 ', {'val1': exam_owner_id, 'val2': exam_config_id, 'val3': candidate_id})
    session_exam_questions_app.commit()
    return result


def get_exam_question(exam_question_id, exam_owner_id):
    exam_question = session_exam_questions_app.query(ExamQuestions).filter_by(id=exam_question_id,
                                                                              exam_owner_id=exam_owner_id).first()
    session_exam_questions_app.commit()
    return exam_question


def update_exam_marks(ce_id, subjective_mark, exam_config_id):
    session_exam_questions_app.query(CandidateExam).filter_by(id=ce_id, exam_config_id=exam_config_id).update(
        {'subjective_mark': subjective_mark})
    session_exam_questions_app.commit()
