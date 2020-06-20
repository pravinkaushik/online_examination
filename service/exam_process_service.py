from sqlalchemy.ext.compiler import compiles
from datetime import datetime

from model import candidate_exam, exam_questions
from model.candidate_exam import session_candidate_exam_app, CandidateExam
from model.candidate import session_candidate_app, Candidate


###################################################################

def prepare_candidate_exam(exam_config_id, candidate_id):
    # validation required exam_owner_id belongs same user
    dt = datetime.utcnow()
    count = session_candidate_exam_app.query(CandidateExam).\
        filter_by(candidate_id=candidate_id, exam_config_id=exam_config_id).count()
    session_candidate_exam_app.commit()
    if count == 0:
        result = session_candidate_exam_app.execute(
            'DELETE from candidate_exam where candidate_id =:val1 and exam_config_id = :val2',
            {'val1': candidate_id, 'val2': exam_config_id})
        result = session_candidate_exam_app.execute(
            'INSERT INTO candidate_exam (exam_questions_id, candidate_id, exam_config_id) SELECT id, :val1, '
            'exam_config_id from test.exam_questions where exam_config_id = :val2',
            {'val1': candidate_id, 'val2': exam_config_id})

        session_candidate_exam_app.commit()

        session_candidate_app.query(Candidate).filter_by(id=candidate_id, exam_config_id=exam_config_id).update(
            {'start_time': dt})
        session_candidate_app.commit()

    return "success"


def get_exam_questions(candidate_id, exam_config_id, page, per_page):
    offset = (page - 1) * per_page
    result = session_candidate_exam_app.execute(
        'SELECT ce.id, ce.exam_questions_id, ce.candidate_id, ce.exam_config_id, ce.is_choice1_selected, '
        'ce.is_choice2_selected, ce.is_choice3_selected, ce.is_choice4_selected, ce.is_choice5_selected, ce.answer,'
        'eq.question, eq.choice1, eq.choice2, eq.choice3, eq.choice4, eq.choice5, eq.question_type, '
        'eq.negative_marks, eq.positive_marks FROM candidate_exam ce inner join exam_questions eq on '
        'ce.exam_questions_id = eq.id WHERE ce.candidate_id=:val1 and ce.exam_config_id=:val2 ORDER BY ce.id LIMIT '
        ':offset, :row_count ',
        {'val1': candidate_id, 'val2': exam_config_id, 'offset': offset, 'row_count': per_page})
    session_candidate_exam_app.commit()
    return result


def update_candidate_exam(cand_exam):
    session_candidate_exam_app.query(CandidateExam).filter_by(id=cand_exam.id,
                                                              exam_config_id=cand_exam.exam_config_id,
                                                              candidate_id=cand_exam.candidate_id).update(
        {'is_choice1_selected': cand_exam.is_choice1_selected, 'is_choice2_selected': cand_exam.is_choice2_selected,
         'is_choice3_selected': cand_exam.is_choice3_selected, 'answer': cand_exam.answer,
         'is_choice4_selected': cand_exam.is_choice4_selected, 'is_choice5_selected': cand_exam.is_choice5_selected})
    session_candidate_exam_app.commit()


def candidate_exam_finish(exam_config_id, candidate_id):
    dt = datetime.utcnow()
    session_candidate_app.query(Candidate).filter_by(id=candidate_id, exam_config_id=exam_config_id).update(
        {'end_time': dt})
    session_candidate_app.commit()
