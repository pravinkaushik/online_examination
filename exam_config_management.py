import decimal
import string

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_claims, jwt_required, verify_jwt_in_request
)
from datetime import datetime
import json
from json import JSONEncoder
from decimal import Decimal
import random
import sys
from sqlalchemy.ext.declarative import DeclarativeMeta

from webApp.model.exam_config import ExamConfig
from webApp.model.candidate import Candidate
from webApp.model.exam_questions import ExamQuestions
from webApp.service import exam_config_management_service, email_service
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
            return jsonify({"error": "ERR0009"}), 401
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
    candidate.start_time = None
    candidate.end_time = None
    exam_config = exam_config_management_service.get_exam_config_by_id(candidate.exam_config_id)
    email_service.send_email_invitation(candidate.email, candidate.exam_config_id, exam_config.exam_name,
                                        candidate.password_hash, exam_config.exam_title)
    exam_config_management_service.create_candidate(candidate)
    return jsonify("001"), 200


@exam_setup_api.route("/resend_invitation/<int:candidate_id>", methods=['GET'])
@admin_required
@jwt_required
def resend_invitation(candidate_id):
    exam_owner_id = get_jwt_claims()['id']
    candidate = exam_config_management_service.get_candidate(candidate_id, exam_owner_id)
    exam_config = exam_config_management_service.get_exam_config_by_id(candidate.exam_config_id)
    email_service.send_email_invitation(candidate.email, candidate.exam_config_id, exam_config.exam_name,
                                        candidate.password_hash, exam_config.exam_title)
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
    exam_owner_id = get_jwt_claims()['id']
    exam_question_all = exam_config_management_service.get_exam_question_all(exam_owner_id, exam_config_id)
    return jsonify([i.serialize for i in exam_question_all]), 200


@exam_setup_api.route("/exam_result_all/<int:exam_config_id>", methods=['GET'])
@admin_required
@jwt_required
def get_exam_result_all(exam_config_id):
    exam_owner_id = get_jwt_claims()['id']
    result = exam_config_management_service.get_exam_result_all(exam_owner_id, exam_config_id)
    results = []
    for row_number, row in enumerate(result):
        results.append({})
        for column_number, value in enumerate(row):
            if isinstance(value, datetime):
                time_zone = results[row_number]["time_zone"]
                results[row_number][row.keys()[column_number]] = convert_local_timestamp(time_zone, value)
            elif isinstance(value, Decimal):
                results[row_number][row.keys()[column_number]] = int(value)
            else:
                results[row_number][row.keys()[column_number]] = value

    return jsonify([dict(row) for row in results]), 200


@exam_setup_api.route("/exam_result/<int:exam_config_id>/<int:candidate_id>", methods=['GET'])
@admin_required
@jwt_required
def get_exam_result(exam_config_id, candidate_id):
    exam_owner_id = get_jwt_claims()['id']
    result = exam_config_management_service.get_exam_result(exam_owner_id, exam_config_id, candidate_id)
    return jsonify([dict(row) for row in result]), 200


@exam_setup_api.route("/exam_marks", methods=['PUT'])
@admin_required
@jwt_required
def update_exam_marks():
    exam_owner_id = get_jwt_claims()['id']
    ce_id = request.json.get('id', None)
    subjective_mark = request.json.get('subjective_mark', None)
    exam_config_id = request.json.get('exam_config_id', None)
    exam_config = exam_config_management_service.get_exam_config(exam_config_id, exam_owner_id)
    if exam_config.exam_owner_id == exam_owner_id:
        exam_config_management_service.update_exam_marks(ce_id, subjective_mark, exam_config_id)
    else:
        return jsonify({"error": "Invalid User."}), 403
    return jsonify("001"), 200


def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            if key == 'start_time' or key == 'end_time':
                utc_dt = datetime.utcfromtimestamp(value)
                json_dict[key] = utc_dt
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


class ExamResultEncoder(JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        if isinstance(o, datetime):
            return (convert_local_timestamp(self.time_zone, o) for o in [o])
        return super(ExamResultEncoder, self)._iterencode(o, markers)


def new_alchemy_encoder(revisit_self=False, fields_to_expand=[]):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (
                            isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__, DeclarativeMeta)):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def convert_local_timestamp(time_zone, utc_time):
    tz = pytz.timezone(time_zone)
    local_dt = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)
    local_dt_none_tz = local_dt.replace(tzinfo=None)
    return datetime.timestamp(local_dt_none_tz)
