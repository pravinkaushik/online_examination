import string

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_claims, jwt_required, verify_jwt_in_request
)
from datetime import datetime
import json
import random
from model.exam_config import ExamConfig
from model.candidate import Candidate
from model.exam_questions import ExamQuestions
from service import exam_config_management_service
from functools import wraps
from flask import Flask, flash, request, redirect, url_for
import pytz

exam_setup_api = Blueprint('exam_setup_api', __name__)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'][0] != 'exam_owner':
            return jsonify(msg='not exam owner!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


# exam_config API
@exam_setup_api.route("/exam_config", methods=['POST'])
@admin_required
@jwt_required
def create_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str, object_hook=date_hook)
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
    exam_config.start_time = convert_utc(exam_config.time_zone, exam_config.start_time)
    exam_config.end_time = convert_utc(exam_config.time_zone, exam_config.end_time)
    exam_config_management_service.create_exam_config(exam_config)
    return jsonify("001"), 200


@exam_setup_api.route("/exam_config", methods=['PUT'])
@admin_required
@jwt_required
def update_exam_config():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str, object_hook=date_hook)
    exam_config = ExamConfig(**j)
    exam_config.exam_owner_id = get_jwt_claims()['id']
    exam_config.start_time = convert_utc(exam_config.time_zone, exam_config.start_time)
    exam_config.end_time = convert_utc(exam_config.time_zone, exam_config.end_time)
    exam_config_management_service.update_exam_config(exam_config)
    return jsonify("001"), 200


@exam_setup_api.route("/exam_config/<int:exam_config_id>", methods=['DELETE'])
@admin_required
@jwt_required
def delete_exam_config(exam_config_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.delete_exam_config(exam_config_id, exam_owner_id)
    return jsonify("001"), 200


@exam_setup_api.route("/exam_config_all", methods=['GET'])
@admin_required
@jwt_required
def get_exam_config_all():
    print(get_jwt_claims()['id'])
    exam_owner_id = get_jwt_claims()['id']
    exam_config_all = exam_config_management_service.get_exam_config_all(exam_owner_id)
    return jsonify([i.serialize for i in exam_config_all]), 200


@exam_setup_api.route("/exam_config/<int:exam_config_id>", methods=['GET'])
@admin_required
@jwt_required
def get_exam_config(exam_config_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_config = exam_config_management_service.get_exam_config(exam_config_id, exam_owner_id)
    return jsonify(exam_config.serialize), 200


# candidate API
@exam_setup_api.route("/candidate_all/<int:exam_config_id>", methods=['GET'])
@admin_required
@jwt_required
def get_candidate_all(exam_config_id):
    print(get_jwt_claims()['id'])
    exam_owner_id = get_jwt_claims()['id']
    candidate_all = exam_config_management_service.get_candidate_all(exam_owner_id, exam_config_id)
    return jsonify([i.serialize for i in candidate_all]), 200


@exam_setup_api.route("/candidate", methods=['POST'])
@admin_required
@jwt_required
def create_candidate():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate = Candidate(**j)
    candidate.exam_owner_id = get_jwt_claims()['id']
    candidate.password_hash = random_string()
    exam_config_management_service.create_candidate(candidate)
    return jsonify("001"), 200


@exam_setup_api.route("/candidate", methods=['PUT'])
@admin_required
@jwt_required
def update_candidate():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    candidate = Candidate(**j)
    candidate.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.update_candidate(candidate)
    return jsonify("001"), 200


@exam_setup_api.route("/candidate/<int:candidate_id>", methods=['DELETE'])
@admin_required
@jwt_required
def delete_candidate(candidate_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.delete_candidate(exam_owner_id, candidate_id)
    return jsonify("001"), 200


@exam_setup_api.route("/candidate/<int:candidate_id>", methods=['GET'])
@admin_required
@jwt_required
def get_candidate(candidate_id):
    exam_owner_id = get_jwt_claims()['id']
    candidate = exam_config_management_service.get_candidate(candidate_id, exam_owner_id)
    return jsonify(candidate.serialize), 200


# exam_question API
@exam_setup_api.route("/exam_question", methods=['POST'])
@admin_required
@jwt_required
def create_exam_question():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_question = ExamQuestions(**j)
    exam_question.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.create_exam_question(exam_question)
    return jsonify("001"), 200


@exam_setup_api.route("/exam_question", methods=['PUT'])
@admin_required
@jwt_required
def update_exam_question():
    j_str = json.dumps(request.get_json())
    j = json.loads(j_str)
    exam_question = ExamQuestions(**j)
    exam_question.exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.update_exam_question(exam_question)
    return jsonify("001"), 200


@exam_setup_api.route("/exam_question/<int:exam_question_id>", methods=['DELETE'])
@admin_required
@jwt_required
def delete_exam_question(exam_question_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_config_management_service.delete_exam_question(exam_owner_id, exam_question_id)
    return jsonify("001"), 200


@exam_setup_api.route("/exam_question/<int:exam_question_id>", methods=['GET'])
@admin_required
@jwt_required
def get_exam_question(exam_question_id):
    exam_owner_id = get_jwt_claims()['id']
    exam_question = exam_config_management_service.get_exam_question(exam_question_id, exam_owner_id)
    return jsonify(exam_question.serialize), 200


@exam_setup_api.route("/exam_question_all/<int:exam_config_id>", methods=['GET'])
@admin_required
@jwt_required
def get_exam_question_all(exam_config_id):
    print(get_jwt_claims()['id'])
    exam_owner_id = get_jwt_claims()['id']
    exam_question_all = exam_config_management_service.get_exam_question_all(exam_owner_id, exam_config_id)
    return jsonify([i.serialize for i in exam_question_all]), 200


'''
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@exam_setup_api.route("/upload-image", methods = ['POST'])
@admin_required
@jwt_required
def upload_file():
    file_name = ""
    if request.method == 'POST':
        # check if the post request has the file part
        print(exam_setup_api.config['UPLOAD_FOLDER'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name = filename
            file.save(os.path.join(exam_setup_api.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return jsonify({
       "status":"true",
       "originalName": file_name,
       "generatedName": file_name,
       "msg":"Image upload successful",
       "imageUrl": exam_setup_api.config['UPLOAD_FOLDER']+ file_name}), 200
'''


def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            if key == 'start_time' or key == 'end_time':
                json_dict[key] = datetime.fromtimestamp(value)
        except:
            pass
    return json_dict


def convert_utc(timezone, local_time):
    local = pytz.timezone(timezone)
    local_dt = local.localize(local_time, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def random_string(string_length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))
