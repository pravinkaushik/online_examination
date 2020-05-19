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
         'end_time': exam_config.end_time,
         'duration_minute': exam_config.duration_minute, 'exam_title': exam_config.exam_title,
         'exam_name': exam_config.exam_name, 'is_multiple_choice': exam_config.is_multiple_choice})
    session_exam_config_app.commit()


def delete_exam_config(exam_config):
    exam_config = ExamConfig.query.filter_by(id=exam_config.id, exam_owner_id=exam_config.exam_owner_id).first()
    session_exam_config_app.delete(exam_config)
    session_exam_config_app.commit()


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
         'correct_answer': exam_question.correct_answer})
    session_exam_questions_app.commit()


def delete_exam_question(exam_question):
    exam_question = ExamQuestions.query.filter_by(id=exam_question.id,
                                                  exam_owner_id=exam_question.exam_owner_id).first()
    session_exam_questions_app.delete(exam_question)
    session_exam_questions_app.commit()
