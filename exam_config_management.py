from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
     get_jwt_claims, jwt_required
)
from datetime import datetime
import json
from model.exam_config import ExamConfig
from model.candidate import Candidate
from model.exam_questions import ExamQuestions
from markupsafe import escape
from service import exam_config_management_service

exam_setup_api = Blueprint('exam_setup_api', __name__)

# exam_config API
@exam_setup_api.route("/validate_login", methods = ['GET'])
@jwt_required
def validate_login():
    return jsonify("001"), 200

# exam_config API
@exam_setup_api.route("/exam_config", methods = ['POST'])
@jwt_required
def create_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str, object_hook=date_hook)  
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.create_exam_config(exam_config)
    return jsonify("001"), 200

@exam_setup_api.route("/exam_config", methods = ['PUT'])
@jwt_required
def update_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str, object_hook=date_hook)
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
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

@exam_setup_api.route("/exam_config_all", methods = ['GET'])
@jwt_required
def get_exam_config_all():
    print(get_jwt_claims()['id'])
    exam_owner_id = get_jwt_claims()['id']
    exam_config_all = exam_config_management_service.get_exam_config_all(exam_owner_id)
    return jsonify([i.serialize for i in exam_config_all]), 200

@exam_setup_api.route("/exam_config/<int:exam_config_id>", methods = ['GET'])
@jwt_required
def get_exam_config(exam_config_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_config = exam_config_management_service.get_exam_config(exam_config_id, exam_owner_id)
    return jsonify(exam_config.serialize), 200

# candidate API
@exam_setup_api.route("/candidate_all/<int:exam_config_id>", methods = ['GET'])
@jwt_required
def get_candidate_all(exam_config_id):
    print(get_jwt_claims()['id'])
    exam_owner_id = get_jwt_claims()['id']
    candidate_all = exam_config_management_service.get_candidate_all(exam_owner_id, exam_config_id)
    return jsonify([i.serialize for i in candidate_all]), 200

@exam_setup_api.route("/candidate", methods = ['POST'])
@jwt_required
def create_candidate():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate = Candidate(**j)
    candidate.exam_owner_id = get_jwt_claims()['id']
    candidate.password_hash = "ramdom"
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

@exam_setup_api.route("/candidate/<int:candidate_id>", methods = ['GET'])
@jwt_required
def get_candidate(candidate_id):
    exam_owner_id = get_jwt_claims()['id']
    candidate = exam_config_management_service.get_candidate(candidate_id, exam_owner_id)
    return jsonify(candidate.serialize), 200

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

@exam_setup_api.route("/exam_question/<int:exam_question_id>", methods = ['GET'])
@jwt_required
def get_exam_question(exam_question_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_question = exam_config_management_service.get_exam_question(exam_question_id, exam_owner_id )
    return jsonify(exam_question.serialize), 200

@exam_setup_api.route("/exam_question_all/<int:exam_config_id>", methods = ['GET'])
@jwt_required
def get_exam_question_all(exam_config_id):
    print(get_jwt_claims()['id'])
    exam_owner_id = get_jwt_claims()['id']
    exam_question_all = exam_config_management_service.get_exam_question_all(exam_owner_id, exam_config_id)
    return jsonify([i.serialize for i in exam_question_all]), 200

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            if(key == 'start_time' or key == 'end_time' ):
                json_dict[key] = datetime.fromtimestamp(value)
        except:
            pass
    return json_dict

