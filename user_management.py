from flask import Flask, jsonify, request
from flask_jwt_extended import (
    get_jwt_claims, JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, fresh_jwt_required
)
from flask import Blueprint
from webApp.service import user_management_service, email_service
from webApp.service import exam_config_management_service
from webApp.model.user import User
import requests
import json
import random
import string

user_management_api = Blueprint('user_management_api', __name__)


# This is an example of a complex object that we could build
# a JWT from. In practice, this will likely be something
# like a SQLAlchemy instance.
class UserObject:
    def __init__(self, id, email, roles):
        self.id = id
        self.email = email
        self.roles = roles


# exam_config API
@user_management_api.route("/validate_login", methods=['GET'])
@jwt_required
def validate_login():
    return jsonify("001"), 200


@user_management_api.route("/home")
@jwt_required
def home():
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_id': get_jwt_claims()['id'],
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }
    return jsonify(ret), 200


@user_management_api.route("/")
@jwt_required
def test_api():
    ret = {
        'test': "Examination API Working"  # ['foo', 'bar']
    }
    return jsonify(ret), 200


@user_management_api.route('/login_exam', methods=['POST'])
def login_exam():
    exam_config_id = request.json.get('exam_config_id', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    candidate = exam_config_management_service.candidate_login(email, exam_config_id, password)
    if candidate is None:
        return jsonify({"error": "ERR0005"}), 401
    if candidate == "C":
        return jsonify({"error": "ERR0006"}), 403
    if candidate == "TO":
        return jsonify({"error": "ERR0002"}), 403

    user = UserObject(id=candidate.id, email=candidate.email, roles=['candidate'])
    ret = {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user),
        'current_identity': email,
        'role': 'candidate'
    }
    return jsonify(ret), 200


@user_management_api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = user_management_service.validate_user(email, password)
    if user is None:
        print("user.id")
        return jsonify({"error": "ERR0005"}), 401
    # Create an example UserObject
    user = UserObject(id=user.id, email=user.email, roles=['exam_owner'])

    # We can now pass this complex object directly to the
    # create_access_token method. This will allow us to access
    # the properties of this object in the user_claims_loader
    # function, and get the identity of this object from the
    # user_identity_loader function.

    ret = {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user),
        'current_identity': email,
        'role': 'exam_owner'
    }
    return jsonify(ret), 200


@user_management_api.route('/signup_social_media', methods=['POST'])
def signup_social_media():
    provider = request.json.get('provider', None)
    auth_token = request.json.get('auth_token', None)
    email = isValidSocialToken(auth_token, provider)

    user_obj = user_management_service.validate_user_email_all_status(email)
    if user_obj is None:
        user_obj = User(0, email, random_string(), "", 1, 1)
        user_management_service.create_user(user_obj)

    # Create an example UserObject
    user = UserObject(id=user_obj.id, email=user_obj.email, roles=['exam_owner'])

    ret = {
        'access_token': create_access_token(identity=user, fresh=True),
        'refresh_token': create_refresh_token(identity=user),
        'current_identity': email,
        'role': 'exam_owner'
    }
    return jsonify(ret), 200


@user_management_api.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user_obj = user_management_service.validate_user_email_all_status(email)
    ret = None
    r_code = 200
    user_obj = None
    if user_obj is None:
        random_str = random_string()+"_"+email
        user_obj = User(0, email, password, random_str, 0, 0)
        user_management_service.create_user(user_obj)
        email_service.send_activation_email(email, random_str)
        ret = {'message': "Activation link has been send to Your Email."}
    else:
        message = "You are already registered. Please use forgot password."
        ret = {'error': "You are already registered with us. Please use forgot password."}
        r_code = 403

    return jsonify(ret), r_code


@user_management_api.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user_obj = user_management_service.validate_user_email(email)
    ret = None
    r_code = 200
    if user_obj is None:
        ret = {'error': "ERR0004"}
        r_code = 403
    else:
        random_str = random_string() + "_" + email
        user_management_service.reset_user_password(email, password, random_str)
        email_service.send_activation_email(email, random_str)
        ret = {'message': "SUC0001"}

    return jsonify(ret), r_code


@user_management_api.route('/activate', methods=['POST'])
def activate():
    key = request.json.get('key', None)
    user_obj = user_management_service.activate_user(key)
    ret = None
    r_code = 200
    if user_obj != 1:
        ret = {'error': "ERR0004"}
        r_code = 403
    else:
        key_arr = key.split("_")
        email_service.send_welcome(key_arr[1])
        user_obj = user_management_service.validate_user_email_all_status(key_arr[1])
        user = UserObject(id=user_obj.id, email=user_obj.email, roles=['exam_owner'])
        ret = {
            'access_token': create_access_token(identity=user, fresh=True),
            'refresh_token': create_refresh_token(identity=user),
            'current_identity': user.email,
            'role': 'exam_owner'
        }
    return jsonify(ret), r_code


# Refresh token endpoint. This will generate a new access token from
# the refresh token, but will mark that access token as non-fresh,
# as we do not actually verify a password in this endpoint.
@user_management_api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    ret = {'access_token': new_token}
    return jsonify(ret), 200


# Fresh login endpoint. This is designed to be used if we need to
# make a fresh token for a user (by verifying they have the
# correct username and password). Unlike the standard login endpoint,
# this will only return a new access token, so that we don't keep
# generating new refresh tokens, which entirely defeats their point.
@user_management_api.route('/fresh-login', methods=['POST'])
def fresh_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = user_management_service.validate_user(email, password)
    if user is None:
        return jsonify({"error": "ERR0005"}), 401

    # Create an example UserObject
    user = UserObject(id=user.id, email=user.email, roles=['exam_owner'])

    new_token = create_access_token(identity=user, fresh=True)
    ret = {'access_token': new_token}
    return jsonify(ret), 200


# Only fresh JWTs can access this endpoint
@user_management_api.route('/protected-fresh', methods=['GET'])
@fresh_jwt_required
def protected_fresh():
    username = get_jwt_identity()
    return jsonify(fresh_logged_in_as=username), 200


@user_management_api.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_id': get_jwt_claims()['id'],
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }
    return jsonify(ret), 200


@user_management_api.route('/contact', methods=['POST'])
def contact():
    print(request.json)
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    message = request.json.get('message', None)
    email_service.send_enquiry(name, email, message)
    r_code = 200
    return jsonify("success"), r_code


def isValidSocialToken(token, provider):
    if provider == "FB":
        API_ENDPOINT = "https://graph.facebook.com/me?fields=email,name&access_token=" + token
        r = requests.get(url=API_ENDPOINT)
        data = json.loads(r.text)
        email = data.get("email", None)
        return email
    else:
        API_ENDPOINT = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token
        r = requests.get(url=API_ENDPOINT)
        data = json.loads(r.text)
        email = data.get("email", None)
        return email


def random_string(string_length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))
