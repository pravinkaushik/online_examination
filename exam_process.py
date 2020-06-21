from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_claims, jwt_required, verify_jwt_in_request
)
import json
from flask_jwt_extended import jwt_required
from model.candidate_exam import CandidateExam
from model.exam_config import ExamConfig
from service import exam_process_service
from service import exam_config_management_service
from functools import wraps
from datetime import datetime

exam_process_api = Blueprint('exam_process_api', __name__)


def candidate_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'][0] != 'candidate':
            return jsonify(error='ERR0007'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


# candidate_exam API
@exam_process_api.route("/prepare_candidate_exam", methods=['POST'])
@candidate_required
@jwt_required
def prepare_candidate_exam():
    exam_config_id = request.json.get('exam_config_id', None)
    candidate_id = get_jwt_claims()['id']
    exam_config = validate_time_frame(candidate_id, exam_config_id)
    if not isinstance(exam_config, ExamConfig):
        return exam_config
    exam_process_service.prepare_candidate_exam(exam_config_id, candidate_id)
    return jsonify("001"), 200


@exam_process_api.route("/candidate_exam", methods=['PUT'])
@candidate_required
@jwt_required
def update_candidate_exam():
    j_str = json.dumps(request.get_json())
    j_arr = json.loads(j_str)
    for j in j_arr:
        candidate_exam = CandidateExam(**j)
        candidate_exam.candidate_id = get_jwt_claims()['id']
        exam_config = validate_time_frame(candidate_exam.candidate_id, candidate_exam.exam_config_id)
        if not isinstance(exam_config, ExamConfig):
            return exam_config
        exam_process_service.update_candidate_exam(candidate_exam)
    return jsonify("001"), 200


@exam_process_api.route("/candidate_exam_finish", methods=['PUT'])
@candidate_required
@jwt_required
def candidate_exam_finish():
    exam_config_id = request.json.get('exam_config_id', None)
    candidate_id = get_jwt_claims()['id']
    exam_process_service.candidate_exam_finish(exam_config_id, candidate_id)
    return jsonify("001"), 200


@exam_process_api.route("/exam_question/<int:exam_config_id>/<int:page>", methods=['GET'])
@candidate_required
@jwt_required
def get_exam_questions(exam_config_id, page):
    candidate_id = get_jwt_claims()['id']
    exam_config = validate_time_frame(candidate_id, exam_config_id)
    if not isinstance(exam_config, ExamConfig):
        return exam_config
    result = exam_process_service.get_exam_questions(candidate_id, exam_config_id, page, exam_config.question_per_page)
    return jsonify([dict(row) for row in result]), 200


@exam_process_api.route("/candidate_exam_config/<int:exam_config_id>", methods=['GET'])
@candidate_required
@jwt_required
def get_candidate_exam_config(exam_config_id):
    candidate_id = get_jwt_claims()['id']
    exam_config = exam_config_management_service.get_exam_config_by_id(exam_config_id)
    return jsonify(exam_config.serialize), 200


@exam_process_api.route("/remain_start_time/<int:exam_config_id>", methods=['GET'])
@candidate_required
@jwt_required
def get_remain_start_time(exam_config_id):
    dt = datetime.utcnow()
    exam_config = exam_config_management_service.get_exam_config_by_id(exam_config_id)
    remain_start_time = 0
    if exam_config.start_time > dt:
        remain_start_time = (exam_config.start_time - dt).total_seconds()
    return jsonify(remain_start_time), 200


@exam_process_api.route("/remain_end_time/<int:exam_config_id>", methods=['GET'])
@candidate_required
@jwt_required
def get_remain_end_time(exam_config_id):
    dt = datetime.utcnow()
    candidate_id = get_jwt_claims()['id']
    exam_config = validate_time_frame(candidate_id, exam_config_id)
    if not isinstance(exam_config, ExamConfig):
        return exam_config
    remain_end_time = 0
    if exam_config.end_time > dt:
        remain_end_time = (exam_config.end_time - dt).total_seconds()
    duration_seconds = exam_config.duration_minute * 60
    if duration_seconds < remain_end_time:
        remain_end_time = duration_seconds

    candidate = exam_config_management_service.get_candidate_by_eid_cid(candidate_id, exam_config_id)
    if candidate.start_time:
        consumed_time = (dt - candidate.start_time).total_seconds()
        remain_end_time = remain_end_time - consumed_time

    return jsonify(remain_end_time), 200


def validate_time_frame(candidate_id, exam_config_id):
    dt = datetime.utcnow()
    exam_config = exam_config_management_service.get_exam_config_by_id(exam_config_id)
    if exam_config.end_time < dt:
        return jsonify({"error": "ERR0002"}), 403

    if exam_config.start_time > dt:
        return jsonify({"error": "ERR0003"}), 403

    candidate = exam_config_management_service.get_candidate_by_eid_cid(candidate_id, exam_config_id)
    if candidate.start_time:
        consumed_time = (dt - candidate.start_time).total_seconds()
        if consumed_time > exam_config.duration_minute * 60:
            return jsonify({"error": "ERR0003"}), 403

    return exam_config
