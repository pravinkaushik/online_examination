from sqlalchemy.ext.compiler import compiles

from model import candidate_exam, exam_questions
from model.candidate_exam import session_candidate_exam_app, CandidateExam
from sqlalchemy.sql.expression import Executable, ClauseElement, select


###################################################################

def prepare_candidate_exam(cand_exam):
    # validation required exam_owner_id belongs same user
    result = session_candidate_exam_app.execute(
        'DELETE from candidate_exam where candidate_id =:val1 and exam_config_id = :val2',
        {'val1': cand_exam.candidate_id, 'val2': cand_exam.exam_config_id})
    result = session_candidate_exam_app.execute(
        'INSERT INTO candidate_exam (exam_questions_id, candidate_id, exam_config_id) SELECT id, :val1, exam_config_id from test.exam_questions where exam_config_id = :val2',
        {'val1': cand_exam.candidate_id, 'val2': cand_exam.exam_config_id})
    session_candidate_exam_app.commit()
    return result


def update_candidate_exam(cand_exam):
    session_candidate_exam_app.query(CandidateExam).filter_by(id=cand_exam.id,
                                                              exam_config_id=cand_exam.exam_config_id,
                                                              candidate_id=cand_exam.candidate_id).update(
        {'provided_answer': cand_exam.provided_answer})
    session_candidate_exam_app.commit()
