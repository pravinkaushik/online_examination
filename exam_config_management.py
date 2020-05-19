from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
     get_jwt_claims, jwt_required
)
from datetime import datetime
import json
from model.exam_config import ExamConfig
from model.candidate import Candidate
from model.exam_questions import ExamQuestions

from service import exam_config_management_service

exam_setup_api = Blueprint('exam_setup_api', __name__)

# exam_config API
@exam_setup_api.route("/exam_config", methods = ['POST'])
@jwt_required
def create_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
    exam_config.start_time = datetime(2015, 6, 5, 11, 12, 12, 10)
    exam_config.end_time = datetime(2015, 6, 5, 11, 12, 12, 10)
    exam_config_management_service.create_exam_config(exam_config)
    return jsonify("001"), 200

@exam_setup_api.route("/exam_config", methods = ['PUT'])
@jwt_required
def update_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
    exam_config.start_time = datetime(2015, 6, 5, 11, 12, 12, 10)
    exam_config.end_time = datetime(2015, 6, 5, 11, 12, 12, 10)
    exam_config_management_service.update_exam_config(exam_config)
    return jsonify("001"), 200

@exam_setup_api.route("/exam_config", methods = ['DELETE'])
@jwt_required
def delete_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.delete_exam_config(exam_config)
    return jsonify("001"), 200

# candidate API
@exam_setup_api.route("/candidate", methods = ['POST'])
@jwt_required
def create_candidate():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate = Candidate(**j)
    candidate.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.create_candidate(candidate)
    return jsonify("001"), 200

@exam_setup_api.route("/candidate", methods = ['PUT'])
@jwt_required
def update_candidate():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate = Candidate(**j)
    candidate.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.update_candidate(candidate)
    return jsonify("001"), 200

@exam_setup_api.route("/candidate", methods = ['DELETE'])
@jwt_required
def delete_candidate():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate = Candidate(**j)
    candidate.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.delete_candidate(candidate)
    return jsonify("001"), 200

# exam_question API
@exam_setup_api.route("/exam_question", methods = ['POST'])
@jwt_required
def create_exam_question():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_question = ExamQuestions(**j)
    exam_question.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.create_exam_question(exam_question)
    return jsonify("001"), 200

@exam_setup_api.route("/exam_question", methods = ['PUT'])
@jwt_required
def update_exam_question():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_question = ExamQuestions(**j)
    exam_question.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.update_exam_question(exam_question)
    return jsonify("001"), 200

@exam_setup_api.route("/exam_question", methods = ['DELETE'])
@jwt_required
def delete_exam_question():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_question = ExamQuestions(**j)
    exam_question.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.delete_exam_question(exam_question)
    return jsonify("001"), 200

