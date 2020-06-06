from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
     get_jwt_claims, jwt_required, verify_jwt_in_request
)
import json
from flask_jwt_extended import jwt_required
from model.candidate_exam import CandidateExam
from service import exam_process_service
from service import exam_config_management_service
from functools import wraps

exam_process_api = Blueprint('exam_process_api', __name__)

def candidate_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'][0] != 'candidate':
            return jsonify(msg='not exam owner!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


# candidate_exam API
@exam_process_api.route("/prepare_candidate_exam", methods = ['POST'])
@candidate_required
@jwt_required
def prepare_candidate_exam():
    exam_config_id = request.json.get('exam_config_id', None)
    candidate_id = get_jwt_claims()['id']
    exam_process_service.prepare_candidate_exam(exam_config_id, candidate_id)
    return jsonify("001"), 200

@exam_process_api.route("/candidate_exam", methods = ['PUT'])
@candidate_required
@jwt_required
def update_candidate_exam():
    j_str = json.dumps(request.get_json())
    j_arr = json.loads(j_str)
    for j in j_arr:
        candidate_exam = CandidateExam(**j)
        candidate_exam.candidate_id = get_jwt_claims()['id']
        exam_process_service.update_candidate_exam(candidate_exam)
    return jsonify("001"), 200

@exam_process_api.route("/exam_question/<int:exam_config_id>/<int:page>", methods = ['GET'])
@candidate_required
@jwt_required
def get_exam_questions(exam_config_id, page):
    candidate_id = get_jwt_claims()['id']
    exam_config = exam_config_management_service.get_exam_config_by_id(exam_config_id)
    result = exam_process_service.get_exam_questions(candidate_id, exam_config_id, page, exam_config.question_per_page)
    return jsonify( [dict(row) for row in result]), 200
#    return jsonify({'result': [dict(row) for row in result]}), 200

@exam_process_api.route("/candidate_exam_config/<int:exam_config_id>", methods = ['GET'])
@candidate_required
@jwt_required
def get_candidate_exam_config(exam_config_id):
    candidate_id = get_jwt_claims()['id']
    exam_config = exam_config_management_service.get_exam_config_by_id(exam_config_id)
    return jsonify(exam_config.serialize), 200