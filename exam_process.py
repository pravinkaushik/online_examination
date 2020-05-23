from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
     get_jwt_claims, jwt_required
)
import json
from flask_jwt_extended import jwt_required
from model.candidate_exam import CandidateExam
from service import exam_process_service

exam_process_api = Blueprint('exam_process_api', __name__)




# candidate_exam API
@exam_process_api.route("/candidate_exam_prep", methods = ['POST'])
@jwt_required
def prepare_candidate_exam():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate_exam = CandidateExam(**j)
    candidate_exam.candidate_id = get_jwt_claims()['id']

    exam_process_service.prepare_candidate_exam(candidate_exam)
    return jsonify("001"), 200

@exam_process_api.route("/candidate_exam", methods = ['PUT'])
@jwt_required
def update_candidate_exam():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate_exam = CandidateExam(**j)
    candidate_exam.candidate_id = get_jwt_claims()['id']
    exam_process_service.update_candidate_exam(candidate_exam)
    return jsonify("001"), 200

